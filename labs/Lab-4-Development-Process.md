# Exercise 4 - Shifting Our Development Process

**Duration**: 60 minutes

## 🎯 Learning Objectives

By the end of this lab, you will be able to:
- Implement new functionality using Copilot Edit and Agent modes effectively
- Understand when to use Edit mode vs. Agent mode
- Apply multitasking strategies with GitHub Copilot
- Use GitHub Copilot Code Review to ensure code quality
- Work iteratively with AI assistance for complex features
- Apply best practices for AI-assisted development

## 📸 Scenario: Implementation Day at ShipIt Industries

🏢 It's implementation day! You've planned your work in Azure DevOps, and now it's time to start coding. Your manager has given you the green light to implement the real GitHub provider integration—the feature that will replace mock data with live information from GitHub.

However, as you're working, a urgent bug report comes in: "Users are seeing an error when trying to view workflows for empty repositories." You'll need to handle this interruption while staying focused on your main feature implementation.

This is where **GitHub Copilot's advanced modes** shine. You'll use:
- **Agent mode** to explore and implement the GitHub provider autonomously  
- **Edit mode** to make targeted bug fixes without losing context
- **Code Review** to ensure quality before committing

Let's see how AI transforms the development phase of the SDLC!

---

## Step 1: Understanding Copilot Modes

Before diving into implementation, let's clarify when to use each mode.

### 1.1 Copilot Mode Comparison

| Mode | Best For | Level of Control | Scope |
|------|----------|------------------|-------|
| **Ask** 💬 | Understanding code, asking questions | Read-only | Information gathering |
| **Edit** ✏️ | Targeted changes to specific files | High control | Single/few files |
| **Agent** 🤖 | Complex features, exploration | Autonomous | Multi-file, codebase-wide |
| **Plan** 📋 | Previewing changes before applying | Review before execution | Variable |

### 1.2 When to Use Edit vs. Agent

**Use Edit Mode when:**
- You know exactly which file(s) need changes
- Making focused refactoring or bug fixes
- Want precise control over what gets modified
- Working with a small, well-defined scope

**Use Agent Mode when:**
- Implementing a new feature across multiple files
- Not sure which files need changes
- Want Copilot to explore and make architectural decisions
- Comfortable with autonomous multi-file modifications

> [!TIP]
> 💡 Think of Edit mode as a precise scalpel, and Agent mode as an autonomous surgical team. Both have their place!

---

## Step 2: Implementing the GitHub Provider with Agent Mode

Let's implement the real GitHub provider using Agent mode.

### 2.1 Start Agent Mode Implementation

Open Copilot Chat in Agent mode and provide clear instructions:

<details>
<summary>💡 Example prompt for Agent mode</summary>

```
@workspace I need to implement the real GitHub provider in app/providers/github.py. 

Requirements:
1. Replace all NotImplementedError methods with working implementations
2. Use PyGithub library for GitHub API access
3. Follow the interface defined in app/providers/base.py
4. Include rate limiting and error handling per .github/copilot-instructions.md
5. Get GitHub token from GITHUB_TOKEN environment variable
6. Add appropriate logging for debugging

Start with implementing list_repositories() and list_workflows(). Make sure to handle authentication properly.
```

</details>

**What Agent Mode Will Do:**
- Analyze the `base.py` interface
- Review the `.github/copilot-instructions.md` policies
- Implement the methods with proper error handling
- Add imports for PyGithub
- Include logging statements
- Potentially update `requirements.txt` if needed

### 2.2 Review Agent's Proposed Changes

Agent mode will show you the changes it plans to make. Review them carefully:

✅ **Check for:**
- Correct imports (`from github import Github`)
- Environment variable usage (`os.getenv('GITHUB_TOKEN')`)
- Error handling with try/except blocks
- Rate limiting awareness
- Proper logging
- Adherence to the base class interface

> [!IMPORTANT]
> Always review Agent mode's changes before accepting them. While highly capable, AI can make mistakes or misunderstand requirements.

### 2.3 Accept and Test Changes

If the changes look good, accept them. Then test the implementation:

1. Update `requirements.txt` if PyGithub wasn't added:
```bash
pip install PyGithub
```

2. Set your GitHub token:
```bash
export GITHUB_TOKEN=your_github_personal_access_token
```

3. Update the application configuration to use the real provider (if needed)

4. Test in Python console:
```python
from app.providers.github import RealGitHubProvider

provider = RealGitHubProvider()
repos = provider.list_repositories()
print(repos)
```

### 2.4 Handle Installation of Dependencies

