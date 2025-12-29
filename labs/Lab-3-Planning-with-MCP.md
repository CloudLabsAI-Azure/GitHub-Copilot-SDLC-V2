# Exercise 3 - Real-World Planning with GitHub Copilot and MCP

**Duration**: 35 minutes

## 🎯 Learning Objectives

By the end of this lab, you will be able to:
- Understand what Model Context Protocol (MCP) is and why it matters
- Set up and configure MCP servers for external integrations
- Connect GitHub Copilot to Azure DevOps using Azure DevOps MCP
- Plan features with Copilot using real project management context
- Create work items and user stories with AI assistance
- Incorporate governance policies into AI-generated suggestions

## 📸 Scenario: Planning at ShipIt Industries

🏢 After exploring the ApproveThis codebase, you meet with your manager at ShipIt Industries to discuss the implementation plan. She mentions:

> "We track all our work in Azure DevOps. Make sure you create work items for the features you'll be implementing. Also, check if there are any existing items assigned to you from the previous developer."

Additionally, she hands you a document titled "ShipIt Industries Development Standards" which includes:
- All API integrations must include rate limiting
- Authentication tokens must be stored securely, never in code
- All workflow dispatches require approval (hence the name ApproveThis!)

Instead of manually switching between your IDE, Azure DevOps, and policy documents, you'll use **Model Context Protocol (MCP)** to bring all this context directly into GitHub Copilot. Let's see how!

---

## Step 1: Introduction to Model Context Protocol (MCP)

### 1.1 What is MCP?

**Model Context Protocol (MCP)** is an open standard that allows AI assistants like GitHub Copilot to connect to external data sources and tools. Think of it as a universal adapter that lets Copilot:

- Query your project management system (Azure DevOps, Jira)
- Access cloud resources (Azure, AWS)  
- Retrieve documentation from knowledge bases
- Execute specialized tools (Terraform, deployment systems)

> [!NOTE]
> MCP extends Copilot's context beyond your codebase. While Copilot normally only knows about your code, MCP allows it to understand your work items, infrastructure state, deployment history, and more.

### 1.2 MCP Servers for This Workshop

In this workshop, you'll work with three MCP servers:

- **Azure DevOps MCP** (This lab) - Connect to Azure Boards for work item management
- **Azure MCP** (Lab 6) - Query and manage Azure resources
- **Terraform MCP** (Lab 6) - Understand infrastructure state and plan changes

For detailed information on MCP architecture and concepts, see the [MCP Configuration Guide](../docs/MCP-Configuration-Guide.md).

---

## Step 2: Azure DevOps MCP Setup

Let's set up the Azure DevOps MCP server to connect Copilot with Azure Boards.

### 2.1 Prerequisites Check

Before proceeding, ensure you have:
- Access to an Azure DevOps organization (your instructor will provide details)
- VS Code with GitHub Copilot and Copilot Chat extensions installed
- Node.js installed (for the MCP server runtime)

### 2.2 Install Azure DevOps MCP Server

The Azure DevOps MCP server is distributed as an npm package. Install it globally:

```bash
npm install -g @modelcontextprotocol/server-azure-devops
```

> [!TIP]
> 💡 If you don't have Node.js installed, download it from [nodejs.org](https://nodejs.org/). The LTS version is recommended.

### 2.3 Create Azure DevOps Personal Access Token (PAT)

You'll need a PAT to authenticate with Azure DevOps:

1. Navigate to your Azure DevOps organization
2. Click your profile icon → **Personal access tokens**
3. Click **+ New Token**
4. Configure the token:
   - **Name**: `Copilot MCP Integration`
   - **Organization**: Select your organization
   - **Expiration**: Choose an appropriate timeframe (e.g., 30 days for training)
   - **Scopes**: Select **Work Items** (Read & Write)
5. Click **Create** and **copy the token value**

> [!IMPORTANT]
> Store your PAT securely! You'll need it in the next step. Once you close the dialog, you cannot retrieve it again.

### 2.4 Configure MCP in VS Code

Configure the MCP server in your VS Code settings:

1. Open VS Code Settings (`Ctrl+,` / `Cmd+,`)
2. Search for "MCP"
3. Click "Edit in settings.json"

