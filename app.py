from flask import *
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/student_dashboard')
def stud_dashboard():
    return "<h1> this will be a student dashboard </h1>"

@app.route('/admin_dashboard')
def admin_dashboard():
    return "<h1> this will an admin dashbaord </h1>"
    
@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return "<h1>about page</h1>"

@app.route('/contact')
def contact ("<h1> this is for the contact page</h1>")


if __name__ == '__main__':
    app.run(debug=True)
