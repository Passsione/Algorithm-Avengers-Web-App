import re,os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import current_user,LoginManager
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laf_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "your_secret_key"   # Secret key for session management later

#Image configuration
UPLOAD_FOLDER = 'static/uploads'  # Folder for uploaded images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check allowed image types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


db.init_app(app)

# Admin Credentials
ADMIN_EMAIL = "12345678@dut4life.ac.za"
ADMIN_PASSWORD = "admin123"

#This is for the student email of DUT so that it can only include dut4life at the end
EMAIL_REGEX = r'^\d{8}@dut4life\.ac\.za$'

# This is for the student number, to make sure that the student number has the exact 8 digits
STUDENT_NUMBER_REGEX = r'^\d{8}$'


# Routes

@app.route('/')   # This router is for the home page or the landing page
def home():
    items = Item.query.all() #Getting all the item from the database
    return render_template('home.html')

@app.route('/signup', methods=['POST', 'GET'])  # This router is for the signup page
def signup():
    if request.method == 'POST':                #POST for submiting the form to the database
        student_num = request.form['student_num']
        student_fname = request.form['student_fname']
        student_lname = request.form['student_lname']
        student_email = request.form['student_email']
        student_quali = request.form['student_quali']
        student_password = request.form['student_password']

        # for email validation of dut
        if not re.match(EMAIL_REGEX, student_email):
            flash("Invalid email format. Please use a valid university email (e.g., 12345678@dut4life.ac.za).", "danger")
            return redirect(url_for('signup'))

        # The student number should only have 8 digits because of the dut policy or whatever...
        if not re.match(STUDENT_NUMBER_REGEX, student_num):
            flash("Student number must be exactly 8 digits.", "danger")
            return redirect(url_for('signup'))

        # Checking to see if student already exists
        existing_student = Student.query.filter(
            (Student.student_email == student_email) | (Student.student_num == student_num)
        ).first()

        if existing_student:
            flash("Student with this email or number already exists!", "danger")
            return redirect(url_for('signup'))

        # Hashing the password before saving
        hashed_password = generate_password_hash(student_password)

        new_stud = Student(                               #creating a new student
            student_num=student_num,
            student_fname=student_fname,
            student_lname=student_lname,
            student_email=student_email,
            student_quali=student_quali,
            student_password=hashed_password  # Storing the hashed password
        )

        db.session.add(new_stud)
        db.session.commit()     # Saving changes in the database
        flash("Account created successfully!", "success")
        return redirect(url_for('home'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])         #This router is for the login page and the admin credential are hardcoded
def login():
    if request.method == 'POST':
        student_email = request.form['student_email']
        student_password = request.form['student_password']

        # Lokhu okokuvalidatha email so that it has the @dut4life.ac.za
        if not re.match(EMAIL_REGEX, student_email):
            flash("Invalid email format. Please use a valid university email (e.g., 12345678@dut4life.ac.za).", "danger")
            return redirect(url_for('student_dashboard'))

        
        if student_email == ADMIN_EMAIL and student_password == ADMIN_PASSWORD: #we are checking for the hardcoded credentials
            session['user_type'] = 'admin'
            session['email'] = student_email
            flash("Welcome, Admin!", "success")
            return redirect(url_for('admin_dashboard')) 

        
        student = Student.query.filter_by(student_email=student_email).first() #Deose the student exist in the database?

        if student and check_password_hash(student.student_password, student_password):
            session['user_type'] = 'student'
            session['email'] = student_email
            flash("Login successful!", "success")
            return redirect(url_for('home'))  # Redirect to student dashboard/home

        flash("Invalid email or password. Please try again.", "danger")

    return render_template('login.html')

#////////////////////////////////////////////////For students/////////////////////////////////////////////////////////////////////

