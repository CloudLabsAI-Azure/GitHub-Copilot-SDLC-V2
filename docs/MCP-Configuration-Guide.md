# Model Context Protocol (MCP) Configuration Guide

This guide provides comprehensive instructions for setting up and configuring Model Context Protocol (MCP) servers to extend GitHub Copilot's capabilities with external data sources and tools.

## 📖 Table of Contents

- [What is MCP?](#what-is-mcp)
- [Why Use MCP with Copilot?](#why-use-mcp-with-copilot)
- [MCP Architecture](#mcp-architecture)
- [General Setup Process](#general-setup-process)
- [Configuring MCP Servers](#configuring-mcp-servers)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)
- [Best Practices](#best-practices)

---

## What is MCP?

**Model Context Protocol (MCP)** is an open standard that enables AI assistants like GitHub Copilot to connect to external data sources and tools. It provides a standardized way for AI models to:

- Access data from external systems (databases, APIs, file systems)
- Execute operations in external tools (deployment systems, infrastructure tools)
- Retrieve context that isn't available in the codebase alone

Think of MCP as a universal adapter that lets your AI assistant "plug into" the rest of your development ecosystem.

### Key Concepts

- **MCP Server**: A service that provides specific functionality (e.g., Azure DevOps integration, Terraform operations)
- **MCP Client**: The AI assistant (GitHub Copilot) that consumes data from MCP servers
- **Tools**: Specific operations an MCP server can perform (e.g., "query work items", "list resources")
- **Resources**: Data that an MCP server can provide (e.g., work item details, infrastructure state)
- **Prompts**: Reusable prompt templates provided by MCP servers

---

## Why Use MCP with Copilot?

### Without MCP
- Copilot only knows about your code
- Manual context switching between tools
- Limited awareness of project state
- No access to organizational systems

### With MCP
- ✅ Copilot knows about your work items, infrastructure, and external systems
- ✅ Ask questions about production resources without leaving your IDE
- ✅ AI suggestions consider real-world constraints and state
- ✅ Integrated workflow across planning, coding, testing, and deployment

---

## MCP Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub Copilot (Client)                  │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Ask Mode     │  │ Edit Mode    │  │ Agent Mode   │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                 │
│         └──────────────────┴──────────────────┘                 │
│                            │                                    │
│                            │ MCP Protocol                       │
└────────────────────────────┼────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        │                    │                    │
┌───────▼────────┐  ┌────────▼────────┐  ┌───────▼────────┐
│ Azure DevOps   │  │ Terraform       │  │ Azure          │
│ MCP Server     │  │ MCP Server      │  │ MCP Server     │
│                │  │                 │  │                │
│ - Work Items   │  │ - State Query   │  │ - Resources    │
│ - Iterations   │  │ - Plan          │  │ - Deployments  │
│ - Repos        │  │ - Validate      │  │ - Monitoring   │
└────────┬───────┘  └────────┬────────┘  └────────┬───────┘
         │                   │                     │
         │                   │                     │
    ┌────▼────┐         ┌────▼────┐          ┌────▼────┐
    │ Azure   │         │ Local   │          │ Azure   │
    │ DevOps  │         │ Terraform│         │ Cloud   │
    │ Service │         │ Files   │          │ API     │
    └─────────┘         └─────────┘          └─────────┘
```

---

## General Setup Process

### Step 1: Install Prerequisites

Before setting up any MCP server, ensure you have:

```bash
# Node.js (required for most MCP servers)
node --version  # Should be v18 or higher

# npm (comes with Node.js)
npm --version
```

If Node.js isn't installed:
- **Windows/macOS**: Download from [nodejs.org](https://nodejs.org/)
- **Linux**: Use your package manager (e.g., `apt install nodejs npm`)

### Step 2: Install MCP Server

Most MCP servers are distributed as npm packages:

```bash
# General pattern
npm install -g @modelcontextprotocol/server-<name>

# Examples
npm install -g @modelcontextprotocol/server-azure-devops
npm install -g @modelcontextprotocol/server-terraform
npm install -g @modelcontextprotocol/server-azure
```

### Step 3: Locate Installation Path

Find where npm installed the package:

```bash
# Get npm global modules path
npm root -g

# Example output (Windows):
# C:\Users\YourUsername\AppData\Roaming\npm\node_modules

# Example output (macOS/Linux):
# /usr/local/lib/node_modules
```

The server executable is typically at:
```
<npm-root>/@modelcontextprotocol/server-<name>/dist/index.js
```

### Step 4: Configure in VS Code

Add the MCP server configuration to VS Code settings:

1. Open VS Code Settings (`Ctrl+,` / `Cmd+,`)
2. Search for "MCP"
3. Click "Edit in settings.json"
4. Add your MCP server configuration

**Example settings.json:**
```json
{
  "github.copilot.chat.mcp.servers": {
    "server-name": {
      "command": "node",
      "args": [
        "/path/to/node_modules/@modelcontextprotocol/server-name/dist/index.js"
      ],
      "env": {
        "ENV_VAR_1": "value1",
        "ENV_VAR_2": "value2"
      }
    }
  }
}
```

### Step 5: Restart VS Code

Close and reopen VS Code to activate the MCP server.

### Step 6: Verify Connection

Test the MCP server in Copilot Chat:

```
@server-name <test command>
```

---

## Configuring MCP Servers

### Azure DevOps MCP

For detailed Azure DevOps MCP setup, see the [Azure DevOps MCP Guide](Azure-DevOps-MCP-Guide.md).

**Quick Configuration:**
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
        "AZURE_DEVOPS_PAT": "your-personal-access-token"
      }
    }
  }
}
```

**Required Environment Variables:**
- `AZURE_DEVOPS_ORG_URL`: Your Azure DevOps organization URL
- `AZURE_DEVOPS_PAT`: Personal Access Token with Work Items permissions

### Terraform MCP

For detailed Terraform MCP setup, see the [Terraform MCP Guide](Terraform-MCP-Guide.md).

**Quick Configuration:**
```json
{
  "github.copilot.chat.mcp.servers": {
    "terraform": {
      "command": "node",
      "args": [
        "/usr/local/lib/node_modules/@modelcontextprotocol/server-terraform/dist/index.js"
      ],
      "env": {
        "TF_WORKSPACE_DIR": "/absolute/path/to/terraform/directory"
      }
    }
  }
}
```

**Required Environment Variables:**
- `TF_WORKSPACE_DIR`: Absolute path to your Terraform configuration directory

### Azure MCP

**Quick Configuration:**
```json
{
  "github.copilot.chat.mcp.servers": {
    "azure": {
      "command": "node",
      "args": [
        "/usr/local/lib/node_modules/@modelcontextprotocol/server-azure/dist/index.js"
      ],
      "env": {
        "AZURE_SUBSCRIPTION_ID": "your-subscription-id",
        "AZURE_TENANT_ID": "your-tenant-id",
        "AZURE_CLIENT_ID": "your-client-id",
        "AZURE_CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

**Required Environment Variables:**
- `AZURE_SUBSCRIPTION_ID`: Azure subscription ID
- `AZURE_TENANT_ID`: Azure AD tenant ID
- `AZURE_CLIENT_ID`: Service principal client ID
- `AZURE_CLIENT_SECRET`: Service principal secret

> [!IMPORTANT]
> For this workshop, Azure credentials are pre-configured as GitHub repository secrets. Ask your instructor for local MCP configuration values if needed.

---

## Troubleshooting

### MCP Server Not Responding

**Symptom**: Copilot doesn't recognize `@server-name` or shows "MCP server error"

**Solutions**:
1. **Verify Installation**:
   ```bash
   npm list -g @modelcontextprotocol/server-name
   ```

2. **Check Path**: Ensure the path in `args` points to the actual `index.js` file

3. **Restart VS Code**: MCP configuration changes require VS Code restart

4. **Check Logs**: Open VS Code Developer Tools (`Help` → `Toggle Developer Tools`) and check Console for errors

### Authentication Failures

**Symptom**: "Unauthorized" or "Authentication failed" errors

**Solutions**:
1. **Verify Credentials**: Double-check environment variable values
2. **Check Permissions**: Ensure PAT or service principal has required permissions
3. **Test Separately**: Test credentials outside of MCP (e.g., Azure CLI, DevOps web UI)

### Environment Variables Not Loading

**Symptom**: MCP server can't find configuration values

**Solutions**:
1. **Use Absolute Paths**: Relative paths in environment variables may not resolve correctly
2. **Escape Special Characters**: Use proper JSON escaping for paths (e.g., `\\` for Windows paths)
3. **Check Spelling**: Environment variable names are case-sensitive

### Performance Issues

**Symptom**: Copilot responses are slow when using MCP

**Solutions**:
1. **Check Network**: MCP servers making API calls depend on network speed
2. **Reduce Scope**: Query smaller datasets (e.g., filter work items by iteration)
3. **Cache Locally**: Some MCP servers support caching for performance

---

## Security Considerations

### Credential Storage

**❌ Don't:**
- Store credentials directly in `settings.json` (it may be synced)
- Commit MCP configuration with secrets to version control
- Share PATs or service principal secrets

**✅ Do:**
- Use environment variables loaded from secure storage
- Rotate credentials periodically
- Use least-privilege access (minimal required permissions)
- Consider using VS Code secrets storage for credentials

### Network Security

- MCP servers make outbound connections to external systems
- Ensure you trust the MCP server source code
- Use encrypted connections (HTTPS) for all MCP communications
- Review what data MCP servers have access to

### Access Control

- Limit MCP server permissions to what's actually needed
- For Azure DevOps: Use PATs with minimal scopes (e.g., only Work Items, not Code)
- For Azure: Use service principals with reader roles where possible
- For Terraform: Ensure the workspace directory only contains intended configs

---

## Best Practices

### Organization

```json
{
  "github.copilot.chat.mcp.servers": {
    // Group related servers
    "azure-devops": { ... },
    "azure": { ... },
    
    // Project-specific servers
    "terraform": { ... }
  }
}
```

### Naming Conventions

- Use descriptive server names: `azure-devops`, not `ado`
- Prefix project-specific servers: `myproject-terraform`
- Keep names short for easy `@mention` usage

### Testing New Servers

1. Configure in a separate workspace first
2. Test with read-only operations
3. Verify credentials have minimal required permissions
4. Monitor behavior before production use

### Documentation

- Document which MCP servers your project uses
- Include setup instructions in project README
- Note any special permissions or access requirements

---

## Related Guides

- [Azure DevOps MCP Guide](Azure-DevOps-MCP-Guide.md) - Detailed Azure Boards integration
- [Terraform MCP Guide](Terraform-MCP-Guide.md) - Infrastructure management with MCP
- [Glossary](Glossary.md) - MCP terminology reference

---

**[← Back to Documentation Index](README.md)**