If Agent mode updated `requirements.txt`, install the new dependencies:

```bash
pip install -r requirements.txt
```

> [!NOTE]
> Agent mode understands dependency management and will often add required packages to `requirements.txt` automatically.

---

## Step 3: Using Edit Mode for Targeted Changes

Now let's handle that urgent bug report using Edit mode.

### 3.1 Understand the Bug

The bug report states: "Users are seeing an error when trying to view workflows for empty repositories."

Open Copilot Chat in Edit mode and investigate:

<details>
<summary>💡 Example prompt for Edit mode</summary>

```
@workspace In Edit mode: Find where workflows are retrieved and displayed in the application. Add error handling for repositories that have no workflows. The specific files that likely need changes are in app/blueprints/main/routes.py.
```

</details>

### 3.2 Apply Targeted Fix

Edit mode will show you the specific changes needed. For example, adding a check:

```python
@main.route('/workflows/<owner>/<repo>')
@login_required
def workflows(owner, repo):
    provider = get_github_provider()
    try:
        workflows = provider.list_workflows(owner, repo)
        if not workflows:
            flash('This repository has no workflows configured.', 'info')
            workflows = []
    except Exception as e:
        flash(f'Error retrieving workflows: {str(e)}', 'error')
        workflows = []
    
    return render_template('workflows.html', workflows=workflows, owner=owner, repo=repo)
```

**Benefits of Edit Mode:**
- You specified the exact file to modify
- Changes are surgical and focused
- Easy to review the diff
- Doesn't touch unrelated code

### 3.3 Verify the Fix

Test the bug fix:

1. Navigate to a repository with no workflows
2. Verify the friendly message appears instead of an error
3. Confirm the page still works for repositories with workflows

---

## Step 4: Multitasking with Copilot

Let's demonstrate how to switch contexts seamlessly with Copilot.

### 4.1 Start a Feature in Agent Mode

Begin implementing another provider method:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Implement the list_workflow_runs() method in app/providers/github.py. Include pagination support for repositories with many runs.
```

</details>

### 4.2 Pause for Context Switch

While Agent is working (or you're reviewing its suggestions), a colleague asks you to quickly fix a typo in the README.

**Switch to Edit mode** without losing your Agent context:

<details>
<summary>💡 Example prompt in Edit mode</summary>

```
In Edit mode: Fix the typo in README.md line 42 where "mananagement" should be "management"
```

</details>

### 4.3 Return to Original Context

After fixing the typo, return to Agent mode's conversation thread and continue reviewing the `list_workflow_runs()` implementation.

> [!TIP]
> 💡 Copilot maintains separate conversation contexts for Ask, Edit, and Agent modes. You can switch between them without losing your place!

---

## Step 5: GitHub Copilot Code Review

Before committing your changes, use Copilot to review them.

### 5.1 Request a General Code Review

Ask Copilot to review your implementation:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Review the changes I made to app/providers/github.py. Check for:
- Security issues (token handling, injection risks)
- Error handling completeness
- Performance concerns
- Adherence to Python best practices
- Missing edge cases
```

</details>

### 5.2 Security-Focused Review

Request a specific security review:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Perform a security review of the GitHub provider implementation. Focus on:
- Authentication token storage and usage
- Input validation
- Potential for API abuse or rate limit violations
- Logging of sensitive information
```

</details>

**Common issues Copilot might find:**
- Token logged in error messages
- Missing input validation on owner/repo parameters
- No rate limit handling for bulk operations
- Potential for injection if user input reaches API calls

### 5.3 Performance Review

Ask for performance optimization suggestions:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Review app/providers/github.py for performance optimization opportunities. Suggest improvements for:
- API call efficiency
- Caching strategies  
- Batch operations
- Connection pooling
```

</details>

### 5.4 Apply Suggested Improvements

Review Copilot's suggestions and apply the ones that make sense:

**Example improvements:**
```python
from functools import lru_cache
from datetime import datetime, timedelta

class RealGitHubProvider(GitHubProvider):
    def __init__(self, token=None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self._github = None
        self._cache_timestamp = None
        self._cache_duration = timedelta(minutes=5)
    
    @property
    def github(self):
        """Lazy-load GitHub client."""
        if self._github is None:
            self._github = Github(self.token)
        return self._github
    
    @lru_cache(maxsize=100)
    def list_repositories(self):
        """List repositories with caching."""
        # ... implementation
```

---

## Step 6: Iterative Development with Feedback

Let's practice iterative development using Copilot feedback.

### 6.1 Implement Initial Version

