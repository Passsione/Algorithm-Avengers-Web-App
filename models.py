from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

# Initialize SQLAlchemy
db = SQLAlchemy()

class ItemStatus(Enum):
    FOUND = 'found'
    LOST = 'lost'
    CLAIMED = 'claimed'
    AVAILABLE = 'Available'

class Student(db.Model):  # Student table
    __tablename__ = 'student'
    student_num = db.Column(db.String(8), primary_key=True)
    student_fname = db.Column(db.String(100), nullable=False)
    student_lname = db.Column(db.String(100), nullable=False)
    student_email = db.Column(db.String(100), nullable=False, unique=True)
    student_password = db.Column(db.String(100), nullable=False)
    student_quali = db.Column(db.String(100), nullable=False)

class Category(db.Model):  # Item Categories
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False, unique=True)

class Item(db.Model):  # Item table
    __tablename__ = 'item'
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    item_desc = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True) 
    status = db.Column(db.Enum(ItemStatus), default=ItemStatus.FOUND)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=True)
    category = db.relationship('Category', backref=db.backref('items', lazy=True))

class Report(db.Model):  # Report entity
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

class ClaimedItem(db.Model):  # Claimed Item entity
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

# New Table for Chat Messages between Student and Admin
class ChatMessage(db.Model):  # Chat messages between student and admin
    __tablename__ = 'chat_message'
    message_id = db.Column(db.Integer, primary_key=True)
    student_num = db.Column(db.String(8), db.ForeignKey('student.student_num'), nullable=False)
    admin_id = db.Column(db.String(8), nullable=True)  # Assuming admins have a student number or use their own identifier
    message_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    student = db.relationship('Student', backref=db.backref('chat_messages', lazy=True))

# New Table for Notifications to Admin and Student
class Notification(db.Model):  # Notifications for both Admin and Student
    __tablename__ = 'notification'
    notification_id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(50), nullable=False)  # 'student' or 'admin'
    user_id = db.Column(db.String(8), nullable=False)  # This would be student_num or admin identifier
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# New Table for Found Item Reports
class FoundItemReport(db.Model):  # Table to track the found item reports
    __tablename__ = 'found_item_report'
    report_id = db.Column(db.Integer, primary_key=True)
    student_num = db.Column(db.String(8), db.ForeignKey('student.student_num'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    location_found = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(ItemStatus), default=ItemStatus.FOUND)  # Found, verified, rejected
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    student = db.relationship('Student', backref=db.backref('found_reports', lazy=True))
    item = db.relationship('Item', backref=db.backref('found_reports', lazy=True))