@app.route('/student_dashboard') # Assuming you have a login system
def student_dashboard():
    student = Student.query.filter_by(student_num=current_user.student_num).first()
    
    # Fetch the student's reports
    reports = Report.query.filter_by(student_num=student.student_num).all()
    
    # Fetch the student's notifications
    notifications = Notification.query.filter_by(user_type='student', user_id=student.student_num).all()
    
    # Fetch the chat messages between the student and admin
    chat_messages = ChatMessage.query.filter_by(student_num=student.student_num).all()

    return render_template('student_dashboard.html', 
                           reports=reports, 
                           notifications=notifications, 
                           chat_messages=chat_messages)

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&For the Reports of found items%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#this is for the students who have found missing items to report them to the admin
@app.route('/report_found/<int:item_id>', methods=['POST', 'GET'])
def report_found(item_id):
    # Ensure the user is logged in
    if not current_user.is_authenticated:
        flash("Please log in to report a found item.", "warning")
        return redirect(url_for('login'))

    # Fetch the item by item_id
    item = Item.query.get_or_404(item_id)

    if request.method == 'POST':
        # Collect form data
        location = request.form['location']
        campus = request.form['campus']
        block = request.form['block']
        item_features = request.form['item_features']

        # Create the new found item report
        new_found_report = Report(
            student_num=current_user.student_num,  # Use current_user instead of session
            item_id=item_id,
            location=location,
            campus=campus,
            block=block,
            item_features=item_features
        )

        # Add the new report to the database
        db.session.add(new_found_report)
        db.session.commit()

        # Optionally update the item status (if you wish to change it to 'reported' or similar)
        item.status = ItemStatus.FOUND  # Assuming you want to track that the item was found
        db.session.commit()

        flash("Your found item report has been submitted. Admin will review it.", "success")
        return redirect(url_for('home'))  # Redirect to home or another appropriate page

    return render_template('report_found_item.html', item=item)




#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$End of the student that report missing items$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#For the student to claim the lost items 
@app.route('/claim/<int:item_id>', methods=['POST'])
def claim_item(item_id):
    if 'email' not in session:
        flash("Please log in to claim an item.", "warning")
        return redirect(url_for('login'))

    item = Item.query.get_or_404(item_id)
    existing_claim = ClaimedItem.query.filter_by(item_id=item_id, student_num=session['student_num']).first()

    if existing_claim:
        flash("You have already claimed this item.", "warning")
        return redirect(url_for('home'))

    new_claim = ClaimedItem(
        student_num=session['student_num'],
        item_id=item_id,
        approval=False  # Firstly the claim is not approve, we should wait for the admin to do that
    )

    db.session.add(new_claim)
    db.session.commit()
    flash("You have successfully claimed the item.", "success")
    return redirect(url_for('home'))

#.///////////////////////////////////////////End for the students///////////////////////////////////////////////////////////


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ For the chat room and notification@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#For the chat room = student to admin message
@app.route('/chat/<int:report_id>', methods=['GET', 'POST'])
def chat_with_admin(report_id):
    report = FoundItemReport.query.get(report_id)
    if request.method == 'POST':
        message = request.form['message']
        new_message = ChatMessage(
            student_num=report.student_num,
            admin_id=None,  # Admin ID will be assigned later
            message_text=message
        )
        db.session.add(new_message)
        db.session.commit()

        # Notify admin about the student's message
        new_notification = Notification(
            user_type='admin',
            user_id='admin_id',  # Replace with actual admin ID, maybe via session or static assignment
            message=f"Student has sent a message regarding found item report (ID: {report.report_id})."
        )
        db.session.add(new_notification)
        db.session.commit()

        return redirect(url_for('chat_with_admin', report_id=report_id))

    # Retrieve the chat messages between student and admin
    chat_messages = ChatMessage.query.filter_by(student_num=report.student_num).all()
    return render_template('chat_room.html', report=report, chat_messages=chat_messages)

# Chat Route for Admin to Respond (Admin to Student)
@app.route('/admin/chat/<int:report_id>', methods=['GET', 'POST'])
def admin_chat(report_id):
    report = FoundItemReport.query.get(report_id)
    
    if request.method == 'POST':
        message = request.form['message']
        
        # Add the admin's message to the chat
        new_message = ChatMessage(
            student_num=report.student_num,
            admin_id=current_user.id,  # Use the logged-in admin's ID
            message_text=message
        )
        db.session.add(new_message)
        db.session.commit()

        # After the admin responds, notify the student
        new_notification = Notification(
            user_type='student',
            user_id=report.student_num,
            message=f"Admin has responded to your found item report (ID: {report.report_id})."
        )
        db.session.add(new_notification)
        db.session.commit()

        return redirect(url_for('admin_chat', report_id=report_id))

    # Retrieve the chat messages between student and admin
    chat_messages = ChatMessage.query.filter_by(student_num=report.student_num).all()
    return render_template('admin_chat_room.html', report=report, chat_messages=chat_messages)

