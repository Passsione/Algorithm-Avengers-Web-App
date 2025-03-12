from flask_sqlalchemy  import *

db = SQLAlchemy()
class Admin(db.Model):  # Admin table
    __tablename__ = 'admin'
    admin_id = db.column(db.Integer, primary_key=true)
    admin_fname = db.column(db.String(100), nullable=false)
    admin_lname = db.column(db.String(100), nullable=false)
    admin_email = db.column(db.String(100), nullable=false)
    admin_password = db.column(db.String(100), nullable=false)


class Item(db.Model): # Item table
    __tablename__ = 'item'
    item_id = db.column(db.Integer, primary_key=true)
    item_name = db.column(db.String(100), nullable=false)
    item_desc = db.column(db.Text, nullable=false)
    item_catergory = db.column(db.String(30))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    admin = db.relationship("Admin", backref=backref("admin", uselist=False))
    
class Student(db.Model): # Student table
    __tablename__ = 'student'

    student_num = db.column(db.Integer, primary_key=true)
    student_fname = db.column(db.String(100), nullable=false)
    student_lname = db.column(db.String(100), nullable=false)
    student_email = db.column(db.String(100), nullable=false)
    student_password = db.column(db.String(100), nullable=false)
    student_quali = db.column(db.String(100), nullable=false)
    student_id = db.column(db.Integer, nullable=false)

'''
Report entity
- report ID
- Student number
- Date & time
- Admin ID
- Item ID
- Location
'''


'''
Claimed Item entity
- Student number
- Item ID
- Admin ID
- Approval
- Description provided by the claimer
'''



