# Exercise 7 - CI/CD Beyond Just GitHub Actions

**Duration**: 45 minutes

## 🎯 Learning Objectives

By the end of this lab, you will be able to:
- Use Azure MCP Server to explore and understand Azure infrastructure with Copilot
- Understand Azure Functions architecture and how they integrate with other systems
- Analyze and comprehend existing Azure Function code for approval workflows
- Deploy Azure Function infrastructure using Terraform and GitHub Actions
- Deploy Azure Function code using the VS Code Azure Functions extension
- Understand the integration points between GitHub Actions, Azure Functions, and ApproveThis

## 🏢 Expanding ApproveThis Capabilities

Erica flags you down over lunch to discuss the next steps for ApproveThis.

> **Erica**: "Hey! Sorry to disturb your lunch, but I wanted to chat about the next steps for the ApproveThis project.
>
> The CI/CD pipeline we've set up with GitHub Actions is great, and everyone loves it. However, not all of our projects use GitHub Actions. Some teams leverage other mechanisms to handle their CI/CD needs.
>
> The next ask is to get ApproveThis working with Azure systems. We have teams that currently use Azure Functions for a variety of workloads, and we want to make sure that ApproveThis can integrate seamlessly with those systems.
>
> We'll likely need the ability to connect to Azure Functions in place for the approval system functionality that we're going to build out next.
>
> Here's the good news: Copilot understands all these platforms. You can ask it to create configurations and even translate between platforms. Let's use that to our advantage."

With that Erica heads back to her desk. Now it's time to get to work!

---

## Step 1: Introduction to Azure MCP Server

Now that you know the goal, let's explore how GitHub Copilot can help us work with Azure Functions through the Azure MCP Server.

### 1.1 Understanding Azure MCP Server

The Azure MCP Server allows GitHub Copilot to directly query and understand your Azure infrastructure. This gives Copilot context about:

- Existing Azure resources (Resource Groups, Function Apps, Storage Accounts)
- Resource configurations and properties
- Deployment status and health
- Resource relationships and dependencies

> [!NOTE]
> The Azure MCP Server was configured during Lab 1 setup. If you haven't set it up yet, refer to the [MCP Configuration Guide](../docs/MCP-Configuration-Guide.md).

### 1.2 Exploring Azure Resources with Copilot

Let's use Copilot with the Azure MCP Server to understand our current Azure infrastructure.

<details>
<summary>💡 Example prompt</summary>

**Copilot Mode**: `Ask`
```
@azure List all resource groups in my Azure subscription. What resources exist in each?
```

</details>

You should see information about existing resource groups and their resources. This context will help us understand where our Azure Functions will be deployed.

### 1.3 Understanding Function Apps

Now let's ask Copilot about Azure Function Apps specifically:

<details>
<summary>💡 Example prompt</summary>

**Copilot Mode**: `Ask`
```
@azure What Azure Function Apps currently exist in my subscription? Show me their configuration and runtime settings.
```

</details>

This gives us a baseline of what's already deployed (if anything) before we create our new approval functions.

---

## Step 2: Exploring the Azure Function Architecture

Before deploying, let's use Copilot to understand the Azure Function code that will support the approval workflow.

### 2.1 Understand the Function Structure

The Azure Functions for ApproveThis are located in `approvethis/azure-functions/`. Let's have Copilot explain the structure:

<details>
<summary>💡 Example prompt</summary>

**Copilot Mode**: `Ask`
```
@workspace Explain the structure of the Azure Functions in approvethis/azure-functions/. What are the two functions and what does each one do?
```

</details>

**Expected findings:**
- **request-approval**: Receives workflow dispatch requests from GitHub Actions and forwards them to ApproveThis
- **approval-response**: Receives approval/denial decisions from ApproveThis and communicates back to GitHub Actions

### 2.2 Analyze the Request-Approval Function

Let's dive deeper into how the request-approval function works:

<details>
<summary>💡 Example prompt</summary>

