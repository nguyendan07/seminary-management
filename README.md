# 📖 Seminary Management System

[![Django](https://img.shields.io/badge/Django-5.2-green?logo=django)](https://www.djangoproject.com/)  
[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)](https://www.postgresql.org/)  
[![Redis](https://img.shields.io/badge/Redis-7.0-red?logo=redis)](https://redis.io/)  
[![Celery](https://img.shields.io/badge/Celery-5.5-green?logo=celery)](https://docs.celeryproject.org/)  

A **modern Django-based web application** for comprehensive management of seminarians (students) and priests (mentors, teachers, and administrators) in a seminary institution.  
This project provides robust tools for administration, class organization, academic tracking, and priest-student mentorship with real-time features and background task processing.

---

## 🚀 Features

### 👥 User Management

- **Unified Authentication System** - Single `User` model for all roles
- **Role-based Access Control** - Seminarian, Priest, Staff, and Admin roles
- **Profile Management** - Detailed profiles for both seminarians and priests
- **Permission System** - Granular permissions based on roles and responsibilities

### 🎓 Seminary Student Management

- **Seminarian Profiles** - Complete personal and academic information
- **Year-based Organization** - Track students by formation year
- **Academic Status Tracking** - Monitor progress through seminary stages
- **Mentor Assignment** - Assign spiritual directors and academic advisors

### ⛪ Priest & Staff Management

- **Priest Profiles** - Position, specialization, and ministry details
- **Role Assignments** - Rector, formator, teacher, spiritual director roles
- **Specialization Areas** - Theology, philosophy, pastoral studies, liturgy, etc.
- **Teaching Assignments** - Manage course and class assignments

### 📚 Academic Management

- **Course Catalog** - Comprehensive curriculum management
- **Class Organization** - Manage yearly cohorts and sections
- **Subject Assignment** - Link courses to qualified instructors
- **Enrollment System** - Student registration and class management
- **Grade Management** - Academic performance tracking and reporting

### 🏛️ Church Structure Integration

- **Diocesan Integration** - Manage relationships with sending dioceses
- **Formation Stages** - Pre-theology, philosophy, theology levels
- **Ordination Tracking** - Monitor progress toward ordination
- **Ministry Assignments** - Track field education and pastoral assignments

### 🔧 Technical Features

- **Real-time Notifications** - Powered by Redis and Celery
- **Background Tasks** - Email notifications, report generation
- **Security Features** - CSP headers, secure authentication
- **Debug Tools** - Development debugging and monitoring
- **Static File Management** - Optimized asset serving with WhiteNoise

---

## 🏗️ Project Structure

```
seminary_management/
├── accounts/           # User authentication and profiles
├── church_structure/   # Diocesan and ecclesiastical hierarchy
├── courses/           # Academic courses and curriculum
├── students/          # Seminarian management
├── teachers/          # Priest and faculty management
├── seminary_management/ # Django project configuration
├── manage.py          # Django management script
├── pyproject.toml     # Project dependencies and configuration
└── requirements files # Dependency management
```

---

## 🛠️ Technology Stack

### Backend

- **Django 5.2** - Modern Python web framework
- **Python 3.13** - Latest Python version
- **PostgreSQL 15** - Robust relational database
- **Redis 7.0** - Caching and session storage

### Task Processing

- **Celery 5.5** - Distributed task queue
- **Django-Celery-Beat** - Periodic task scheduling

### Development & Production

- **Gunicorn** - WSGI HTTP Server
- **WhiteNoise** - Static file serving
- **Django Debug Toolbar** - Development debugging
- **Loguru** - Advanced logging

### Security

- **Django-CSP** - Content Security Policy
- **CSRF Protection** - Cross-site request forgery protection
- **Secure Headers** - Security-focused HTTP headers

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- PostgreSQL 15+
- Redis 7.0+
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/nguyendan07/seminary-management.git
   cd seminary-management
   ```

2. **Set up virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -e .
   ```

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your database, Redis, and other settings
   ```

5. **Set up database**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Start Redis server**

   ```bash
   redis-server
   ```

7. **Start Celery worker** (in separate terminal)

   ```bash
   celery -A seminary_management worker -l info
   ```

8. **Run development server**

   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000` to access the application.

---

## 📚 Data Model Overview

### Core Models

- **User** → Base authentication with role-based access (Seminarian, Priest, Staff, Admin)
- **SeminarianProfile** → Extended profile for seminary students
- **PriestProfile** → Extended profile for clergy and faculty
- **Class** → Yearly cohorts and academic groupings
- **Subject/Course** → Academic curriculum and course catalog
- **Enrollment** → Student-subject relationships with academic tracking

### Relationships

- Users have role-specific profiles (Seminarian or Priest)
- Seminarians can be enrolled in multiple subjects
- Priests can teach multiple subjects and mentor multiple seminarians
- Classes organize seminarians by year and academic level
- Church structure defines diocesan and hierarchical relationships

---

## 🔧 Development

### Running Tests

```bash
python manage.py test
```

### Code Quality

```bash
# Format code
black .
isort .

# Lint code
flake8 .
```

### Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Load Sample Data

```bash
python manage.py loaddata dev_data.json
```

After loading the sample data, you can log in to the admin page with:

- Username: admin
- Email: <admin@local.com>
- Password: 3ZbfEy-&JG23

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Support

For support and questions:

- 📧 Email: <support@seminary-management.com>
- 📖 Documentation: [Wiki](https://github.com/nguyendan07/seminary-management/wiki)
- 🐛 Issues: [GitHub Issues](https://github.com/nguyendan07/seminary-management/issues)

---

*Built with ❤️ for seminary education and formation*
