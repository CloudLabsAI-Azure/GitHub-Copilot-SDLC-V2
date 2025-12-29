# GitHub Copilot Glossary

This glossary provides definitions for key terms, features, and concepts used throughout the GitHub Copilot Advanced Workshop.

## Core Concepts

### GitHub Copilot
An AI-powered code completion and assistance tool that helps developers write code faster by providing intelligent suggestions, explanations, and code generation capabilities.

### GitHub Copilot Chat
A conversational AI interface within VS Code that allows developers to ask questions, get explanations, and request code generation through natural language conversation.

### Context
The information GitHub Copilot uses to generate relevant suggestions. This includes:
- Currently open files
- Selected code
- Recent edits
- Project structure
- Repository instructions

## Chat Modes

### Ask Mode
A read-only mode for understanding code without making changes. Ideal for:
- Getting explanations of code
- Understanding project structure
- Learning about technologies and patterns

### Edit Mode
A targeted mode for making specific changes to files you explicitly identify. Features:
- Precise control over which files are modified
- Shows diff of proposed changes
- Best for focused refactoring and bug fixes

### Plan Mode
A preview mode that shows what changes Copilot would make without executing them. Used to:
- Validate approach before committing
- Understand impact of changes
- Review reasoning behind decisions

### Agent Mode
An autonomous mode that explores the codebase and makes decisions about what to change. Capabilities:
- Multi-file modifications
- Architectural decisions
- Complex problem-solving

## Customization Features

### Personal Instructions
User-level settings that apply across all repositories. Configure at:
- https://github.com/copilot

### Repository Instructions
Project-specific guidelines stored in `.github/copilot-instructions.md`. Used to:
- Define coding standards
- Specify project architecture
- Set framework-specific patterns

### Organization Instructions
Company-wide standards set by organization administrators.

### Instruction Hierarchy
Priority order for instruction application:
1. Personal Instructions (highest)
2. Repository Instructions
3. Organization Instructions (lowest)

## Prompt Files

### Prompt File
A reusable template for AI interactions stored in `.github/prompts/`. Contains:
- YAML header with metadata
- Markdown body with template

### Variables in Prompt Files
- `${workspaceFolder}` - Current workspace path
- `${file}` - Current file path
- `${selection}` - Selected text
- `${input:name:placeholder}` - User input field

## Custom Agents

### Custom Agent
A specialized AI assistant configured with specific expertise. Defined in `.github/agents/` with:
- Name and description
- Instructions for behavior
- Tool access permissions

### Agent Tools
Capabilities available to custom agents:
- `read` - Read file contents
- `search` - Search codebase
- `edit` - Modify files

## Model Context Protocol (MCP)

### MCP
Model Context Protocol - a standard for connecting AI assistants to external data sources and tools. Enables Copilot to access external systems like Azure DevOps, Terraform, and cloud providers.

### MCP Server
A service that provides data or functionality to Copilot through the MCP interface. Examples:
- GitHub MCP Server
- Slack MCP Server
- Jira MCP Server
- Azure DevOps MCP Server
- Terraform MCP Server
- Azure MCP Server

### Azure DevOps MCP
An MCP server that connects Copilot to Azure Boards for work item management, sprint planning, and project tracking.

### Terraform MCP
An MCP server that enables Copilot to understand Terraform state, validate configurations, and explain infrastructure code.

### Toolsets
Categories of functionality provided by MCP servers:
- `issues` - GitHub issue management
- `pull_requests` - PR workflows
- `repositories` - Repository information
- `code_search` - Search across repos
- `work_items` - Azure DevOps work items
- `terraform_state` - Terraform infrastructure state

## Copilot Spaces

### Copilot Space
A dedicated, persistent AI workspace with:
- Custom instructions
- Curated context files
- Focused conversations

### Space Context
The files, issues, and documentation added to a Space to guide AI responses.

## Coding Agent

### Coding Agent
An autonomous AI developer that works on GitHub issues independently. Features:
- Assigns to issues like a team member
- Creates branches and pull requests
- Works asynchronously

