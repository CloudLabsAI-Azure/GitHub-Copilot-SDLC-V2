# Exercise 5 - Testing Isn't an Afterthought Anymore

**Duration**: 30 minutes

## 🎯 Learning Objectives

By the end of this lab, you will be able to:
- Use GitHub Copilot to generate comprehensive test suites
- Set up and configure Playwright for end-to-end (E2E) testing with Flask
- Implement unit tests for models, providers, and routes
- Create E2E tests that validate complete user workflows
- Understand AI-assisted test-driven development (TDD)
- Identify edge cases and negative test scenarios with Copilot

## 📸 Scenario: Quality Gates at ShipIt Industries

🏢 Your manager at ShipIt Industries reviews your GitHub provider implementation and is impressed! However, she has one concern:

> "This looks great, but where are the tests? We require at least 80% test coverage for all new code. Also, since ApproveThis handles critical deployment approvals, we need end-to-end tests to ensure the entire workflow functions correctly."

She continues:

> "The previous developer left almost no tests. We need comprehensive test coverage before we can deploy this to production. Can you get that done quickly?"

With GitHub Copilot, testing is no longer an afterthought that takes days. Let's see how AI can help you generate comprehensive test suites in minutes!

---

## Step 1: Introduction to AI-Assisted Testing

### 1.1 Why Testing with Copilot is Different

Traditional testing challenges:
- ❌ Writing tests is time-consuming and repetitive
- ❌ Easy to miss edge cases
- ❌ Test maintenance can be tedious
- ❌ Setting up test fixtures requires boilerplate code

With GitHub Copilot:
- ✅ Generate test cases from implementation code
- ✅ AI suggests edge cases you might not consider
- ✅ Automatic test fixture generation
- ✅ Consistent test patterns across the codebase

### 1.2 Types of Tests for ApproveThis

We'll implement three types of tests:

1. **Unit Tests** - Test individual components in isolation
   - Models (User, Role, DispatchRequest)
   - Providers (MockProvider, GitHubProvider)
   - Utilities and helpers

2. **Integration Tests** - Test components working together
   - Route handlers with database
   - Provider interactions with application logic
   - RBAC permission enforcement

3. **End-to-End (E2E) Tests** - Test complete user workflows
   - Login flows
   - Workflow dispatch process
   - Approval workflows
   - Role-based UI differences

> [!NOTE]
> For detailed Playwright setup and configuration, see the [Playwright Testing Guide](../docs/Playwright-Testing-Guide.md).

---

## Step 2: Setting Up the Testing Infrastructure

Let's set up pytest and Playwright for comprehensive testing.

### 2.1 Install Testing Dependencies

Add testing packages to your requirements (or create a separate `requirements-dev.txt`):

```bash
pip install pytest pytest-flask pytest-cov playwright
playwright install
```

### 2.2 Create Test Configuration

Ask Copilot to create a pytest configuration:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create a pytest.ini configuration file in the approvethis directory with settings for:
- Test discovery pattern
- Coverage reporting
- Verbose output
- Environment variable handling for tests
```

</details>

Expected `pytest.ini`:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --cov=app
    --cov-report=html
    --cov-report=term-missing
env =
    FLASK_ENV=testing
    DATABASE_URL=sqlite:///:memory:
```

### 2.3 Create Test Fixtures

Create `approvethis/tests/conftest.py` with common test fixtures:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create tests/conftest.py with pytest fixtures for:
1. Flask test client
2. Test database (in-memory SQLite)
3. Sample user objects for each role (viewer, developer, admin)
4. Authenticated test client for each role
5. Sample dispatch request objects
Use the application factory pattern from app/__init__.py
```

</details>

This will create essential fixtures like:
```python
@pytest.fixture
def app():
    """Create application instance for testing."""
    # ... setup code

@pytest.fixture
def client(app):
    """Test client for making requests."""
    return app.test_client()

@pytest.fixture
def viewer_user(app):
    """Create a viewer role user for testing."""
    # ... user creation

@pytest.fixture
def auth_client_viewer(client, viewer_user):
    """Authenticated client as viewer."""
    # ... authentication
```

---

## Step 3: Generating Unit Tests

Let's use Copilot to generate comprehensive unit tests.

### 3.1 Test the Role Model

Create `approvethis/tests/test_models/test_role.py`:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create comprehensive unit tests for the Role model in app/models/role.py. Test:
- Permission bit flag operations (has_permission, add_permission, remove_permission)
- Role creation with default permissions
- insert_roles() static method creates all default roles correctly
- Permission combinations work as expected
- Edge cases like adding duplicate permissions or removing non-existent ones
Save as tests/test_models/test_role.py
```

</details>

**Key tests Copilot will generate:**
```python
def test_add_permission(app):
    """Test adding permissions to a role."""
    role = Role(name='TestRole')
    role.add_permission(Permission.VIEW_REPOS)
    assert role.has_permission(Permission.VIEW_REPOS)
    
def test_permission_bitwise_operations(app):
    """Test multiple permissions using bit flags."""
    role = Role(name='TestRole')
    role.add_permission(Permission.VIEW_REPOS)
    role.add_permission(Permission.VIEW_WORKFLOWS)
    assert role.has_permission(Permission.VIEW_REPOS)
    assert role.has_permission(Permission.VIEW_WORKFLOWS)
    assert not role.has_permission(Permission.DISPATCH_WORKFLOW)
```

