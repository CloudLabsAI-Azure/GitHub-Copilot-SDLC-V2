# Copilot Advanced Workshop SDLC - Copilot Instructions

This repository serves as a training tool for learning how to use GitHub Copilot effectively throughout the software development lifecycle (SDLC). The repository is split into 3 main sections:

1. **Hands-on Labs**: Practical exercises to learn how to use Copilot for various development tasks. These are in the `labs/` directory.
2. **Best Practices**: Guidelines and tips for maximizing the benefits of Copilot in your workflow. These are in the `docs` directory.
3. **Learning Application**: A sample Flask application called ApproveThis that demonstrates how to apply Copilot in a real-world project. The code is in the `approvethis/` directory.

# Hands-on Labs

The `labs/` directory contains step-by-step exercises for using Copilot in different scenarios, such as:

- Gaining familiarity with a new codebase quickly and efficiently
- Refactoring existing code
- Writing tests
- Generating documentation
- Integrating with CI/CD pipelines

Each lab is built around a running real-world scenario to give the most practical experience possible. All of the materials required to complete the labs are included in the repository, and instructions along with step-by-step guidance are provided in the lab markdown files.


# ApproveThis Application

## Project Overview

ApproveThis is a Flask-based workflow dispatch and approval system for managing GitHub Actions workflows. It's a training application demonstrating modern Flask patterns (Application Factory, Provider Pattern, RBAC).

## Architecture

### Application Structure
```
approvethis/app/
├── __init__.py          # Application factory (create_app)
├── extensions.py        # Flask extensions (db, login_manager, migrate)
├── blueprints/          # Route modules (auth, main, api, jobs)
├── models/              # SQLAlchemy models with RBAC (User, Role, Permission)
├── providers/           # GitHub API abstraction layer (mock/real implementations)
│   └── execution/       # Job execution providers (GitHub Actions, Azure Functions)
├── templates/           # Jinja2 templates organized by blueprint
└── utils/               # Auth decorators (permission_required, admin_required)
```

### Key Patterns

**Provider Pattern** - Abstract API calls via `app/providers/base.py`. Use `get_provider()` factory:
```python
from app.providers import get_provider
provider = get_provider()  # Returns MockGitHubProvider or RealGitHubProvider
repos = provider.list_repositories()
```

**RBAC with Permission Bit Flags** - See `app/models/role.py`:
```python
from app.models import Permission
from app.utils import permission_required

@permission_required(Permission.DISPATCH_WORKFLOW)
def my_route():
    ...
```
Permissions: `VIEW_REPOS=1`, `VIEW_WORKFLOWS=2`, `VIEW_RUNS=4`, `DISPATCH_WORKFLOW=8`, `MANAGE_APPROVALS=16`, `MANAGE_USERS=32`, `ADMIN=64`

**Execution Providers** - `app/providers/execution/base.py` defines interface for job execution backends (GitHub Actions, Azure Functions).

## Development Workflow

### Setup & Run
```bash
cd approvethis
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
flask seed all  # Seeds roles, users, targets, jobs
flask run       # Runs on http://127.0.0.1:5001
```

### Test Users
| Username | Password | Role | Can Dispatch? |
|----------|----------|------|---------------|
| viewer | viewer123 | Viewer | No |
| developer | developer123 | LeadDeveloper | Yes |
| admin | admin123 | GlobalAdmin | Yes + Full Admin |

### Database Migrations
```bash
flask db migrate -m "Description"
flask db upgrade
```

## Code Conventions

### Adding New Routes
1. Create blueprint in `app/blueprints/<name>/` with `__init__.py` and `routes.py`
2. Register in `app/__init__.py` → `register_blueprints()`
3. Use `@login_required` and `@permission_required()` decorators
4. Templates go in `app/templates/<blueprint_name>/`

### Adding New Models
1. Create in `app/models/<name>.py` extending `db.Model`
2. Export from `app/models/__init__.py`
3. Add seed method if needed (see `Role.insert_roles()`, `User.insert_default_users()`)
4. Register in CLI `app/cli/seed.py` if seedable

### Provider Implementation
When adding real API integrations, implement the abstract methods from:
- `SourceControlProvider` in `app/providers/base.py` for source control
- `ExecutionProvider` in `app/providers/execution/base.py` for job execution

### Configuration
Config classes in `config.py`: `DevelopmentConfig`, `TestingConfig`, `ProductionConfig`
- `GITHUB_PROVIDER`: Set to `'mock'` or `'github'`
- Mock data lives in `app/mock_data/*.json`

## Testing Strategy
- **pytest** with **pytest-flask** for unit/integration tests
- **playwright** for E2E testing
- Test directory structure: `tests/unit/`, `tests/integration/`, `tests/e2e/`

## Azure Functions Integration
The `azure-functions/` directory contains serverless functions for GitHub Actions ↔ ApproveThis communication:
- `request-approval` - Receives approval requests from GitHub Actions
- `approval-response` - Sends approval decisions back to GitHub
- `trigger-workflow` - Triggers workflow_dispatch after approval

## Common Tasks

**Add a new job definition**: Modify `JobDefinition.seed_jobs()` in `app/models/job_definition.py`

**Add execution target type**: Add constant to `ExecutionTargetType` in `app/models/execution_target.py`, create provider in `app/providers/execution/`

**Protect a route by permission**: Use `@permission_required(Permission.FLAG_NAME)` decorator

**Access current user**: `from flask_login import current_user` - has `can(permission)` method
