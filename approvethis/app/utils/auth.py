"""Authentication and authorization utilities."""
from functools import wraps
from flask import abort
from flask_login import current_user


def permission_required(permission):
    """
    Decorator for views that require specific permissions.
    
    Args:
        permission: Permission bit flag from Permission class
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Decorator for views that require admin access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