### 3.2 Test the User Model

Create `approvethis/tests/test_models/test_user.py`:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create unit tests for the User model in app/models/user.py. Test:
- User creation with password hashing
- Password verification (correct and incorrect passwords)
- User-role relationship
- Permission checking through user's role
- String representation (__repr__)
Create comprehensive tests in tests/test_models/test_user.py
```

</details>

### 3.3 Test the DispatchRequest Model

Create `approvethis/tests/test_models/test_dispatch_request.py`:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create tests for the DispatchRequest model focusing on:
- Dispatch request creation with required fields
- Status transitions (pending -> approved/rejected)
- Timestamp fields (created_at, updated_at, approved_at)
- User relationship (request owner)
- Approval fields (approved_by, rejection_reason)
Save as tests/test_models/test_dispatch_request.py
```

</details>

### 3.4 Run Unit Tests

Execute the unit tests:

```bash
cd approvethis
pytest tests/test_models/ -v
```

Review the coverage report:
```bash
pytest tests/test_models/ --cov=app/models --cov-report=term-missing
```

> [!TIP]
> 💡 Ask Copilot to explain any test failures: `@workspace Why is test_permission_bitwise_operations failing? Here's the error: [paste error]`

---

## Step 4: Testing the Provider Layer

Now let's test the provider implementations.

### 4.1 Test the Mock Provider

Create `approvethis/tests/test_providers/test_mock_provider.py`:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create tests for the MockGitHubProvider in app/providers/mock.py. Verify:
- list_repositories() returns mock repository data
- list_workflows() returns workflows for a given repo
- list_workflow_runs() returns run history
- get_workflow_run() returns detailed run information
- dispatch_workflow() simulates successful dispatch
- All returned data matches the expected schema
Save as tests/test_providers/test_mock_provider.py
```

</details>

### 4.2 Test the Real GitHub Provider (with mocking)

Create tests for the real provider using mocking:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create tests for RealGitHubProvider in app/providers/github.py using unittest.mock to mock the PyGithub library. Test:
- Successful repository listing
- Successful workflow listing
- Error handling for API failures
- Rate limiting behavior
- Authentication with token
- Proper logging of operations
Use pytest-mock or unittest.mock for mocking GitHub API calls.
Save as tests/test_providers/test_github_provider.py
```

</details>

**Example test with mocking:**
```python
from unittest.mock import Mock, patch
import pytest

def test_list_repositories_success(app):
    """Test successful repository listing."""
    with patch('app.providers.github.Github') as mock_github:
        # Setup mock
        mock_repo = Mock()
        mock_repo.full_name = 'owner/repo'
        mock_repo.description = 'Test repo'
        mock_github.return_value.get_user.return_value.get_repos.return_value = [mock_repo]
        
        # Execute
        provider = RealGitHubProvider(token='fake_token')
        repos = provider.list_repositories()
        
        # Assert
        assert len(repos) > 0
        assert repos[0]['full_name'] == 'owner/repo'
```

---

## Step 5: End-to-End Testing with Playwright

Now for the exciting part—E2E tests that validate entire user workflows!

### 5.1 Configure Playwright for Flask

