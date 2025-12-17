# ApproveThis - Flask Learning Application

## Quick Start Guide

### 1. Installation
```bash
cd approvethis
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Database Setup
```bash
cp .env.example .env
flask db upgrade
flask seed all
```

### 3. Run Application
```bash
flask run
```

### 4. Login
- URL: http://127.0.0.1:5000
- Credentials: viewer/viewer123, developer/developer123, or admin/admin123

## What's Built

✅ Complete Flask application with Application Factory pattern
✅ RBAC system with 3 roles and 7 permissions
✅ Provider pattern for GitHub API abstraction
✅ Mock data for repositories, workflows, and runs
✅ 5 REST API endpoints
✅ 5 UI routes with modern responsive design
✅ Flask-Login authentication
✅ SQLite database with Flask-Migrate
✅ CLI commands for seeding data
✅ Comprehensive documentation

## File Count
- 52 application files
- ~2,000 lines of code
- 23 Python files
- 16 HTML templates
- Complete CSS and JavaScript

See README.md in the approvethis directory for full documentation.
