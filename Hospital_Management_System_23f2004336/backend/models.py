from flask_sqlalchemy import SQLAlchemy
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False) 
    email = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(30), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    patient = db.relationship("Patients", back_populates="user", uselist=False, cascade="all, delete")
    doctor = db.relationship("Doctors", back_populates="user", uselist=False, cascade="all, delete")

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class Patients(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    user = db.relationship("Users", back_populates="patient")
    appointments = db.relationship("Appointments", back_populates="patient", cascade="all, delete-orphan")

class Doctors(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.department_id", ondelete='SET NULL'), nullable=True)
    
    specialization = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    consultation_fee = db.Column(db.Integer, nullable=False, default=0)
    
    availability = db.Column(db.String(100), default="Mon-Fri, 9 AM - 5 PM")
    
    address = db.Column(db.String(200), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)

    user = db.relationship("Users", back_populates="doctor")
    department = db.relationship("Departments", back_populates="doctors")
    appointments = db.relationship("Appointments", back_populates="doctor", cascade="all, delete-orphan")


class Departments(db.Model):
    __tablename__ = "departments"
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    
    doctors = db.relationship("Doctors", back_populates="department")

class Appointments(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False)
    
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    appointment_status = db.Column(db.String(20), nullable=False, default='Booked') 
    
    reason = db.Column(db.String(255), nullable=True)
    patient = db.relationship("Patients", back_populates="appointments")
    doctor = db.relationship("Doctors", back_populates="appointments")
    treatment = db.relationship("Treatments", back_populates="appointment", uselist=False, cascade="all, delete-orphan")

class Treatments(db.Model):
    __tablename__ = "treatments"
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id', ondelete='CASCADE'), nullable=False)
    
    diagnosis = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text, nullable=True) 
    notes = db.Column(db.Text, nullable=True)
    treatment_date = db.Column(db.Date, default=date.today)
    next_visit = db.Column(db.Date, nullable=True)
    
    appointment = db.relationship("Appointments", back_populates="treatment")