### Session Logs
Records of Coding Agent's decision-making process, including:
- Files analyzed
- Implementation approach
- Tests run

### Copilot Branch
Branches created by Coding Agent, prefixed with `copilot/`.

## AI Models

### Premium Request
API calls to advanced AI models that count against usage limits.

### Unlimited Models
AI models with no request limits (0x multiplier).

### Auto Model
Automatic model selection that chooses the best model for each task with 10% discount.

## Development Concepts

### Scaffolding
Pre-built project structure with working examples and extension points.

### Extension Points
Marked locations in code (TODO comments) where learners add functionality.

### Mock Data
Simulated data used during development before connecting to real databases.

## VS Code Features

### Ghost Text
Faded code suggestions that appear inline while typing.

### Chat Participants
Specialized Copilot features accessed with `@` prefix:
- `@workspace` - Full project context
- `@terminal` - Terminal operations
- `@vscode` - Editor features

### Slash Commands
Quick actions accessed with `/` prefix:
- `/explain` - Get code explanation
- `/fix` - Suggest bug fixes
- `/tests` - Generate tests
- `/doc` - Generate documentation

## Workflow Terms

### RAG (Retrieval Augmented Generation)
Technique where AI searches codebase for relevant context before generating code.

### Iteration
Refining AI-generated code through follow-up prompts.

### Context Window
The amount of information an AI model can process at once.

## Best Practices Terms

### Single Responsibility
Principle that each agent/prompt should focus on one specific domain.

### Idiomatic Code
Code that follows the conventions and patterns typical of a language or framework.

### Type Safety
Use of static types to catch errors at compile time (TypeScript, C#, etc.).

---

## ApproveThis Application Terms

### ApproveThis
The learning application for this workshop - a centralized job/workflow dispatch and approval system for managing CI/CD processes across multiple platforms.

### ShipIt Industries
The fictional company scenario for this workshop. Participants join ShipIt Industries to complete the ApproveThis application.

### Approval Workflow
The core feature of ApproveThis where workflow dispatches require approval from GlobalAdmin users before execution.

### Execution Provider
An abstraction layer in ApproveThis for connecting to different job execution platforms (GitHub Actions, Azure Functions, etc.).

### Job Definition
A template in ApproveThis that defines a job type (e.g., "Terraform Plan - Dev"). Specifies what to execute and where.

### Job Execution
A record of a specific job run in ApproveThis, including status, logs, and timestamps.

### Execution Target
Configuration in ApproveThis defining where jobs can execute (GitHub Actions workflow, Azure Function, etc.).

### Provider Pattern
Architectural pattern in ApproveThis using abstract base classes to support multiple implementations (mock vs. real GitHub API).

### DispatchRequest
Model in ApproveThis representing a workflow dispatch request, including approval status and audit trail.

## Testing Terms

### End-to-End (E2E) Testing
Testing complete user workflows from start to finish in a real browser environment using tools like Playwright.

### Playwright
A modern browser automation framework for E2E testing that supports multiple browsers and provides auto-waiting features.

### Test Fixture
Reusable test setup code (e.g., authenticated client, test database) defined in pytest conftest.py files.

### Page Object Model
A testing pattern that encapsulates page interactions in classes for maintainable E2E tests.

### Mock Provider
A test implementation of the provider pattern that returns fake data without making real API calls.

## Infrastructure Terms

### Infrastructure as Code (IaC)
Managing and provisioning infrastructure through code (e.g., Terraform) rather than manual processes.

### Terraform Module
A reusable, self-contained package of Terraform configurations that creates specific infrastructure resources.

### Terraform State
A file tracking the current state of managed infrastructure, used to plan and apply changes.

### Environment Configuration
Infrastructure definitions for specific environments (dev, staging, production) with different resource sizes and settings.

---

**Tip**: Use `Ctrl+F` / `Cmd+F` to quickly find specific terms in this glossary.
