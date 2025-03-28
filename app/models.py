# app/models.py
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)                   
    name = db.Column(db.String(50))                                  
    username = db.Column(db.String(50), unique=True, nullable=False) 
    password = db.Column(db.String(100))                             
    last_login = db.Column(db.DateTime)                              
    last_password_change = db.Column(db.DateTime)                    
    last_failed_login = db.Column(db.DateTime)                       
    user_role = db.Column(db.String(20))                             
    must_change_password = db.Column(db.Boolean, default=True)       
    def __repr__(self):
        return f'<User {self.username}>'

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Location ID
    name = db.Column(db.String(100), nullable=False)  # Location name
    address = db.Column(db.String(200))  # Location address
    created_by = db.Column(db.String(50))  # Username of the creator
    def __repr__(self):
        return f'<Location {self.name}>'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Item ID
    name = db.Column(db.String(100), nullable=False)  # Item name
    category = db.Column(db.String(50))  # Item category
    created_by = db.Column(db.String(50))  # Username of the creator
    item_user = db.Column(db.String(50))  # Assigned user (one of current users)
    # Store location as foreign key referencing Location.id
    item_location = db.Column(db.Integer, db.ForeignKey('location.id'))
    # Relationship to access location details easily
    location = db.relationship('Location', backref='items', lazy=True)
    price = db.Column(db.Float)  # Item price

    def __repr__(self):
        return f'<Item {self.name}>'
