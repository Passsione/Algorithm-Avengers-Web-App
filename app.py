import re, os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laf_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "your_secret_key"  # Secret key for session management

# Image Configuration
UPLOAD_FOLDER = 'static/uploads'  # Folder for uploaded images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Route to redirect to if login is required

# User Loader for Flask-Login
@login_manager.user_loader
def load_user(student_num):
    return Student.query.get(int(student_num))

# Function to check allowed image types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db.init_app(app)

# Admin Credentials
ADMIN_EMAIL = "12345678@dut4life.ac.za"
ADMIN_PASSWORD = "admin123"

# Regex for email and student number validation
EMAIL_REGEX = r'^\d{8}@dut4life\.ac\.za$'
STUDENT_NUMBER_REGEX = r'^\d{8}$'


# Routes

@app.route('/')
def home():
    items = Item.query.all()
    return render_template('home.html', items=items)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        student_num = request.form['student_num']
        student_fname = request.form['student_fname']
        student_lname = request.form['student_lname']
        student_email = request.form['student_email']
        student_quali = request.form['student_quali']
        student_password = request.form['student_password']

        # Validate email and student number
        if not re.match(EMAIL_REGEX, student_email):
            flash("Invalid email format. Please use a valid university email (e.g., 12345678@dut4life.ac.za).", "danger")
            return redirect(url_for('signup'))

        if not re.match(STUDENT_NUMBER_REGEX, student_num):
            flash("Student number must be exactly 8 digits.", "danger")
            return redirect(url_for('signup'))

        # Check if student already exists
        existing_student = Student.query.filter(
            (Student.student_email == student_email) | (Student.student_num == student_num)
        ).first()

        if existing_student:
            flash("Student with this email or number already exists!", "danger")
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = generate_password_hash(student_password)

        # Create new student
        new_stud = Student(
            student_num=student_num,
            student_fname=student_fname,
            student_lname=student_lname,
            student_email=student_email,
            student_quali=student_quali,
            student_password=hashed_password
        )

        db.session.add(new_stud)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        student_email = request.form['student_email']
        student_password = request.form['student_password']

        # Validate email
        if not re.match(EMAIL_REGEX, student_email):
            flash("Invalid email format. Please use a valid university email (e.g., 12345678@dut4life.ac.za).", "danger")
            return redirect(url_for('login'))

        # Check admin credentials
        if student_email == ADMIN_EMAIL and student_password == ADMIN_PASSWORD:
            # login_user(Admin)
            session['user_type'] = 'admin'
            session['email'] = student_email
            flash("Welcome, Admin!", "success")
            return redirect(url_for('admin_dashboard'))

        # Check student credentials
        student = Student.query.filter_by(student_email=student_email).first()
        if student and check_password_hash(student.student_password, student_password):
            login_user(student)  # Log in the student using Flask-Login
            session['user_type'] = 'student'
            session['email'] = student_email
            flash("Login successful!", "success")
            return redirect(url_for('home') )

        flash("Invalid email or password. Please try again.", "danger")
    

    return render_template('login.html')



#///////////////////////////////////////////////////////For the student///////////////////////////////////////////////////////////////
@app.route('/student_dashboard')
@login_required
def student_dashboard():
    student = current_user  # Use current_user from Flask-Login
    reports = Report.query.filter_by(student_num=student.student_num).all()
    notifications = Notification.query.filter_by(user_type='student', user_id=student.student_num).all()
    chat_messages = ChatMessage.query.filter_by(student_num=student.student_num).all()

    return render_template('student_dashboard.html', 
                           reports=reports, 
                           notifications=notifications, 
                           chat_messages=chat_messages)

@app.route('/report_found/<int:item_id>', methods=['POST', 'GET'])
@login_required
def report_found(item_id):
    item = Item.query.get_or_404(item_id)

    if request.method == 'POST':
        location = request.form['location']
        campus = request.form['campus']
        block = request.form['block']
        item_features = request.form['item_features']
        
        # Create the new found item report
        new_found_report = Report(
            student_num=current_user.student_num,  # Use current_user from Flask-Login
            item_id=item_id,
            location=location,
            campus=campus,
            block=block,
            item_features=item_features
        )

        db.session.add(new_found_report)
        db.session.commit()

        # Update the item status
        item.status = ItemStatus.FOUND
        db.session.commit()

        flash("Your found item report has been submitted. Admin will review it.", "success")
        return redirect(url_for('home'))

    return render_template('report_found_item.html', item=item)

