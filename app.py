from flask import *
from models import *
# from functools import wraps

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laf_db.db'



# Routes

@app.route('/')                  #function for the landing page
def home():
  return render_template('home.html')

@app.route('/about/')                    #function for the about page
def about():
    return render_template('about.html')


@app.route('/SignUp/')                   #function for the signup page
def signup_view():
    return render_template('signup.html')


@app.route('/StudentCard/')                   #function for claiming a student card page
def student_card():
    return render_template('student_card.html')

    
@app.route('/Searching/')                   #function for searching for a lost item page
def searching():
    return render_template('searching.html')

@app.route('/Browse/')                   #function for browsing items page
def browse():
    return render_template('browse.html')

@app.route('/Report/')                   #function for making a report page
def report():
    return render_template('report.html')

@app.route('/Claim/')                   #function for claiming an item page
def claim():
    return render_template('item.html')

@app.route('/LogIn/')                   #function for the Login page
def login_view():
    return render_template('Login.html')


@app.route('/Profile/')                   #function for the Profile page
def user_profile():
    return render_template('userprofile.html')


if __name__ == '__main__':
    app.run(debug=True)

