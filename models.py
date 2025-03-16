from flask_sqlalchemy  import *

db = SQLAlchemy()

class Admin(db.Model):  # Admin table
    __tablename__ = 'admin'
    admin_id = db.column(db.Integer, primary_key=True)
    admin_fname = db.column(db.String(100), nullable=False)
    admin_lname = db.column(db.String(100), nullable=False)
    admin_email = db.column(db.String(100), nullable=False)
    admin_password = db.column(db.String(100), nullable=False)


class Item(db.Model):  # Item table
    __tablename__ = 'item'
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    item_desc = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))  # Reference to Category table
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'))  # FK to Admin table
    
    category = db.relationship('Category', backref='items')
    admin = db.relationship('Admin', backref=db.backref('items', lazy=True))

    
class Category(db.Model):  # Item Categories
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False, unique=True)  # Category name (unique)

    
class Student(db.Model): # Student table
    __tablename__ = 'student'

    student_num = db.column(db.Integer, primary_key=True)
    student_fname = db.column(db.String(100), nullable=False)
    student_lname = db.column(db.String(100), nullable=False)
    student_email = db.column(db.String(100), nullable=False)
    student_password = db.column(db.String(100), nullable=False)
    student_quali = db.column(db.String(100), nullable=False)
    student_id = db.column(db.Integer, nullable=False)



class Report(db.Model):  # Report entity
    __tablename__ = 'report'

    report_id = db.Column(db.Integer, primary_key=True)
    student_num = db.Column(db.Integer, db.ForeignKey('student.student_num'), nullable=False)
    student = db.relationship('Student', backref=db.backref('reports', lazy=True))
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    item = db.relationship('Item', backref=db.backref('reports', lazy=True))
    location = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class ClaimedItem(db.Model):  # Claimed Item entity
    __tablename__ = 'claimed_item'

    claimed_item_id = db.Column(db.Integer, primary_key=True)
    student_num = db.Column(db.Integer, db.ForeignKey('student.student_num'), nullable=False)
    student = db.relationship('Student', backref=db.backref('claimed_items', lazy=True))
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    item = db.relationship('Item', backref=db.backref('claimed_items', lazy=True))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'), nullable=False)
    admin = db.relationship('Admin', backref=db.backref('claimed_items', lazy=True))
    approval = db.Column(db.Boolean, nullable=False, default=False)
    description = db.Column(db.Text, nullable=True)




