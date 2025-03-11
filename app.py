from flask import *
from pymongo import *
app = Flask(__name__)

app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Database
# client = pymongo.MongoClient('localhost', 27017)
# db = client.user_login_system

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

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/about/')                    #function for the about page
def about():
    return render_template('about.html')

@app.route('/contact/')                   #function for the contact page
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)