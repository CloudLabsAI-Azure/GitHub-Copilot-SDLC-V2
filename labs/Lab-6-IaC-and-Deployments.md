# Exercise 6 - IaC and Deployments with GitHub Copilot

**Duration**: 30 minutes

## 🎯 Learning Objectives

By the end of this lab, you will be able to:
- Use GitHub Copilot to understand existing Terraform infrastructure code
- Navigate and explore Terraform module structures with AI assistance
- Understand the PR-based deployment workflow for infrastructure changes
- Trigger infrastructure deployments through GitHub Actions
- Verify deployment status and understand the deployment pipeline

## 🏢 Infrastructure Deployment at ShipIt Industries

With that high priority issue out of the way it's time to get back to working on ApproveThis.

Your GitHub provider implementation is tested and ready. Erica now wants to discuss deployment:

> **Erica**: "Great progress on the code! Now let's talk deployment. At ShipIt, we try to manage all IaC using **Terraform**. We try to avoid clicking around in cloud consoles - everything is versioned, reviewed, and automated.
>
> I've already set up Terraform modules for ApproveThis. The deployment process is straightforward: when you open a PR, terraform plan runs automatically. When the PR is merged to main, terraform apply runs to deploy to dev.
>
> Let's walk through how it all works so you can deploy your changes!"

---

> [!IMPORTANT]
> Up to this point the labs have provided example prompts for most exercises to make sure you understand how to interact with Copilot effectively. From here on out, the labs will include fewer example prompts. The goal is to encourage you to think about how to best prompt Copilot for your own needs. 
>
> Not everyone will have the same level of familiarity with the technologies used in this workshop, so the labs will still provide helpful information about what to prompt on and what to look for in the responses, but you will need to take a more active role in crafting your own prompts.
>
> Remember, working with Copilot is an iterative process. If the first response isn't quite what you need, refine your prompt or ask follow-up questions to get closer to your goal.

## Step 1: Understanding the Terraform Structure

Let's use Copilot to understand the existing Terraform setup since we're new to this codebase.

### 1.1 Explore the Module Structure

Let's ask Copilot to explain the overall structure of the Terraform code.

The Terraform code for ApproveThis is located in the `approvethis/terraform/` directory. 

We want to know:

- What modules exist?
- How are they organized?
- What does each module create?

> [!TIP]
> Remember that you can always use Copilot to help you locate files even if you aren't familiar with the repo structure or technologies. There's nothing wrong with having Copilot help you undestand the code enough to ask better questions!

<!-- ```
terraform/
├── modules/
│   ├── azure-function/     # Azure Function App module
│   ├── app-service/        # Azure App Service module  
│   └── storage-account/    # Azure Storage Account module
└── environments/
    ├── dev/                # Development environment
    └── production/         # Production environment
``` -->

### 1.2 Understand the App Service Module

Ok great! We now have a basic understnding of the module structure. Given that the App Service is where the ApproveThis Flask application will be deployed let's dive deeper into that module.

We can have Copilot give us a more in depth explanation of the App Service module. 

We want to know:

- What Azure resources does it create?
- What are the required variables and outputs?

**Key resources created:**
- Azure App Service Plan (compute tier)
- Azure App Service (the web application host)
- Application settings configuration

### 1.3 Compare Environment Configurations

Understanding the differences between dev and production is important for knowing what you're deploying:

Let's have Copilot help us compare the two environment configurations.

**Typical differences:**
- App Service Plan tier (Basic for dev, Premium for prod)
- Number of instances
- Storage redundancy settings

> [!TIP]
> 💡 For detailed Terraform documentation, see [approvethis/terraform/README.md](../approvethis/terraform/README.md) which contains comprehensive information about prerequisites, variables, and deployment options.

## Step 2: Understanding the Deployment Workflow

ShipIt Industries uses a PR-based deployment workflow. Let's understand how it works.

### 2.1 Review the Terraform Workflows

The Terraform process is broken into two main workflows `terraform-plan.yml` and `terraform-apply.yml`.

We need to understand how each workflow works so we can use them effectively.

- When does each workflow trigger?
- What does each workflow do?
- How do they report their results?
- What environment do they target?

Once you've gotten a grasp of the workflows it's time to get ready to deploy!

## Step 3: Triggering a Deployment via PR

Now let's walk through the actual deployment process.

### 3.1 Commit and Push Your Changes

