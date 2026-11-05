# FieldPro – Field Service Management System

FieldPro is a web-based Field Service Management System built using Django. It helps customers raise service requests, managers assign technicians, and technicians manage service activities.

## Features

### Customer
- Customer registration and login
- Create service requests
- View service request history
- View request details
- Cancel eligible requests
- Track service request status

### Manager
- View customer service requests
- Assign technicians to requests
- Monitor service request progress

### Technician
- View assigned service requests
- Update request status
- Mark requests as completed

## Technology Stack

- Python
- Django
- SQLite
- HTML5
- CSS3
- JavaScript
- Font Awesome

## Project Structure

- `core/` – Main Django project
- `users/` – User authentication and service management application
- `manage.py` – Django management utility

## Installation and Setup

1. Clone this repository:

   `git clone YOUR_GITHUB_REPOSITORY_URL`

2. Open the project folder.

3. Create and activate a Python virtual environment.

4. Install Django:

   `pip install django`

5. Run migrations:

   `python manage.py migrate`

6. Start the development server:

   `python manage.py runserver`

7. Open `http://127.0.0.1:8000/` in your browser.

## Testing

Run the following command:

`python manage.py test`

## Project Purpose

This project demonstrates Django development, role-based authentication, database relationships, CRUD operations, and service request management.

## Author

S. Shanmukha
