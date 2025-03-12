from flask import *
from user import routes

app = Flask(__name__)

# Route

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

'''
@app.route('/contact/')                   #function for the contact page
def contact():
    return render_template('contact.html')
'''

@app.route('/SignUp/')                   #function for the signup page
def signup_view():
    return render_template('signup.html')



if __name__ == '__main__':
    app.run(debug=True)

