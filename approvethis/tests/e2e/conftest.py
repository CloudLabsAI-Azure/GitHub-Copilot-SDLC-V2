"""E2E fixture configuration for Playwright tests."""
import pytest
import multiprocessing
import time
from playwright.sync_api import Page, expect
from app import create_app
from app.extensions import db
from app.models import Role, User


@pytest.fixture(scope="session")
def e2e_app():
    """Create Flask application for E2E testing."""
    app = create_app("testing")
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SERVER_NAME": None,  # Allow any host for testing
    })
    
    with app.app_context():
        db.create_all()
        
        # Insert roles
        Role.insert_roles()
        
        # Create test users
        viewer_role = Role.query.filter_by(name="Viewer").first()
        dev_role = Role.query.filter_by(name="LeadDeveloper").first()
        admin_role = Role.query.filter_by(name="GlobalAdmin").first()
        
        viewer = User(username="viewer", email="viewer@test.com", role=viewer_role)
        viewer.set_password("viewer")
        
        developer = User(username="developer", email="dev@test.com", role=dev_role)
        developer.set_password("developer")
        
        admin = User(username="admin", email="admin@test.com", role=admin_role)
        admin.set_password("admin")
        
        db.session.add_all([viewer, developer, admin])
        db.session.commit()
    
    yield app
    
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="session")
def live_server(e2e_app):
    """Start Flask server for E2E tests."""
    def run_server():
        e2e_app.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False)
    
    # Start server in a separate process
    process = multiprocessing.Process(target=run_server)
    process.start()
    
    # Wait for server to start
    time.sleep(2)
    
    # Provide server URL
    class LiveServer:
        url = "http://127.0.0.1:5001"
    
    yield LiveServer()
    
    # Shutdown server
    process.terminate()
    process.join(timeout=5)
    if process.is_alive():
        process.kill()


@pytest.fixture
def authenticated_page_viewer(page: Page, live_server):
    """Page fixture that's already logged in as viewer."""
    page.goto(f"{live_server.url}/login")
    page.fill("input[name='username']", "viewer")
    page.fill("input[name='password']", "viewer")
    page.click("button[type='submit']")
    page.wait_for_url(f"{live_server.url}/dashboard")
    return page


@pytest.fixture
def authenticated_page_developer(page: Page, live_server):
    """Page fixture that's already logged in as developer."""
    page.goto(f"{live_server.url}/login")
    page.fill("input[name='username']", "developer")
    page.fill("input[name='password']", "developer")
    page.click("button[type='submit']")
    page.wait_for_url(f"{live_server.url}/dashboard")
    return page


@pytest.fixture
def authenticated_page_admin(page: Page, live_server):
    """Page fixture that's already logged in as admin."""
    page.goto(f"{live_server.url}/login")
    page.fill("input[name='username']", "admin")
    page.fill("input[name='password']", "admin")
    page.click("button[type='submit']")
    page.wait_for_url(f"{live_server.url}/dashboard")
    return page


# Helper function for login (can be used directly in tests)
def login_as(page: Page, live_server, username: str, password: str):
    """Helper function to log in as a specific user."""
    page.goto(f"{live_server.url}/login")
    page.fill("input[name='username']", username)
    page.fill("input[name='password']", password)
    page.click("button[type='submit']")
    page.wait_for_url(f"{live_server.url}/dashboard")
