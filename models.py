from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from enum import Enum

# Initialize SQLAlchemy
db = SQLAlchemy()

class ItemStatus(Enum):
    FOUND = 'found'
    LOST = 'lost'
    CLAIMED = 'claimed'
    AVAILABLE = 'available'

class Student(db.Model, UserMixin):
    __tablename__ = 'student'
    student_num = db.Column(db.String(8), primary_key=True)
    student_fname = db.Column(db.String(100), nullable=False)
    student_lname = db.Column(db.String(100), nullable=False)
    student_email = db.Column(db.String(100), nullable=False, unique=True)
    student_password = db.Column(db.String(100), nullable=False)
    student_quali = db.Column(db.String(100), nullable=False)

    def get_id(self):
        return self.student_num

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False, unique=True)

class Item(db.Model):
    __tablename__ = 'item'
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    item_desc = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Enum(ItemStatus), default=ItemStatus.FOUND, nullable=False)  # Use Enum
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=True)
    category = db.relationship('Category', backref=db.backref('items', lazy=True))

class Report(db.Model):
    __tablename__ = 'report'
    report_id = db.Column(db.Integer, primary_key=True)
    student_num = db.Column(db.String(8), db.ForeignKey('student.student_num'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    campus = db.Column(db.String(100), nullable=False)
    block = db.Column(db.String(100), nullable=False)
    item_features = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    student = db.relationship('Student', backref=db.backref('reports', lazy=True))
    item = db.relationship('Item', backref=db.backref('reports', lazy=True))

class ClaimedItem(db.Model):
    __tablename__ = 'claimed_item'
    claimed_item_id = db.Column(db.Integer, primary_key=True)
    student_num = db.Column(db.String(8), db.ForeignKey('student.student_num'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    approval = db.Column(db.Boolean, nullable=False, default=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    student = db.relationship('Student', backref=db.backref('claimed_items', lazy=True))
    item = db.relationship('Item', backref=db.backref('claimed_items', lazy=True))

class Notification(db.Model):
    __tablename__ = 'notification'
    notification_id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(50), nullable=False)  # 'student' or 'admin'
    user_id = db.Column(db.String(8), nullable=False)  # This would be student_num or admin identifier
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class FoundItemReport(db.Model):
    __tablename__ = 'found_item_report'
    report_id = db.Column(db.Integer, primary_key=True)
    student_num = db.Column(db.String(8), db.ForeignKey('student.student_num'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    location_found = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(ItemStatus), default=ItemStatus.FOUND, nullable=False)  # Use Enum
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    student = db.relationship('Student', backref=db.backref('found_reports', lazy=True))
    item = db.relationship('Item', backref=db.backref('found_reports', lazy=True))

