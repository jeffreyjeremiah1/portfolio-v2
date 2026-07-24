# 🚀 Flask Portfolio CMS

A modern, production-ready portfolio website built with **Flask**, featuring a secure admin dashboard, project management system, contact form, and responsive user interface.

This application serves as both a personal portfolio and a lightweight content management system (CMS), allowing the administrator to manage portfolio projects and contact messages without modifying the source code.

---

## 📸 Screenshots

> Add screenshots after deployment.

| Home Page | Admin Dashboard |
|-----------|-----------------|
| ![Home](screenshots/home.png) | ![Dashboard](screenshots/dashboard.png) |

| Projects Management | Messages |
|---------------------|----------|
| ![Projects](screenshots/projects.png) | ![Messages](screenshots/messages.png) |

---

# ✨ Features

## Public Website

- Responsive Bootstrap 5 interface
- Hero section
- About section
- Skills section
- Services section
- Portfolio projects
- Contact form
- GitHub & Live Demo links
- Custom 404 & 500 error pages

---

## Admin Dashboard

Secure authentication using Flask-Login.

Features include:

- Dashboard overview
- Project management
- Contact message management
- Search projects
- Search messages
- Pagination
- Project image upload
- Flash notifications
- Bootstrap confirmation modal
- Responsive admin layout
- Sidebar navigation

---

# 🛠 Technology Stack

### Backend

- Python 3
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-WTF
- Flask-Login

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Jinja2 Templates
- Font Awesome

### Database

- SQLite (Development)
- PostgreSQL (Production Ready)

### Development Tools

- Git
- GitHub
- VS Code

---

# 📁 Project Structure

```
portfolio-cms/
│
├── migrations/
├── routes/
│   ├── admin.py
│   ├── auth.py
│   └── public.py
│
├── templates/
│   ├── admin/
│   ├── auth/
│   ├── errors/
│   ├── partials/
│   └── public/
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── uploads/
│
├── forms.py
├── models.py
├── config.py
├── app.py
├── requirements.txt
└── README.md
```

---

# 🔐 Authentication

The admin panel is protected using **Flask-Login**.

Authenticated users can:

- Create projects
- Edit projects
- Delete projects
- Read contact messages
- Delete messages

Unauthenticated users cannot access administrative routes.

---

# 📷 Image Uploads

Projects support image uploads.

Features include:

- Secure filenames
- Upload size limits
- Image storage inside `static/uploads`

---

# 📬 Contact System

Visitors can submit messages through the contact form.

Messages are:

- Stored in the database
- Displayed in the admin dashboard
- Marked as read when opened
- Searchable
- Paginated

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/flask-portfolio-cms.git
```

Enter the project

```bash
cd flask-portfolio-cms
```

Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```
SECRET_KEY=your_secret_key

DATABASE_URL=sqlite:///portfolio.db
```

---

# Database Setup

Initialize the database

```bash
flask db upgrade
```

Run the application

```bash
python app.py
```

Visit

```
http://127.0.0.1:5000
```

---

# Current Features

- ✅ Secure login
- ✅ Admin dashboard
- ✅ Project CRUD
- ✅ Contact form
- ✅ Message inbox
- ✅ Search
- ✅ Pagination
- ✅ Flash messages
- ✅ Responsive design
- ✅ Bootstrap modal confirmation
- ✅ SQLAlchemy ORM
- ✅ Flask Blueprints
- ✅ Flask-Migrate
- ✅ Custom error pages

---

# Planned Improvements

- User profile management
- Password change
- Email notifications
- Visitor analytics dashboard
- Resume management
- Image optimization
- PostgreSQL deployment
- Docker support
- CI/CD pipeline
- Unit testing
- REST API
- Dark mode

---

# Learning Objectives

This project demonstrates practical knowledge of:

- Flask application architecture
- MVC principles
- SQLAlchemy ORM
- Database migrations
- Authentication
- CRUD operations
- File uploads
- Form validation
- Server-side rendering
- Bootstrap UI
- Git workflow
- Secure configuration using environment variables

---

# License

This project is licensed under the MIT License.

---

# Author

**Jeffrey Jeremiah**

Management Information Systems (MIS)

GitHub:
https://github.com/YOUR_USERNAME

LinkedIn:
https://linkedin.com/in/YOUR_LINKEDIN

Email:
YOUR_EMAIL@example.com

---

## ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub.