from flask import *
from functools import wraps
import pymongo
from user import routes

app = Flask(__name__)


# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

# Routes

@app.route('/')                  #function for the landing page
def home():
  return render_template('home.html')

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

