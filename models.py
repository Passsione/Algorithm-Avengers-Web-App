from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
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
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_num = db.Column(db.String(8), unique=True, nullable=False)
    student_fname = db.Column(db.String(100), nullable=False)
    student_lname = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, default=0) 
    student_email = db.Column(db.String(100), nullable=False, unique=True)
    student_password = db.Column(db.String(255), nullable=False)

    # UserMixin already implements get_id, so no need for this
    def get_id(self):
        return self.student_id

class Campus(db.Model):
    __tablename__ = 'campus'
    campus_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campus_name = db.Column(db.String(100), nullable=False)
    campus_block = db.Column(db.String(50), nullable=False)

class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(50), nullable=False, unique=True)

class Report(db.Model):
    __tablename__ = 'report'
    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.campus_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    img_url = db.Column(db.String(255)) 

    student = db.relationship('Student', backref=db.backref('reports', lazy=True))
    campus = db.relationship('Campus', backref=db.backref('reports', lazy=True))

class Item(db.Model):
    __tablename__ = 'item'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(100), nullable=False)
    item_desc = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Enum(ItemStatus), default=ItemStatus.FOUND, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.report_id'), nullable=True)

    category = db.relationship('Category', backref=db.backref('items', lazy=True))
    report = db.relationship('Report', backref=db.backref('items', lazy=True))

    # Relationship to Campus via Report


class ItemDescription(db.Model):
    __tablename__ = 'item_description'
    description_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('report.report_id'), nullable=False)
    item_description = db.Column(db.Text, nullable=False)

    item = db.relationship('Item', backref=db.backref('descriptions', lazy=True))
    report = db.relationship('Report', backref=db.backref('descriptions', lazy=True))

class ClaimedItem(db.Model):
    __tablename__ = 'claimed_item'
    claim_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    description_id = db.Column(db.Integer, db.ForeignKey('item_description.description_id'), nullable=True)
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.campus_id'), nullable=False)
    approval = db.Column(db.Boolean, default=False, nullable=False)
    matching_score = db.Column(db.Float, nullable=True)  # Store the matching score between 0 and 10
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship('Student', backref=db.backref('claimed_items', lazy=True, cascade='all, delete-orphan'))
    item = db.relationship('Item', backref=db.backref('claimed_items', lazy=True, cascade='all, delete-orphan'))
    description = db.relationship('ItemDescription', backref=db.backref('claimed_items', lazy=True, cascade='all, delete-orphan'))
    campus = db.relationship('Campus', backref=db.backref('claimed_items', lazy=True))


class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Notification {self.message}>"


class FoundItemReport(db.Model):
    __tablename__ = 'found_item_report'
    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    location_found = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(ItemStatus), default=ItemStatus.FOUND, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('Student', backref=db.backref('found_reports', lazy=True))
    item = db.relationship('Item', backref=db.backref('found_reports', lazy=True))
