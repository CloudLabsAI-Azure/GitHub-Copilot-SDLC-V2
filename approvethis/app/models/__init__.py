"""Models package."""
from app.models.role import Role, Permission
from app.models.user import User
from app.models.dispatch_request import DispatchRequest

__all__ = ['Role', 'Permission', 'User', 'DispatchRequest']
