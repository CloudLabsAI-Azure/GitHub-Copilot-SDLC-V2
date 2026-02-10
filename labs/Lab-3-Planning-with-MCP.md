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

## 🏢 Planning at ShipIt Industries

You're wrapping up your codebase exploration when Erica, your team lead, stops by your desk:

> **Erica**: "Hey! I hope your exploration of the codebase went well. Before you start coding, let's talk about how we plan work here at ShipIt.
>
> We use **Azure DevOps** for work tracking and sprint planning. Each feature needs a work item with clear acceptance criteria. But here's the cool part - we don't have to context-switch between VS Code and Azure DevOps. We use **MCP** to let Copilot talk directly to our Azure Boards.
>
> I need you to create work items for the GitHub API integration we discussed, as well as some other future enhancements we want to make. Let me show you how we can do it with Copilot and MCP."

This lab introduces a powerful Copilot capability: **connecting to external tools and data sources** via MCP. Instead of leaving your editor to check work items, create tasks, or update project boards, Copilot can do it for you.

> [!IMPORTANT]
> **Model Context Protocol (MCP)** is an open standard that allows AI assistants like GitHub Copilot to securely connect to external data sources and tools. Think of it as giving Copilot "plugins" for your development infrastructure.

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

## Step 2: Azure DevOps MCP Setup

Let's set up the Azure DevOps MCP server to connect Copilot with Azure Boards.

### 2.1 Prerequisites Check

Before proceeding, ensure you have:
- Access to an Azure DevOps organization (your instructor will provide details)
- VS Code with GitHub Copilot and Copilot Chat extensions installed

### 2.2 Install the Azure DevOps MCP Server

The Azure DevOps MCP server by Microsoft is available in the GitHub MCP Registry and can be installed directly from VS Code:

1. Open the **Extensions** panel (`Ctrl+Shift+X` / `Cmd+Shift+X`)
2. Click the **filter icon** in the search bar and select **MCP Server**
   - If this is your first time using the MCP server gallery, follow the on-screen prompts to enable it
3. Search for `Azure DevOps` in the search bar
4. Select the **Azure DevOps** MCP server by **microsoft** from the results
5. Click **Install**
6. 

This will automatically create the server configuration in your `.vscode/mcp.json` file with the recommended `npx`-based setup:

```json
{
  "inputs": [
    {
      "id": "ado_org",
      "type": "promptString",
      "description": "Azure DevOps organization name  (e.g. 'contoso')"
    }
  ],
  "servers": {
    "ado": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@azure-devops/mcp", "${input:ado_org}"]
    }
  }
}
```

> [!NOTE]
> The `npx` command automatically downloads and runs the latest version of the Azure DevOps MCP server — no global install required. When the server starts, VS Code will prompt you for your Azure DevOps organization name.

### 2.3 Start the Server and Authenticate

1. After installation, the server should automatically start. If it doesn't, you can start it manually:
   - Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
   - Search for `MCP: Start Server` and select the Azure DevOps server from the list
   - Click the settings icon next to the server in the MCP panel and select **Start Server**
2. When prompted, enter your **Azure DevOps organization name** (e.g., `contoso`)
3. If prompted, confirm that you **trust** the MCP server
4. The first time an ADO tool is invoked, your **browser will open** prompting you to sign in with your Microsoft account — use the credentials associated with your Azure DevOps organization

> [!IMPORTANT]
> The Azure DevOps MCP server uses browser-based Microsoft authentication. No Personal Access Token (PAT) is required. Ensure you sign in with the account that has access to your organization's Azure DevOps instance.

### 2.4 Verify MCP Connection

Test the connection in Copilot Chat:

<details>
<summary>💡 Example ADO MCP prompt</summary>

**Copilot Mode**: `Agent`
```
List the work items assigned to me in the current iteration.
```

</details>

If configured correctly, Copilot will query Azure DevOps and return your work items!

## Step 3: Planning Features with External Context

Now that Copilot can access Azure DevOps, let's use it for real-world planning.

### 3.1 Query Existing Work Items

Check if there are work items related to ApproveThis:

<details>
<summary>💡 Example prompt for checking work items</summary>

**Copilot Mode**: `Agent`
```
Search for work items in ADO related to "ApproveThis" or "GitHub provider integration". What's the current status?
```

</details>

You might find:
- Existing user stories from the previous developer
- Bug reports or technical debt items
- Feature requests from stakeholders
- OR you might find nothing, which lets us know we need to create new work items!

### 3.2 Create User Stories for ApproveThis Features

Since it doesn't look like there are existing work items, let's have Copilot help us prioritize and create them.

Remember that Erica mentioned several features that need implementation:
- Real GitHub API integration
- Approval workflow system
- E2E testing
- Multi-platform CI/CD

Use Copilot `Ask` mode to help create a prioritized list of what needs to be implemented:

<details>
<summary>💡 Example prompt to create features list</summary>

**Copilot Mode**: `Ask`
```
We need to create user stories for the following features in Azure DevOps:

- Real GitHub API integration (provider implementation)
- Job execution routes and UI
- E2E testing
- Approval workflow implementation
- Azure Function execution provider
- Additional CI/CD platform integrations

Can you help me prioritize these features based on dependencies and complexity and provide an overall outline for each user story? This will be used with the Azure DevOps MCP to create the work items.
```

