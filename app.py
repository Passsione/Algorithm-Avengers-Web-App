from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re,os
from model import *  # Assuming your models are defined in this file
from collections import Counter
import random
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Change as needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To suppress a warning from SQLAlchemy
db.init_app(app) 


app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # or another SMTP provider
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'  # Use an app-specific password or env variable
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'

mail = Mail(app)


login_manager = LoginManager()
login_manager.init_app(app) 
login_manager.login_view = 'login' 
 

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(student_id):
    # Use the primary key for fetching the user
    return Student.query.get(int(student_id))



# Email Validation Function
def validate_email(email):
    pattern = r'^\d{8}@dut4life\.ac\.za$'
    return re.match(pattern, email)


@app.route('/')
def home():
    return render_template("home.html")


# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        student_num = request.form['student_num']
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate Email Format
        if not validate_email(email):
            flash("Invalid email format! Use 8 digits followed by @dut4life.ac.za", 'danger')
            return redirect(url_for('signup'))

        # Check if Student Number is 8 Digits
        if not student_num.isdigit() or len(student_num) != 8:
            flash("Student number must be exactly 8 digits.", 'danger')
            return redirect(url_for('signup'))

        # Check if Passwords Match
        if password != confirm_password:
            flash("Passwords do not match!", 'danger')
            return redirect(url_for('signup'))

        # Hash Password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Check if Email Already Exists
        existing_user = Student.query.filter_by(student_email=email).first()
        if existing_user:
            flash("Email already registered!", 'danger')
            return redirect(url_for('signup'))

        # Save New Student to Database
        new_student = Student(
            student_num=student_num,
            student_fname=fname,
            student_lname=lname,
            student_email=email,
            student_password=hashed_password
        )

        db.session.add(new_student)
        db.session.commit()

        flash("Signup successful! You can now log in.", 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


#Login router
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if it's a hardcoded admin login
        if email == "12345678@dut4life.ac.za" and password == "12345678":
            session['is_admin'] = True  # You can use this to track if the user is an admin
            session['user_email'] = email
            flash("Logged in as Admin", "success")
            return redirect(url_for("admin_dashboard"))  # Redirect to the admin dashboard

        # Otherwise, check if it's a student login
        student = Student.query.filter_by(student_email=email).first()

        if student and check_password_hash(student.student_password, password):
            login_user(student)  # Flask-Login manages the session
            flash("Logged in successfully as a student", "success")
            return redirect(url_for("student_dashboard"))  # Redirect to the student dashboard

        flash("Invalid credentials", "danger")  # Flash an error if login fails

    return render_template("login.html")  # Render the login page if GET request



#The matching algorithm

def calculate_matching_score(item_desc, claim_desc):
    # Return 0 if either description is missing
    if not item_desc or not claim_desc:
        return 0

    # Tokenize the descriptions into lowercase words
    item_words = set(re.findall(r'\w+', item_desc.lower()))
    claim_words = set(re.findall(r'\w+', claim_desc.lower()))

    # Calculate the intersection and union of the words
    intersection = item_words.intersection(claim_words)
    union = item_words.union(claim_words)

    # Calculate Jaccard similarity and scale it to 0-10
    if len(union) == 0:
        return 0
    jaccard_similarity = len(intersection) / len(union)
    matching_score = jaccard_similarity * 10  # Scale to 0-10

    return round(matching_score, 2)



#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ Student Dashboard Route $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@app.route('/student_dashboard', methods=['GET', 'POST'])
@login_required
def student_dashboard():
    # Static list of categories
    categories = ['Bottles', 'Bags', 'Phones', 'Balls', 'Shoes', 'Others']

    # Default query for items (fetch all items) 
    items = Item.query.all()   

    selected_category = None  # To store the selected category for the form

    # Check if a category is selected from the form
    if request.method == 'POST': 
        selected_category = request.form.get('category')  # Get category selected by the user
        if selected_category:
            # Filter items by the selected category 
            items = Item.query.filter_by(category_name=selected_category).all()
 
    return render_template('student_dashboard.html', categories=categories, items=items, selected_category=selected_category)


#student reporting the item that they found missing in the campus
from flask_login import current_user, login_required

@app.route('/report', methods=['GET', 'POST'])
@login_required  # Ensures only authenticated users can access this route
def report():
    if not current_user.is_authenticated:
        flash("You need to be logged in to report an item.", "danger")
        return redirect(url_for('login'))

    campuses = [
        {'name': 'Steve Biko', 'blocks': ['S1', 'S2', 'S3']},
        {'name': 'Riston Campus', 'blocks': ['B1', 'B2', 'B3']},
        {'name': 'ML Sultan', 'blocks': ['L1', 'L2', 'L3']}
    ]

    if request.method == 'POST': 
        # Get form data
        item_name = request.form['item_name']
        item_desc = request.form['item_desc']
        campus_name = request.form['campus_name']
        campus_block = request.form['campus_block']
        img_url = request.form['img_url']

        # Find the selected campus
        campus = Campus.query.filter_by(campus_name=campus_name).first()
        if not campus:
            campus = Campus(campus_name=campus_name, campus_block=campus_block)
            db.session.add(campus)
            db.session.commit()

        # Create a new Report
        report = Report(student_id=current_user.student_id, campus_id=campus.campus_id, img_url=img_url)
        db.session.add(report)
        db.session.commit()

        # Create a new Item
        item = Item(item_name=item_name, report_id=report.report_id, item_desc=item_desc)
        db.session.add(item)
        db.session.commit()

        flash("Thank you for reuniting the item with the owner!", 'success')
        return redirect(url_for('thank_you'))  # Ensure this is returned after POST

    # Handle GET request by rendering the report form
    return render_template('report.html', campuses=campuses)  # This is needed for GET requests


@app.route('/thank_you')  
@login_required
def thank_you():
    # Reward the student with 5 points when they visit the Thank You page
    current_user.points += 5  # Add 5 points to the student's account
    db.session.commit()

    return render_template('thank_you.html', points=current_user.points)



#student claiming the items
@app.route('/claim_item/<int:item_id>', methods=['POST'])
@login_required
def claim_item(item_id):
    item = Item.query.get_or_404(item_id)

    if item.status == ItemStatus.FOUND:
        # Step 1: Create a ClaimedItem (without description_id)
        claim = ClaimedItem(
            student_id=current_user.student_id,
            item_id=item.item_id,
            campus_id=item.report.campus_id,
            approval=False  # Default to False
        )
        db.session.add(claim)
        db.session.commit()

        # Step 2: Notify the admin about the claim
        notification = Notification(
            message=f"Student {current_user.student_fname} {current_user.student_lname} has initiated a claim for item {item.item_name}. Please review the claim details."
        )
        db.session.add(notification)
        db.session.commit()

        flash('Redirecting to claim form. Please complete the claim details.', 'info')
        return redirect(url_for('claim_item_page', claim_id=claim.claim_id))
    else:
        flash('Item is not available for claiming.', 'danger')
        return redirect(url_for('student_dashboard'))



@app.route('/claim_item_page/<int:claim_id>', methods=['GET', 'POST'])
@login_required
def claim_item_page(claim_id):
    claim = ClaimedItem.query.get_or_404(claim_id)
    item = Item.query.get_or_404(claim.item_id)  # Get the item associated with the claim

    if request.method == 'POST':
        description = request.form.get('description')

        if not description:
            flash('You must provide a description for the claim.', 'danger')
            return redirect(url_for('claim_item_page', claim_id=claim.claim_id))

        # Step 1: Create an ItemDescription
        item_description = ItemDescription(
            item_id=item.item_id,
            report_id=item.report.report_id,
            item_description=description
        ) 
        db.session.add(item_description)
        db.session.commit()

        # Step 2: Update the ClaimedItem with the description_id
        claim.description_id = item_description.description_id  # Link the description to the claim
        claim.approval = False  # Still waiting for admin approval
        db.session.commit()

        flash('Claim details updated successfully. Waiting for admin approval.', 'success')
        return redirect(url_for('student_dashboard'))

    return render_template('claim_item.html', claim=claim, item=item)




#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ End of student $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


#////////////////////////////////////////////// Admin Dashboard Route////////////////////////////////////////////
@app.route('/admin_dashboard')
def admin_dashboard(): 
    if not session.get('admin_logged_in'): 
        flash("Access denied.", 'danger')
        return redirect(url_for('login'))
    
    # Fetch all the required data
    students = Student.query.all() 
    items = Item.query.all()
    claimed_items = ClaimedItem.query.all()
    notifications = Notification.query.order_by(Notification.created_at.desc()).all()
    # Pass everything to the template
    return render_template(
        'admin_dashboard.html',
        students=students, 
        items=items,
        claimed_items=claimed_items 
    )



#For adding items in the website
@app.route('/admin/add_item', methods=['GET', 'POST'])
def add_item():
    if not session.get("is_admin"):
        flash("You must be an admin to access that page.", "danger")
        return redirect(url_for("login")) 

    categories = Category.query.all()

    # Define campuses with their respective blocks
    campuses = [
        {'name': 'Steve Biko', 'blocks': ['S1', 'S2', 'S3']},
        {'name': 'Riston Campus', 'blocks': ['B1', 'B2', 'B3']},
        {'name': 'ML Sultan', 'blocks': ['L1', 'L2', 'L3']}
    ]

    if request.method == 'POST':
        # Extract form data
        item_name = request.form['item_name']
        item_desc = request.form['item_desc']
        status = request.form['status']
        category_name = request.form['category_name']
        category_id = None
        campus_name = request.form.get('campus_name')
        campus_block = request.form.get('campus_block')

        # Check if campus name and block match
        campus = next((campus for campus in campuses if campus['name'] == campus_name), None)
        if not campus or campus_block not in campus['blocks']:
            flash('Invalid campus block selected.', 'danger')
            return redirect(url_for('add_item'))

        # Handle image upload
        image_url = None
        if 'item_image' in request.files:
            image = request.files['item_image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                image_url = f"images/{filename}"

        # Create the item 
        new_item = Item(
            item_name=item_name,
            item_desc=item_desc,
            status=ItemStatus(status),
            category_id=category_id,
            campus_name=campus_name,
            campus_block=campus_block,
            image_url=image_url
        )
        db.session.add(new_item)
        db.session.commit()

        flash('Item added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_item.html', categories=categories, campuses=campuses)


  
#for deleting items from the table
@app.route('/admin/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if not session.get("is_admin"):  # Ensure that only admins can delete
        return redirect(url_for("login"))

    # Find the item by its ID
    item_to_delete = Item.query.get(item_id)

    if item_to_delete:
        db.session.delete(item_to_delete)
        db.session.commit()
        flash('Item deleted successfully!', 'success')
    else:
        flash('Item not found!', 'danger')

    return redirect(url_for('admin_dashboard'))  # Redirect to the admin dashboard


#For the claimed items from the students
@app.route('/admin/claim_item/<int:claim_id>', methods=['GET', 'POST'])
def admin_claim_item(claim_id):
    if not session.get("is_admin"):
        flash("You must be an admin to access that page.", "danger")
        return redirect(url_for("login", next=request.url))

    claim = ClaimedItem.query.get_or_404(claim_id)
    item = claim.item
    description = ItemDescription.query.get_or_404(claim.description_id)

    if claim.matching_score is None:
        matching_score = calculate_matching_score(item.item_desc, claim.description.item_description)
        claim.matching_score = matching_score
        db.session.commit()

    if request.method == 'POST':
        approval = request.form.get('approval')
        student_email = claim.student.student_email  # Assuming you have a relationship to student
        student_name = claim.student.student_fname

        if approval == 'approve':
            claim.approval = True
            # Generate a random collection date (e.g. within 3 to 7 days)
            collect_date = datetime.utcnow() + timedelta(days=random.randint(3, 7))
            message_body = f"""Dear {student_name},

Your claim for the item '{item.item_name}' has been **approved**.

You can collect your item on: {collect_date.strftime('%Y-%m-%d')} at the Lost & Found Office.

Thank you.
"""
        else:
            claim.approval = False
            message_body = f"""Dear {student_name},

Unfortunately, your claim for the item '{item.item_name}' has been **rejected** after careful review.

Please contact support if you think this is a mistake.

Regards,
Lost & Found Admin
"""

        db.session.commit()

        # Send email
        try:
            msg = Message("Claim Status Update", recipients=[student_email])
            msg.body = message_body
            mail.send(msg)
            flash('Claim has been processed and email sent successfully.', 'success')
        except Exception as e:
            flash(f"Error sending email: {e}", 'danger')

        return redirect(url_for('admin_dashboard'))

    return render_template('admin_claim_item.html', claim=claim, item=item, matching_score=claim.matching_score)



#//////////////////////////////////////////////End of admin///////////////////////////////////////////////////////
  


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email'] 
        message = request.form['message']
        # Process or store the form data (send email, save to database, etc.)
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

 
 
@app.route('/logout')   
@login_required
def logout():
    logout_user()  # Log the user out
    flash("You have been logged out.", 'success')
    return redirect(url_for('login'))  # Redirect to login page after logout


# Create the tables when app starts, only do this in dev environment
with app.app_context(): 
    db.create_all()
 
if __name__ == "__main__":    
    app.run(debug=True)   