Add the Azure DevOps MCP configuration:

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
        "AZURE_DEVOPS_PAT": "your-personal-access-token-here"
      }
    }
  }
}
```

**Adjust the following:**
- **Path to index.js**: Use the global npm modules path (run `npm root -g` to find it)
- **AZURE_DEVOPS_ORG_URL**: Your Azure DevOps organization URL
- **AZURE_DEVOPS_PAT**: The PAT you created in step 2.3

> [!TIP]
> 💡 For detailed platform-specific configuration steps, see the [Azure DevOps MCP Guide](../docs/Azure-DevOps-MCP-Guide.md).

### 2.5 Restart VS Code

Close and reopen VS Code to activate the MCP server.

### 2.6 Verify MCP Connection

Test the connection in Copilot Chat:

<details>
<summary>💡 Example prompt</summary>

```
@azure-devops List the work items assigned to me in the current iteration.
```

</details>

If configured correctly, Copilot will query Azure DevOps and return your work items!

---

## Step 3: Planning Features with External Context

Now that Copilot can access Azure DevOps, let's use it for real-world planning.

### 3.1 Query Existing Work Items

Check if there are work items related to ApproveThis:

<details>
<summary>💡 Example prompt</summary>

```
@azure-devops Search for work items related to "ApproveThis" or "GitHub provider integration". What's the current status?
```

</details>

You might find:
- Existing user stories from the previous developer
- Bug reports or technical debt items
- Feature requests from stakeholders

### 3.2 Create User Stories for GitHub Provider

Based on your Lab 2 exploration, you know the real GitHub provider needs implementation. Ask Copilot to help create user stories:

<details>
<summary>💡 Example prompt</summary>

```
@workspace @azure-devops Based on the NotImplementedError findings in app/providers/github.py, help me create user stories in Azure DevOps for implementing the real GitHub provider. Each method should be its own story with acceptance criteria.
```

</details>

Copilot will:
1. Analyze the `github.py` file
2. Identify the methods that need implementation
3. Generate user story titles and descriptions
4. Create acceptance criteria based on the `base.py` interface
5. Submit the work items to Azure DevOps

**Expected user stories:**
- "Implement list_repositories() in GitHub provider"
- "Implement list_workflows() in GitHub provider"  
- "Implement dispatch_workflow() in GitHub provider"
- etc.

### 3.3 Review and Refine User Stories

Review the created work items in Azure DevOps. Ask Copilot to enhance them:

<details>
<summary>💡 Example prompt</summary>

```
@azure-devops For work item #123 (GitHub provider - list_repositories), add technical details about:
- Required GitHub API endpoint
- Authentication approach
- Rate limiting considerations
- Error handling requirements
```

</details>

---

## Step 4: Governance Policy Integration

ShipIt Industries has development standards. Let's ensure Copilot respects them.

### 4.1 Create Copilot Instructions File

Create a `.github` directory in the repository root (if it doesn't exist):

```bash
mkdir -p /home/runner/work/copilot-advanced-workshop-sdlc/copilot-advanced-workshop-sdlc/.github
```

Create `.github/copilot-instructions.md`:

```markdown
# ShipIt Industries Development Standards

## API Integration Requirements

- All external API integrations MUST include rate limiting
- API calls MUST have retry logic with exponential backoff
- All errors MUST be logged with appropriate context
- Authentication tokens MUST be stored in environment variables, never hardcoded

## Security Standards

- All user inputs MUST be validated and sanitized
- Authentication tokens MUST use secure storage mechanisms
- Sensitive data MUST NOT appear in logs or error messages

## Workflow Dispatch Standards

- All workflow dispatches REQUIRE approval from GlobalAdmin users
- Dispatch requests MUST be logged with user, timestamp, and parameters
- Failed dispatches MUST be retried according to configured retry policy

## Code Quality

- All new code MUST include unit tests
- Test coverage MUST be at least 80% for new files
- All public functions MUST have docstrings
- Follow PEP 8 style guide for Python code

## ApproveThis Specific Guidelines

