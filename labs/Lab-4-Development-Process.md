# Exercise 4 - Shifting Our Development Process

**Duration**: 60 minutes

## 🎯 Learning Objectives

By the end of this lab, you will be able to:
- Delegate implementation tasks to GitHub Copilot Coding Agent
- Trigger and manage coding agent tasks from VS Code
- Monitor and steer coding agent progress using Agent Panel and Mission Control
- Use GitHub Copilot Code Review to ensure code quality
- Work iteratively with AI assistance for complex features
- Apply best practices for AI-assisted development with autonomous agents

## 🏢 Implementation Day at ShipIt Industries

Erica reviews your planning work and gives you the green light to start implementing:

> **Erica**: "Great planning! The work items look solid, and I love the detailed acceptance criteria. Now let's build it!
>
> For the GitHub provider, I'd recommend having Copilot help you come up with an implementation plan, and then delegate the implementation to a Copilot Coding Agent. This is a complex task that will touch multiple files, add dependencies, and needs to follow our established patterns—perfect for a coding agent to handle autonomously.
>
> You can trigger the coding agent right from VS Code and monitor its progress in real-time. While it's working, I'll show you some of the cool features like Mission Control and real-time steering.
>
> Oh, and don't forget to request a Copilot Code Review before you open a PR. It catches a lot of issues early."

Let's implement the real GitHub API provider following ShipIt's development workflow!

---

## Step 1: Creating an Implementation Plan with Plan Mode

Before diving into code, let's use Copilot's Plan mode to create a structured implementation approach.

### 1.1 Create a Feature Branch

First, create a feature branch for your implementation work:

```bash
git checkout -b feature/github-provider-implementation
```

### 1.2 Open Copilot Chat in Plan Mode

1. Open the Copilot Chat panel
2. Click the mode selector dropdown at the bottom of the chat
3. Select **Plan** mode

Plan mode is designed to help you think through implementation strategies before writing code. It creates a structured outline that you can review and refine.

### 1.3 Request an Implementation Plan

Ask Copilot to create a detailed implementation plan for the GitHub provider task in ADO:

<details>
<summary>💡 Example planning prompt</summary>

> [!NOTE]
> You need to replace `XXX` with the actual Azure DevOps work item ID for the GitHub provider task.

**Copilot Mode**: `Plan`
```
I need to implement the real GitHub provider. The work item is in Azure DevOps under ID XXX. Please help me create an implementation plan.
```

</details>

### 1.4 Review the Generated Plan

Copilot will generate a structured implementation plan. Review it for:

✅ **Completeness:**
- Does it cover all methods in the `base.py` interface?
- Are dependencies like PyGithub identified?
- Is authentication strategy addressed?

✅ **Correctness:**
- Does the approach align with existing patterns in the codebase?
- Are the steps in a logical order?
- Does it follow the guidelines in `.github/copilot-instructions.md`?

✅ **Feasibility:**
- Are the steps actionable?
- Is the scope appropriate for the task?

### 1.5 Refine the Plan as Needed

If the plan needs adjustments, ask Copilot to refine specific sections:

<details>
<summary>💡 Example refinement prompts</summary>

**Copilot Mode**: `Plan`
```
Can you expand the error handling section to include specific GitHub API error codes we should handle?
```

```
Add a section for caching strategy to minimize API calls and respect rate limits.
```

```
Include steps for updating the configuration to switch between mock and real providers.
```

</details>

## Step 2: Delegating to GitHub Copilot Coding Agent

Now that we have a solid implementation plan from Step 1, it's time to delegate the actual coding work to GitHub Copilot Coding Agent. Unlike the traditional Agent mode in VS Code Chat, the Copilot Coding Agent is an autonomous AI agent that works in a secure cloud environment, handling the implementation while you monitor and steer its progress.

### 2.1 Understanding Copilot Coding Agent

Before we trigger the agent, let's understand what makes it different:

**Traditional Copilot Agent Mode:**
- Runs locally in your VS Code environment
- Requires your machine to stay active
- Works within a single chat session
- Limited to your local compute resources

**Copilot Coding Agent:**
- Runs autonomously in a secure GitHub cloud environment
- Works even when VS Code is closed or your machine is off
- Creates a draft pull request with its changes
- Can be monitored and steered in real-time from multiple interfaces
- Provides detailed session logs and progress tracking

Think of the Coding Agent as a junior developer on your team—you assign it a task with clear instructions, it goes off to work independently, and you can check in on progress or provide guidance as needed.

