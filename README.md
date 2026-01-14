# GitHub Copilot Advanced Workshop: Copilot throughout the SDLC

A hands-on training repository designed to help developers learn how to effectively integrate **GitHub Copilot** throughout the entire **Software Development Lifecycle (SDLC)**.

## 🎯 Workshop Overview

This workshop provides practical, lab-based exercises that demonstrate how GitHub Copilot can accelerate development across all phases of the SDLC—from requirements and design through implementation, testing, and deployment.

### Learning Objectives

By completing this workshop, participants will learn to:

- Leverage GitHub Copilot throughout the entire software development lifecycle
- Use Model Context Protocol (MCP) to connect Copilot with external systems
- Apply advanced Copilot modes (Edit, Agent, Plan) for different scenarios
- Generate comprehensive test suites with AI assistance
- Manage infrastructure as code with Copilot and MCP
- Deliver production-ready features with AI partnership

## 🏢 Workshop Scenario: ShipIt Industries

Throughout this workshop, you'll be working in a real-world scenario:

> **The Situation at ShipIt Industries**
>
> Due to rapid internal growth, ShipIt Industries has found it increasingly difficult to manage their various CI/CD processes. Deployments and jobs are scattered across multiple environments—GitHub Actions, Azure deployments, Azure Functions, and more—with no single place to view or control them.
>
> To solve this, management has greenlit the development of an internal application called **ApproveThis**. This tool will centralize job and deployment management into a single, unified interface. Key requirements include:
> - **Visibility**: View all jobs and deployments from one location
> - **Control**: Trigger and manage workflows across different platforms
> - **Approvals**: Require approvals before critical deployments execute
> - **RBAC**: Role-based access control for safe, seamless use across teams
>
> **Your Role**: The initial version of ApproveThis was built by another developer who has since left the company. Management has assigned you to take over the application and implement the remaining functionality. You'll use GitHub Copilot throughout the entire software development lifecycle to complete this mission.
>
> Let's help ShipIt Industries ship it—safely and with approval! 🚀

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

## 📚 Lab Exercises

All lab exercises are located in the [`labs/`](labs/) directory:

| Lab | Title | Duration | Description |
|-----|-------|----------|-------------|
| [Lab 1](labs/Lab-1-Setup-and-Configuration.md) | Setup and Configuration | 20 min | Set up environment and run ApproveThis |
| [Lab 2](labs/Lab-2-Your-Assignment.md) | Your Assignment | 20 min | Explore codebase and identify next steps |
| [Lab 3](labs/Lab-3-Planning-with-MCP.md) | Planning with MCP | 35 min | Use Azure DevOps MCP for planning |
| [Lab 4](labs/Lab-4-Development-Process.md) | Development Process | 60 min | Implement features with Copilot modes |
| [Lab 5](labs/Lab-5-Testing-with-Copilot.md) | Testing with Copilot | 30 min | E2E testing with Playwright |
| [Lab 6](labs/Lab-6-IaC-and-Deployments.md) | IaC and Deployments | 30 min | Terraform and Azure deployments |
| [Lab 7](labs/Lab-7-CI-CD-Beyond-GitHub-Actions.md) | CI/CD Beyond GitHub Actions | 45 min | Multi-platform CI/CD (in development) |
| [Lab 8](labs/Lab-8-Capstone-Approvals.md) | Capstone: Approvals | 60+ min | Implement approval workflows end-to-end |

**Total Duration**: Approximately 5-6 hours

## 🔐 Pre-Configured Repository

Your training repository comes pre-configured with:
- Azure credentials for Terraform deployments
- Required subscription and authentication secrets
- All dependencies and configurations needed for the labs

See [Lab 1: Setup and Configuration](labs/Lab-1-Setup-and-Configuration.md) for detailed setup instructions.

## 📁 Repository Structure

```
├── approvethis/          # Main Flask application
│   ├── app/              # Application package
│   │   ├── blueprints/   # Route modules (auth, main, api, jobs)
│   │   ├── models/       # Database models
│   │   ├── providers/    # GitHub API abstraction
│   │   ├── templates/    # Jinja2 HTML templates
│   │   └── static/       # CSS and JavaScript
│   ├── migrations/       # Database migrations
│   ├── terraform/        # Infrastructure as Code
│   ├── tests/            # Test suites (unit, integration, E2E)
│   └── requirements.txt  # Python dependencies
├── docs/                 # Documentation and reference guides
│   ├── MCP-Configuration-Guide.md
│   ├── Azure-DevOps-MCP-Guide.md
│   ├── Terraform-MCP-Guide.md
│   ├── Playwright-Testing-Guide.md
│   ├── Glossary.md
│   └── agents/           # Copilot agent configurations
├── labs/                 # Workshop lab exercises
│   ├── Lab-1-Setup-and-Configuration.md
│   ├── Lab-2-Your-Assignment.md
│   ├── Lab-3-Planning-with-MCP.md
│   ├── Lab-4-Development-Process.md
│   ├── Lab-5-Testing-with-Copilot.md
│   ├── Lab-6-IaC-and-Deployments.md
│   ├── Lab-7-CI-CD-Beyond-GitHub-Actions.md
│   └── Lab-8-Capstone-Approvals.md
└── README.md             # This file
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
   See [Lab 1: Setup and Configuration](labs/Lab-1-Setup-and-Configuration.md) for detailed setup instructions.

## 📖 Additional Resources

- [ApproveThis Application README](approvethis/README.md) - Detailed application documentation
- [Documentation Index](docs/README.md) - All reference guides and materials
- [Glossary](docs/Glossary.md) - Key terms and definitions
- [Agent Configurations](docs/agents/README.md) - Copilot agent setup guides

## 📄 License

See [LICENSE](LICENSE) for details.