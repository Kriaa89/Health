# MedConnect - Healthcare Management System

MedConnect is a comprehensive healthcare management system built with Django that facilitates interactions between doctors, nurses, and patients. The system allows for appointment scheduling, patient management, and real-time status tracking.

## Features

- **User Management**
  - Multi-role authentication (Doctors, Nurses, Patients)
  - Secure registration and login
  - Profile management with profile pictures

- **Appointment System**
  - Book appointments with preferred doctors
  - Real-time availability checking
  - Appointment status tracking (Pending, Confirmed, Completed, Cancelled)
  - Automatic time slot management

- **Dashboards**
  - Doctor Dashboard: Manage appointments, view patient details
  - Patient Dashboard: Book appointments, view medical history
  - Nurse Dashboard: View schedules and assist in patient management

## Prerequisites

- Python 3.8 or higher
- Django 4.0 or higher
- Virtual Environment

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd connect
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv djangoPy3Env
djangoPy3Env\Scripts\activate

# Linux/Mac
python3 -m venv djangoPy3Env
source djangoPy3Env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Common Issues and Solutions

### 1. Database Migration Issues
If you encounter migration errors:
```bash
# Remove all migrations files (except __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

# Remove the database
rm db.sqlite3

# Recreate migrations
python manage.py makemigrations
python manage.py migrate
```

### 2. Static Files Not Loading
If static files aren't loading properly:
```bash
python manage.py collectstatic
```

### 3. Permission Issues
For file permission issues on Linux/Mac:
```bash
chmod +x manage.py
chmod -R 755 media/
```

### 4. Virtual Environment Issues
If the virtual environment isn't working:
```bash
# Deactivate current environment (if any)
deactivate

# Remove old environment
rm -rf djangoPy3Env

# Create new environment
python -m venv djangoPy3Env

# Activate and reinstall dependencies
source djangoPy3Env/bin/activate  # or djangoPy3Env\Scripts\activate on Windows
pip install -r requirements.txt
```

### 5. Port Already in Use
If port 8000 is already in use:
```bash
# Kill the process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
sudo lsof -t -i:8000 | xargs kill -9
```

## Project Structure

```
connect/
├── accounts/           # User authentication and profiles
├── appointments/       # Appointment management
├── doctors/           # Doctor-specific functionality
├── nurses/            # Nurse-specific functionality
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
├── media/            # User-uploaded files
├── manage.py         # Django management script
└── requirements.txt  # Project dependencies
```

## Usage

1. Access the admin interface at: `http://localhost:8000/admin/`
2. Main application at: `http://localhost:8000/`
3. Register as a doctor or patient
4. Log in and access your dashboard
5. Start managing or booking appointments

## Development Commands

```bash
# Create a new app
python manage.py startapp app_name

# Make model changes
python manage.py makemigrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Shell
python manage.py shell

# Clear sessions
python manage.py clearsessions
```

## Security Notes

1. Never commit sensitive information (e.g., SECRET_KEY)
2. Use environment variables for sensitive data
3. Keep DEBUG=False in production
4. Regularly update dependencies
5. Backup your database regularly

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please create an issue in the repository or contact the development team.