**Key dependencies:**
- GitHub provider must work before dispatch approvals make sense
- Job execution framework should be functional before adding approval gates
- RBAC is already implemented and can be leveraged

</details>

With our prioritized list, let's create user stories in Azure DevOps for the items Copilot helped us come up with.

> [!IMPORTANT]
> As we need to make use of the ADO MCP to create the work items the best approach is to use `Agent` mode. This will allow Copilot to interact with ADO directly through the MCP connection.
>
> Ensure you have the ADO MCP tools enabled for Agent mode in the tool configuration dropdown.

<details>
<summary>💡 Example prompt for creating ADO work items</summary>

**Copilot Mode**: `Agent`
```
Now that we have the prioritized feature list and outline, can you help me create user stories in Azure DevOps for each feature? Include requirements and acceptance criteria based on existing models and patterns in the codebase.

For tasks that will be implemented later and that rely on other features yet to be implemented, make note of that in the description.

Do not include any direct implementation details in the user stories; focus on what needs to be done from a feature perspective.
```

</details>

Copilot will:
1. Analyze all relevant code files and models
2. Identify the methods that need implementation
3. Generate user story titles and descriptions
4. Submit the work items to Azure DevOps

> [!TIP]
> To enhance Copilot's capabilities when planning out features, consider making use of [custom agents](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents) that are specifically designed to help with project management tasks. This can further streamline the process of creating and managing work items.

### 3.3 Review and Refine User Stories

Review the created work items in Azure DevOps.

**Remember**, Copilot is a powerful assistant, but it's important to validate and refine the generated content to ensure it meets your team's standards.

If you see anything that needs adjustment, you can either edit the work items directly in Azure DevOps or ask Copilot to help refine them:

<details>
<summary>💡 Example prompt to modify a work item</summary>

> [!NOTE]
> **This prompt is strictly an example. The actual work item IDs will vary based on your Azure DevOps instance and the work items created by Copilot.**

**Copilot Mode**: `Agent`
```
For work item #123 (GitHub provider - list_repositories), add technical details about:
- Required GitHub API endpoint
- Authentication approach
- Rate limiting considerations
- Error handling requirements
```

</details>

## Step 4: Governance Policy Integration

ShipIt Industries has development standards. Let's ensure Copilot respects them.

### 4.1 Copilot Instructions File Review

It's always important to review existing instructions in the `.github/copilot-instructions.md` file to understand what policies and guidelines are already in place in the repository. This file may contain coding standards, documentation requirements, testing guidelines, and other required policies that Copilot will use as context when generating suggestions.

**Review the instructions file:**

1. Open `.github/copilot-instructions.md` in VS Code
2. Skim through the file and note the following sections:
   - **Project Overview** - High-level description of the ApproveThis application
   - **Architecture** - Application structure and file organization
   - **Key Patterns** - Provider Pattern, RBAC with Permission Bit Flags, Execution Providers
   - **Development Workflow** - Setup commands, test users, and database migrations
   - **Code Conventions** - Guidelines for adding routes, models, and provider implementations
   - **Testing Strategy** - Testing frameworks and directory structure

3. Pay attention to how the instructions define:
   - Where new code should be placed
   - Which patterns to follow (e.g., Provider Pattern, RBAC decorators)
   - Required imports and conventions

> [!NOTE]
> Copilot automatically reads this file when generating suggestions for your project. Well-structured instructions help Copilot produce code that aligns with your team's standards from the start.

### 4.2 Incorporating Governance Standards through Copilot Spaces

While the `copilot-instructions.md` file defines standards at the repository level, ShipIt Industries also maintains **organization-wide** governance policies, coding standards, security requirements, and review guidelines that apply across all repositories.

These policies live in a **Copilot Space**, a shared knowledge context that Copilot can reference alongside your codebase. Think of it as a centralized policy library that Copilot can consult when generating suggestions, ensuring consistency across the entire organization.

#### Enable Copilot Spaces in Your IDE

A Copilot Space has already been created with ShipIt's governance policies. To access Spaces from VS Code, you need to install the GitHub MCP server and enable the `copilot_spaces` toolset.

1. If you haven't already installed the GitHub MCP server:
   - Open the **Extensions** panel (`Ctrl+Shift+X` / `Cmd+Shift+X`)
   - Click the **filter icon** in the search bar and select **MCP Server**
   - Search for `github` and select the **GitHub MCP Server**
   - Click **Install**

2. Enable the Copilot Spaces toolset:
   - Open **VS Code Settings** (`Ctrl+,` / `Cmd+,`)
   - Search for `GitHub MCP toolsets`
   - Locate the **GitHub > Copilot > Chat > GitHub MCP Server: Toolsets** setting
   - Add `copilot_spaces` to the list of enabled toolsets

> [!IMPORTANT]
> The `copilot_spaces` toolset is **not included** by default. You must explicitly enable it through the settings as described above.

