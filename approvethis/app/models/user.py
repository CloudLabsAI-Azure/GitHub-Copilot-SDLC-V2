"""User model with Flask-Login integration."""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.role import Permission


class User(UserMixin, db.Model):
    """User model."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    dispatch_requests = db.relationship('DispatchRequest', backref='requester', lazy='dynamic')
    
    def set_password(self, password):
        """Set password hash."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def can(self, perm):
        """Check if user has a specific permission."""
        return self.role is not None and self.role.has_permission(perm)
    
    def is_admin(self):
        """Check if user is an admin."""
        return self.can(Permission.ADMIN)
    
    @staticmethod
    def insert_default_users():
        """Insert default users for development."""
        from app.models.role import Role
        
        users = [
            {
                'username': 'viewer',
                'password': 'viewer123',
                'email': 'viewer@example.com',
                'role': 'Viewer'
            },
            {
                'username': 'developer',
                'password': 'developer123',
                'email': 'developer@example.com',
                'role': 'LeadDeveloper'
            },
            {
                'username': 'admin',
                'password': 'admin123',
                'email': 'admin@example.com',
                'role': 'GlobalAdmin'
            }
        ]
        
        for user_data in users:
            user = User.query.filter_by(username=user_data['username']).first()
            if user is None:
                role = Role.query.filter_by(name=user_data['role']).first()
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    role=role
                )
                user.set_password(user_data['password'])
                db.session.add(user)
        
        db.session.commit()
    
    def __repr__(self):
        return f'<User {self.username}>'