Start with a basic implementation:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Implement dispatch_workflow() in app/providers/github.py with basic functionality
```

</details>

### 6.2 Test and Get Feedback

Test the implementation and note issues:
- What if the workflow file doesn't exist?
- What if the ref (branch) is invalid?
- How do we know if the dispatch succeeded?

### 6.3 Refine Based on Feedback

Ask Copilot to improve based on test findings:

<details>
<summary>💡 Example prompt</summary>

```
@workspace The dispatch_workflow() implementation needs improvements:
1. Validate that the workflow file exists before dispatching
2. Validate that the ref exists in the repository  
3. Return more detailed success/failure information
4. Handle GitHub API errors gracefully
Update the implementation with these enhancements.
```

</details>

### 6.4 Add Comprehensive Error Handling

Continue iterating:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Add comprehensive error handling to dispatch_workflow() for these scenarios:
- Invalid authentication token
- Repository not found or no access
- Workflow file doesn't exist
- Invalid ref (branch/tag)
- Workflow doesn't support workflow_dispatch event
- Rate limit exceeded
Each error should have a specific, helpful error message.
```

</details>

---

## Step 7: Documenting Changes

Use Copilot to generate documentation for your implementation.

### 7.1 Generate Docstrings

Ask Copilot to add comprehensive docstrings:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Add comprehensive docstrings to all methods in app/providers/github.py following Google style guide format. Include parameters, return types, exceptions raised, and usage examples.
```

</details>

### 7.2 Create API Documentation

Generate user-facing documentation:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create API documentation for the GitHub provider in Markdown format. Include:
- Overview of functionality
- Configuration requirements (environment variables)
- Available methods with parameters  
- Example usage
- Error handling information
- Rate limiting considerations
Save this as docs/GitHub-Provider-API.md
```

</details>

### 7.3 Generate Commit Message

Use Copilot to craft a detailed commit message:

<details>
<summary>💡 Example prompt</summary>

```
Generate a detailed commit message for the GitHub provider implementation following Conventional Commits format. Include the Azure DevOps work item link.
```

</details>

**Example output:**
```
feat(providers): implement real GitHub API provider

- Implemented all methods from GitHubProvider interface
- Added rate limiting with exponential backoff
- Included comprehensive error handling and logging
- Environment-based authentication via GITHUB_TOKEN
- Added caching for frequently accessed data
- Updated requirements.txt with PyGithub dependency

Breaking changes: None
Testing: Manual testing against live GitHub API

Resolves AB#123, AB#124, AB#125
```

---

## 🏆 Exercise Wrap-Up

Excellent work! You've experienced how AI transforms the development phase of the SDLC. Let's review what you accomplished:

### ✅ What You Accomplished

- [x] Implemented the real GitHub provider using Agent mode
- [x] Fixed an urgent bug using Edit mode with surgical precision
- [x] Demonstrated multitasking by switching between contexts seamlessly
- [x] Performed comprehensive code review with Copilot assistance
- [x] Applied security, performance, and quality improvements
- [x] Iterated on implementation based on testing and feedback
- [x] Generated documentation and commit messages with AI assistance

---

## 🤔 Reflection Questions

Take a moment to consider:

1. How did using Agent mode vs. Edit mode change your development workflow?
2. What types of issues did Copilot Code Review catch that you might have missed?
3. How did the ability to multitask (switch contexts) improve your productivity?
4. In what scenarios would you prefer manual implementation over AI assistance?
5. How can you integrate these AI-assisted development practices into your team's workflow?

---

## 🎓 Key Takeaways

- **Agent mode** excels at complex, multi-file features where exploration is needed
- **Edit mode** provides precision for targeted changes to specific files
- **Context switching** between modes maintains productivity during interruptions
- **AI code review** catches security, performance, and quality issues systematically
- **Iterative development** with AI feedback improves code quality incrementally
- **Documentation generation** saves time while maintaining consistency
- **Governance policies** (from `.github/copilot-instructions.md`) ensure standards compliance automatically

---

## 🔜 Coming Up Next

In **Lab 5: Testing Isn't an Afterthought Anymore**, you'll discover how GitHub Copilot transforms testing from a chore into an integrated part of development. You'll generate comprehensive unit tests, implement end-to-end testing with Playwright, and see how AI can identify edge cases you might miss. Get ready to achieve better test coverage in less time!

---

**[← Back to Lab 3](Lab-3-Planning-with-MCP.md)** | **[Continue to Lab 5: Testing with Copilot →](Lab-5-Testing-with-Copilot.md)**
