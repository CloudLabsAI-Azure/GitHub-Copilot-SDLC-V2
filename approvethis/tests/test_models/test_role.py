"""Unit tests for the Role model."""
import pytest
from app.models import Role, Permission
from app.extensions import db


class TestRoleModel:
    """Test suite for Role model functionality."""
    
    def test_role_creation(self, app):
        """Test creating a new role."""
        with app.app_context():
            role = Role(name="TestRole", description="A test role")
            db.session.add(role)
            db.session.commit()
            
            assert role.id is not None
            assert role.name == "TestRole"
            assert role.description == "A test role"
            assert role.permissions == 0
    
    def test_add_permission(self, app):
        """Test adding a permission to a role."""
        with app.app_context():
            role = Role(name="TestRole")
            role.add_permission(Permission.VIEW_REPOS)
            
            assert role.has_permission(Permission.VIEW_REPOS)
            assert not role.has_permission(Permission.DISPATCH_WORKFLOW)
    
    def test_add_multiple_permissions(self, app):
        """Test adding multiple permissions to a role."""
        with app.app_context():
            role = Role(name="TestRole")
            role.add_permission(Permission.VIEW_REPOS)
            role.add_permission(Permission.VIEW_WORKFLOWS)
            role.add_permission(Permission.VIEW_RUNS)
            
            assert role.has_permission(Permission.VIEW_REPOS)
            assert role.has_permission(Permission.VIEW_WORKFLOWS)
            assert role.has_permission(Permission.VIEW_RUNS)
            assert not role.has_permission(Permission.DISPATCH_WORKFLOW)
    
    def test_remove_permission(self, app):
        """Test removing a permission from a role."""
        with app.app_context():
            role = Role(name="TestRole")
            role.add_permission(Permission.VIEW_REPOS)
            role.add_permission(Permission.VIEW_WORKFLOWS)
            
            assert role.has_permission(Permission.VIEW_REPOS)
            
            role.remove_permission(Permission.VIEW_REPOS)
            
            assert not role.has_permission(Permission.VIEW_REPOS)
            assert role.has_permission(Permission.VIEW_WORKFLOWS)
    
    def test_reset_permissions(self, app):
        """Test resetting all permissions."""
        with app.app_context():
            role = Role(name="TestRole")
            role.add_permission(Permission.VIEW_REPOS)
            role.add_permission(Permission.VIEW_WORKFLOWS)
            
            role.reset_permissions()
            
            assert role.permissions == 0
            assert not role.has_permission(Permission.VIEW_REPOS)
            assert not role.has_permission(Permission.VIEW_WORKFLOWS)
    
    def test_insert_default_roles(self, app):
        """Test that default roles are created correctly."""
        with app.app_context():
            # Roles are already inserted by conftest fixture
            viewer = Role.query.filter_by(name="Viewer").first()
            developer = Role.query.filter_by(name="LeadDeveloper").first()
            admin = Role.query.filter_by(name="GlobalAdmin").first()
            
            assert viewer is not None
            assert developer is not None
            assert admin is not None
            
            # Verify Viewer permissions
            assert viewer.has_permission(Permission.VIEW_REPOS)
            assert viewer.has_permission(Permission.VIEW_WORKFLOWS)
            assert viewer.has_permission(Permission.VIEW_RUNS)
            assert not viewer.has_permission(Permission.DISPATCH_WORKFLOW)
            
            # Verify LeadDeveloper permissions
            assert developer.has_permission(Permission.VIEW_REPOS)
            assert developer.has_permission(Permission.DISPATCH_WORKFLOW)
            
            # Verify GlobalAdmin permissions
            assert admin.has_permission(Permission.VIEW_REPOS)
            assert admin.has_permission(Permission.DISPATCH_WORKFLOW)
            assert admin.has_permission(Permission.MANAGE_APPROVALS)
            assert admin.has_permission(Permission.ADMIN)
    
    def test_add_duplicate_permission(self, app):
        """Test that adding a duplicate permission doesn't change the value."""
        with app.app_context():
            role = Role(name="TestRole")
            role.add_permission(Permission.VIEW_REPOS)
            initial_perms = role.permissions
            
            # Adding the same permission again should not change the value
            role.add_permission(Permission.VIEW_REPOS)
            
            assert role.permissions == initial_perms
            assert role.has_permission(Permission.VIEW_REPOS)
