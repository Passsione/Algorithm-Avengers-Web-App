from flask import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laf_db.db'  # Your database URI
 

# Routes

@app.route('/')  # Handle the login form
def handle_login():
    return render_template('login.html')
    
@app.route('/home/')  # Home page
def home():
    return render_template('home.html')

@app.route('/about/')  # About page
def about():
    return render_template('about.html')

@app.route('/SignUp/')  # Sign Up page
def signup_view():
    return render_template('signup.html')


@app.route('/StudentCard/')  # Claim student card page
def student_card():
    return render_template('student_card.html')

@app.route('/Claim/')  # Claim an item page
def claim():
    return render_template('item.html')

@app.route('/Searching/')  # Searching for a lost item page
def searching():
    return render_template('searching.html')

@app.route('/Browse/')  # Browse items page
def browse():
    return render_template('browse.html')

@app.route('/Report/')  # Report an item page
def report():
    return render_template('report.html')

@app.route('/Profile/')  # User Profile page
def user_profile():
    return render_template('userprofile.html')

# @app.route('/logout')  # Logout route
# def logout():   
if __name__ == '__main__':
    app.run(debug=True)