@app.route('/claim/<int:item_id>', methods=['POST'])
@login_required
def claim_item(item_id):
    item = Item.query.get_or_404(item_id)
    existing_claim = ClaimedItem.query.filter_by(item_id=item_id, student_num=current_user.student_num).first()

    if existing_claim:
        flash("You have already claimed this item.", "warning")
        return redirect(url_for('home'))
    if request.method == 'POST':
        new_claim = ClaimedItem(
            student_num=current_user.student_num,
            item_id=item_id,
            approval=False  # Initially not approved
        )

        db.session.add(new_claim)
        db.session.commit()
        flash("You have successfully claimed the item.", "success")
        return redirect(url_for('home'))

#//////////////////////////////////////////////End of the student/////////////////////////////////////////////////////////////




#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$Start of the admin$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'email' not in session or session['email'] != ADMIN_EMAIL:  # Check if admin is logged in
        flash("Please log in as admin to access this page.", "warning")
        return redirect(url_for('login'))
    
    # Fetch data for the admin dashboard
    lost_items = Item.query.all()
    found_reports = FoundItemReport.query.all()
    claims = ClaimedItem.query.all()
    
    return render_template('admin_dashboard.html', 
                           lost_items=lost_items, 
                           found_reports=found_reports, 
                           claims=claims)

@app.route('/add_lost_item', methods=['GET', 'POST'])          #The admin can add lost item to the system
def add_lost_item():
    if 'email' not in session or session['email'] != ADMIN_EMAIL:  # Check if admin is logged in
        flash("Please log in as admin to access this page.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        item_name = request.form.get('name')
        item_desc = request.form.get('description')
        category_id = request.form.get('category_id')  
        status = ItemStatus.AVAILABLE  # This is the default status for the item
        
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

@app.route('/verify_found_item/<int:report_id>', methods=['GET'])   #This is for verifying the item
def verify_found_item(report_id):
    if 'email' not in session or session['email'] != ADMIN_EMAIL:  # Check if admin is logged in
        flash("Please log in as admin to verify found items.", "warning")
        return redirect(url_for('login'))
    
    report = FoundItemReport.query.get_or_404(report_id)
    
    # Create the new lost item based on the found report
    new_item = Item(
        item_name=report.item_name,
        item_desc=report.description,
        status=ItemStatus.AVAILABLE
    )
    db.session.add(new_item)
    db.session.commit()

    flash("Found item has been verified and posted as a lost item.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/approve_claim/<int:claim_id>', methods=['GET'])  #This is for approving the claims of the student's item
def approve_claim(claim_id):
    if 'email' not in session or session['email'] != ADMIN_EMAIL:  # Check if admin is logged in
        flash("Please log in as admin to approve claims.", "warning")
        return redirect(url_for('login'))
    
    claim = ClaimedItem.query.get_or_404(claim_id)
    item = claim.item
    item.status = ItemStatus.CLAIMED  # Mark the item as claimed
    db.session.commit()
    
    flash(f"Claim for {item.item_name} has been approved.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/reject_claim/<int:claim_id>', methods=['GET']) #This is for rejecting the claims of the student's item
def reject_claim(claim_id):
    if 'email' not in session or session['email'] != ADMIN_EMAIL:  # Check if admin is logged in
        flash("Please log in as admin to reject claims.", "warning")
        return redirect(url_for('login'))
    
    claim = ClaimedItem.query.get_or_404(claim_id)
    
    # Optionally, notify the student their claim was rejected
    db.session.delete(claim)
    db.session.commit()
    
    flash(f"Claim for {claim.item.item_name} has been rejected.", "danger")
    return redirect(url_for('admin_dashboard'))

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$End of the admin$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/logout')  #this is the logout route
# @login_required # if uncommented, admin can't log out
def logout():
    logout_user()  # Log out the user using Flask-Login
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)