3. Verify the Spaces tools are available:
   - Open the **Copilot Chat** panel and select **Agent** mode
   - Click the **tools icon** (wrench) in the chat input box
   - Expand the list of tools for **GitHub**
   - Confirm that `get_copilot_space` and `list_copilot_spaces` are listed and enabled

#### Access the Governance Space

Copilot Spaces are accessed in VS Code through **Agent mode** by referencing the Space by name in your prompt. Copilot will automatically use the MCP tools to find and retrieve context from the Space.

1. Open **Copilot Chat** and ensure you are in **Agent** mode
2. Reference the governance Space in your prompt — Copilot will use the `list_copilot_spaces` and `get_copilot_space` tools to locate and load the Space's context automatically

<details>
<summary>💡 Example prompt to verify Space access</summary>

**Copilot Mode**: `Agent`
```
Using the Copilot Space 'ShipIt Governance' owned by our organization, summarize the coding standards and governance policies defined in the Space.
```

</details>

> [!TIP]
> 💡 You don't need to remember the exact Space name. You can also use a natural language description and Copilot will search for matching Spaces. For example: `Summarize the governance policies from the Copilot Space for ShipIt coding standards.`

Copilot should return information about ShipIt's organization-wide standards, such as:
- Required code review approvals
- Security and authentication guidelines
- Documentation requirements for new features
- Testing coverage thresholds

#### Validate Policy Compliance

Now let's verify that Copilot respects both the repository-level instructions and the organization-wide governance policies when generating suggestions.

<details>
<summary>💡 Example prompt to check policy compliance</summary>

**Copilot Mode**: `Agent`
```
Based on both the repository's copilot-instructions.md and the governance policies from the ShipIt Governance Copilot Space, what patterns and standards must I follow when implementing the real GitHub provider? Are there any conflicts between the two?
```

</details>

Copilot will cross-reference both sources and highlight:
- Repository-specific patterns (Provider Pattern, RBAC decorators)
- Organization-wide requirements (security policies, testing standards)
- Any areas where both align or where additional attention is needed

<details>
<summary>💡 Example prompt to test governance awareness</summary>

**Copilot Mode**: `Agent`
```
I want to add a new route that exposes repository data from the GitHub API. Based on the governance standards from the ShipIt Governance Space and the repository instructions, what security considerations, authentication requirements, and permission checks must be in place before I implement this?
```

</details>

> [!NOTE]
> Copilot Spaces give organizations a way to enforce standards **across repositories** without duplicating instructions in every repo. When combined with repository-level `copilot-instructions.md`, you get a layered policy model — organization-wide governance plus project-specific conventions.

### 4.3 Generate Technical Design Documentation

You can even have Copilot draft a technical design document for the GitHub provider implementation that adheres to your organization's standards:

<details>
<summary>💡 Example design doc generation prompt</summary>

**Copilot Mode**: `Agent`
```
Please create a technical design document for the future GitHub provider implementation. Include architecture diagrams (in Mermaid), API endpoints used, authentication flow, and testing strategy.
```

</details>

Copilot will generate comprehensive documentation that you can refine and commit to the repository.

---

## 🏆 Exercise Wrap-Up

Outstanding! You've successfully integrated GitHub Copilot with external project management tools using MCP. Let's review your accomplishments:

### ✅ What You Accomplished

- [x] Understood what Model Context Protocol (MCP) is and its benefits
- [x] Installed and configured Azure DevOps MCP server
- [x] Authenticated with Azure DevOps via browser-based sign-in
- [x] Queried existing work items through Copilot
- [x] Created user stories for GitHub provider implementation
- [x] Established governance policies in `.github/copilot-instructions.md`
- [x] Demonstrated how Copilot respects organizational policies
- [x] Planned sprints and linked work items to code

## 🤔 Reflection Questions

Take a moment to consider:

1. How does MCP change the way you interact with GitHub Copilot compared to just using it for code?
2. What benefits do you see in having Copilot aware of your work items and organizational policies?
3. How might you use MCP with other systems in your organization (e.g., documentation wikis, monitoring systems)?
4. What risks or concerns arise from giving AI access to external systems, and how can they be mitigated?

## 🎓 Key Takeaways

- **MCP extends Copilot beyond code** to include project management, infrastructure, and external tools
- **Azure DevOps MCP** enables seamless integration between coding and work item tracking
- **Copilot instructions** (`.github/copilot-instructions.md`) enforce organizational standards automatically
- **Governance policies** can be encoded as AI context, ensuring compliance without manual enforcement
- **Cross-tool planning** becomes possible when AI has access to multiple systems simultaneously
- **Context-aware AI** produces better results by understanding not just code, but business requirements

## Coming Up Next

In **Lab 4: Shifting Our Development Process**, you'll put your plan into action! You'll implement the real GitHub provider using Copilot's advanced modes (Edit and Agent), practice multitasking with AI assistance, and use GitHub Copilot Code Review to ensure quality. Get ready to see how AI transforms the development phase of the SDLC!

**[← Back to Lab 2](Lab-2-Your-Assignment.md)** | **[Continue to Lab 4: Development Process →](Lab-4-Development-Process.md)**