### 2.2 Prerequisites

Before delegating to the Coding Agent, ensure you have:

1. **GitHub Copilot subscription** (Pro, Business, or Enterprise)
2. **GitHub Pull Requests extension** installed in VS Code
3. **Coding Agent enabled** for your account (check with your admin if unsure)
4. The **implementation plan** from Step 1 still available in your Copilot Chat

> [!TIP]
> To enhance your Coding Agent experience, you can enable the UI integration setting in VS Code:
> ```json
> "githubPullRequests.codingAgent.uiIntegration": true
> ```
> This adds helpful buttons and UI elements for delegating tasks to the Coding Agent.

### 2.3 Delegating the Task to Coding Agent

There are several ways to trigger a Coding Agent task from VS Code. We'll use the method that leverages the plan we created:

#### Option 1: Delegate from Copilot Chat (Recommended)

1. **Ensure your implementation plan from Step 1 is visible** in the Copilot Chat panel. If you closed it, you can retrieve it by asking Copilot to show the previous plan.

2. **Open Copilot Chat** and compose a delegation prompt that includes the plan context:

<details>
<summary>💡 Example delegation prompt</summary>

```
I need you to implement the GitHub provider based on the implementation plan we created. Please work as a Coding Agent to:

1. Implement all the methods from the plan
2. Add the PyGithub dependency
3. Include proper error handling and rate limiting
4. Follow the patterns in the existing codebase
5. Update configuration as needed

Use the detailed implementation plan we created earlier as your guide. Create a draft pull request when you're done.
```

</details>

3. **Look for the "Delegate to Coding Agent" button** that appears in the Copilot Chat response (if you have the UI integration enabled), or explicitly request that Copilot work as a Coding Agent.

4. **Confirm the delegation** when prompted. The Coding Agent will:
   - Create a new branch for the work
   - Begin implementing the changes in the cloud environment
   - Open a draft pull request to track progress

#### Option 2: Assign an Issue to Copilot

If you created a GitHub issue for this task:

1. Open the **GitHub Pull Requests & Issues** view in VS Code
2. Find the issue for the GitHub provider implementation
3. Right-click and select **Assign to Copilot**
4. The Coding Agent will pick up the issue and start working

### 2.4 Monitoring Progress with the Agent Panel

Once you've delegated the task, the Coding Agent starts working independently. You can monitor its progress without keeping VS Code open!

**In VS Code:**

1. Open the **Pull Requests** view in the left sidebar
2. Look for the **"Copilot on My Behalf"** section
3. You'll see your active Coding Agent task listed with:
   - Current status (Working, Completed, Failed)
   - The branch name
   - Time elapsed
   - Number of files changed

4. **Click on the task** to see:
   - Real-time session logs showing what the agent is doing
   - Files being modified
   - Build and test results
   - Agent's reasoning and decision-making process

> [!TIP]
> The Agent Panel provides a "session replay" view—you can see each action the agent takes as it works through the implementation plan. This transparency helps you understand and trust the agent's decisions.

### 2.5 Exploring Mission Control on GitHub.com

While the Coding Agent is working, let's explore **Mission Control**—GitHub's centralized dashboard for managing all your AI coding agent tasks. This is where the real power of autonomous agents shines!

#### Accessing Mission Control

