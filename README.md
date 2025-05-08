# 🧩 Task Management System

A role-based Task Management System built with **Django**. This application supports three user roles:

- **SuperAdmin** – Manages Admins and Users, creates and assigns tasks, and views reports.
- **Admin** – Manages Users and their tasks, and views reports.
- **User** – Views and updates their assigned tasks with status and completion reports.

---

## 🚀 Features

### Authentication
- JWT-based login system
- Role-based redirection
- Session-based HTML login for web admin panel

### SuperAdmin Capabilities
- Create Admins and Users
- Create and assign tasks
- View all tasks and completion reports

### Admin Capabilities
- Create Users
- Assign tasks to Users
- View reports for Users

### User Capabilities
- View their assigned tasks
- Submit task completion reports with worked hours
- Update task status

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/task-management.git
cd task-management

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
🔐 Login Endpoint
HTML Login (for Admin Panel)
URL: /user_login/

Method: POST

Form Fields:

  username

  password

Redirects based on user role:

SuperAdmin → /superadmin/dashboard/

Admin → /dashboard/admin

User → /user/dashboard/

Note : use this username = Athul , password = Athul123# .its a super admin after login u can acces the services


