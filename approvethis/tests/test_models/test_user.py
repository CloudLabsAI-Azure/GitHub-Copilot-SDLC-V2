"""Unit tests for the User model."""
import pytest
from app.models import User, Role, Permission
from app.extensions import db


class TestUserModel:
    """Test suite for User model functionality."""
    
    def test_user_creation(self, app):
        """Test creating a new user."""
        with app.app_context():
            role = Role.query.filter_by(name="Viewer").first()
            user = User(
                username="testuser",
                email="test@example.com",
                role=role
            )
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.username == "testuser"
            assert user.email == "test@example.com"
            assert user.role == role
    
    def test_password_hashing(self, app):
        """Test that passwords are hashed and not stored in plain text."""
        with app.app_context():
            user = User(username="testuser", email="test@example.com")
            user.set_password("mypassword")
            
            # Password hash should not be the plain text password
            assert user.password_hash != "mypassword"
            assert user.password_hash is not None
    
    def test_password_verification_correct(self, app):
        """Test password verification with correct password."""
        with app.app_context():
            user = User(username="testuser", email="test@example.com")
            user.set_password("mypassword")
            
            assert user.check_password("mypassword") is True
    
    def test_password_verification_incorrect(self, app):
        """Test password verification with incorrect password."""
        with app.app_context():
            user = User(username="testuser", email="test@example.com")
            user.set_password("mypassword")
            
            assert user.check_password("wrongpassword") is False
    
    def test_user_has_permission_through_role(self, app, viewer_user):
        """Test that users inherit permissions from their role."""
        with app.app_context():
            user = User.query.filter_by(username="viewer").first()
            
            # Viewer should have VIEW_REPOS permission
            assert user.role.has_permission(Permission.VIEW_REPOS)
            
            # Viewer should NOT have DISPATCH_WORKFLOW permission
            assert not user.role.has_permission(Permission.DISPATCH_WORKFLOW)
    
    def test_developer_permissions(self, app, developer_user):
        """Test that developer has correct permissions."""
        with app.app_context():
            user = User.query.filter_by(username="developer").first()
            
            assert user.role.has_permission(Permission.VIEW_REPOS)
            assert user.role.has_permission(Permission.VIEW_WORKFLOWS)
            assert user.role.has_permission(Permission.DISPATCH_WORKFLOW)
            assert not user.role.has_permission(Permission.MANAGE_APPROVALS)
    
    def test_admin_permissions(self, app, admin_user):
        """Test that admin has all permissions."""
        with app.app_context():
            user = User.query.filter_by(username="admin").first()
            
            assert user.role.has_permission(Permission.VIEW_REPOS)
            assert user.role.has_permission(Permission.DISPATCH_WORKFLOW)
            assert user.role.has_permission(Permission.MANAGE_APPROVALS)
            assert user.role.has_permission(Permission.ADMIN)
    
    def test_user_repr(self, app, viewer_user):
        """Test the __repr__ method."""
        with app.app_context():
            user = User.query.filter_by(username="viewer").first()
            
            repr_string = repr(user)
            assert "User" in repr_string
            assert "viewer" in repr_string