**Copilot Mode**: `Ask`
```
@workspace Review the request-approval function in approvethis/azure-functions/request-approval/__init__.py. Explain:
1. What payload does it expect from GitHub Actions?
2. How does it validate the request?
3. Where does it forward the request?
4. What does it return to the caller?
```

</details>

Take time to review Copilot's explanation and look at the actual code. Understanding this flow is crucial for Lab 8.

### 2.3 Analyze the Approval-Response Function

Now let's understand the reverse flow:

<details>
<summary>💡 Example prompt</summary>

**Copilot Mode**: `Ask`
```
@workspace Review the approval-response function in approvethis/azure-functions/approval-response/__init__.py. Explain:
1. What payload does it expect from ApproveThis?
2. How does it communicate the decision back to GitHub?
3. What environment variables does it need?
4. How does it handle approved vs. denied requests?
```

</details>

### 2.4 Understanding the Integration Flow

Have Copilot create a visual representation of how these functions integrate:

<details>
<summary>💡 Example prompt</summary>

**Copilot Mode**: `Ask`
```
@workspace Create a sequence diagram or detailed explanation showing the complete approval workflow flow:
1. GitHub Actions workflow starts
2. Request approval function is called
3. ApproveThis receives and processes request
4. User approves/denies in ApproveThis UI
5. Response function is called
6. GitHub Actions workflow continues/stops

Include all the components and data passed between them.
```

</details>

---

## Step 3: Understanding the Terraform Configuration

The Azure Functions infrastructure is defined in Terraform. Let's explore how it's configured.

### 3.1 Review the Azure Function Module

Ask Copilot to explain the Terraform module that creates the Function App:

<details>
<summary>💡 Example prompt</summary>

**Copilot Mode**: `Ask`
```
@workspace Explain the Terraform configuration in approvethis/terraform/modules/azure-function/. What Azure resources does it create and how are they configured?
```

</details>

**Key resources to understand:**
- Resource Group for organizing resources
- Storage Account (required for Azure Functions)
- App Service Plan (compute resources)
- Linux Function App (the actual function host)

### 3.2 Understand the App Settings

The Function App needs specific configuration. Have Copilot explain the app settings:

<details>
<summary>💡 Example prompt</summary>

**Copilot Mode**: `Ask`
```
@workspace What app settings are configured in the azure-function Terraform module? What does each setting do and why is it needed?
```

</details>

**Critical settings:**
- `APPROVETHIS_API_URL`: Where the ApproveThis app is hosted
- `APPROVETHIS_API_KEY`: Authentication for calling ApproveThis
- `GITHUB_TOKEN`: Authentication for calling GitHub API
- `FUNCTIONS_WORKER_RUNTIME`: Specifies Python runtime

### 3.3 Review CORS Configuration

For the functions to be called from GitHub Actions and ApproveThis, CORS needs to be configured:

<details>
<summary>💡 Example prompt</summary>

**Copilot Mode**: `Ask`
```
@workspace How is CORS configured in the azure-function Terraform module? Why is this important for the approval workflow?
```

</details>

---

## Step 4: Deploying Azure Functions Infrastructure

Now let's deploy the Azure Function infrastructure using the GitHub Actions workflow.

### 4.1 Understanding the Deployment Workflow

Before running the workflow, let's understand what it does:

<details>
<summary>💡 Example prompt</summary>

**Copilot Mode**: `Ask`
```
@workspace Explain the deploy-azure-functions.yml workflow. What does it do and how is it different from the regular terraform-apply workflow?
```

</details>

**Key differences:**
- Targets only the `terraform_function` module
- Deploys just the Function App infrastructure
- Doesn't deploy the function code (we'll do that in Step 5)

### 4.2 Trigger the Deployment Workflow

> [!IMPORTANT]
> This step requires Azure credentials to be configured in your repository. If you're in a workshop environment, your instructor will let you know if this step should be run or simulated.

If Azure credentials are configured, let's deploy the infrastructure:

1. Navigate to your repository on GitHub
2. Go to the **Actions** tab
3. Select the **Deploy Azure Functions Infrastructure** workflow
4. Click **Run workflow**
5. Select the environment (choose `dev`)
6. Click **Run workflow**

