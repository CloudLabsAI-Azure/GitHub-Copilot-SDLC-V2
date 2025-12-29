"""E2E tests for login functionality."""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_successful_login_viewer(page: Page, live_server):
    """Test successful login as viewer redirects to dashboard."""
    page.goto(f"{live_server.url}/login")
    
    # Fill login form
    page.fill("input[name='username']", "viewer")
    page.fill("input[name='password']", "viewer")
    
    # Submit
    page.click("button[type='submit']")
    
    # Verify redirect to dashboard
    page.wait_for_url(f"{live_server.url}/dashboard")
    
    # Verify user is logged in
    expect(page.locator("text=Welcome")).to_be_visible()


@pytest.mark.e2e
def test_failed_login_wrong_password(page: Page, live_server):
    """Test login fails with incorrect password."""
    page.goto(f"{live_server.url}/login")
    
    page.fill("input[name='username']", "viewer")
    page.fill("input[name='password']", "wrongpassword")
    page.click("button[type='submit']")
    
    # Should stay on login page or show error
    # Note: Adjust selector based on actual error message in your app
    # This is a template - replace with actual implementation
    expect(page.locator("text=Invalid")).to_be_visible()


@pytest.mark.e2e  
def test_failed_login_nonexistent_user(page: Page, live_server):
    """Test login fails with non-existent username."""
    page.goto(f"{live_server.url}/login")
    
    page.fill("input[name='username']", "nonexistent")
    page.fill("input[name='password']", "password")
    page.click("button[type='submit']")
    
    # Should show error
    expect(page.locator("text=Invalid")).to_be_visible()


@pytest.mark.e2e
def test_logout(page: Page, live_server):
    """Test logout functionality."""
    # Login first
    page.goto(f"{live_server.url}/login")
    page.fill("input[name='username']", "viewer")
    page.fill("input[name='password']", "viewer")
    page.click("button[type='submit']")
    page.wait_for_url(f"{live_server.url}/dashboard")
    
    # Click logout
    # Note: Adjust selector based on actual logout link in your app
    page.click("a[href='/logout']")
    
    # Should redirect to login
    page.wait_for_url(f"{live_server.url}/login")
    
    # Trying to access dashboard should redirect to login
    page.goto(f"{live_server.url}/dashboard")
    page.wait_for_url(f"{live_server.url}/login")


@pytest.mark.e2e
def test_protected_route_requires_login(page: Page, live_server):
    """Test that accessing protected routes redirects to login."""
    # Try to access dashboard without logging in
    page.goto(f"{live_server.url}/dashboard")
    
    # Should redirect to login
    page.wait_for_url(f"{live_server.url}/login")
