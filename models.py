from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Admin(db.Model):  # Admin table
    __tablename__ = 'admin'
    admin_id = db.column(db.Integer, primary_key=True)
    admin_fname = db.column(db.String(100), nullable=False)
    admin_lname = db.column(db.String(100), nullable=False)
    admin_email = db.column(db.String(100), nullable=False)
    admin_password = db.column(db.String(100), nullable=False)


class Item(db.Model): # Item table
    __tablename__ = 'item'
    item_id = db.column(db.Integer, primary_key=True)
    item_name = db.column(db.String(100), nullable=False)
    item_desc = db.column(db.Text, nullable=False)
    item_catergory = db.column(db.String(30))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    admin = db.relationship("Admin", backref=db.backref("admin", uselist=False))

    def __repr__(self):     # Instance of the class when printed
        return f'<Item {self.id}>'
    
class Student(db.Model): # Student table
    __tablename__ = 'student'

    student_num = db.column(db.Integer, primary_key=True)
    student_fname = db.column(db.String(100), nullable=False)
    student_lname = db.column(db.String(100), nullable=False)
    student_email = db.column(db.String(100), nullable=False)
    student_password = db.column(db.String(100), nullable=False)
    student_quali = db.column(db.String(100), nullable=False)
    student_id = db.column(db.Integer, nullable=False)



'''
Report entity
- report ID
- Student number
- Date & time #default = db.func.current_timestamp()
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