### 4.3 Monitor the Deployment

Watch the workflow execution:

1. Click on the workflow run to see details
2. Observe each step: Init, Plan, Apply
3. Look for the **Terraform Output** step to see the created resources

**Expected outputs:**
- Function App name
- Function App URL
- Function endpoints for request-approval and approval-response

### 4.4 Verify in Azure Portal (Optional)

If you have access to the Azure Portal:

1. Navigate to the Azure Portal
2. Find the Resource Group (e.g., `rg-approvethis-func-dev`)
3. Verify the Function App was created
4. Check the Configuration settings to see the app settings

Alternatively, use the Azure MCP Server:

<details>
<summary>💡 Example prompt</summary>

**Copilot Mode**: `Ask`
```
@azure Show me the newly created Function App and its configuration. What app settings are currently set?
```

</details>

---

## Step 5: Deploying Function Code with VS Code

The infrastructure is deployed, but we haven't deployed the actual function code yet. Let's use the Azure Functions VS Code extension to deploy the code.

### 5.1 Install Azure Functions Extension

If you haven't already installed it:

1. Open VS Code Extensions view (`Ctrl+Shift+X` / `Cmd+Shift+X`)
2. Search for "Azure Functions"
3. Install the **Azure Functions** extension by Microsoft
4. Reload VS Code if prompted

### 5.2 Sign in to Azure

1. Click on the Azure icon in the VS Code sidebar
2. Click **Sign in to Azure**
3. Follow the authentication flow in your browser
4. Return to VS Code after successful sign-in

### 5.3 Deploy the Functions

Now let's deploy the function code:

1. In VS Code, navigate to `approvethis/azure-functions/`
2. Right-click on the `azure-functions` folder
3. Select **Deploy to Function App...**
4. Choose your subscription
5. Select the Function App you created (e.g., `func-approvethis-dev-001`)
6. Confirm the deployment when prompted

> [!TIP]
> The deployment may take a few minutes. VS Code will show progress in the output panel.

### 5.4 Verify the Deployment

After deployment completes:

1. In the Azure Functions extension panel, expand your Function App
2. You should see two functions:
   - `request-approval`
   - `approval-response`
3. Right-click on each function and select **Copy Function Url** to get the endpoint URLs

### 5.5 Test the Functions (Optional)

If you want to test that the functions are working, you can use a tool like curl or Postman:

<details>
<summary>💡 Test request-approval function</summary>

```bash
curl -X POST https://your-function-app.azurewebsites.net/api/approval/request?code=YOUR_FUNCTION_KEY \
  -H "Content-Type: application/json" \
  -d '{
    "workflow": "deploy-production",
    "repository": "org/repo",
    "branch": "main",
    "requestor": "testuser",
    "run_id": "12345"
  }'
```

Expected response (may show error about ApproveThis URL not configured, which is expected):
```json
{
  "error": "Function not properly configured"
}
```

This is normal - the function needs the `APPROVETHIS_API_URL` to be configured, which will be done in Lab 8.

</details>

### 5.6 Configure Secrets (Preview for Lab 8)

The functions need certain secrets to work properly. These will be fully configured in Lab 8, but let's understand what's needed:

<details>
<summary>💡 Example prompt</summary>

**Copilot Mode**: `Ask`
```
@workspace What secrets and environment variables need to be configured in the Azure Function App for the approval functions to work? Where should these be set?
```

</details>

**Secrets needed:**
- `APPROVETHIS_API_URL`: URL of the deployed ApproveThis application
- `APPROVETHIS_API_KEY`: API key for authentication
- `GITHUB_TOKEN`: GitHub PAT for API calls

> [!NOTE]
> In Lab 8, you'll configure these secrets as part of implementing the complete approval workflow.

---

## Step 6: Understanding the Integration Points

Now that we have the functions deployed, let's understand how they'll integrate with the rest of the system.

### 6.1 GitHub Actions Integration

Have Copilot explain how GitHub Actions will call these functions:

<details>
<summary>💡 Example prompt</summary>