# Mark Notification as Read
@app.route('/mark_notification_read/<int:notification_id>')
def mark_notification_read(notification_id):
    notification = Notification.query.get(notification_id)
    notification.read = True
    db.session.commit()

    return redirect(url_for('student_dashboard'))  # Or admin's dashboard


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@End of chat room and notification @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$For the Admin$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'email' not in session:  # Check if the admin is logged in
        flash("Please log in to access the admin dashboard.", "warning")
        return redirect(url_for('login'))
    
    # Get all the lost items and claims for the admin to manage
    lost_items = Item.query.all()  # List of lost items
    found_reports = FoundItemReport.query.all()  # List of found item reports
    claims = ClaimedItem.query.all()  # List of claims
    
    return render_template('admin_dashboard.html', lost_items=lost_items, found_reports=found_reports, claims=claims)


#for the admin to add lost items into the system
@app.route('/add_lost_item', methods=['GET', 'POST'])
def add_lost_item():
    if request.method == 'POST':
        item_name = request.form.get('name')
        item_desc = request.form.get('description')
        category_id = request.form.get('category_id')  # Optional category
        status = ItemStatus.AVAILABLE  # Default status
        
        # Validate input
        if not item_name or not item_desc:
            flash('Item name and description are required!', 'danger')
            return redirect(request.url)
        
        # Handle Image Upload
        image_url = None
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                image_url = f"static/uploads/{filename}"  # Store relative path

        # Create new item entry
        new_item = Item(
            item_name=item_name,
            item_desc=item_desc,
            status=status,
            category_id=category_id if category_id else None,
            image_url=image_url
        )

        db.session.add(new_item)
        db.session.commit()
        flash('Lost item has been added successfully!', 'success')

        return redirect(url_for('admin_dashboard'))  

    categories = Category.query.all()  # Fetch categories for dropdown
    return render_template('add_lost_item.html', categories=categories)


#this is for the admin to verify the items that were reported

@app.route('/verify_found_item/<int:report_id>', methods=['GET'])
def verify_found_item(report_id):
    if 'email' not in session:  # Check if the admin is logged in
        flash("Please log in to verify found items.", "warning")
        return redirect(url_for('login'))
    
    report = FoundItemReport.query.get_or_404(report_id)
    
    # Create the new lost item based on the found report
    new_item = Item(name=report.item_name, description=report.description, status='Available')
    db.session.add(new_item)
    db.session.commit()

    flash("Found item has been verified and posted as a lost item.", "success")
    return redirect(url_for('admin_dashboard'))

#for approving claimed items
@app.route('/approve_claim/<int:claim_id>', methods=['GET'])
def approve_claim(claim_id):
    if 'email' not in session:
        flash("Please log in to approve claims.", "warning")
        return redirect(url_for('login'))
    
    claim = ClaimedItem.query.get_or_404(claim_id)
    item = claim.item
    item.status = 'Claimed'  # Mark the item as claimed
    db.session.commit()
    
    flash(f"Claim for {item.name} has been approved.", "success")
    return redirect(url_for('admin_dashboard'))

#this is the route for rejecting claimed items

@app.route('/reject_claim/<int:claim_id>', methods=['GET'])
def reject_claim(claim_id):
    if 'email' not in session:
        flash("Please log in to reject claims.", "warning")
        return redirect(url_for('login'))
    
    claim = ClaimedItem.query.get_or_404(claim_id)
    
    # Optionally, notify the student their claim was rejected
    db.session.delete(claim)
    db.session.commit()
    
    flash(f"Claim for {claim.item.name} has been rejected.", "danger")
    return redirect(url_for('admin_dashboard'))


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$End for the admin$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#The about router
@app.route('/about')
def about():
    return render_template('about.html')

#The contact page 
@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
