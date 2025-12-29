# Exercise 6 - IaC and Deployments with GitHub Copilot

**Duration**: 30 minutes

## 🎯 Learning Objectives

By the end of this lab, you will be able to:
- Use GitHub Copilot with Azure and Terraform MCP servers
- Understand and navigate existing Terraform infrastructure code
- Enhance Terraform modules with AI assistance
- Execute infrastructure deployments through GitHub Actions
- Trigger Terraform operations from the ApproveThis application
- Validate and test infrastructure changes safely

## 📸 Scenario: Infrastructure Deployment at ShipIt Industries

🏢 Your manager at ShipIt Industries is thrilled with your progress on ApproveThis. Now she has a new challenge:

> "We need to deploy ApproveThis to Azure so teams can start using it. The previous developer created some Terraform modules, but they're incomplete. We need to:
> 1. Understand what infrastructure is already defined
> 2. Complete any missing components
> 3. Deploy to a dev environment first, then production
> 4. Enable teams to trigger Terraform plans through the ApproveThis UI (that's the whole point!)

> Can you use Copilot to understand the Terraform code and get us deployed? And remember—we need approval workflows for production deployments!"

With **Azure MCP** and **Terraform MCP**, you'll bring infrastructure context directly into Copilot. Let's see how AI transforms infrastructure as code!

---

## Step 1: Understanding MCP for Infrastructure

### 1.1 Why MCP for Infrastructure?

Traditional IaC challenges:
- ❌ Understanding complex Terraform modules takes time
- ❌ Knowing current Azure resource state requires portal visits
- ❌ Changes risk breaking existing infrastructure
- ❌ Difficult to plan changes without deep Terraform knowledge

With Azure and Terraform MCP:
- ✅ Query current Azure resource state from your IDE
- ✅ Ask Copilot about Terraform module structure and dependencies
- ✅ Validate changes before applying them
- ✅ Understand resource relationships and outputs

### 1.2 MCP Servers for Infrastructure

For this lab, you'll use:

1. **Azure MCP Server**
   - Query Azure resources and their state
   - Understand resource groups, app services, functions
   - Check current deployment status

2. **Terraform MCP Server**
   - Understand Terraform state
   - Query module outputs and variables
   - Validate configuration syntax
   - Plan changes before applying

> [!NOTE]
> For detailed installation and configuration, see the [Terraform MCP Guide](../docs/Terraform-MCP-Guide.md) and [MCP Configuration Guide](../docs/MCP-Configuration-Guide.md).

---

## Step 2: Setting Up Infrastructure MCP Servers

### 2.1 Install Azure MCP Server

Install the Azure MCP server via npm:

```bash
npm install -g @modelcontextprotocol/server-azure
```

### 2.2 Configure Azure MCP

Add Azure MCP configuration to your VS Code settings.json:

```json
{
  "github.copilot.chat.mcp.servers": {
    "azure": {
      "command": "node",
      "args": [
        "C:\\Users\\YourUsername\\AppData\\Roaming\\npm\\node_modules\\@modelcontextprotocol\\server-azure\\dist\\index.js"
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

> [!IMPORTANT]
> Your training repository has Azure credentials pre-configured as GitHub secrets. You can use those values for local MCP configuration. Ask your instructor for access to these values if needed.

### 2.3 Install Terraform MCP Server

Install the Terraform MCP server:

```bash
npm install -g @modelcontextprotocol/server-terraform
```

### 2.4 Configure Terraform MCP

Add Terraform MCP to your settings.json:

```json
{
  "github.copilot.chat.mcp.servers": {
    "terraform": {
      "command": "node",
      "args": [
        "C:\\Users\\YourUsername\\AppData\\Roaming\\npm\\node_modules\\@modelcontextprotocol\\server-terraform\\dist\\index.js"
      ],
      "env": {
        "TF_WORKSPACE_DIR": "/home/runner/work/copilot-advanced-workshop-sdlc/copilot-advanced-workshop-sdlc/approvethis/terraform"
      }
    }
  }
}
```

### 2.5 Verify MCP Connections

Restart VS Code and test the connections:

<details>
<summary>💡 Example prompts to test</summary>

```
@azure List resource groups in my subscription

@terraform Show me the Terraform modules in this repository
```

</details>

---

## Step 3: Exploring Existing Terraform Infrastructure

Let's use Copilot to understand the existing Terraform setup.

### 3.1 Understand the Module Structure

Navigate to `approvethis/terraform/` and ask Copilot:

<details>
<summary>💡 Example prompt</summary>

```
@workspace @terraform Explain the Terraform module structure in approvethis/terraform/. What modules exist, how are they organized, and what does each module create?
```

</details>

**Expected structure:**
```
terraform/
├── modules/
│   ├── azure-function/     # Azure Function App module
│   ├── app-service/        # Azure App Service module  
│   └── storage-account/    # Azure Storage Account module
└── environments/
    ├── dev/                # Development environment
    └── production/         # Production environment
```

### 3.2 Explore the App Service Module

Examine the app-service module:

<details>
<summary>💡 Example prompt</summary>

```
@terraform Analyze the app-service module in terraform/modules/app-service/. What Azure resources does it create? What are the required variables and outputs?
```

</details>

**Key resources:**
- Azure App Service Plan
- Azure App Service (Linux/Windows)
- Application settings and connection strings
- Deployment slots (staging/production)

### 3.3 Understand Environment Configurations

Compare dev and production environments:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Compare terraform/environments/dev/main.tf and terraform/environments/production/main.tf. What are the differences in configuration? What resources are the same vs. different?
```

</details>

Typical differences:
- App Service Plan tier (Basic for dev, Standard/Premium for prod)
- Number of instances
- Auto-scaling configuration
- Backup and disaster recovery settings

---

## Step 4: Enhancing Terraform Modules

Let's improve the existing Terraform modules with Copilot's help.

### 4.1 Add Missing Outputs

Ask Copilot to identify and add useful outputs:

<details>
<summary>💡 Example prompt</summary>

```
@terraform Review terraform/modules/app-service/outputs.tf. What additional outputs would be useful for consuming modules? Consider:
- Application URL
- Staging slot URL
- Resource IDs for cross-module references
- Connection strings for databases
Add these outputs to the file.
```

</details>

**Example additions:**
```hcl
output "app_service_default_hostname" {
  description = "Default hostname of the App Service"
  value       = azurerm_app_service.main.default_site_hostname
}

output "app_service_staging_hostname" {
  description = "Hostname of the staging slot"
  value       = azurerm_app_service_slot.staging.default_site_hostname
}

output "app_service_id" {
  description = "Resource ID of the App Service"
  value       = azurerm_app_service.main.id
}
```

### 4.2 Add Monitoring and Diagnostics

Enhance the app-service module with monitoring:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Add Application Insights monitoring to the app-service module in terraform/modules/app-service/main.tf. Include:
- Application Insights resource
- Automatic instrumentation for the App Service
- Connection to Log Analytics workspace
- Standard metrics and alerts
Follow Azure best practices for naming and tagging.
```

</details>

### 4.3 Implement Security Best Practices

Ask Copilot for security improvements:

<details>
<summary>💡 Example prompt</summary>

```
@terraform Review the app-service module for security best practices. Suggest improvements for:
- HTTPS enforcement
- TLS version requirements
- Managed identity usage
- IP restrictions
- Virtual network integration
Apply recommended changes to terraform/modules/app-service/main.tf
```

</details>

### 4.4 Add Variables for Customization

Make the module more flexible:

<details>
<summary>💡 Example prompt</summary>

```
@workspace The app-service module should support additional customization. Add variables in terraform/modules/app-service/variables.tf for:
- Custom domain support
- SSL certificate configuration
- Scaling rules (min/max instances)
- Application settings map
- Environment-specific tags
Include descriptions and default values.
```

</details>

---

## Step 5: Validating Terraform Changes

Before deploying, let's validate the changes.

### 5.1 Terraform Validation

Run Terraform validation:

```bash
cd approvethis/terraform/environments/dev
terraform init
terraform validate
```

If there are errors, ask Copilot:

<details>
<summary>💡 Example prompt</summary>

```
@terraform I'm getting this Terraform validation error: [paste error]. What's wrong and how do I fix it?
```

</details>

### 5.2 Terraform Plan with MCP

Use the Terraform MCP to run a plan:

<details>
<summary>💡 Example prompt</summary>

```
@terraform Run a Terraform plan for the dev environment. What resources will be created, modified, or destroyed?
```

</details>

> [!TIP]
> 💡 Always review the Terraform plan output carefully before applying. Look for unexpected deletions or modifications.

### 5.3 Check for Drift

Compare current Azure state with Terraform state:

<details>
<summary>💡 Example prompt</summary>

```
@azure @terraform Are there any Azure resources in the resource group "approvethis-dev-rg" that are not managed by Terraform? Check for drift.
```

</details>

---

## Step 6: Deploying via GitHub Actions

Your repository has pre-configured secrets for Azure deployment. Let's use them!

### 6.1 Review the Terraform Workflow

Examine `.github/workflows/terraform-deploy.yml`:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Explain the GitHub Actions workflow in .github/workflows/terraform-deploy.yml. What are the steps, and what secrets does it use?
```

</details>

**Expected workflow steps:**
1. Checkout code
2. Setup Terraform
3. Azure login using OIDC or service principal
4. Terraform init
5. Terraform plan
6. (Manual approval for production)
7. Terraform apply

### 6.2 Verify Pre-Configured Secrets

As mentioned in Lab 1, verify these secrets exist in your repository:

- `AZURE_CLIENT_ID`
- `AZURE_TENANT_ID`
- `AZURE_SUBSCRIPTION_ID`
- `ARM_CLIENT_ID`
- `ARM_CLIENT_SECRET`
- `ARM_TENANT_ID`

> [!NOTE]
> These secrets were pre-configured by your instructor. You don't need to create them.

### 6.3 Enhance the Workflow

Add improvements to the workflow:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Enhance the Terraform GitHub Actions workflow to:
1. Add Terraform fmt check before plan
2. Post plan output as a PR comment
3. Add cost estimation using Infracost (if available)
4. Require manual approval before applying to production
5. Save plan artifacts for review
Update .github/workflows/terraform-deploy.yml
```

</details>

### 6.4 Trigger the Workflow

Trigger the workflow manually or via push:

1. Navigate to Actions tab in GitHub
2. Select "Terraform Deploy" workflow
3. Click "Run workflow"
4. Choose environment (dev)
5. Monitor the execution

---

## Step 7: Application-Triggered Deployments

The ultimate goal: triggering Terraform from ApproveThis UI!

### 7.1 Understand the Job Execution Framework

Review the job execution models:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Explain how JobDefinition, JobExecution, and ExecutionTarget models work together in app/models/. How would we configure a Terraform plan job?
```

</details>

**Job execution flow:**
1. **JobDefinition** - Template defining what to execute (e.g., "Terraform Plan - Dev")
2. **ExecutionTarget** - Where to execute (GitHub Actions, Azure Function, etc.)
3. **JobExecution** - Record of specific execution with status and logs

### 7.2 Create a Terraform Job Definition

Ask Copilot to help create job definitions:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create a database seed script or migration to add JobDefinition entries for Terraform operations:
1. "Terraform Plan - Dev Environment"
2. "Terraform Apply - Dev Environment"  
3. "Terraform Plan - Production Environment"
4. "Terraform Apply - Production Environment"

Each should target the "GitHub Actions" ExecutionTarget and include appropriate parameters for environment selection.
```

</details>

### 7.3 Implement Jobs Blueprint Routes

If not already implemented, create routes for job execution:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Implement routes in app/blueprints/jobs/routes.py for:
- Listing available job definitions
- Viewing job execution history
- Triggering a new job execution
- Viewing job execution details and logs
Follow the existing blueprint patterns and include RBAC checks.
```

</details>

### 7.4 Test Terraform Execution from UI

Once implemented:

1. Login to ApproveThis as admin
2. Navigate to Jobs section
3. Select "Terraform Plan - Dev Environment"
4. Click "Execute"
5. Monitor progress in the UI
6. View execution logs

> [!IMPORTANT]
> Production Terraform applies should require approval! This is part of your Lab 8 capstone challenge.

---

## Step 8: Infrastructure Documentation

Document the infrastructure for the team.

### 8.1 Generate Module Documentation

Create comprehensive docs:

<details>
<summary>💡 Example prompt</summary>

```
@terraform Generate detailed documentation for each Terraform module in terraform/modules/. Include:
- Purpose and description
- Resources created
- Required variables with descriptions
- Optional variables with defaults
- Outputs and their use cases
- Usage examples
Create terraform/modules/README.md with this documentation.
```

</details>

### 8.2 Create Environment-Specific Guides

Document environment configurations:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create a deployment guide for each environment (dev and production). Include:
- Prerequisites and required secrets
- Step-by-step deployment instructions
- Validation steps post-deployment
- Rollback procedures
- Troubleshooting common issues
Save as terraform/environments/DEPLOYMENT_GUIDE.md
```

</details>

---

## 🏆 Exercise Wrap-Up

Excellent work! You've mastered infrastructure as code with AI assistance. Let's review what you accomplished:

### ✅ What You Accomplished

- [x] Set up Azure and Terraform MCP servers for infrastructure context
- [x] Explored and understood existing Terraform module structure
- [x] Enhanced Terraform modules with additional outputs and features
- [x] Implemented security and monitoring best practices
- [x] Validated Terraform configuration and planned changes safely
- [x] Deployed infrastructure using GitHub Actions with pre-configured secrets
- [x] Configured job definitions for Terraform execution via ApproveThis UI
- [x] Generated comprehensive infrastructure documentation

---

## 🤔 Reflection Questions

Take a moment to consider:

1. How does MCP access to Azure and Terraform state change infrastructure development?
2. What risks exist when AI suggests infrastructure changes, and how can you mitigate them?
3. How does integrating Terraform execution into ApproveThis improve operational workflows?
4. What's the value of infrastructure approval workflows for production deployments?
5. How can AI-generated documentation stay in sync with infrastructure changes?

---

## 🎓 Key Takeaways

- **MCP for infrastructure** brings Azure and Terraform context into your development environment
- **Terraform validation** should always be done before applying changes
- **GitHub Actions with pre-configured secrets** enables secure, automated deployments
- **Infrastructure documentation** can be generated and maintained with AI assistance
- **Job execution framework** enables triggering infrastructure operations from application UI
- **Security and monitoring** should be built into infrastructure from the start
- **Environment separation** (dev/production) prevents accidental production changes

---

## 🔜 Coming Up Next

In **Lab 7: CI/CD Beyond GitHub Actions**, you'll explore how GitHub Copilot can help with CI/CD across multiple platforms—not just GitHub Actions, but also Azure DevOps Pipelines, Jenkins, and more. You'll see how Copilot's knowledge extends across the entire DevOps ecosystem!

**Note:** Lab 7 is currently being finalized and will focus on multi-platform CI/CD patterns.

---

**[← Back to Lab 5](Lab-5-Testing-with-Copilot.md)** | **[Continue to Lab 7: CI/CD Beyond GitHub Actions →](Lab-7-CI-CD-Beyond-GitHub-Actions.md)**
