from flask import *            #imported all necessary libraries to use
app = Flask(__name__)

@app.route('/')                  #function for the landing page
def home():
    return render_template('home.html')
 
@app.route('/student_dashboard')     #function for what the logged in student 
def stud_dashboard():
    return "<h1> this will be a student dashboard </h1>"

@app.route('/admin_dashboard')        #function for the logged in admin
def admin_dashboard():
    return "<h1> this will an admin dashbaord </h1>"
    
@app.route('/login/')         
def login():
    return render_template('login.html')

@app.route('/about')                    #function for the about page
def about():
    return "<h1>about page</h1>"

@app.route('/contact')                   #function for the contact page
def contact "<h1> this is for the contact page</h1>"


if __name__ == '__main__':
    app.run(debug=True)