1. **Navigate to GitHub.com** in your browser
2. Go directly to **[github.com/copilot/agents](https://github.com/copilot/agents)** or click on **Copilot** in the top navigation
3. Look for the **"Agents"** or **"Mission Control"** section in the navigation

Alternatively, you can access agent tasks from the GitHub interface by looking for the agents or task management options in the Copilot menu.

#### Understanding the Mission Control Dashboard

Mission Control provides a **unified, real-time dashboard** for all your Copilot Coding Agent tasks:

**Key Features:**

1. **Task Overview**
   - See all active, completed, and failed agent sessions
   - View status indicators for each task at a glance
   - Quickly jump between multiple agent sessions

2. **Session Details**
   - Click any task to see detailed information:
     - Session logs and agent reasoning
     - Files changed with inline diffs
     - Build and test results
     - Timeline of agent actions
     - Associated pull request

3. **Task Switcher**
   - Easily switch between multiple agent tasks
   - Filter by status (active, completed, failed)
   - See which tasks need your attention

4. **Quick Actions**
   - Open in VS Code
   - Open in Codespaces
   - View pull request
   - Provide feedback to the agent

**Why Mission Control Matters:**

- **No more tab juggling**: Everything you need is in one place—no hunting through issues, PRs, and comments
- **Multi-repository view**: See agent tasks across all your repositories
- **Historical tracking**: Review past agent sessions to learn from their approach
- **Team visibility**: See what coding agents are working on across your team

> [!NOTE]
> Mission Control is especially powerful when running multiple coding agent tasks in parallel. You can delegate several independent tasks (e.g., "add tests," "update documentation," "refactor module X") and monitor them all from one dashboard.

### 2.6 Real-Time Steering: Guiding Your Coding Agent

One of the most powerful features of Copilot Coding Agent is **real-time steering**—the ability to provide guidance while the agent is actively working, not just after it completes.

#### How Real-Time Steering Works

Unlike traditional asynchronous feedback (leaving PR comments after work is done), you can interact with the Coding Agent while it's working:

**From VS Code:**

1. **Open your Coding Agent task** in the Pull Requests view
2. **Look at the Files Changed view** to see what the agent is modifying
3. **Add comments directly in the diff** if you notice issues or want to suggest changes
4. The agent will **see your feedback and adapt** as soon as its current tool call completes

**From Mission Control:**

1. **Navigate to your active agent session** in Mission Control
2. **Use the chat input** at the bottom of the session view
3. **Send messages to the agent** like:
   - "Make sure to add comprehensive error handling"
   - "Use the logging pattern from utils.py"
   - "Don't forget to update the configuration file"
4. The agent incorporates your feedback in real-time

**Example Steering Scenarios:**

- **Course Correction**: "I see you're using library X, but we prefer library Y for this purpose"
- **Additional Requirements**: "Also add caching to minimize API calls"
- **Style Preferences**: "Please use type hints for all function parameters"
- **Priority Shifts**: "Focus on getting the basic implementation working first, skip the advanced features for now"

> [!IMPORTANT]
> Real-time steering makes the human-AI collaboration truly iterative. You don't need to wait for the agent to finish, review everything, and request changes—you can guide the work as it happens, saving significant time.

#### Best Practices for Steering

- **Be specific**: Vague feedback like "this doesn't look right" is less helpful than "use async/await for the API calls"
- **Provide context**: Reference specific files, functions, or patterns in the codebase
- **Intervene early**: If you see the agent going down the wrong path, steer it immediately
- **Trust but verify**: The agent is capable, but your domain knowledge is valuable

### 2.7 Reviewing the Coding Agent's Work

Once the Coding Agent completes its task (or you decide it's made enough progress), it's time to review the pull request.

#### Where to Review

**Option 1: In VS Code**

1. Go to the **Pull Requests** view
2. Click on your Coding Agent's draft PR
3. Review the changes with VS Code's built-in diff viewer
4. Test the implementation locally by checking out the branch

**Option 2: On GitHub.com**

1. Navigate to the pull request in your repository
2. Review the **Files Changed** tab
3. Check the **Session Logs** to understand the agent's decision-making
4. Look at any automated checks or tests

#### What to Check For

✅ **Correctness:**
- Does it implement all methods from the plan?
- Are the dependencies correctly added to `requirements.txt`?
- Is the authentication strategy implemented as planned?

✅ **Code Quality:**
- Proper error handling with try/except blocks
- Rate limiting awareness for API calls
- Consistent with existing code patterns
- Appropriate logging

✅ **Completeness:**
- All files mentioned in the plan are updated
- Configuration is updated correctly
- No obvious missing pieces

> [!IMPORTANT]
> Even though the Coding Agent is highly capable, you are still responsible for the final code quality. Always review carefully before merging—the agent is a powerful assistant, not a replacement for human judgment.

### 2.8 Testing the Implementation

Let's test the GitHub provider implementation to ensure it works correctly:

1. **Check out the agent's branch** in VS Code:
   ```bash
   git fetch
   git checkout <agent-branch-name>
   ```

2. **Install any new dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your GitHub token** according to the implementation:
   ```bash
   export GITHUB_TOKEN="your-token-here"
   ```

4. **Run the application** and test the GitHub provider:
   - Start the application
   - Navigate to the repository listing section
   - Verify repositories load from your GitHub account
   - Test workflow listing and other features

5. **Check the logs** for any errors or warnings

> [!TIP]
> If you encounter issues during testing, you can provide feedback to the agent in the PR comments or steer it to make corrections. You can also make small fixes yourself—the agent's work is a starting point, and you can iterate on it just like you would with code from any team member.

### 2.9 Iterating with the Coding Agent

If the initial implementation needs adjustments:

1. **Provide feedback in the PR**: Leave comments on specific lines or overall feedback
2. **Request changes via chat**: In Mission Control or VS Code, tell the agent what needs to change
3. **Let the agent iterate**: It can make additional commits to address your feedback
4. **Alternatively, make small fixes yourself**: For minor issues, it may be faster to make the change directly

The beauty of the Coding Agent is that it can iterate just like a human developer—you provide feedback, it makes adjustments, and you review again.

## Step 3: Documenting Changes

One of the areas where Copilot really shines is in generating documentation. Historically this has been a tedious task that many developers skip or do poorly. However, with Copilot we can generate high quality documentation quickly and easily.

> [!NOTE]
> If the Coding Agent hasn't completed yet or you want to iterate on the documentation separately, you can handle this step in parallel or after the agent finishes. You can also request the Coding Agent to include comprehensive documentation as part of its implementation task.

### 3.1 Generate Docstrings

You can ask the Coding Agent to add docstrings, or add them yourself with Copilot's help in Chat:

<details>
<summary>💡 Example prompt for Coding Agent (via real-time steering)</summary>

```
Please add comprehensive docstrings to all methods in the GitHub provider following Google style guide format. Include parameters, return types, exceptions raised, and usage examples.
```

</details>

<details>
<summary>💡 Example prompt in Copilot Chat (if doing manually)</summary>

**Copilot Mode**: `Chat` or `Edit`
```
Add comprehensive docstrings to all methods in app/providers/github.py following Google style guide format. Include parameters, return types, exceptions raised, and usage examples.
```

</details>

### 3.2 Create API Documentation

Generate user-facing documentation:

<details>
<summary>💡 Example prompt for Coding Agent (via real-time steering)</summary>

```
Create API documentation for the GitHub provider in Markdown format. Include:
- Overview of functionality
- Configuration requirements (environment variables)
- Available methods with parameters  
- Example usage
- Error handling information
- Rate limiting considerations
Save this as docs/GitHub-Provider-API.md
```

</details>

<details>
<summary>💡 Example prompt in Copilot Chat (if doing manually)</summary>

**Copilot Mode**: `Chat`
```
Create API documentation for the GitHub provider in Markdown format. Include:
- Overview of functionality
- Configuration requirements (environment variables)
- Available methods with parameters  
- Example usage
- Error handling information
- Rate limiting considerations
Save this as docs/GitHub-Provider-API.md
```

</details>

> [!TIP]
> Documentation is a great candidate for parallel work. While the Coding Agent handles the core implementation, you can work on documentation, write tests, or handle other tasks. This is one advantage of autonomous agents—they free you up to multitask effectively.

## Step 4: GitHub Copilot Code Review

Now that the Coding Agent has completed its work (or you've made additional changes), it's time to get a code review before we finalize everything.

### 4.1 Request a Code Review

GitHub Copilot can perform an automated code review on the pull request created by the Coding Agent, or on any uncommitted changes you've made.

**For the Coding Agent's Pull Request:**

1. Navigate to the **Pull Requests** view in VS Code
2. Open the draft PR created by the Coding Agent
3. Click the **Request Copilot Review** button in the PR view
4. Copilot will analyze the entire PR and provide feedback

**For Uncommitted Changes:**

1. Open the Source Control panel (`Ctrl+Shift+G`)
2. Click the **Code Review** button at the top of the panel on the `CHANGES` section. The button looks like a message box with `<>` in it.
3. This will trigger Copilot to analyze your uncommitted changes and provide feedback through inline comments in the diff view

> [!NOTE]
> The Coding Agent may have already performed self-review during its implementation. However, getting an additional Copilot review with fresh context can catch issues the agent might have missed.

### 4.2 Apply Suggested Improvements

Review Copilot's suggestions and apply the ones that make sense and deny/reject those that don't:

**Common review suggestions might include:**
- Adding error handling for edge cases
- Improving variable or function names for clarity
- Adding type hints or additional documentation
- Addressing potential security vulnerabilities
- Optimizing performance-critical sections
- Ensuring consistent code style with the rest of the codebase

> [!TIP]
> If the Coding Agent is still active, you can provide review feedback directly to it via real-time steering, and it will make the necessary corrections. Otherwise, you can make the changes yourself or request them as PR comments.

## Step 5: Finishing Up

Now that we've reviewed the Coding Agent's implementation, tested it, documented it, and had Copilot review the code, it's time to finalize our work.

### 5.1 Merge or Update the Coding Agent's PR

Depending on your workflow, you have several options:

**Option 1: Merge the Coding Agent's PR as-is**
- If all tests pass and the code review looks good, you can merge the agent's PR directly
- The agent created a proper branch and PR, just like a human team member would

**Option 2: Make Additional Changes**
- Check out the agent's branch locally
- Make any final tweaks or improvements
- Commit your changes to the same branch
- The PR will automatically update

**Option 3: Continue with the Draft**
- Keep the PR as a draft if you want to add more features
- Continue iterating with the Coding Agent or make changes yourself

### 5.2 Generating Commit Messages

If you're making additional commits on top of the Coding Agent's work, Copilot can help you create detailed commit messages that follow best practices.

To have Copilot generate a commit message for your changes:

1. Open the `Source Control panel` (`Ctrl+Shift+G`)
2. Stage your changes
3. Click into the **commit message** input box
4. Click the **Generate Commit Message** button (sparkle icon ✨) at the end of the input box
5. Review and edit the generated message as needed

### 5.3 Sync Our Changes

For this lab, we'll keep the PR as a draft and not merge it yet. We'll be working with PRs in a later lab where we'll explore the full code review and approval process.

1. **Ensure all your changes are committed** to the feature branch (either the agent's branch or your own)
2. **Push the branch** if you made local changes:
   ```bash
   git push
   ```
3. **Verify the PR is updated** on GitHub.com

> [!NOTE]
> The Coding Agent's PR is already on GitHub since it works in the cloud. You only need to push if you made additional local changes on top of the agent's work.

---

## 🏆 Exercise Wrap-Up

Excellent work! You've experienced how AI transforms the development phase of the SDLC. Let's review what you accomplished:

### ✅ What You Accomplished

- [x] Created a detailed implementation plan using Plan mode
- [x] Delegated complex implementation work to GitHub Copilot Coding Agent
- [x] Monitored autonomous agent progress using the Agent Panel in VS Code
- [x] Explored Mission Control for centralized agent task management
- [x] Used real-time steering to guide the coding agent while it worked
- [x] Performed comprehensive code review with Copilot assistance
- [x] Tested and validated the agent's implementation
- [x] Learned to work with autonomous AI agents as team members
- [x] Generated documentation and commit messages with AI assistance

## 🤔 Reflection Questions

Take a moment to consider:

1. How does delegating to an autonomous Coding Agent change your development workflow compared to traditional coding?
2. What types of tasks are best suited for Coding Agents vs. tasks you should handle yourself?
3. How did real-time steering improve your ability to guide the agent's work?
4. What value does Mission Control provide when managing multiple agent tasks?
5. How would you integrate Coding Agents into your team's workflow? What guidelines would you establish?
6. What surprised you most about the Coding Agent's capabilities or limitations?

## 🎓 Key Takeaways

- **Copilot Coding Agent** works autonomously in the cloud, enabling true delegation of development tasks
- **Mission Control** provides centralized visibility and management for all AI coding agent tasks
- **Real-time steering** allows you to guide agents as they work, not just after completion
- **Agent Panel** in VS Code integrates agent task management directly into your IDE
- **Autonomous agents** can handle complex, multi-file tasks while you focus on architecture and review
- **Transparency and trust** come from detailed session logs showing agent reasoning and decisions
- **Human oversight remains critical**—agents are powerful assistants, not replacements for developer judgment
- **Parallel task execution** enables unprecedented productivity by running multiple agent tasks simultaneously
- **Governance policies** (from `.github/copilot-instructions.md`) ensure agents follow team standards automatically

## Coming Up Next

In **Lab 5: Testing Isn't an Afterthought Anymore**, you'll discover how GitHub Copilot transforms testing from a chore into an integrated part of development. You'll generate comprehensive unit tests, implement end-to-end testing with Playwright, and see how AI can identify edge cases you might miss. Building on the GitHub provider implementation from this lab, you'll achieve better test coverage in less time!

**[← Back to Lab 3](Lab-3-Planning-with-MCP.md)** | **[Continue to Lab 5: Testing with Copilot →](Lab-5-Testing-with-Copilot.md)**
