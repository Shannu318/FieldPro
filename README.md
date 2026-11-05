# FieldPro – Field Service Management System

FieldPro is a web-based Field Service Management System built using Python and Django. It helps customers raise service requests, managers assign technicians, and technicians manage service activities.

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
- `requirements.txt` – Project dependencies
- `.env.example` – Environment variable template
- `manage.py` – Django management utility

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Shannu318/FieldPro.git
cd FieldPro
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure environment variables

Create your own `.env` file by copying `.env.example`.

**Windows:**

```bash
copy .env.example .env
```

**macOS / Linux:**

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your own Django secret key.

You can generate a new secret key using:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Never share or upload your real `.env` file.

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Start the development server

```bash
python manage.py runserver
```

### 8. Open the application

Visit:

`http://127.0.0.1:8000/`

## Testing

Run the following command:

```bash
python manage.py test
```

## Project Purpose

This project demonstrates Django development, role-based authentication, database relationships, CRUD operations, and service request management.

## Author

**S. Shanmukha**

GitHub: [Shannu318](https://github.com/Shannu318)
