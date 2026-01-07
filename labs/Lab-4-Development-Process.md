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

## 🏢 Implementation Day at ShipIt Industries

Erica reviews your planning work and gives you the green light to start implementing:

> **Erica**: "Great planning! The work items look solid, and I love the detailed acceptance criteria. Now let's build it!
>
> For the GitHub provider, I'd recommend having Copilot help you come up with an implementation plan, and then execute it using Agent mode. It will likely need to touch the provider file, add dependencies, potentially update config, and follow our established patterns so Agent mode makes the most sense.
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

## Step 2: Implementing the GitHub Provider with Agent Mode

Let's implement the real GitHub provider using Agent mode.

### 2.1 Start Agent Mode Implementation

 There are 2 main ways to have Copilot implement the plan we just created:

 1. While still in Plan mode, you can click the `Start Implementation` button at the bottom left of the chat panel. This will switch you to Agent mode and insert a minimal prompt telling Copilot to implement the plan. All you need to do next is submit the prompt.
 2. Alternatively, you can manually switch to Agent mode using the mode selector dropdown at the bottom of the chat panel. Then instruct Copilot to implement the GitHub provider based on the plan you created.

Either method will get the job done. Whether you click to start implementation or manually switch to Agent mode, you can supply additional prompt context to guide Copilot if necessary.

At this point you should have submitted your prompt to Agent mode and Copilot should now be working on the implementation. **If you haven't done so yet, do that now.**

### 2.2 Review Agent's Proposed Changes

Since we had Copilot create a plan for us before we startedthe implementation, Agent mode should have a solid understanding of what to do. 

**However**, just like with any code written by another individual (human or AI), it's critical to review the proposed changes carefully before accepting them.

✅ **Check for:**
- Correct imports (I.e. `from github import Github`)
- Environment variable usage (`os.getenv('GITHUB_TOKEN')`)
- Error handling with try/except blocks
- Rate limiting awareness
- Proper logging
- Adherence to the base class interface

> [!IMPORTANT]
> Always review Agent mode's changes before accepting them. While highly capable, AI can make mistakes or misunderstand requirements.

### 2.3 Accept and Prep Changes

If the changes look good, accept them. Then, let's get ready to test the implementation:

1. Update `requirements.txt` if new dependencies weren't added:

> [!NOTE]
> Copilot understands dependency management and will often add required packages to `requirements.txt` automatically.

2. Set your GitHub token according to the authentication strategy defined in the plan:

3. Update the application configuration to use the real provider (if needed)

### 2.4 Handle Installation of Dependencies

If Agent mode updated `requirements.txt`, install the new dependencies:

```bash
pip install -r requirements.txt
```

### 2.5 Test the Implementation

Now that our changes are accepted and dependencies are installed, let's test the GitHub provider:

1. If your application is not running, start it.
2. Navigate to the section of the app that lists GitHub repositories.
3. Verify that repositories are listed correctly from your GitHub account.
4. Test other functionalities like listing workflows for the repositories.

> [!IMPORTANT]
> If you encounter issues while testing and don't immediately know what's wrong, your first step should be to enlist the help of Copilot in debugging what is going. Copilot is often significantly faster at diagnosing issues than manual debugging or searching for the Stack Overflow post that addresses your problem.
>
> Remember, since Copilot is directly integrated into your IDE, it has context about your codebase as well as access to the terminal running your code. This is a very powerful tool at your disposal for diagnosing and fixing issues quickly.

## Step 3: Documenting Changes

One of the areas were Copilot really shines is in generating documentation. Historically this has been a tedious task that many developers skip or do poorly. However, with Copilot we can generate high quality documentation quickly and easily.

### 3.1 Generate Docstrings

Ask Copilot to add comprehensive docstrings:

<details>
<summary>💡 Example prompt</summary>

**Copilot Mode**: `Agent`
```
Add comprehensive docstrings to all methods in app/providers/github.py following Google style guide format. Include parameters, return types, exceptions raised, and usage examples.
```

</details>

### 3.2 Create API Documentation

Generate user-facing documentation:

<details>
<summary>💡 Example prompt</summary>

**Copilot Mode**: `Agent`
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

## Step 4: GitHub Copilot Code Review

Now that we've tested our changes and verified that they work, we should get that committed to our feature branch. 

Before committing your changes though, let's have Copilot do a code review on them to make sure we didn't miss anything.

### 4.1 Request a Code Review

To request a Code Review from Copilot on our uncommitted changes we need to do the following:

1. Open the Source Control panel (`Ctrl+Shift+G`)
2. Click the **Code Review** button at the top of the panel on the `CHANGES` section. The button looks like a message box with `<>` in it.
3. This will trigger Copilot to analyze your uncommitted changes and provide feedback through in line comments in the diff view. These comments will include an explanation of what it thinks the issue is along with suggested improvements.

### 4.2 Apply Suggested Improvements

Review Copilot's suggestions and apply the ones that make sense and deny/reject those that don't:

# TODO take a screenshot of code review suggestions and include it here
**Example improvements:**

## Step 5: Finishing Up

Now that we've implemented the GitHub provider, tested it, documented it, and had Copilot review our code, it's time to finalize our work.

### 5.1 Generating Commit Messages

Copilot can help you to create detailed commit messages that follow best practices. While you always want to review and potentially edit the generated commit message, this can save you a lot of time and help ensure consistency.

To have Copilot generate a commit message for your changes:

1. Open the `Source Control panel` (`Ctrl+Shift+G`)
2. Click into the **commit message** input box
3. Click the **Generate Commit Message** button (similar to ✨) at the end of the input box.

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

### 5.2 Sync Our Changes

We need to commit our changes to our feature branch and push them up to the repo. 

We do not want to open a Pull request yet. We will be doing this in a later lab.

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

## 🤔 Reflection Questions

Take a moment to consider:

1. How did using Agent mode vs. Edit mode change your development workflow?
2. What types of issues did Copilot Code Review catch that you might have missed?
3. How did the ability to multitask (switch contexts) improve your productivity?
4. In what scenarios would you prefer manual implementation over AI assistance?
5. How can you integrate these AI-assisted development practices into your team's workflow?

## 🎓 Key Takeaways

- **Agent mode** excels at complex, multi-file features where exploration is needed
- **Edit mode** provides precision for targeted changes to specific files
- **Context switching** between modes maintains productivity during interruptions
- **AI code review** catches security, performance, and quality issues systematically
- **Iterative development** with AI feedback improves code quality incrementally
- **Documentation generation** saves time while maintaining consistency
- **Governance policies** (from `.github/copilot-instructions.md`) ensure standards compliance automatically

## Coming Up Next

In **Lab 5: Testing Isn't an Afterthought Anymore**, you'll discover how GitHub Copilot transforms testing from a chore into an integrated part of development. You'll generate comprehensive unit tests, implement end-to-end testing with Playwright, and see how AI can identify edge cases you might miss. Get ready to achieve better test coverage in less time!

**[← Back to Lab 3](Lab-3-Planning-with-MCP.md)** | **[Continue to Lab 5: Testing with Copilot →](Lab-5-Testing-with-Copilot.md)**
