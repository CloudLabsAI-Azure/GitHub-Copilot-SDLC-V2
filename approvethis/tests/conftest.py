"""Pytest configuration and fixtures for ApproveThis tests."""
import pytest
import os
import tempfile
from app import create_app
from app.extensions import db
from app.models import Role, User, DispatchRequest


@pytest.fixture(scope="session")
def app():
    """Create and configure a Flask application instance for testing."""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()
    
    # Configure app for testing
    app = create_app("testing")
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "WTF_CSRF_ENABLED": False,  # Disable CSRF for testing
        "SERVER_NAME": "localhost.localdomain",
    })
    
    # Create database and tables
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
    
    # Cleanup
    with app.app_context():
        db.session.remove()
        db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the app."""
    return app.test_cli_runner()


@pytest.fixture
def viewer_user(app):
    """Get the viewer test user."""
    with app.app_context():
        return User.query.filter_by(username="viewer").first()


@pytest.fixture
def developer_user(app):
    """Get the developer test user."""
    with app.app_context():
        return User.query.filter_by(username="developer").first()


@pytest.fixture
def admin_user(app):
    """Get the admin test user."""
    with app.app_context():
        return User.query.filter_by(username="admin").first()


@pytest.fixture
def auth_client_viewer(client, viewer_user):
    """Get an authenticated test client as viewer."""
    client.post("/login", data={
        "username": "viewer",
        "password": "viewer"
    }, follow_redirects=True)
    return client


@pytest.fixture
def auth_client_developer(client, developer_user):
    """Get an authenticated test client as developer."""
    client.post("/login", data={
        "username": "developer",
        "password": "developer"
    }, follow_redirects=True)
    return client


@pytest.fixture
def auth_client_admin(client, admin_user):
    """Get an authenticated test client as admin."""
    client.post("/login", data={
        "username": "admin",
        "password": "admin"
    }, follow_redirects=True)
    return client


@pytest.fixture
def sample_dispatch_request(app, developer_user):
    """Create a sample dispatch request for testing."""
    with app.app_context():
        dispatch = DispatchRequest(
            owner="testorg",
            repo="testrepo",
            workflow_id="test.yml",
            workflow_name="Test Workflow",
            ref="main",
            inputs="{}",
            status="pending",
            user_id=developer_user.id
        )
        db.session.add(dispatch)
        db.session.commit()
        
        # Return the ID instead of the object (which becomes detached)
        dispatch_id = dispatch.id
    
    # Yield for test use
    yield dispatch_id
    
    # Cleanup
    with app.app_context():
        DispatchRequest.query.filter_by(id=dispatch_id).delete()
        db.session.commit()


@pytest.fixture(autouse=True)
def reset_database_state(app):
    """Reset database state before each test."""
    with app.app_context():
        # Clean up any dispatch requests from previous tests
        DispatchRequest.query.delete()
        db.session.commit()
    
    yield
    
    # Cleanup after test
    with app.app_context():
        DispatchRequest.query.delete()
        db.session.commit()
