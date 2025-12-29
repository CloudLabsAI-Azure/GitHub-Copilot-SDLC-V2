# Terraform MCP Guide

This guide provides detailed instructions for setting up and using the Terraform Model Context Protocol (MCP) server to integrate Terraform infrastructure management with GitHub Copilot.

## 📖 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Available Operations](#available-operations)
- [Common Use Cases](#common-use-cases)
- [Integration with ApproveThis](#integration-with-approvethis)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## Overview

The **Terraform MCP server** enables GitHub Copilot to:
- Understand Terraform state and configuration
- Query infrastructure resources and their attributes
- Validate Terraform configuration syntax
- Plan infrastructure changes
- Explain module dependencies and outputs
- Generate Terraform documentation

This integration brings infrastructure context into your development workflow, enabling AI-assisted infrastructure as code (IaC) development.

---

## Prerequisites

Before setting up Terraform MCP, ensure you have:

1. **Terraform Installed**
   - Terraform CLI version 1.0 or higher
   - Verify with: `terraform version`

2. **Node.js and npm**
   - Node.js v18 or higher
   - npm (comes with Node.js)

3. **VS Code with Copilot**
   - VS Code with GitHub Copilot extension
   - GitHub Copilot Chat extension

4. **Terraform Configuration**
   - At least one Terraform project/workspace
   - Terraform initialized (`terraform init` already run)

---

## Installation

### Step 1: Install the Terraform MCP Server

```bash
npm install -g @modelcontextprotocol/server-terraform
```

### Step 2: Verify Installation

```bash
npm list -g @modelcontextprotocol/server-terraform
```

### Step 3: Locate Installation Path

```bash
# Get npm global modules path
npm root -g

# macOS/Linux typically: /usr/local/lib/node_modules
# Windows typically: C:\Users\YourUsername\AppData\Roaming\npm\node_modules
```

---

## Configuration

### VS Code Settings Configuration

1. Open VS Code Settings (`Ctrl+,` / `Cmd+,`)
2. Search for "MCP"
3. Click "Edit in settings.json"
4. Add the Terraform MCP configuration:

**Windows Configuration:**
```json
{
  "github.copilot.chat.mcp.servers": {
    "terraform": {
      "command": "node",
      "args": [
        "C:\\Users\\YourUsername\\AppData\\Roaming\\npm\\node_modules\\@modelcontextprotocol\\server-terraform\\dist\\index.js"
      ],
      "env": {
        "TF_WORKSPACE_DIR": "C:\\Users\\YourUsername\\Projects\\myapp\\terraform"
      }
    }
  }
}
```

**macOS/Linux Configuration:**
```json
{
  "github.copilot.chat.mcp.servers": {
    "terraform": {
      "command": "node",
      "args": [
        "/usr/local/lib/node_modules/@modelcontextprotocol/server-terraform/dist/index.js"
      ],
      "env": {
        "TF_WORKSPACE_DIR": "/home/username/projects/myapp/terraform"
      }
    }
  }
}
```

### For ApproveThis Workshop

```json
{
  "github.copilot.chat.mcp.servers": {
    "terraform": {
      "command": "node",
      "args": [
        "/usr/local/lib/node_modules/@modelcontextprotocol/server-terraform/dist/index.js"
      ],
      "env": {
        "TF_WORKSPACE_DIR": "/absolute/path/to/copilot-advanced-workshop-sdlc/approvethis/terraform"
      }
    }
  }
}
```

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `TF_WORKSPACE_DIR` | Yes | Absolute path to Terraform configuration directory | `/home/user/project/terraform` |
| `TF_VAR_*` | No | Terraform variables (same as `TF_VAR_` prefix in CLI) | `TF_VAR_environment=dev` |

> [!IMPORTANT]
> Use **absolute paths** for `TF_WORKSPACE_DIR`. Relative paths may not resolve correctly.

### Restart VS Code

After configuration, restart VS Code to activate the MCP server.

### Verify Connection

Test the connection in Copilot Chat:

```
@terraform What modules exist in this Terraform configuration?
```

---

## Available Operations

The Terraform MCP server supports the following operations:

### Configuration Queries

**List Modules**:
```
@terraform What Terraform modules are in this configuration?
@terraform Show me the module structure
```

**Explain Modules**:
```
@terraform Explain what the app-service module does
@terraform What resources does the azure-function module create?
```

**View Variables**:
```
@terraform What variables does the app-service module require?
@terraform Show me all variables with their default values
```

**View Outputs**:
```
@terraform What outputs does the app-service module provide?
@terraform Show me the output values from the last apply
```

### State Queries

**Query Resources**:
```
@terraform What resources are currently in the Terraform state?
@terraform Show me all Azure App Services in the state
@terraform What's the current state of resource 'azurerm_app_service.main'?
```

**Resource Attributes**:
```
@terraform What's the hostname of the app service?
@terraform Show me the resource ID of the storage account
```

**Drift Detection**:
```
@terraform Are there any resources in state that differ from configuration?
```

### Validation and Planning

**Validate Configuration**:
```
@terraform Validate the Terraform configuration
@terraform Check for syntax errors in the terraform files
```

**Plan Changes**:
```
@terraform What changes would be made if I run terraform apply?
@terraform Show me the plan for the dev environment
```

**Explain Plan**:
```
@terraform Why is Terraform planning to replace the app service?
@terraform Explain the changes in this plan output
```

### Documentation Generation

**Generate Docs**:
```
@terraform Generate documentation for the app-service module
@terraform Create a README for the terraform/modules directory
```

---

## Common Use Cases

### Understanding Existing Infrastructure

**Scenario**: You're new to the project and need to understand the Terraform setup.

```
@workspace @terraform Explain the Terraform module structure in approvethis/terraform/. What does each module create and how do they relate?
```

### Adding New Resources

**Scenario**: You need to add Application Insights to the app-service module.

```
@workspace @terraform I want to add Application Insights to the app-service module. Show me:
1. What resources to add
2. What variables to expose
3. What outputs to provide
4. How to connect it to the existing app service
```

### Troubleshooting Plans

**Scenario**: Terraform plan shows unexpected changes.

```
@terraform I ran terraform plan and it wants to destroy and recreate the app service. Why? Here's the relevant plan output: [paste output]
```

### Environment Comparison

**Scenario**: Ensure dev and production environments are configured correctly.

```
@workspace @terraform Compare the dev and production environment configurations in terraform/environments/. What are the key differences?
```

### Module Development

**Scenario**: Create a new Terraform module.

```
@workspace @terraform Create a new module for Azure SQL Database in terraform/modules/sql-database with:
- Firewall rules
- Backup configuration
- Failover group support
- Standard variables and outputs
Follow the pattern used in existing modules.
```

### Security Review

**Scenario**: Ensure Terraform follows security best practices.

```
@terraform Review the app-service module for security best practices:
- HTTPS enforcement
- TLS version
- Managed identity
- Network restrictions
- Diagnostic logging
```

---

## Integration with ApproveThis

The ApproveThis application includes a job execution framework that can trigger Terraform operations.

### Job Definitions for Terraform

ApproveThis can define jobs for Terraform operations:

**Terraform Plan - Dev**:
```
@workspace How would I configure a JobDefinition in ApproveThis to trigger 'terraform plan' for the dev environment via GitHub Actions?
```

**Terraform Apply - Production**:
```
@workspace Create a JobDefinition for terraform apply to production that requires approval before execution. Use the approval workflow from Lab 8.
```

### Monitoring Terraform Execution

**Query Job Status**:
```
@workspace @terraform How can I display terraform plan output in the ApproveThis UI after a job executes?
```

### Terraform via GitHub Actions

ApproveThis triggers Terraform through GitHub Actions workflows:

```
@workspace @terraform Explain how the GitHub Actions workflow .github/workflows/terraform-deploy.yml executes terraform. What secrets does it use?
```

---

## Troubleshooting

### "Terraform not initialized" Error

**Error**: "Backend initialization required"

**Solutions**:
```bash
cd /path/to/terraform/directory
terraform init
```

Ensure `terraform init` has been run in the `TF_WORKSPACE_DIR` before using the MCP server.

### State Lock Errors

**Error**: "Error acquiring state lock"

**Solutions**:
1. **Wait for concurrent operation**: Another process may be running
2. **Force unlock** (use cautiously):
   ```bash
   terraform force-unlock <lock-id>
   ```
3. **Check backend**: Verify state backend is accessible

### Invalid Path Configuration

**Error**: MCP server can't find Terraform files

**Solutions**:
1. **Use absolute paths**: Ensure `TF_WORKSPACE_DIR` is absolute
2. **Verify path exists**:
   ```bash
   ls -la /path/specified/in/TF_WORKSPACE_DIR
   ```
3. **Check permissions**: Ensure read access to Terraform files

### Module Not Found

**Error**: "Module not installed"

**Solutions**:
```bash
cd /path/to/terraform/directory
terraform init
```

This downloads external modules referenced in configuration.

### Performance Issues

**Issue**: Slow responses from Terraform MCP

**Solutions**:
1. **Reduce state size**: Large state files slow queries
2. **Use workspaces**: Separate environments into different workspaces
3. **Optimize queries**: Ask specific questions rather than broad queries

---

## Best Practices

### Workspace Organization

**Structure your Terraform**:
```
terraform/
├── modules/              # Reusable modules
│   ├── app-service/
│   ├── azure-function/
│   └── storage-account/
└── environments/         # Environment-specific configs
    ├── dev/
    │   ├── main.tf
    │   ├── variables.tf
    │   └── backend.tf
    └── production/
        ├── main.tf
        ├── variables.tf
        └── backend.tf
```

Point `TF_WORKSPACE_DIR` to the environment directory you're working with.

### Query Specificity

**❌ Avoid broad queries**:
```
@terraform Tell me everything about this Terraform configuration
```

**✅ Prefer specific queries**:
```
@terraform What variables does the app-service module require and what are their default values?
```

### Validation Before Changes

**Always validate before planning**:
```
@terraform Validate the configuration
# Review results
@terraform Show me the plan
```

### Documentation

**Keep docs in sync**:
```
@terraform Generate updated documentation for all modules in terraform/modules/
```

Run this after significant module changes.

### Security

**Sensitive Values**:
- Never put sensitive values in Terraform files
- Use variables with sensitive = true
- Store secrets in Azure Key Vault or similar
- Use MCP to verify no sensitive data in outputs

```
@terraform Check all module outputs. Are any marked as sensitive? Should any be?
```

---

## Example Workflow

### 1. Understand Current State

```
@terraform What resources exist in the current state?
@terraform What's the current environment configuration?
```

### 2. Plan Changes

```
@workspace I need to add a new output to the app-service module for the staging slot URL. Show me what changes are needed.
```

### 3. Implement Changes

Let Copilot help implement:
```
@workspace Update terraform/modules/app-service/outputs.tf to add an output for the staging slot default hostname
```

### 4. Validate

```
@terraform Validate the updated configuration
```

### 5. Plan and Review

```
@terraform Run a plan. What changes will be made?
```

### 6. Apply (via ApproveThis or CLI)

Either trigger via ApproveThis job execution or:
```bash
terraform apply
```

---

## Related Guides

- [MCP Configuration Guide](MCP-Configuration-Guide.md) - General MCP setup
- [Glossary](Glossary.md) - Terraform and IaC terminology

---

**[← Back to Documentation Index](README.md)**
