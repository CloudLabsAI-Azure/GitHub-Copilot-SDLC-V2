# ApproveThis - Workflow Dispatch & Approval System

ApproveThis is a Flask-based learning application designed for teaching GitHub Copilot throughout the Software Development Lifecycle (SDLC). It serves as an internal job/workflow/process scheduling and approval tool for managing GitHub Actions workflows.

## 🎯 Purpose

This application is a **training tool** that demonstrates:
- Modern Flask application architecture (Application Factory pattern)
- Role-Based Access Control (RBAC) with fine-grained permissions
- Provider pattern for API abstraction
- RESTful API design
- GitHub Actions workflow management
- Clean separation of concerns with Blueprints

## ✨ Features

### Current Features
- **Authentication & Authorization**: Flask-Login with RBAC
- **Role Management**: Three built-in roles (Viewer, LeadDeveloper, GlobalAdmin)
- **Repository Browsing**: View GitHub repositories
- **Workflow Management**: List and view GitHub Actions workflows
- **Workflow Runs**: Track workflow execution history
- **Run Details**: View detailed job and step information
- **Workflow Dispatch**: Trigger workflow_dispatch workflows (permission-based)
- **Provider Pattern**: Abstract GitHub API calls with mock implementation

### Future Enhancements (Extension Points)
- Real GitHub API integration
- Approval workflows for workflow dispatches
- Dynamic form generation for workflow inputs
- Background task processing with Celery
- Webhook handlers for workflow events
- Advanced filtering and search
- Run log viewing
- User management UI

## 🏗️ Architecture

### Application Factory Pattern
The application uses Flask's Application Factory pattern with blueprints for modular organization:

```
app/
├── __init__.py              # Application factory
├── extensions.py            # Flask extensions (SQLAlchemy, Flask-Login, etc.)
├── providers/               # GitHub API abstraction layer
│   ├── base.py             # Abstract provider interface
│   ├── mock.py             # Mock implementation with JSON data
│   └── github.py           # Real GitHub API (placeholder)
├── models/                  # Database models
│   ├── user.py             # User with Flask-Login
│   ├── role.py             # Role & Permission (RBAC)
│   └── dispatch_request.py # Workflow dispatch tracking
├── blueprints/              # Application blueprints
│   ├── auth/               # Authentication routes
│   ├── main/               # UI routes
│   └── api/                # REST API endpoints
├── templates/               # Jinja2 templates
├── static/                  # CSS, JavaScript
└── cli/                     # CLI commands
```

### Provider Pattern
The provider pattern abstracts GitHub API calls, making it easy to:
- Develop with mock data
- Test without hitting the real GitHub API
- Switch between mock and real implementations
- Add caching or rate limiting in the future

### RBAC System

**Permission Bit Flags:**
- `VIEW_REPOS = 1` - View repositories
- `VIEW_WORKFLOWS = 2` - View workflows
- `VIEW_RUNS = 4` - View workflow runs
- `DISPATCH_WORKFLOW = 8` - Trigger workflow dispatches
- `MANAGE_APPROVALS = 16` - Manage approvals (future)
- `MANAGE_USERS = 32` - User management (future)
- `ADMIN = 64` - Full admin access (future)

**Built-in Roles:**
1. **Viewer**: Read-only access (VIEW_REPOS + VIEW_WORKFLOWS + VIEW_RUNS)
2. **LeadDeveloper**: Can dispatch workflows (all Viewer permissions + DISPATCH_WORKFLOW)
3. **GlobalAdmin**: Full access (all permissions)

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone or navigate to the directory:**
   ```bash
   cd approvethis
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env if needed
   ```

5. **Initialize the database:**
   ```bash
   flask db upgrade
   ```

6. **Seed the database with roles and default users:**
   ```bash
   flask seed all
   ```

7. **Run the application:**
   ```bash
   flask run
   ```

8. **Access the application:**
   Open your browser and navigate to: `http://127.0.0.1:5000`

### Default Login Credentials

| Username  | Password      | Role           | Permissions                           |
|-----------|---------------|----------------|---------------------------------------|
| viewer    | viewer123     | Viewer         | Read-only access                      |
| developer | developer123  | LeadDeveloper  | Read access + dispatch workflows      |
| admin     | admin123      | GlobalAdmin    | Full administrative access            |

## 📡 API Endpoints

All API endpoints require authentication and appropriate permissions.

### Repositories
- `GET /api/repos` - List all repositories (requires VIEW_REPOS)

