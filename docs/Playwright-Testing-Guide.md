# Playwright Testing Guide

This guide provides comprehensive instructions for setting up and using Playwright for end-to-end (E2E) testing of the ApproveThis Flask application.

## 📖 Table of Contents

- [Overview](#overview)
- [Why Playwright for Flask?](#why-playwright-for-flask)
- [Installation](#installation)
- [Configuration](#configuration)
- [Writing Tests](#writing-tests)
- [Running Tests](#running-tests)
- [Common Patterns](#common-patterns)
- [Debugging](#debugging)
- [CI/CD Integration](#cicd-integration)
- [Best Practices](#best-practices)

---

## Overview

**Playwright** is a modern end-to-end testing framework that enables testing web applications across multiple browsers (Chromium, Firefox, WebKit). For Flask applications like ApproveThis, Playwright provides:

- **Full browser automation** - Test the complete user experience
- **Multi-browser support** - Ensure compatibility across browsers
- **Auto-waiting** - Automatically waits for elements to be ready
- **Screenshots and videos** - Visual debugging of test failures
- **Network interception** - Mock API responses when needed
- **Python API** - Native Python support for Flask apps

---

## Why Playwright for Flask?

### Advantages

✅ **Real Browser Testing**: Tests run in actual browsers, catching issues unit tests miss  
✅ **User Perspective**: Validates complete workflows from the user's point of view  
✅ **RBAC Validation**: Test that UI properly reflects permission differences  
✅ **JavaScript Execution**: Tests client-side JavaScript behavior  
✅ **Visual Regression**: Catch UI breakage with screenshots  

### Compared to Selenium

| Feature | Playwright | Selenium |
|---------|------------|----------|
| Auto-waiting | ✅ Built-in | ❌ Manual waits |
| Browser contexts | ✅ Isolated | ❌ Shared state |
| Network interception | ✅ Yes | ⚠️ Limited |
| Speed | ✅ Faster | ⚠️ Slower |
| Modern web features | ✅ Excellent | ⚠️ Good |

---

## Installation

### Step 1: Install Playwright for Python

In your ApproveThis application directory:

```bash
cd approvethis
pip install playwright pytest-playwright
```

### Step 2: Install Browser Binaries

Playwright requires browser binaries to be installed:

```bash
playwright install
```

This downloads Chromium, Firefox, and WebKit browsers (~300MB).

**For CI/CD (install only Chromium)**:
```bash
playwright install chromium
```

### Step 3: Verify Installation

```bash
playwright --version
```

Expected output:
```
Version 1.x.x
```

### Step 4: Update requirements.txt

Add to `approvethis/requirements-dev.txt` (or `requirements.txt`):

```txt
playwright==1.40.0
pytest-playwright==0.4.3
```

---

## Configuration

### Create Playwright Configuration

Create `approvethis/tests/e2e/playwright.config.py`:

```python
"""Playwright configuration for ApproveThis E2E tests."""
import os
from playwright.sync_api import Browser

# Base URL for the application
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

# Browser configuration
BROWSER_CONFIG = {
    "headless": os.getenv("CI", "false").lower() == "true",  # Headless in CI
    "slow_mo": 100 if os.getenv("DEBUG") else 0,  # Slow down for debugging
}

# Test configuration
TEST_CONFIG = {
    "base_url": BASE_URL,
    "screenshot_on_failure": True,
    "video_on_failure": True,
    "trace_on_failure": True,
}

# Timeout configurations (milliseconds)
TIMEOUTS = {
    "default": 30000,  # 30 seconds
    "navigation": 60000,  # 60 seconds for page loads
}
```

### Pytest Configuration for E2E Tests

Add to `approvethis/pytest.ini`:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Playwright-specific
playwright_browser = chromium
playwright_headless = true
playwright_slow_mo = 0

# Markers for different test types
markers =
    e2e: End-to-end tests (requires running Flask app)
    unit: Unit tests
    integration: Integration tests
```

---

## Writing Tests

### Test Structure

Playwright tests for Flask applications follow this pattern:

```python
from playwright.sync_api import Page, expect

def test_example(page: Page, live_server):
    """Test description."""
    # Navigate to page
    page.goto(f"{live_server.url}/some-page")
    
    # Interact with elements
    page.fill("input[name='username']", "testuser")
    page.click("button[type='submit']")
    
    # Assert results
    expect(page).to_have_url(f"{live_server.url}/dashboard")
    expect(page.locator("text=Welcome")).to_be_visible()
```

### Fixture for Live Flask Server

Create `approvethis/tests/e2e/conftest.py`:

```python
"""Pytest fixtures for Playwright E2E tests."""
import pytest
import multiprocessing
from app import create_app
from app.extensions import db
from flask import Flask

@pytest.fixture(scope="session")
def app():
    """Create Flask application for testing."""
    app = create_app("testing")
    
    with app.app_context():
        db.create_all()
        # Seed test data
        from app.models import Role, User
        Role.insert_roles()
        
        # Create test users
        viewer = User(username="viewer", email="viewer@test.com")
        viewer.set_password("viewer")
        developer = User(username="developer", email="dev@test.com")
        developer.set_password("developer")
        admin = User(username="admin", email="admin@test.com")
        admin.set_password("admin")
        
        # Assign roles
        viewer_role = Role.query.filter_by(name="Viewer").first()
        dev_role = Role.query.filter_by(name="LeadDeveloper").first()
        admin_role = Role.query.filter_by(name="GlobalAdmin").first()
        
        viewer.role = viewer_role
        developer.role = dev_role
        admin.role = admin_role
        
        db.session.add_all([viewer, developer, admin])
        db.session.commit()
    
    yield app
    
    with app.app_context():
        db.drop_all()

@pytest.fixture(scope="session")
def live_server(app):
    """Start Flask server for E2E tests."""
    # Start server in a separate process
    process = multiprocessing.Process(
        target=app.run, 
        kwargs={"port": 5001, "use_reloader": False}
    )
    process.start()
    
    # Wait for server to start
    import time
    time.sleep(2)
    
    # Provide server URL
    class LiveServer:
        url = "http://localhost:5001"
    
    yield LiveServer()
    
    # Shutdown server
    process.terminate()
    process.join()

@pytest.fixture
def authenticated_page(page: Page, live_server):
    """Page fixture that's already logged in as developer."""
    page.goto(f"{live_server.url}/login")
    page.fill("input[name='username']", "developer")
    page.fill("input[name='password']", "developer")
    page.click("button[type='submit']")
    expect(page).to_have_url(f"{live_server.url}/dashboard")
    return page
```

### Example: Login Test

Create `approvethis/tests/e2e/test_login.py`:

```python
"""E2E tests for authentication flows."""
from playwright.sync_api import Page, expect

def test_successful_login_viewer(page: Page, live_server):
    """Test successful login redirects to dashboard."""
    page.goto(f"{live_server.url}/login")
    
    # Fill login form
    page.fill("input[name='username']", "viewer")
    page.fill("input[name='password']", "viewer")
    
    # Submit
    page.click("button[type='submit']")
    
    # Verify redirect
    expect(page).to_have_url(f"{live_server.url}/dashboard")
    
    # Verify user is logged in
    expect(page.locator("text=Welcome")).to_be_visible()
    expect(page.locator("text=viewer")).to_be_visible()

def test_failed_login_wrong_password(page: Page, live_server):
    """Test login fails with incorrect password."""
    page.goto(f"{live_server.url}/login")
    
    page.fill("input[name='username']", "viewer")
    page.fill("input[name='password']", "wrongpassword")
    page.click("button[type='submit']")
    
    # Should stay on login page
    expect(page).to_have_url(f"{live_server.url}/login")
    
    # Error message should appear
    expect(page.locator("text=Invalid username or password")).to_be_visible()

def test_logout(page: Page, live_server):
    """Test logout functionality."""
    # Login first
    page.goto(f"{live_server.url}/login")
    page.fill("input[name='username']", "viewer")
    page.fill("input[name='password']", "viewer")
    page.click("button[type='submit']")
    
    # Click logout
    page.click("a[href='/logout']")
    
    # Should redirect to login
    expect(page).to_have_url(f"{live_server.url}/login")
    
    # Trying to access dashboard should redirect to login
    page.goto(f"{live_server.url}/dashboard")
    expect(page).to_have_url(f"{live_server.url}/login")
```

### Example: Workflow Test with RBAC

Create `approvethis/tests/e2e/test_workflows.py`:

```python
"""E2E tests for workflow management."""
from playwright.sync_api import Page, expect

def test_viewer_cannot_dispatch_workflow(page: Page, live_server):
    """Test that viewers cannot see dispatch buttons."""
    # Login as viewer
    page.goto(f"{live_server.url}/login")
    page.fill("input[name='username']", "viewer")
    page.fill("input[name='password']", "viewer")
    page.click("button[type='submit']")
    
    # Navigate to workflows
    page.goto(f"{live_server.url}/workflows/testorg/testrepo")
    
    # Dispatch button should NOT be visible
    expect(page.locator("button:has-text('Dispatch')")).not_to_be_visible()

def test_developer_can_dispatch_workflow(page: Page, live_server):
    """Test that developers can see dispatch buttons."""
    # Login as developer
    page.goto(f"{live_server.url}/login")
    page.fill("input[name='username']", "developer")
    page.fill("input[name='password']", "developer")
    page.click("button[type='submit']")
    
    # Navigate to workflows
    page.goto(f"{live_server.url}/workflows/testorg/testrepo")
    
    # Dispatch button SHOULD be visible
    expect(page.locator("button:has-text('Dispatch')")).to_be_visible()
    
    # Click dispatch
    page.click("button:has-text('Dispatch'):first")
    
    # Dispatch form should appear
    expect(page.locator("form[action*='dispatch']")).to_be_visible()
```

---

## Running Tests

### Run All E2E Tests

```bash
cd approvethis
pytest tests/e2e/ -v
```

### Run Specific Test File

```bash
pytest tests/e2e/test_login.py -v
```

### Run with Headed Browser (see the browser)

```bash
pytest tests/e2e/ --headed
```

### Run with Specific Browser

```bash
# Chromium (default)
pytest tests/e2e/ --browser chromium

# Firefox
pytest tests/e2e/ --browser firefox

# WebKit (Safari engine)
pytest tests/e2e/ --browser webkit
```

### Run with Slow Motion (for debugging)

```bash
pytest tests/e2e/ --headed --slowmo 500
```

### Generate HTML Report

```bash
pytest tests/e2e/ --html=test-report.html
```

---

## Common Patterns

### Waiting for Elements

Playwright auto-waits, but you can explicitly wait:

```python
# Wait for element to be visible
page.wait_for_selector("button.submit", state="visible")

# Wait for navigation
page.wait_for_url("**/dashboard")

# Wait for function
page.wait_for_function("() => document.readyState === 'complete'")
```

### Interacting with Forms

```python
# Text input
page.fill("input[name='username']", "testuser")

# Checkbox
page.check("input[type='checkbox']")
page.uncheck("input[type='checkbox']")

# Radio button
page.click("input[type='radio'][value='option1']")

# Select dropdown
page.select_option("select[name='role']", "LeadDeveloper")

# File upload
page.set_input_files("input[type='file']", "path/to/file.txt")
```

### Taking Screenshots

```python
# Full page screenshot
page.screenshot(path="screenshot.png")

# Element screenshot
page.locator(".dashboard").screenshot(path="dashboard.png")

# In test for debugging
def test_example(page: Page, live_server):
    page.goto(f"{live_server.url}/dashboard")
    page.screenshot(path="tests/screenshots/debug.png")
```

### Network Mocking

```python
def test_with_mocked_api(page: Page, live_server):
    """Test with mocked GitHub API response."""
    # Mock API response
    page.route("**/api/github/repos", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='[{"name": "test-repo", "full_name": "org/test-repo"}]'
    ))
    
    page.goto(f"{live_server.url}/repositories")
    expect(page.locator("text=test-repo")).to_be_visible()
```

---

## Debugging

### Visual Debugging with Playwright Inspector

```bash
pytest tests/e2e/test_login.py --headed --slowmo 500 -k test_successful_login
```

### Debug Mode

```python
# Add this line in your test to pause and inspect
page.pause()
```

### Screenshots on Failure

Configure in `conftest.py`:

```python
@pytest.fixture(autouse=True)
def screenshot_on_failure(page: Page, request):
    """Take screenshot on test failure."""
    yield
    if request.node.rep_call.failed:
        page.screenshot(path=f"tests/screenshots/{request.node.name}.png")
```

### Video Recording

```python
@pytest.fixture(scope="session")
def browser_context_args():
    """Configure browser context with video recording."""
    return {
        "record_video_dir": "tests/videos/",
        "record_video_size": {"width": 1280, "height": 720}
    }
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd approvethis
          pip install -r requirements.txt
          pip install playwright pytest-playwright
          playwright install --with-deps chromium
      
      - name: Run E2E tests
        run: |
          cd approvethis
          pytest tests/e2e/ -v --headed
      
      - name: Upload screenshots on failure
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: test-screenshots
          path: approvethis/tests/screenshots/
```

---

## Best Practices

### 1. Use Page Object Model

**Bad**:
```python
def test_login(page):
    page.fill("#username", "user")
    page.fill("#password", "pass")
    page.click("button")
```

**Good**:
```python
class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("input[name='username']")
        self.password_input = page.locator("input[name='password']")
        self.submit_button = page.locator("button[type='submit']")
    
    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.submit_button.click()

def test_login(page):
    login_page = LoginPage(page)
    login_page.login("user", "pass")
```

### 2. Test User Journeys, Not Implementation

Focus on what users do, not how the code works:

```python
def test_complete_approval_workflow(page, live_server):
    """Test complete workflow from request to approval."""
    # Developer requests dispatch
    # Admin approves request
    # Workflow is triggered
    # User sees success message
```

### 3. Keep Tests Independent

Each test should work in isolation:

```python
@pytest.fixture(autouse=True)
def reset_database(app):
    """Reset database before each test."""
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        # Seed required data
```

### 4. Use Meaningful Test Names

```python
# Bad
def test_1(page): ...

# Good
def test_admin_can_approve_dispatch_request(page): ...
```

### 5. Avoid Hard-Coded Waits

```python
# Bad
import time
time.sleep(5)

# Good  
page.wait_for_selector(".loading-complete")
expect(page.locator(".result")).to_be_visible()
```

---

## Related Guides

- [Glossary](Glossary.md) - Testing terminology

---

**[← Back to Documentation Index](README.md)**
