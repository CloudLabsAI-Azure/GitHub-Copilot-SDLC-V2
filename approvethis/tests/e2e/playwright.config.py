"""Playwright configuration for ApproveThis E2E tests."""
import os

# Base URL for the application
# In tests, we'll use a live server fixture, but this provides a default
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

# Browser configuration
BROWSER_CONFIG = {
    # Run headless in CI environments
    "headless": os.getenv("CI", "false").lower() == "true",
    
    # Slow down operations for debugging (milliseconds)
    # Set DEBUG=true environment variable to enable
    "slow_mo": 100 if os.getenv("DEBUG") else 0,
    
    # Browser viewport size
    "viewport": {
        "width": 1280,
        "height": 720
    },
}

# Test configuration
TEST_CONFIG = {
    "base_url": BASE_URL,
    
    # Take screenshots on test failure
    "screenshot_on_failure": True,
    
    # Record video on test failure
    "video_on_failure": True,
    
    # Trace on failure for debugging
    "trace_on_failure": True,
}

# Timeout configurations (milliseconds)
TIMEOUTS = {
    # Default timeout for all operations
    "default": 30000,  # 30 seconds
    
    # Navigation timeout (page loads)
    "navigation": 60000,  # 60 seconds
    
    # Expect timeout for assertions
    "expect": 5000,  # 5 seconds
}

# Screenshot directory
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")

# Video directory
VIDEO_DIR = os.path.join(os.path.dirname(__file__), "videos")

# Trace directory
TRACE_DIR = os.path.join(os.path.dirname(__file__), "traces")

# Create directories if they don't exist
for directory in [SCREENSHOT_DIR, VIDEO_DIR, TRACE_DIR]:
    os.makedirs(directory, exist_ok=True)

# Playwright browser types to test against
# By default, test with Chromium only
# Set TEST_ALL_BROWSERS=true to test against all browsers
BROWSERS = ["chromium"]
if os.getenv("TEST_ALL_BROWSERS", "false").lower() == "true":
    BROWSERS = ["chromium", "firefox", "webkit"]

# Test user credentials
# These match the users created in conftest.py
TEST_USERS = {
    "viewer": {
        "username": "viewer",
        "password": "viewer",
        "role": "Viewer"
    },
    "developer": {
        "username": "developer",
        "password": "developer",
        "role": "LeadDeveloper"
    },
    "admin": {
        "username": "admin",
        "password": "admin",
        "role": "GlobalAdmin"
    }
}