**Copilot Mode**: `Ask`
```
@workspace How would a GitHub Actions workflow call the request-approval Azure Function? Show me an example workflow step that makes this call.
```

</details>

Copilot should show you something like:

```yaml
- name: Request Approval
  id: request_approval
  run: |
    response=$(curl -X POST ${{ secrets.APPROVAL_FUNCTION_URL }} \
      -H "Content-Type: application/json" \
      -d '{
        "workflow": "${{ github.workflow }}",
        "repository": "${{ github.repository }}",
        "branch": "${{ github.ref_name }}",
        "requestor": "${{ github.actor }}",
        "run_id": "${{ github.run_id }}"
      }')
    echo "Response: $response"
```

### 6.2 ApproveThis Integration

Now understand how ApproveThis will use these functions:

<details>
<summary>💡 Example prompt</summary>

**Copilot Mode**: `Ask`
```
@workspace How will the ApproveThis application call the approval-response function when a user approves or denies a request? What Python code would make this call?
```

</details>

### 6.3 Understanding the Complete Flow

Let's have Copilot create a comprehensive explanation:

<details>
<summary>💡 Example prompt</summary>

**Copilot Mode**: `Ask`
```
@workspace Create a detailed walkthrough of the complete approval workflow from start to finish:
1. GitHub Actions workflow triggers
2. Calls request-approval function
3. ApproveThis receives and displays request
4. User approves/denies
5. ApproveThis calls approval-response function
6. GitHub workflow continues or stops

Include code examples and explain what happens at each step.
```

</details>

---

## 🏆 Exercise Wrap-Up

Excellent work! You've successfully set up the Azure Functions integration for ApproveThis. Let's review what you accomplished:

### ✅ What You Accomplished

- [x] Used Azure MCP Server to explore and understand Azure infrastructure
- [x] Analyzed the Azure Function code for request-approval and approval-response
- [x] Understood the Terraform configuration for Azure Functions
- [x] Deployed Azure Function infrastructure using GitHub Actions workflow
- [x] Deployed Azure Function code using VS Code Azure Functions extension
- [x] Verified function deployment and endpoints
- [x] Understood the integration points for Lab 8

## 🤔 Reflection Questions

Take a moment to consider:

1. How did the Azure MCP Server help you understand the Azure infrastructure without leaving VS Code?
2. What are the benefits of separating infrastructure deployment (Terraform) from code deployment (VS Code extension)?
3. How do the two Azure Functions work together to create a bidirectional communication channel?
4. What security considerations are important when deploying Azure Functions that communicate with GitHub?
5. How does understanding the function architecture now help you prepare for implementing the approval workflow in Lab 8?

## 🎓 Key Takeaways

- **Azure MCP Server** provides Copilot with context about your Azure resources and infrastructure
- **Terraform modules** define infrastructure in a reusable, version-controlled way
- **Azure Functions** can act as middleware between different systems (GitHub ↔ ApproveThis)
- **Function-level authentication** (`authLevel: "function"`) provides basic security with function keys
- **Environment variables** in Function Apps store configuration and secrets securely
- **VS Code Azure Functions extension** simplifies function code deployment
- **Separation of concerns**: Infrastructure via Terraform, code via VS Code, configuration via Azure Portal/secrets
- **Copilot with MCP** can help you understand, deploy, and debug cloud infrastructure

## 🔜 Coming Up Next

In **Lab 8: Capstone Challenge - ApproveThis Requires Approvals**, you'll apply everything you've learned throughout this workshop to implement the signature feature of ApproveThis: the approval workflow! 

You'll use the Azure Functions you just deployed to create a complete approval system where:
- Deployment workflows request approval before executing
- GlobalAdmin users can approve or deny requests
- The approval decision is communicated back to GitHub Actions
- The workflow continues or stops based on the decision

This is your opportunity to work autonomously with Copilot as your development partner and demonstrate mastery of AI-assisted SDLC practices.

**[← Back to Lab 6](Lab-6-IaC-and-Deployments.md)** | **[Continue to Lab 8: Capstone Challenge →](Lab-8-Capstone-Approvals.md)**
