MediCare: Hospital Management System
A full-stack role-based web application built to connect hospital administration, doctors, and patients in one seamless platform.

 Tech Stack

Frontend: Vue.js 3, Bootstrap 5 


Backend: Flask (Python), SQLite 


Background Tasks: Celery & Redis 

 How to Run the Project
To get the full application running, you will need to open a few different terminal windows. Follow these steps in order:

Step 1: Start the Backend (Flask API)
Open your first terminal, navigate to the backend folder, and activate your virtual environment.

Bash
# 1. Navigate to backend directory
cd backend

# 2. Activate virtual environment (Windows)
venv\Scripts\activate
# OR for Mac/Linux: source venv/bin/activate

# 3. Install requirements (if you haven't already)
pip install -r requirements.txt

# 4. Start the Flask server
python app.py
The backend is now running on http://127.0.0.1:5000.

Step 2: Start the Frontend (Vue.js)
Open a second terminal window and navigate to the frontend folder.

Bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies (only needed the first time)
npm install

# 3. Start the Vue development server
npm run serve
The frontend is now running on http://localhost:8080.

Step 3: Start Background Jobs (Redis & Celery)
For the automated emails, monthly reports, and CSV exports to work, you need to start the background workers. Open three more terminal windows, ensuring you are in the backend folder with your virtual environment activated for the Celery commands.

Terminal 3 (Start Redis):

Bash
redis-server
# If using WSL on Windows, use: sudo service redis-server start
Terminal 4 (Start Celery Worker):

Bash
# Ensure you are in the 'backend' folder and venv is active!
celery -A app.celery worker -l info --pool=solo
Terminal 5 (Start Celery Beat / The Scheduler):

Bash
# Ensure you are in the 'backend' folder and venv is active!
celery -A app.celery beat -l info