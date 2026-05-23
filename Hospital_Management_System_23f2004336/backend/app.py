from flask import Flask, request, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_cors import CORS
from models import db, Users, Patients, Doctors, Appointments,Treatments
from config import Config
from datetime import datetime
import os
import csv
import json
import random
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, time, date, timedelta
import csv
from celery import Celery
from celery.schedules import crontab
import smtplib
from email.message import EmailMessage
from celery.schedules import crontab
from flask import render_template
from flask_caching import Cache

app = Flask(__name__)
CORS(app)

cache = Cache(app, config={
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_URL": "redis://localhost:6379/0",
    "CACHE_DEFAULT_TIMEOUT": 300
})

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config.from_object(Config)

app.config['broker_url'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['broker_url'])
celery.conf.update(app.config)

celery.conf.timezone = 'Asia/Kolkata' 

celery.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'send_daily_reminders',
        'schedule': crontab(hour=8, minute=0), 
    },
    'send-monthly-reports': {
        'task': 'send_monthly_reports',
        'schedule': crontab(day_of_month='1', hour=0, minute=0),
    }
}

db.init_app(app)
api = Api(app)
jwt = JWTManager(app)

def create_tables():
    with app.app_context():
        db.create_all()
        if not Users.query.filter_by(role='admin').first():
            admin = Users(
                username='admin', 
                email='admin@hospital.com', 
                role='admin', 
                first_name='Super', 
                last_name='Admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin Created Successfully")
        else:
            print("Tables checked. Admin already exists.")


def send_hospital_email(to_address, subject, content, is_html=False):
    import smtplib
    from email.message import EmailMessage
    
    SENDER_EMAIL = "guptashubhi006@gmail.com"
    APP_PASSWORD = "abcd efgh ijkl mnop" # replace with your google app password

    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_address

    if is_html:
        msg.set_content(content, subtype='html')
    else:
        msg.set_content(content)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print(f" EMAIL SENT to {to_address} via Gmail!")
        return True
    except Exception as e:
        print(f" SMTP Error: {e}")
        return False
    
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    existing_email = db.session.scalar(db.select(Users).filter_by(email=data.get('email')))
    if existing_email:
        return jsonify({"message": "Email already registered"}), 400
        
    existing_username = db.session.scalar(db.select(Users).filter_by(username=data.get('username')))
    if existing_username:
        return jsonify({"message": "Username already taken"}), 400

    new_user = Users(
        username=data['username'],
        email=data['email'],
        role='patient',  
        first_name=data['first_name'],
        last_name=data['last_name']
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    
    db.session.flush() 

    new_patient = Patients(
        user_id=new_user.id,
        date_of_birth=None, 
        gender=data.get('gender', 'Other'),
        address=data.get('address', ''),
        phone_number=data.get('phone_number', '')
    )
    db.session.add(new_patient)

    db.session.commit()
    return jsonify({"message": "Patient registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Users.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        access_token = create_access_token(
            identity=str(user.id), 
            additional_claims={'role': user.role}
        )
        return jsonify({
            "access_token": access_token, 
            "role": user.role,
            "username": user.username,
            "first_name": user.first_name
        }), 200
    
    return jsonify({"message": "Invalid credentials"}), 401


@app.route('/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"message": "Access denied"}), 403

    return jsonify({
        "total_doctors": Doctors.query.count(),
        "total_patients": Patients.query.count(),
        "total_users": Users.query.count()
    }), 200

@app.route('/admin/users', methods=['GET'])
@jwt_required()
def admin_users():
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"message": "Access denied"}), 403

    doctors = db.session.query(Doctors, Users).join(Users).all()
    doctor_list = []
    for doc, user in doctors:
        doctor_list.append({
            "id": doc.id,
            "user_id": user.id,
            "name": f"{user.first_name} {user.last_name}",
            "specialization": doc.specialization,
            "is_approved": True, 
            "role": "doctor"
        })

    patients = db.session.query(Patients, Users).join(Users).all()
    patient_list = []
    for pat, user in patients:
        patient_list.append({
            "id": pat.id,
            "user_id": user.id,
            "name": f"{user.first_name} {user.last_name}",
            "role": "patient"
        })

    return jsonify({"doctors": doctor_list, "patients": patient_list}), 200

@app.route('/admin/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"message": "Access denied"}), 403

    user_to_delete = Users.query.get(user_id)
    if not user_to_delete:
        return jsonify({"message": "User not found"}), 404
    
    if user_to_delete.role == 'admin':
        return jsonify({"message": "Cannot delete admin"}), 400

    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

@app.route('/admin/add_doctor', methods=['POST'])
@jwt_required()
def add_doctor():
    claims = get_jwt()
    if str(claims.get('role')).lower() != 'admin':
        return jsonify({'message': 'Access Denied: Admin only'}), 403

    data = request.get_json()
    
    if db.session.scalar(db.select(Users).filter_by(email=data['email'])):
        return jsonify({'message': 'Email already exists'}), 400

    full_name_parts = data['name'].strip().split(' ', 1)
    first_name_val = full_name_parts[0]
    last_name_val = full_name_parts[1] if len(full_name_parts) > 1 else "Doctor"

    safe_username = data['name'].strip().lower().replace(" ", "_")
    
    if db.session.scalar(db.select(Users).filter_by(username=safe_username)):
        safe_username = f"{safe_username}{random.randint(10,99)}"

    new_user = Users(
        username=safe_username,
        email=data['email'],
        role='doctor',
        first_name=first_name_val,
        last_name=last_name_val
    )
    new_user.set_password(data['password']) 
    
    db.session.add(new_user)
    db.session.flush() 

    new_doctor = Doctors(
        user_id=new_user.id,
        specialization=data['specialization'],
        experience=0,
        qualification="MBBS",
        consultation_fee=500,
        address=data.get('address', ''),       
        phone_number=data.get('phone_number', ''),
        department_id=data.get('department_id', None) 
    )
    db.session.add(new_doctor)
    db.session.commit()

    return jsonify({'message': 'Doctor added successfully'}), 201

@app.route('/admin/update_doctor/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_doctor(user_id):
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({'message': 'Access Denied'}), 403

    data = request.get_json()
    user_to_edit = Users.query.get(user_id)
    doctor_profile = Doctors.query.filter_by(user_id=user_id).first()

    if not user_to_edit or not doctor_profile:
        return jsonify({'message': 'Doctor not found'}), 404

    if 'name' in data and data['name']:
        user_to_edit.username = data['name']
        parts = data['name'].strip().split(' ', 1)
        user_to_edit.first_name = parts[0]
        user_to_edit.last_name = parts[1] if len(parts) > 1 else "Doctor"

    if 'password' in data and data['password'].strip():
        user_to_edit.password = generate_password_hash(data['password'])

    if 'specialization' in data: doctor_profile.specialization = data['specialization']
    if 'experience' in data: doctor_profile.experience = data['experience']
    if 'qualification' in data: doctor_profile.qualification = data['qualification']
    if 'consultation_fee' in data: doctor_profile.consultation_fee = data['consultation_fee']
    if 'address' in data: doctor_profile.address = data['address']
    if 'phone_number' in data: doctor_profile.phone_number = data['phone_number']
    if 'department_id' in data and data['department_id']: doctor_profile.department_id = data['department_id']

    db.session.commit()
    return jsonify({'message': 'Doctor profile updated successfully'}), 200


@app.route('/admin/trigger/daily', methods=['POST', 'OPTIONS'])
@jwt_required()
def trigger_daily_reminders():
    if request.method == 'OPTIONS': return jsonify({'message': 'OK'}), 200
    send_daily_reminders.delay() 
    return jsonify({'message': 'Daily reminders started!'}), 200

@app.route('/admin/trigger/monthly', methods=['POST', 'OPTIONS'])
@jwt_required()
def trigger_monthly_reports():
    if request.method == 'OPTIONS': return jsonify({'message': 'OK'}), 200
    send_monthly_reports.delay() 
    return jsonify({'message': 'Monthly reports started!'}), 200


@app.route('/patient/doctors', methods=['GET'])
@jwt_required()
def get_doctors_with_availability():
    doctors = Doctors.query.all()
    result = []

    for doc in doctors:
        user = db.session.get(Users, doc.user_id)
        
        raw_val = doc.availability or ""
        display_text = "Schedule not set"

        try:
            sched_dict = json.loads(raw_val)
            if sched_dict:
                available_days = [d for d, info in sched_dict.items() if info.get('is_available')]
                
                if len(available_days) == 7:
                    display_text = "Available 7 Days a Week"
                elif len(available_days) > 0:
                    display_text = f"Available {len(available_days)} Days a Week"
                else:
                    display_text = "Currently on Leave"
            else:
                display_text = "Schedule not set"
        except:
            display_text = raw_val if raw_val else "Schedule not set"
        result.append({
            'id': doc.id,
            'name': f"Dr. {user.first_name} {user.last_name}" if user else "Unknown",
            'specialization': doc.specialization,
            'fee': doc.consultation_fee,
            'availability_text': display_text 
        })

    return jsonify(result), 200


@app.route('/patient/book', methods=['POST', 'OPTIONS'])
@jwt_required()
def book_appointment():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200

    current_user_id = get_jwt_identity()
    patient = Patients.query.filter_by(user_id=current_user_id).first()
    data = request.get_json()
    
    req_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    req_time = datetime.strptime(data['time'], '%H:%M').time()
    date_str = req_date.strftime('%Y-%m-%d')
    
    doctor = Doctors.query.get(data['doctor_id'])
    
    try:
        schedule = json.loads(doctor.availability)
        day_config = schedule.get(date_str)
        
        if not day_config or not day_config.get('is_available'):
            return jsonify({'message': 'Doctor is on leave or unavailable on this specific date.'}), 400
            
        start_time = datetime.strptime(day_config['start_time'], '%H:%M').time()
        end_time = datetime.strptime(day_config['end_time'], '%H:%M').time()
        
        if not (start_time <= req_time <= end_time):
            f_start = start_time.strftime('%I:%M %p')
            f_end = end_time.strftime('%I:%M %p')
            return jsonify({'message': f'On {date_str}, this doctor is only available from {f_start} to {f_end}.'}), 400
            
    except Exception as e:
        if not (time(9, 0) <= req_time <= time(17, 0)):
             return jsonify({'message': 'Doctor is only available between 09:00 AM and 05:00 PM.'}), 400

    conflict = Appointments.query.filter_by(doctor_id=doctor.id, appointment_date=req_date, appointment_time=req_time).first()
    if conflict and conflict.appointment_status != 'Cancelled':
        return jsonify({'message': 'Doctor is already booked at that exact time.'}), 400

    new_appt = Appointments(patient_id=patient.id, doctor_id=data['doctor_id'], appointment_date=req_date, appointment_time=req_time, appointment_status='Booked')
    db.session.add(new_appt)
    db.session.commit()
    
    return jsonify({'message': 'Appointment booked successfully!'}), 201
    

@app.route('/patient/my_appointments', methods=['GET', 'OPTIONS'])
@jwt_required()
def my_appointments():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200

    current_user_id = get_jwt_identity()
    patient = Patients.query.filter_by(user_id=current_user_id).first()
    
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
        
    appts = Appointments.query.filter_by(patient_id=patient.id).order_by(Appointments.appointment_date.desc()).all()
    output = []
    
    for a in appts:
        doctor = db.session.get(Doctors, a.doctor_id)
        doc_user = db.session.get(Users, doctor.user_id)
        
        treatment = Treatments.query.filter_by(appointment_id=a.id).first()
        
        output.append({
            'id': a.id,
            'doctor_name': f"Dr. {doc_user.first_name} {doc_user.last_name}",
            'specialization': doctor.specialization,
            'date': str(a.appointment_date),
            'time': str(a.appointment_time),
            'status': a.appointment_status,
            'diagnosis': treatment.diagnosis if treatment else "N/A",
            'prescription': treatment.prescription if treatment else "N/A",
            'notes': treatment.notes if treatment and treatment.notes else "",
            'next_visit': str(treatment.next_visit) if treatment and treatment.next_visit else ""
        })
        
    return jsonify(output), 200

@app.route('/patient/appointment/<int:appt_id>/cancel', methods=['PUT', 'OPTIONS'])
@jwt_required()
def cancel_appointment(appt_id):
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200

    current_user_id = get_jwt_identity()
    patient = Patients.query.filter_by(user_id=current_user_id).first()
    appt = db.session.get(Appointments, appt_id)

    if not appt or appt.patient_id != patient.id:
        return jsonify({'message': 'Appointment not found'}), 404

    if appt.appointment_status in ['Booked', 'Confirmed']:
        appt.appointment_status = 'Cancelled'
        db.session.commit()
        return jsonify({'message': 'Appointment cancelled successfully'}), 200
    else:
        return jsonify({'message': 'Cannot cancel this appointment'}), 400


@app.route('/patient/appointment/<int:appt_id>/reschedule', methods=['PUT', 'OPTIONS'])
@jwt_required()
def reschedule_appointment(appt_id):
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200

    current_user_id = get_jwt_identity()
    patient = Patients.query.filter_by(user_id=current_user_id).first()
    appt = Appointments.query.get(appt_id)

    if not appt or appt.patient_id != patient.id:
        return jsonify({'message': 'Appointment not found'}), 404

    data = request.get_json()
    req_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    req_time = datetime.strptime(data['time'], '%H:%M').time()
    date_str = req_date.strftime('%Y-%m-%d')

    doctor = db.session.get(Doctors, appt.doctor_id)

    try:
        import json
        schedule = json.loads(doctor.availability)
        day_config = schedule.get(date_str)
        
        if not day_config or not day_config.get('is_available'):
            return jsonify({'message': 'Doctor is on leave or unavailable on this date.'}), 400
            
        start_time = datetime.strptime(day_config['start_time'], '%H:%M').time()
        end_time = datetime.strptime(day_config['end_time'], '%H:%M').time()
        
        if not (start_time <= req_time <= end_time):
            return jsonify({'message': 'Time is outside doctor availability.'}), 400
    except Exception:
        if not (time(9, 0) <= req_time <= time(17, 0)):
             return jsonify({'message': 'Doctor is only available between 09:00 AM and 05:00 PM.'}), 400

    conflict = Appointments.query.filter(
        Appointments.doctor_id == doctor.id,
        Appointments.appointment_date == req_date,
        Appointments.appointment_time == req_time,
        Appointments.id != appt.id, 
        Appointments.appointment_status != 'Cancelled'
    ).first()

    if conflict:
        return jsonify({'message': 'Doctor is already booked at that exact time.'}), 400

    appt.appointment_date = req_date
    appt.appointment_time = req_time
    appt.appointment_status = 'Booked' 
    db.session.commit()

    return jsonify({'message': 'Appointment rescheduled successfully!'}), 200


@app.route('/patient/profile', methods=['GET', 'PUT', 'OPTIONS'])
@jwt_required()
def manage_patient_profile():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200

    current_user_id = get_jwt_identity()
    user = db.session.get(Users, current_user_id)
    patient = Patients.query.filter_by(user_id=current_user_id).first()

    if request.method == 'GET':
        return jsonify({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': patient.phone_number,
            'address': patient.address,
            'gender': patient.gender,
            'dob': str(patient.date_of_birth) if patient.date_of_birth else ''
        }), 200

    if request.method == 'PUT':
        data = request.get_json()
        
        if 'first_name' in data: user.first_name = data['first_name']
        if 'last_name' in data: user.last_name = data['last_name']
        if 'password' in data and data['password'].strip():
            user.set_password(data['password'])

        if 'phone_number' in data: patient.phone_number = data['phone_number']
        if 'address' in data: patient.address = data['address']
        if 'gender' in data: patient.gender = data['gender']
        if 'dob' in data and data['dob']: 
            patient.date_of_birth = datetime.strptime(data['dob'], '%Y-%m-%d').date()

        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    
@app.route('/patient/doctor/<int:doc_id>/schedule', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_doctor_schedule_for_patient(doc_id):
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    
    doctor = Doctors.query.get(doc_id)
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
    today = date.today()
    next_7_days = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    
    try:
        saved_schedule = json.loads(doctor.availability) if doctor.availability else {}
    except:
        saved_schedule = {}

    output = []
    for d in next_7_days:
        if d in saved_schedule:
            output.append({'date': d, **saved_schedule[d]})
        else:
            output.append({'date': d, 'is_available': True, 'start_time': '09:00', 'end_time': '17:00'})
            
    return jsonify(output), 200

@celery.task(name="app.export_patient_history_task")
def export_patient_history_task(patient_id, user_email):
    with app.app_context():
        history = Appointments.query.filter_by(patient_id=patient_id, appointment_status='Completed').all()
        
        patient = db.session.get(Patients, patient_id)
        patient_user = db.session.get(Users, patient.user_id)
        
        filename = f"patient_{patient_id}_history.csv"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'User ID', 
                'Username', 
                'Consulting Doctor', 
                'Appointment Date', 
                'Diagnosis', 
                'Treatment Given', 
                'Next Visit Suggested'
            ])
            
            for appt in history:
                treatment = Treatments.query.filter_by(appointment_id=appt.id).first()
                
                doctor = db.session.get(Doctors, appt.doctor_id)
                doc_user = db.session.get(Users, doctor.user_id)
                doc_name = f"Dr. {doc_user.first_name} {doc_user.last_name}"
                
                diag = treatment.diagnosis if treatment else "N/A"
                tx_given = treatment.prescription if treatment else "N/A"
                next_v = str(treatment.next_visit) if (treatment and treatment.next_visit) else "Not Specified"
                
                writer.writerow([
                    patient_user.id,
                    patient_user.username,
                    doc_name,
                    str(appt.appointment_date),
                    diag,
                    tx_given,
                    next_v
                ])
        
        download_url = f"http://127.0.0.1:5000/static/uploads/{filename}"
        
        subject = "Your Detailed Medical History Export is Ready"
        body = f"Hello {patient_user.first_name},\n\n" \
               f"Your detailed treatment history has been generated. " \
               f"You can download the CSV file here: {download_url}"
        
        send_hospital_email(user_email, subject, body)
        
        return filepath
    
@celery.task(name="send_daily_reminders")
def send_daily_reminders():
    with app.app_context():
        today_obj = date.today()
        today_str = today_obj.strftime('%Y-%m-%d')
        
        print(f"\n ATTEMPTING REMINDERS FOR {today_str} ")

        all_appts = Appointments.query.all()
        print(f"Total appointments in DB: {len(all_appts)}")

        appointments = Appointments.query.filter(
            (Appointments.appointment_date == today_obj) | (Appointments.appointment_date == today_str),
            Appointments.appointment_status.in_(['Booked', 'Confirmed'])
        ).all()
        
        print(f"Matching appointments found for today: {len(appointments)}")
        
        for appt in appointments:
            print(f"Processing Appointment ID: {appt.id} for Patient ID: {appt.patient_id}")
            
            patient = db.session.get(Patients, appt.patient_id)
            if not patient:
                print("Error: Patient record not found.")
                continue
                
            user = db.session.get(Users, patient.user_id)
            doctor = db.session.get(Doctors, appt.doctor_id)
            doc_user = db.session.get(Users, doctor.user_id) if doctor else None

            if user and doc_user:
                subject = "Reminder: Hospital Appointment Today!"
                body = f"Dear {user.first_name}, reminder for your appointment with Dr. {doc_user.last_name} today at {appt.appointment_time}."
                
                print(f"Attempting to send real email to: {user.email}")
                send_hospital_email(user.email, subject, body)
                print("Email function called successfully.")
            else:
                print("Error: Missing User or Doctor details for this appointment.")

        print(" REMINDER JOB FINISHED \n")
        return "Task complete"
    
celery.conf.beat_schedule = {
    'daily-morning-reminder': {
        'task': 'send_daily_reminders', 
        'schedule': crontab(hour=8, minute=0),
    },
    'monthly-doctor-report': {
        'task': 'send_monthly_reports',
        'schedule': crontab(0, 0, day_of_month='1'),
    },
}
celery.conf.timezone = 'Asia/Kolkata'


@celery.task(name="send_monthly_reports")
def send_monthly_reports():
    with app.app_context():
        today = datetime.today()
        start_of_month = date(today.year, today.month, 1)
        
        doctors = Doctors.query.all()
        print(f"\n RUNNING MONTHLY DOCTOR REPORTS JOB FOR {today.strftime('%B %Y')}")
        
        for doc in doctors:
            user = db.session.get(Users, doc.user_id)
            
            completed_appts = Appointments.query.filter(
                Appointments.doctor_id == doc.id,
                Appointments.appointment_status == 'Completed',
                Appointments.appointment_date >= start_of_month 
            ).all()
            
            report_entries = []
            for appt in completed_appts:
                treatment_record = Treatments.query.filter_by(appointment_id=appt.id).first()
                patient = db.session.get(Patients, appt.patient_id)
                p_user = db.session.get(Users, patient.user_id)
                
                if treatment_record:
                    report_entries.append({
                        "date": appt.appointment_date,
                        "patient_name": f"{p_user.first_name} {p_user.last_name}",
                        "diagnosis": treatment_record.diagnosis,
                        "treatment": treatment_record.prescription
                    })

            html_body = render_template(
                'monthly_report.html',
                doctor_name=user.last_name,
                generated_at=today.strftime('%B %Y'),
                report_data=report_entries
            )
            
            if user.email:
                send_hospital_email(
                    user.email, 
                    "Your Monthly Activity Report", 
                    html_body, 
                    is_html=True
                )
                print(f"Report sent to: {user.email}")
            
        return "Monthly reports sent."


@app.route('/patient/export_history', methods=['POST', 'OPTIONS'])
@jwt_required()
def trigger_export():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)
    patient = Patients.query.filter_by(user_id=current_user_id).first()
    
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
        
    export_patient_history_task.delay(patient.id, user.email)
    
    return jsonify({'message': 'Export started! You will receive an email alert shortly.'}), 202


@app.route('/doctor/appointments', methods=['GET'])
@jwt_required()
def get_doctor_appointments():
    current_user_id = get_jwt_identity()
    doctor = Doctors.query.filter_by(user_id=current_user_id).first()
    
    if not doctor:
        return jsonify({'message': 'Doctor profile not found'}), 404
        
    appts = Appointments.query.filter_by(doctor_id=doctor.id).all()
    output = []
    
    for a in appts:
        patient = db.session.get(Patients, a.patient_id)
        p_user = Users.query.get(patient.user_id)
        
        output.append({
            'id': a.id,
            'patient_id': a.patient_id,  
            'patient_name': f"{p_user.first_name} {p_user.last_name}",
            'date': str(a.appointment_date),
            'time': str(a.appointment_time),
            'status': a.appointment_status,
            'remarks': ""
        })
    return jsonify(output), 200

@app.route('/doctor/update_profile', methods=['PUT'])
@jwt_required()
def doctor_update_profile():
    current_user_id = get_jwt_identity()
    doctor = Doctors.query.filter_by(user_id=current_user_id).first()
    
    if not doctor:
        return jsonify({'message': 'Doctor profile not found'}), 404

    data = request.get_json()

    if 'availability' in data:
        doctor.availability = data['availability']
    if 'consultation_fee' in data:
        doctor.consultation_fee = data['consultation_fee']
    
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully!'}), 200


@app.route('/get_dashboard_data', methods=['GET'])
@jwt_required()
def get_dashboard_data():
    try:
        users = Users.query.all()
        user_list = []
        
        for user in users:
            user_data = {
                'id': user.id,
                'user_id': user.id,
                'username': f"{user.first_name} {user.last_name}",
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'role': user.role,
                'status': 'Active',
            }
            if user.role == 'doctor':
                doctor_profile = Doctors.query.filter_by(user_id=user.id).first()
                if doctor_profile:
                    user_data.update({
                        'specialization': doctor_profile.specialization,
                        'experience': doctor_profile.experience,
                        'qualification': doctor_profile.qualification,
                        'consultation_fee': doctor_profile.consultation_fee,
                        'address': doctor_profile.address,
                        'phone_number': doctor_profile.phone_number
                    })
            user_list.append(user_data)

        return jsonify({
            'users': user_list,
            'stats': {
                'doctors': Users.query.filter_by(role='doctor').count(),
                'patients': Users.query.filter_by(role='patient').count(),
                'appointments': Appointments.query.count()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/doctors', methods=['GET'])
@cache.cached(timeout=60)
def get_doctors_public():
    
    print(" DATABASE HIT: Fetching public doctor list...")
    doctors = Doctors.query.all()
    output = []
    
    for doc in doctors:
        user = db.session.get(Users, doc.user_id)
        if user:
            output.append({
                'id': doc.id,
                'name': f"Dr. {user.first_name} {user.last_name}",
                'specialization': doc.specialization,
                'fee': doc.consultation_fee
            })
            
    return jsonify(output), 200


@app.route('/doctor/treat_patient', methods=['POST', 'OPTIONS'])
@jwt_required()
def treat_patient():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    try:
        data = request.get_json()
        
        next_visit_str = data.get('next_visit')
        next_visit_date = None
        
        if next_visit_str and next_visit_str.strip():
            try:
                next_visit_date = datetime.strptime(next_visit_str, '%Y-%m-%d').date()
            except ValueError:
                print(f"Warning: Received invalid date format: {next_visit_str}")

        new_treatment = Treatments(
            appointment_id=data['appointment_id'],
            diagnosis=data['diagnosis'],
            prescription=data['prescription'],
            notes=data.get('notes', ''),
            next_visit=next_visit_date 
        )
        db.session.add(new_treatment)
        appt = db.session.get(Appointments, data['appointment_id'])
        if appt:
            appt.appointment_status = "Completed"
        
        db.session.commit()
        return jsonify({'message': 'Treatment saved successfully!'}), 201
        
    except Exception as e:
        db.session.rollback()
        print("ERROR SAVING TREATMENT:", str(e))
        return jsonify({'message': 'Database error', 'error': str(e)}), 500
    
@app.route('/doctor/patient_history/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient_history(patient_id):
    history = Appointments.query.filter_by(patient_id=patient_id, appointment_status='Completed').all()
    output = []
    
    for appt in history:
        treatment = Treatments.query.filter_by(appointment_id=appt.id).first()
        
        doctor = db.session.get(Doctors, appt.doctor_id)
        doc_user = db.session.get(Users, doctor.user_id) if doctor else None
        
        if treatment and doc_user: 
            output.append({
                'id': treatment.id,  
                'date': str(appt.appointment_date),
                'doctor': f"Dr. {doc_user.first_name} {doc_user.last_name}",
                'diagnosis': treatment.diagnosis,
                'prescription': treatment.prescription,
                'notes': treatment.notes if treatment.notes else "",       
                'next_visit': str(treatment.next_visit) if treatment.next_visit else ""
            })
    
    return jsonify(output), 200


@app.route('/doctor/appointment/<int:id>', methods=['PUT', 'OPTIONS'])
@jwt_required()
def update_appointment_status(id):
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200

    data = request.get_json()
    appt = Appointments.query.get(id)
    
    if not appt:
        return jsonify({'message': 'Appointment not found'}), 404
        
    if 'status' in data:
        appt.appointment_status = data['status']
    
    db.session.commit()
    return jsonify({'message': 'Appointment updated'}), 200

@app.route('/doctor/profile', methods=['GET'])
@jwt_required()
def get_doctor_profile():
    current_user_id = get_jwt_identity()
    doctor = Doctors.query.filter_by(user_id=current_user_id).first()
    
    if not doctor:
        return jsonify({'message': 'Doctor profile not found'}), 404
        
    return jsonify({
        'availability': doctor.availability,
        'consultation_fee': doctor.consultation_fee
    }), 200

@app.route('/doctor/schedule', methods=['GET'])
@jwt_required()
def get_doctor_schedule():
    current_user_id = get_jwt_identity()
    doctor = Doctors.query.filter_by(user_id=current_user_id).first()
    
    today = date.today()
    next_7_days = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    
    try:
        saved_schedule = json.loads(doctor.availability) if doctor.availability else {}
    except:
        saved_schedule = {} 

    output = []
    for d in next_7_days:
        if d in saved_schedule:
            output.append({'date': d, **saved_schedule[d]})
        else:
            output.append({'date': d, 'is_available': True, 'start_time': '09:00', 'end_time': '17:00'})
            
    return jsonify({'schedule': output, 'fee': doctor.consultation_fee}), 200

import json

@app.route('/doctor/schedule', methods=['PUT', 'OPTIONS'])
@jwt_required()
def update_doctor_schedule():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    current_user_id = get_jwt_identity()
    
    doctor = db.session.scalar(db.select(Doctors).filter_by(user_id=current_user_id))
    
    if not doctor:
        return jsonify({"message": "Doctor profile not found"}), 404

    try:
        data = request.get_json()
        schedule_list = data.get('schedule', [])
        
        schedule_dict = {}
        for day in schedule_list:
            schedule_dict[day['date']] = {
                'is_available': day.get('is_available', False),
                'start_time': day.get('start_time', '09:00'),
                'end_time': day.get('end_time', '17:00')
            }
        
        doctor.availability = json.dumps(schedule_dict)
        
        if 'fee' in data:
            doctor.consultation_fee = data['fee']
        
        db.session.commit()
        return jsonify({'message': '7-Day Schedule updated successfully!'}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Schedule Save Error: {str(e)}")
        return jsonify({"message": "Failed to save schedule"}), 500

@app.route('/doctor/update_treatment/<int:t_id>', methods=['PUT'])
@jwt_required()
def update_treatment(t_id):
    claims = get_jwt()
    if str(claims.get('role')).lower() != 'doctor':
        return jsonify({"message": "Doctor access required"}), 403

    current_user_id = get_jwt_identity()
    current_doctor = db.session.scalar(db.select(Doctors).filter_by(user_id=current_user_id))
    
    if not current_doctor:
        return jsonify({"message": "Doctor profile not found"}), 404

    treatment = db.session.get(Treatments, t_id)
    if not treatment:
        return jsonify({"message": "Record not found"}), 404

    appointment = db.session.get(Appointments, treatment.appointment_id)
    if not appointment or appointment.doctor_id != current_doctor.id:
        return jsonify({"message": "Unauthorized: You can only edit your own patient records."}), 403

    data = request.get_json()
    treatment.diagnosis = data.get('diagnosis', treatment.diagnosis)
    treatment.prescription = data.get('prescription', treatment.prescription)
  
    db.session.commit()
    return jsonify({"message": "History updated successfully"}), 200


@app.route('/admin/stats', methods=['GET', 'OPTIONS'])
@jwt_required()
def admin_stats():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    total_doctors = Doctors.query.count()
    total_patients = Patients.query.count()
    total_appointments = Appointments.query.count()
    
    return jsonify({
        'doctors': total_doctors,
        'patients': total_patients,
        'appointments': total_appointments
    }), 200

@app.route('/admin/appointments', methods=['GET', 'OPTIONS'])
@jwt_required()
def admin_all_appointments():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    appts = Appointments.query.all()
    result = []
    for appt in appts:
        patient_record = db.session.get(Patients, appt.patient_id)
        patient_user = db.session.get(Users, patient_record.user_id) if patient_record else None

        doctor_record = db.session.get(Doctors, appt.doctor_id)
        doctor_user = db.session.get(Users, doctor_record.user_id) if doctor_record else None       
        result.append({
            'id': appt.id,
            'patient_name': f"{patient_user.first_name} {patient_user.last_name}",
            'doctor_name': f"Dr. {doctor_user.first_name} {doctor_user.last_name}",
            'date': str(appt.appointment_date),
            'time': str(appt.appointment_time),
            'status': appt.appointment_status
        })
    return jsonify(result), 200

@app.route('/admin/appointment/<int:appt_id>', methods=['DELETE', 'OPTIONS'])
@jwt_required() 
def admin_delete_appointment(appt_id):
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    claims = get_jwt()
    if str(claims.get('role')).lower() != 'admin':
        return jsonify({"message": "Admin access required"}), 403

    appt = db.session.get(Appointments, appt_id) 
    if not appt:
        return jsonify({"message": "Appointment not found"}), 404
    
    db.session.delete(appt)
    db.session.commit()
    return jsonify({"message": "Appointment removed by Admin"}), 200

@app.route('/admin/doctors', methods=['GET', 'POST', 'OPTIONS'])
@jwt_required()
def manage_doctors():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    if request.method == 'GET':
        doctors = Doctors.query.all()
        result = []
        for d in doctors:
            user = db.session.get(Users, d.user_id)
            if user:
                exp = getattr(d, 'experience_years', 'N/A')
                spec = getattr(d, 'specialization', 'General')
                
                result.append({
                    'id': d.id,
                    'user_id': user.id,
                    'name': f"{user.first_name} {user.last_name}",
                    'email': user.email,
                    'specialization': spec,
                    'experience': exp
                })
        return jsonify(result), 200
        
    if request.method == 'POST':
        data = request.get_json()
        
        if Users.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400
            
        generated_username = data['email'].split('@')[0]
            
        new_user = Users(
            username=generated_username,  
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role='Doctor',
            is_active=True 
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.flush() 
        
        new_doctor = Doctors(
            user_id=new_user.id,
            specialization=data.get('specialization', 'General'),
            experience=data.get('experience') or data.get('experience_years') or 0, 
            consultation_fee=data.get('fee') or data.get('consultation_fee') or 500,
            qualification=data.get('qualification', 'MBBS'), 
            availability=data.get('availability', 'Mon-Fri, 9 AM - 5 PM')
        )
        
        if hasattr(new_doctor, 'experience_years'):
            new_doctor.experience_years = data.get('experience_years', 0)
            
        db.session.add(new_doctor)
        db.session.commit()
        return jsonify({'message': 'Doctor added successfully'}), 201
    
@app.route('/admin/doctor/<int:doc_id>', methods=['PUT', 'DELETE', 'OPTIONS'])
@jwt_required()
def edit_doctor(doc_id):
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    doctor = db.session.get(Doctors, doc_id)
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
        
    user = db.session.get(Users, doctor.user_id)
    
    if request.method == 'DELETE':
        try:
            db.session.delete(doctor)
            if user:
                db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'Doctor deleted successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Failed to delete doctor', 'error': str(e)}), 500

    if request.method == 'PUT':
        data = request.get_json()
        
        if 'first_name' in data: user.first_name = data['first_name']
        if 'last_name' in data: user.last_name = data['last_name']
        
        if 'specialization' in data: doctor.specialization = data['specialization']
        
        if hasattr(doctor, 'experience_years') and 'experience' in data:
            doctor.experience_years = data['experience']
            
        db.session.commit()
        return jsonify({'message': 'Doctor updated successfully'}), 200

@app.route('/admin/patients', methods=['GET', 'OPTIONS'])
@jwt_required()
def admin_patients():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200

    claims = get_jwt()
    if str(claims.get('role')).lower() != 'admin':
        return jsonify({"message": "Admin access required"}), 403

    patients = Patients.query.all()
    result = []
    for p in patients:
        user = db.session.get(Users, p.user_id)
        
        if user:
            gender = getattr(p, 'gender', 'N/A')
            phone = getattr(p, 'phone_number', 'N/A')

            result.append({
                'id': p.id,
                'name': f"{user.first_name} {user.last_name}",
                'email': user.email,
                'gender': gender,
                'phone': phone
            })
    return jsonify(result), 200


@app.route('/admin/patient/<int:pat_id>', methods=['DELETE', 'OPTIONS'])
@jwt_required()
def delete_patient(pat_id):
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    patient = Patients.query.get(pat_id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
        
    user = Users.query.get(patient.user_id)
    
    Appointments.query.filter_by(patient_id=pat_id).delete()
    
    db.session.delete(patient)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Patient removed successfully'}), 200


@app.route('/admin/patient/<int:pat_id>', methods=['PUT', 'OPTIONS'])
@jwt_required()
def edit_patient(pat_id):
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
        
    data = request.get_json()
    patient = Patients.query.get(pat_id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
        
    user = Users.query.get(patient.user_id)
    
    if 'first_name' in data: user.first_name = data['first_name']
    if 'last_name' in data: user.last_name = data['last_name']
    
    if hasattr(patient, 'gender') and 'gender' in data:
        patient.gender = data['gender']
    if hasattr(patient, 'phone_number') and 'phone' in data:
        patient.phone_number = data['phone']
        
    db.session.commit()
    return jsonify({'message': 'Patient updated successfully'}), 200


if __name__ == '__main__':
    create_tables() 
    app.run(debug=True)