Create `approvethis/tests/e2e/playwright.config.py`:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create a Playwright configuration for testing the Flask application. Include:
- Base URL configuration (http://localhost:5000)
- Browser settings (headless mode for CI)
- Screenshot on failure
- Video recording for failed tests
- Timeout configurations
Save as tests/e2e/playwright.config.py
```

</details>

### 5.2 Create Login Flow Tests

Create `approvethis/tests/e2e/test_login.py`:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create Playwright E2E tests for the login flow. Test:
1. Successful login with valid credentials (viewer user)
2. Failed login with invalid password
3. Failed login with non-existent username
4. Redirect to login page when accessing protected routes
5. Logout functionality
6. Session persistence across page navigation

The login page is at /login with username and password fields.
Save as tests/e2e/test_login.py
```

</details>

**Example E2E test:**
```python
from playwright.sync_api import Page, expect

def test_successful_login(page: Page, live_server):
    """Test successful login redirects to dashboard."""
    page.goto(f"{live_server.url}/login")
    
    page.fill('input[name="username"]', 'viewer')
    page.fill('input[name="password"]', 'viewer')
    page.click('button[type="submit"]')
    
    expect(page).to_have_url(f"{live_server.url}/dashboard")
    expect(page.locator('text=Welcome')).to_be_visible()
```

### 5.3 Create Workflow Tests

Create `approvethis/tests/e2e/test_workflows.py`:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create Playwright tests for the workflow management features:
1. View repositories list as authenticated user
2. Navigate to workflows for a specific repository
3. View workflow runs for a workflow
4. View detailed information for a specific run
5. Verify that viewers cannot see dispatch buttons
6. Verify that developers can see dispatch buttons

Use the Playwright Page object model pattern for maintainability.
Save as tests/e2e/test_workflows.py
```

</details>

### 5.4 Create Dispatch and Approval Tests

Create `approvethis/tests/e2e/test_dispatch.py`:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create E2E tests for the workflow dispatch and approval process:
1. Developer creates a dispatch request
2. Request appears in pending approvals list
3. Viewer cannot approve requests (no permission)
4. Admin can approve requests
5. Approved request triggers workflow
6. Admin can reject requests with reason
7. Rejected requests show rejection reason

This tests the complete approval workflow that's the core of ApproveThis!
Save as tests/e2e/test_dispatch.py
```

</details>

---

## Step 6: Testing Edge Cases with Copilot

One of Copilot's superpowers is suggesting edge cases you might not think of.

### 6.1 Ask Copilot for Edge Cases

For any test file, ask Copilot to identify missing scenarios:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Review tests/test_models/test_role.py and suggest edge cases I might have missed. Consider:
- Boundary conditions
- Invalid inputs
- Concurrent modifications
- Null/None values
- SQL injection attempts
- Unicode and special characters
```

</details>

### 6.2 Generate Negative Test Cases

Ask for negative testing scenarios:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create negative test cases for the dispatch workflow:
- What happens if required fields are missing?
- What if workflow_id doesn't exist?
- What if ref (branch) is invalid?
- What if user lacks permission?
- What if GitHub API is down?
- What if approval is attempted twice?
Add these tests to tests/test_routes/test_api.py
```

</details>

### 6.3 Test Security Vulnerabilities

Generate security-focused tests:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create security tests for authentication and authorization:
- SQL injection attempts in login form
- XSS attempts in workflow inputs
- CSRF token validation
- Session fixation attempts
- Permission boundary testing (accessing resources without permission)
- Token exposure in logs or error messages
Create tests/test_security.py with these tests
```

</details>

---

## Step 7: Achieving and Maintaining Coverage

Let's ensure we meet the 80% coverage requirement.

### 7.1 Check Current Coverage

Run tests with coverage reporting:

```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```

Open `htmlcov/index.html` to see a detailed visual coverage report.

### 7.2 Identify Coverage Gaps

Ask Copilot to help improve coverage:

<details>
<summary>💡 Example prompt</summary>

```
@workspace The coverage report shows app/blueprints/jobs/routes.py has only 45% coverage. Generate tests to cover the missing lines. Here are the uncovered line numbers: [paste from coverage report]
```

</details>

### 7.3 Generate Test Data Fixtures

Create reusable test data:

<details>
<summary>💡 Example prompt</summary>

```
@workspace Create a test data factory in tests/factories.py using factory_boy or similar pattern. Include factories for:
- User (with different roles)
- Repository
- Workflow
- WorkflowRun
- DispatchRequest
This will make test data creation consistent and easy.
```

</details>

---

## 🏆 Exercise Wrap-Up

Outstanding! You've transformed testing from an afterthought into an integral part of development. Let's review your accomplishments:

### ✅ What You Accomplished

- [x] Set up comprehensive testing infrastructure (pytest, Playwright)
- [x] Created test configuration and fixtures in conftest.py
- [x] Generated unit tests for models (User, Role, DispatchRequest)
- [x] Implemented provider tests with mocking
- [x] Created E2E tests for login, workflows, and dispatch
- [x] Identified edge cases and negative test scenarios with Copilot
- [x] Achieved test coverage requirements (80%+)
- [x] Established patterns for future test maintenance

---

## 🤔 Reflection Questions

Take a moment to consider:

1. How did AI-assisted test generation change your approach to testing?
2. What edge cases did Copilot suggest that you wouldn't have thought of?
3. How does having comprehensive tests affect your confidence in deploying code?
4. What's the balance between AI-generated tests and human-written tests?
5. How can E2E tests catch issues that unit tests might miss?

---

## 🎓 Key Takeaways

- **AI test generation** dramatically reduces the time required for comprehensive coverage
- **Copilot suggests edge cases** that improve test robustness
- **E2E tests with Playwright** validate complete user workflows, not just isolated functions
- **Test fixtures and factories** make test data management consistent and maintainable
- **Coverage tools** identify gaps, and Copilot can fill them quickly
- **Security testing** should be explicit, testing for injection, XSS, and authorization issues
- **Testing is no longer an afterthought**—it's a natural part of the AI-assisted development process

---

## 🔜 Coming Up Next

In **Lab 6: IaC and Deployments**, you'll use GitHub Copilot with Azure and Terraform MCP servers to understand and enhance infrastructure as code. You'll explore the existing Terraform modules, make improvements, and deploy infrastructure through both GitHub Actions and the ApproveThis application. Get ready to see how AI transforms infrastructure management!

---

**[← Back to Lab 4](Lab-4-Development-Process.md)** | **[Continue to Lab 6: IaC and Deployments →](Lab-6-IaC-and-Deployments.md)**
