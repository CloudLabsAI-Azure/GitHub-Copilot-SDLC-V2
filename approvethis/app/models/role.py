"""Role and Permission models for RBAC."""
from app.extensions import db


class Permission:
    """Permission bit flags."""
    VIEW_REPOS = 1
    VIEW_WORKFLOWS = 2
    VIEW_RUNS = 4
    DISPATCH_WORKFLOW = 8
    MANAGE_APPROVALS = 16
    MANAGE_USERS = 32
    ADMIN = 64


class Role(db.Model):
    """Role model for RBAC."""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    permissions = db.Column(db.Integer, default=0, nullable=False)
    description = db.Column(db.String(256))
    
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
    
    def has_permission(self, perm):
        """Check if role has a specific permission."""
        return self.permissions & perm == perm
    
    def add_permission(self, perm):
        """Add a permission to the role."""
        if not self.has_permission(perm):
            self.permissions += perm
    
    def remove_permission(self, perm):
        """Remove a permission from the role."""
        if self.has_permission(perm):
            self.permissions -= perm
    
    def reset_permissions(self):
        """Reset all permissions."""
        self.permissions = 0
    
    @staticmethod
    def insert_roles():
        """Insert default roles into the database."""
        roles = {
            'Viewer': [
                Permission.VIEW_REPOS,
                Permission.VIEW_WORKFLOWS,
                Permission.VIEW_RUNS
            ],
            'LeadDeveloper': [
                Permission.VIEW_REPOS,
                Permission.VIEW_WORKFLOWS,
                Permission.VIEW_RUNS,
                Permission.DISPATCH_WORKFLOW
            ],
            'GlobalAdmin': [
                Permission.VIEW_REPOS,
                Permission.VIEW_WORKFLOWS,
                Permission.VIEW_RUNS,
                Permission.DISPATCH_WORKFLOW,
                Permission.MANAGE_APPROVALS,
                Permission.MANAGE_USERS,
                Permission.ADMIN
            ]
        }
        
        descriptions = {
            'Viewer': 'Read-only access to repositories, workflows, and runs',
            'LeadDeveloper': 'Can view and dispatch workflows',
            'GlobalAdmin': 'Full administrative access'
        }
        
        for role_name, perms in roles.items():
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name, description=descriptions.get(role_name))
            role.reset_permissions()
            for perm in perms:
                role.add_permission(perm)
            db.session.add(role)
        
        db.session.commit()
    
    def __repr__(self):
        return f'<Role {self.name}>'
