# GitHub Copilot Advanced Workshop: SDLC Integration

A hands-on training repository designed to help developers learn how to effectively integrate **GitHub Copilot** throughout the entire **Software Development Lifecycle (SDLC)**.

## 🎯 Workshop Overview

This workshop provides practical, lab-based exercises that demonstrate how GitHub Copilot can accelerate development across all phases of the SDLC—from requirements and design through implementation, testing, and deployment.

### Learning Objectives

By completing this workshop, participants will learn to:

- Leverage GitHub Copilot for code generation and completion
- Use Copilot to write tests, documentation, and commit messages
- Apply Copilot effectively during code reviews and refactoring
- Integrate Copilot into debugging and troubleshooting workflows
- Understand best practices for prompt engineering with Copilot

## 🛠️ The Learning Application: ApproveThis

The workshop centers around building out **ApproveThis**—a job/workflow/process scheduling and approval tool built with **Python** and **Flask**.

### Application Overview

ApproveThis is designed as an internal workflow dispatch and approval system for managing GitHub Actions workflows, as well as other CI/CD systems and deployment environments (Azure, Terraform, etc.). Throughout the labs, participants will progressively build out the application's functionality using GitHub Copilot.

**Key Technologies:**
- **Python 3.8+** - Core programming language
- **Flask** - Web application framework
- **SQLAlchemy** - Database ORM
- **Flask-Login** - Authentication
- **Jinja2** - Templating engine

**Application Features (to be built):**
- User authentication and role-based access control (RBAC)
- Repository browsing and management
- Workflow listing and execution
- Workflow run tracking and monitoring
- Approval workflows for workflow dispatches
- RESTful API endpoints

### Architecture Highlights

The application follows modern Flask best practices:
- **Application Factory Pattern** for flexible configuration
- **Blueprint-based Organization** for modular code structure
- **Provider Pattern** for API abstraction (mock/real GitHub integration)
- **Role-Based Access Control** with granular permissions

## 📁 Repository Structure

```
├── approvethis/          # Main Flask application
│   ├── app/              # Application package
│   │   ├── blueprints/   # Route modules (auth, main, api)
│   │   ├── models/       # Database models
│   │   ├── providers/    # GitHub API abstraction
│   │   ├── templates/    # Jinja2 HTML templates
│   │   └── static/       # CSS and JavaScript
│   ├── migrations/       # Database migrations
│   └── requirements.txt  # Python dependencies
├── docs/                 # Documentation and references
│   └── agents/           # Copilot agent configurations
└── labs/                 # Workshop lab exercises (coming soon)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- GitHub Copilot access (individual or business)
- VS Code with GitHub Copilot extension (recommended)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Coveros/copilot-advanced-workshop-sdlc.git
   cd copilot-advanced-workshop-sdlc
   ```

2. **Navigate to the application directory:**
   ```bash
   cd approvethis
   ```

3. **Follow the setup instructions:**
   See [approvethis/QUICKSTART.md](approvethis/QUICKSTART.md) for detailed setup instructions.

## 📚 Labs

*Labs are currently under development and will be added soon.*

The labs will guide participants through building out ApproveThis functionality while learning to leverage GitHub Copilot at each stage of development.

## 📖 Additional Resources

- [ApproveThis Application README](approvethis/README.md) - Detailed application documentation
- [Glossary](docs/Glossary.md) - Key terms and definitions
- [Agent Configurations](docs/agents/README.md) - Copilot agent setup guides

## 📄 License

See [LICENSE](LICENSE) for details.