If you have any changes that haven't been committed yet and should be included in the deployment, commit and push them now.

> [!TIP]
> Remember that you can have Copilot help write commit messages for you!
>
> 1. Open the `Source Control panel` (`Ctrl+Shift+G`)
> 2. Click into the **commit message** input box
> 3. Click the **Generate Commit Message** button (similar to ✨) at the end of the input box.

### 3.2 Open a Pull Request

1. Navigate to your repository on GitHub
2. Have Copilot help you draft a PR description that summarizes your changes and their purpose
3. Create the pull request

### 3.3 Watch the Terraform Plan Run

Once your PR is created:

1. Navigate to the **Actions** tab in your repository
2. You should see a "Terraform Plan" workflow running
3. Wait for it to complete
4. Go back to your PR - you'll see a comment with the plan output!

**What to look for in the plan comment:**
- ✅ Format check status
- ✅ Initialization status
- ✅ Validation status
- 📖 The actual plan showing what will be created/modified

### 3.5 Merge the PR to Deploy

> [!IMPORTANT]
> In a real world scenario, you always want to do human code review. Human code reviews are vital to team collaboration, knowledge sharing, and maintaining code quality. Additionally, Copilot is **BLOCKED** from approving PRs by GitHub as a safety feature.

Once you've reviewed the plan output:

1. Get approval from a reviewer (or approve your own PR if permitted)
2. Click "Merge pull request"
3. Navigate to the **Actions** tab
4. Watch the "Terraform Apply" workflow run automatically

> [!IMPORTANT]
> The apply workflow deploys to the `dev` environment. In a real production scenario, production deployments would require additional approvals and potentially a separate workflow trigger.

## Step 4: Verifying the Deployment

After the apply workflow completes, let's verify what was deployed.

### 4.1 Check the Workflow Summary

1. Navigate to the completed "Terraform Apply" workflow run
2. Click on the job to see detailed logs
3. Look for the "Terraform Output" step to see what resources were created

### 4.2 Understanding the Job Execution Framework (Preview)

ApproveThis includes a job execution framework that could be used to trigger Terraform operations from the UI. Ask Copilot about it:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Explain how JobDefinition, JobExecution, and ExecutionTarget models work together in app/models/. How could this framework be used to trigger Terraform operations from the application UI?
```

</details>

This framework will be important in **Lab 8: Capstone** where you'll implement approval workflows for production deployments!

---

## 🏆 Exercise Wrap-Up

Excellent work! You've learned how infrastructure deployment works at ShipIt Industries. Let's review what you accomplished:

### ✅ What You Accomplished

- [x] Explored and understood existing Terraform module structure using Copilot
- [x] Learned how environment configurations differ (dev vs. production)
- [x] Understood the PR-based deployment workflow (plan on PR, apply on merge)
- [x] Identified required secrets and configuration for deployments
- [x] Triggered a Terraform plan by opening a PR
- [x] Deployed infrastructure changes by merging a PR
- [x] Previewed the job execution framework for future UI-triggered deployments

## 🤔 Reflection Questions

Take a moment to consider:

1. How does Copilot help you understand infrastructure code you didn't write?
2. What are the benefits of a PR-based deployment workflow over manual deployments?
3. Why is it important to see the Terraform plan before applying changes?
4. How does separating dev and production environments reduce risk?
5. What additional safeguards might you want for production deployments?

## 🎓 Key Takeaways

- **Copilot for IaC understanding** helps you quickly grasp unfamiliar Terraform structures
- **PR-based deployments** ensure all infrastructure changes are reviewed before applying
- **Terraform plan comments** give reviewers visibility into what will change
- **Automatic triggers** (plan on PR, apply on merge) create a predictable deployment flow
- **Environment separation** (dev/production) prevents accidental production changes
- **Job execution framework** enables future integration of deployments into application workflows

## 🔜 Coming Up Next

In **Lab 7: CI/CD Beyond GitHub Actions**, you'll explore how GitHub Copilot can help with CI/CD across multiple platforms—not just GitHub Actions, but also Azure DevOps Pipelines, Jenkins, and more. You'll see how Copilot's knowledge extends across the entire DevOps ecosystem!

**[← Back to Lab 5](Lab-5-Testing-with-Copilot.md)** | **[Continue to Lab 7: CI/CD Beyond GitHub Actions →](Lab-7-CI-CD-Beyond-GitHub-Actions.md)**
