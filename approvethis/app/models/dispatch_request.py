"""DispatchRequest model."""
from datetime import datetime
from app.extensions import db


class DispatchRequest(db.Model):
    """Model for tracking workflow dispatch requests."""
    __tablename__ = 'dispatch_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(128), nullable=False)
    repo = db.Column(db.String(128), nullable=False)
    workflow_id = db.Column(db.String(128), nullable=False)
    workflow_name = db.Column(db.String(256))
    ref = db.Column(db.String(128), nullable=False)
    inputs = db.Column(db.Text)
    status = db.Column(db.String(32), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<DispatchRequest {self.owner}/{self.repo}:{self.workflow_name}>'
