from flask import *
# from functools import wraps

app = Flask(__name__)



# Routes

@app.route('/')                  #function for the landing page
def home():
  return render_template('home.html')

@app.route('/login/')
def login ():
  return render_template('login.html')

@app.route('/signup/')
def signup ():
  return render_template('sign_up.html')

@app.route('/about/')                    #function for the about page
def about():
    return render_template('about.html')


@app.route('/SignUp/')                   #function for the signup page
def signup_view():
    return render_template('signup.html')


@app.route('/LogIn/')                   #function for the Login page
def login_view():
    return render_template('Login.html')


@app.route('/Profile/')                   #function for the Profile page
def user_profile():
    return render_template('userprofile.html')

if __name__ == '__main__':
    app.run(debug=True)