### Workflows
- `GET /api/repos/{owner}/{repo}/workflows` - List workflows (requires VIEW_WORKFLOWS)
- `POST /api/repos/{owner}/{repo}/workflows/{workflow_id}/dispatch` - Dispatch workflow (requires DISPATCH_WORKFLOW)

### Workflow Runs
- `GET /api/repos/{owner}/{repo}/runs` - List workflow runs (requires VIEW_RUNS)
- `GET /api/repos/{owner}/{repo}/runs/{run_id}` - Get run details (requires VIEW_RUNS)

### Example API Call

```bash
# Login first to get a session cookie, then:
curl -X POST http://localhost:5000/api/repos/acme-corp/web-app/workflows/1002/dispatch \
  -H "Content-Type: application/json" \
  -d '{"ref": "main", "inputs": {}}'
```

## 🎓 Learning Paths

### For Beginners
1. Explore the application structure
2. Review the RBAC implementation
3. Study the provider pattern
4. Understand Flask blueprints

### For Intermediate Learners
1. Implement new API endpoints
2. Add new permissions and roles
3. Create custom workflow input forms
4. Add filtering and search features

### For Advanced Learners
1. Integrate real GitHub API
2. Implement approval workflows
3. Add Celery background tasks
4. Create webhook handlers
5. Add comprehensive test coverage

## 🛠️ CLI Commands

```bash
# Seed all data (roles + users)
flask seed all

# Seed only roles
flask seed roles

# Seed only users
flask seed users

# Database migrations
flask db init       # Initialize migrations (already done)
flask db migrate    # Create a new migration
flask db upgrade    # Apply migrations
flask db downgrade  # Rollback migrations
```

## 🔧 Configuration

Configuration is managed through `config.py` with three environments:

- **Development**: Debug enabled, SQLite database, mock provider
- **Testing**: In-memory SQLite, CSRF disabled
- **Production**: Production-ready settings, configurable provider

Environment variables (set in `.env`):
- `FLASK_ENV`: Environment name (development, testing, production)
- `SECRET_KEY`: Secret key for sessions
- `DATABASE_URL`: Database connection string
- `GITHUB_PROVIDER`: Provider type (mock or github)

## 🧪 Development

### Project Structure Highlights

**Models**: SQLAlchemy models with Flask-Login integration
- Proper relationships and foreign keys
- Business logic in model methods
- Static methods for seeding data

**Blueprints**: Organized by functionality
- `auth`: Login/logout
- `main`: UI routes
- `api`: REST API

**Templates**: Component-based organization
- Reusable components in `components/`
- Layout inheritance with `base.html`
- Macros for common patterns

**Provider Pattern**: Clean abstraction
- Abstract base class defines interface
- Mock implementation uses JSON files
- Easy to add real GitHub integration

### Mock Data

Mock data is stored in `app/mock_data/`:
- `repositories.json` - Sample repositories
- `workflows.json` - Workflows per repository
- `workflow_runs.json` - Workflow run history
- `workflow_run_details/` - Detailed run information with jobs and steps

## 🔐 Security Considerations

This is a **training application**. For production use, consider:
- Use strong SECRET_KEY
- Enable HTTPS
- Implement rate limiting
- Add CSRF protection for all forms
- Use environment variables for sensitive data
- Implement proper session management
- Add audit logging
- Validate and sanitize all inputs
- Implement OAuth for GitHub authentication

## 🤝 Contributing

This is a learning application. Students are encouraged to:
1. Fork the repository
2. Create feature branches
3. Implement new features or improvements
4. Submit pull requests with clear descriptions

## 📚 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Login](https://flask-login.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub REST API](https://docs.github.com/en/rest)

## 📝 License

This is a training application. Check the repository license for details.

## 🆘 Troubleshooting

### Database Issues
```bash
# Reset database
rm approvethis.db
flask db upgrade
flask seed all
```

### Import Errors
```bash
# Ensure you're in the virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Run on a different port
flask run --port 5001
```

## 🎯 Next Steps

1. **Try It Out**: Login with different users to see permission differences
2. **Explore the Code**: Follow the request flow from route to template
3. **Make Changes**: Add a new feature or modify existing ones
4. **Integrate GitHub**: Replace mock provider with real GitHub API calls
5. **Add Tests**: Write unit and integration tests
6. **Deploy**: Learn deployment with Gunicorn and nginx

---

**Built for learning. Designed for exploration. Ready for enhancement.**
