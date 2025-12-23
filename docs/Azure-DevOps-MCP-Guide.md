# Azure DevOps MCP Guide

This guide provides detailed instructions for setting up and using the Azure DevOps Model Context Protocol (MCP) server to integrate Azure Boards with GitHub Copilot.

## 📖 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Authentication Setup](#authentication-setup)
- [Configuration](#configuration)
- [Available Operations](#available-operations)
- [Common Use Cases](#common-use-cases)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## Overview

The **Azure DevOps MCP server** enables GitHub Copilot to:
- Query work items from Azure Boards
- Create and update work items
- Search across iterations and sprints
- Link code changes to work items
- Query repository and pipeline information

This integration brings your project management context directly into your coding environment, enabling AI-assisted planning and development with full organizational context.

---

## Prerequisites

Before setting up Azure DevOps MCP, ensure you have:

1. **Azure DevOps Organization Access**
   - A valid Azure DevOps organization
   - Permissions to create Personal Access Tokens (PATs)

2. **Node.js and npm**
   - Node.js v18 or higher
   - npm (comes with Node.js)

3. **VS Code with Copilot**
   - VS Code with GitHub Copilot extension
   - GitHub Copilot Chat extension

4. **Azure DevOps Project**
   - At least one project in your organization
   - Work items to query (or permission to create them)

---

## Installation

### Step 1: Install the Azure DevOps MCP Server

```bash
npm install -g @modelcontextprotocol/server-azure-devops
```

### Step 2: Verify Installation

```bash
npm list -g @modelcontextprotocol/server-azure-devops
```

Expected output:
```
C:\Users\YourUsername\AppData\Roaming\npm
└── @modelcontextprotocol/server-azure-devops@x.x.x
```

### Step 3: Locate Installation Path

```bash
# Windows
where node
# Then look in %APPDATA%\npm\node_modules

# macOS/Linux
which node
npm root -g
```

---

## Authentication Setup

Azure DevOps MCP uses **Personal Access Tokens (PAT)** for authentication.

### Creating a Personal Access Token

1. Navigate to your Azure DevOps organization: `https://dev.azure.com/YourOrganization`

2. Click on your **profile icon** (top right) → **Personal access tokens**

3. Click **+ New Token**

4. Configure your token:
   - **Name**: `Copilot MCP Integration` (or any descriptive name)
   - **Organization**: Select your organization
   - **Expiration**: Choose an appropriate timeframe
     - For training: 30 days
     - For production: Consider your organization's policies
   - **Scopes**: Select **Custom defined**

5. **Required Scopes** (minimum):
   - ✅ **Work Items**: Read & Write
   - ✅ **Project and Team**: Read (optional, for project queries)
   - ✅ **Code**: Read (optional, for repository integration)

6. Click **Create**

7. **Copy the token immediately** - you cannot retrieve it later!

> [!IMPORTANT]
> Store your PAT securely! Consider using a password manager. Never commit PATs to version control.

### Token Security Best Practices

- **Minimal Scope**: Only grant permissions you actually need
- **Expiration**: Use the shortest reasonable expiration time
- **Rotation**: Create a calendar reminder to rotate tokens before expiry
- **Revocation**: If compromised, revoke immediately in Azure DevOps

---

## Configuration

### VS Code Settings Configuration

1. Open VS Code Settings (`Ctrl+,` / `Cmd+,`)
2. Search for "MCP"
3. Click "Edit in settings.json"
4. Add the Azure DevOps MCP configuration:

**Windows Configuration:**
```json
{
  "github.copilot.chat.mcp.servers": {
    "azure-devops": {
      "command": "node",
      "args": [
        "C:\\Users\\YourUsername\\AppData\\Roaming\\npm\\node_modules\\@modelcontextprotocol\\server-azure-devops\\dist\\index.js"
      ],
      "env": {
        "AZURE_DEVOPS_ORG_URL": "https://dev.azure.com/YourOrganization",
        "AZURE_DEVOPS_PAT": "your-personal-access-token-here",
        "AZURE_DEVOPS_PROJECT": "YourProjectName"
      }
    }
  }
}
```

**macOS/Linux Configuration:**
```json
{
  "github.copilot.chat.mcp.servers": {
    "azure-devops": {
      "command": "node",
      "args": [
        "/usr/local/lib/node_modules/@modelcontextprotocol/server-azure-devops/dist/index.js"
      ],
      "env": {
        "AZURE_DEVOPS_ORG_URL": "https://dev.azure.com/YourOrganization",
        "AZURE_DEVOPS_PAT": "your-personal-access-token-here",
        "AZURE_DEVOPS_PROJECT": "YourProjectName"
      }
    }
  }
}
```

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `AZURE_DEVOPS_ORG_URL` | Yes | Full URL to your Azure DevOps organization | `https://dev.azure.com/MyCompany` |
| `AZURE_DEVOPS_PAT` | Yes | Personal Access Token | `abcdef1234567890...` |
| `AZURE_DEVOPS_PROJECT` | No | Default project name (can be overridden in queries) | `ApproveThis` |

### Restart VS Code

After configuration, restart VS Code to activate the MCP server.

### Verify Connection

Test the connection in Copilot Chat:

```
@azure-devops List the work items in the current iteration
```

If configured correctly, Copilot will query Azure DevOps and return work items!

---

## Available Operations

The Azure DevOps MCP server supports the following operations:

### Work Item Queries

**List Work Items**:
```
@azure-devops List all active work items
@azure-devops Show work items assigned to me
@azure-devops Find work items in the current iteration
```

**Search Work Items**:
```
@azure-devops Search for work items with title containing "GitHub provider"
@azure-devops Find bugs with high priority
@azure-devops Show user stories for the next sprint
```

**Get Work Item Details**:
```
@azure-devops Show details for work item #123
@azure-devops What is the status of work item #456?
```

### Create Work Items

**Create User Story**:
```
@azure-devops Create a user story titled "Implement real GitHub provider" with description "Replace mock provider with real GitHub API integration"
```

**Create Bug**:
```
@azure-devops Create a bug: "Login fails for users with special characters in username"
```

**Create Task**:
```
@azure-devops Create a task "Write unit tests for Role model" assigned to me
```

### Update Work Items

**Update Status**:
```
@azure-devops Update work item #123 to status "Active"
@azure-devops Move work item #456 to "Closed"
```

**Assign Work Items**:
```
@azure-devops Assign work item #789 to john.doe@company.com
```

**Add Comments**:
```
@azure-devops Add comment to work item #123: "Implementation complete, ready for review"
```

### Iteration and Sprint Queries

**Current Iteration**:
```
@azure-devops What work items are in the current iteration?
@azure-devops Show the current sprint backlog
```

**Specific Iteration**:
```
@azure-devops List work items in iteration "Sprint 5"
```

### Project and Team Information

**List Projects**:
```
@azure-devops What projects exist in this organization?
```

**Team Members**:
```
@azure-devops Who are the members of the ApproveThis team?
```

---

## Common Use Cases

### Planning a Feature

**Scenario**: Use Copilot to create a set of user stories for a new feature.

```
@workspace @azure-devops Based on the NotImplementedError in app/providers/github.py, create user stories for implementing each method. Each story should have:
- Clear title
- Description with acceptance criteria
- Assigned to the current iteration
```

### Linking Code to Work Items

**Scenario**: Generate commit messages that link to work items.

```
@azure-devops Generate a commit message for implementing the list_repositories() method that links to work item #123
```

**Output**:
```
Implement list_repositories() in GitHub provider

- Connects to GitHub API using PyGithub library
- Includes rate limiting and error handling
- Authenticates using GITHUB_TOKEN from environment

Resolves AB#123
```

The `AB#123` syntax automatically links the commit to Azure Boards work item #123.

### Sprint Planning

**Scenario**: Organize work items for an upcoming sprint.

```
@azure-devops Help me plan Sprint 6. Show all unassigned user stories, sort by priority, and suggest which ones should be in the sprint based on their story points.
```

### Status Updates

**Scenario**: Get a quick status update on your assigned work.

```
@azure-devops What work items are assigned to me? Group by status and show remaining work hours.
```

### Cross-Reference with Code

**Scenario**: Find work items related to a specific file.

```
@workspace @azure-devops Are there any work items related to app/providers/github.py? Show their current status.
```

---

## Troubleshooting

### "MCP server error" or No Response

**Possible Causes**:
1. Server not installed correctly
2. Path in configuration is incorrect
3. VS Code not restarted after configuration

**Solutions**:
```bash
# Verify installation
npm list -g @modelcontextprotocol/server-azure-devops

# Check the path in settings.json matches the installation location
npm root -g

# Restart VS Code completely (close all windows)
```

### Authentication Failures

**Error**: "401 Unauthorized" or "403 Forbidden"

**Solutions**:
1. **Verify PAT is valid**: Try using it in Azure DevOps web UI or REST API
2. **Check PAT scopes**: Ensure Work Items (Read & Write) is enabled
3. **Verify organization URL**: Must be exact (e.g., `https://dev.azure.com/MyOrg`)
4. **Check PAT expiration**: Create a new PAT if expired

### Work Items Not Found

**Error**: "No work items found" or empty results

**Solutions**:
1. **Verify project name**: Ensure `AZURE_DEVOPS_PROJECT` is correct
2. **Check permissions**: Verify you have access to the project in Azure DevOps
3. **Refine query**: Be more specific in your search criteria

### Slow Performance

**Issue**: Queries take a long time to complete

**Solutions**:
1. **Reduce scope**: Query specific iterations instead of all work items
2. **Use filters**: Filter by state, assigned user, or work item type
3. **Check network**: Azure DevOps API calls depend on network latency

---

## Best Practices

### Query Efficiency

**❌ Avoid**:
```
@azure-devops List all work items in the organization
```

**✅ Prefer**:
```
@azure-devops List active work items in the current iteration for project ApproveThis
```

### Work Item Creation

**Include sufficient detail**:
```
@azure-devops Create a user story:
Title: "Implement approval workflow API endpoints"
Description: "Create REST API endpoints for approval operations including create request, approve, reject, and list pending"
Acceptance Criteria:
- POST /api/approvals/requests creates pending request
- GET /api/approvals/pending lists all pending (admin only)
- POST /api/approvals/<id>/approve approves request
- Proper RBAC checks on all endpoints
```

### Linking Work Items

Always use the `AB#<id>` syntax in commit messages:
```
feat: implement GitHub provider

Connects to real GitHub API for repository and workflow data.

Resolves AB#123
Related to AB#124, AB#125
```

### Security

- **Never commit PATs** to version control
- **Use workspace-specific settings** if PATs differ across projects
- **Rotate tokens regularly**
- **Use least-privilege**: Only grant required scopes

---

## Related Guides

- [MCP Configuration Guide](MCP-Configuration-Guide.md) - General MCP setup
- [Glossary](Glossary.md) - MCP and Azure DevOps terminology

---

**[← Back to Documentation Index](README.md)**