- Use the provider pattern for all external service integrations
- Leverage existing RBAC system for permission checks
- All database changes require migrations via Flask-Migrate
- Follow the blueprint organization for new routes
```

> [!IMPORTANT]
> Copilot instructions take effect immediately. Copilot will now incorporate these policies into all code suggestions.

### 4.2 Test Policy Integration

Ask Copilot to generate code and observe how it follows the policies:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Help me implement the list_repositories() method in app/providers/github.py
```

</details>

Notice that Copilot's suggestions now include:
- Environment variable for API token (not hardcoded)
- Rate limiting considerations
- Error handling with logging
- Docstrings

This is the power of governance through AI context!

---

## Step 5: Cross-Tool Planning

Let's plan a sprint using Copilot with Azure DevOps context.

### 5.1 Create a Sprint Plan

Ask Copilot to help organize work items into a sprint:

<details>
<summary>💡 Example prompt</summary>

```
@azure-devops Based on the user stories we created for GitHub provider implementation, help me create a 2-week sprint plan. Consider dependencies and prioritize core functionality first.
```

</details>

Copilot will:
- Identify dependencies (e.g., authentication before API calls)
- Suggest sprint ordering
- Estimate story points based on complexity
- Create a sprint backlog

### 5.2 Link Code Changes to Work Items

When you start implementing in Lab 4, you can link commits to work items:

<details>
<summary>💡 Example prompt</summary>

```
@azure-devops Generate a commit message for implementing list_repositories() that links to work item #123
```

</details>

Example output:
```
Implement list_repositories() in GitHub provider

- Connects to GitHub API using PyGithub library
- Includes rate limiting with exponential backoff
- Authenticates using GITHUB_TOKEN from environment
- Includes comprehensive error handling

Resolves AB#123
```

The `AB#123` syntax automatically links the commit to Azure Boards!

### 5.3 Generate Technical Design Documentation

Use Copilot to draft a technical design document:

<details>
<summary>💡 Example prompt</summary>

```
@workspace @azure-devops Create a technical design document for the GitHub provider implementation. Include architecture diagrams (in Mermaid), API endpoints used, authentication flow, and testing strategy.
```

</details>

Copilot will generate comprehensive documentation that you can refine and commit to the repository.

---

## 🏆 Exercise Wrap-Up

Outstanding! You've successfully integrated GitHub Copilot with external project management tools using MCP. Let's review your accomplishments:

### ✅ What You Accomplished

- [x] Understood what Model Context Protocol (MCP) is and its benefits
- [x] Installed and configured Azure DevOps MCP server
- [x] Created Personal Access Token for Azure DevOps authentication
- [x] Queried existing work items through Copilot
- [x] Created user stories for GitHub provider implementation
- [x] Established governance policies in `.github/copilot-instructions.md`
- [x] Demonstrated how Copilot respects organizational policies
- [x] Planned sprints and linked work items to code

---

## 🤔 Reflection Questions

Take a moment to consider:

1. How does MCP change the way you interact with GitHub Copilot compared to just using it for code?
2. What benefits do you see in having Copilot aware of your work items and organizational policies?
3. How might you use MCP with other systems in your organization (e.g., documentation wikis, monitoring systems)?
4. What risks or concerns arise from giving AI access to external systems, and how can they be mitigated?

---

## 🎓 Key Takeaways

- **MCP extends Copilot beyond code** to include project management, infrastructure, and external tools
- **Azure DevOps MCP** enables seamless integration between coding and work item tracking
- **Copilot instructions** (`.github/copilot-instructions.md`) enforce organizational standards automatically
- **Governance policies** can be encoded as AI context, ensuring compliance without manual enforcement
- **Cross-tool planning** becomes possible when AI has access to multiple systems simultaneously
- **Context-aware AI** produces better results by understanding not just code, but business requirements

---

## 🔜 Coming Up Next

In **Lab 4: Shifting Our Development Process**, you'll put your plan into action! You'll implement the real GitHub provider using Copilot's advanced modes (Edit and Agent), practice multitasking with AI assistance, and use GitHub Copilot Code Review to ensure quality. Get ready to see how AI transforms the development phase of the SDLC!

---

**[← Back to Lab 2](Lab-2-Your-Assignment.md)** | **[Continue to Lab 4: Development Process →](Lab-4-Development-Process.md)**
