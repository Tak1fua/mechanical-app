from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tax_id = db.Column(db.String(20), unique=True, nullable=False)
    contact_info = db.Column(db.String(200))
    vehicles = db.relationship('Vehicle', backref='company', lazy=True)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(20), unique=True, nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    history = db.relationship('ServiceHistory', backref='vehicle', lazy=True)

class ServiceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Float)
