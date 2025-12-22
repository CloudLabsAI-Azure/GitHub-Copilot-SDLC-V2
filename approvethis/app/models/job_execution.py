"""Job Execution model for tracking job runs."""
from datetime import datetime
from app.extensions import db


class ExecutionStatus:
    """Execution status constants."""
    PENDING_APPROVAL = 'pending_approval'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    QUEUED = 'queued'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


class JobExecution(db.Model):
    """Job execution model - tracks job runs."""
    __tablename__ = 'job_executions'
    
    id = db.Column(db.Integer, primary_key=True)
    job_definition_id = db.Column(db.Integer, db.ForeignKey('job_definitions.id'), nullable=False)
    inputs = db.Column(db.Text)  # JSON inputs
    status = db.Column(db.String(64), default=ExecutionStatus.QUEUED, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    requested_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approved_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_at = db.Column(db.DateTime)
    rejection_reason = db.Column(db.Text)
    result = db.Column(db.Text)  # JSON execution output
    error_message = db.Column(db.Text)
    external_id = db.Column(db.String(256))  # ID in external system
    external_url = db.Column(db.String(512))  # URL to view execution
    github_run_id = db.Column(db.Integer)  # For GitHub Actions
    
    requester = db.relationship('User', foreign_keys=[requested_by_id], backref='job_executions')
    approver = db.relationship('User', foreign_keys=[approved_by_id], backref='approved_executions')
    
    def to_dict(self):
        """Convert execution to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'job_definition_id': self.job_definition_id,
            'job_name': self.job_definition.name if self.job_definition else None,
            'inputs': self.inputs,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'requested_by': self.requester.username if self.requester else None,
            'approved_by': self.approver.username if self.approver else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'rejection_reason': self.rejection_reason,
            'result': self.result,
            'error_message': self.error_message,
            'external_id': self.external_id,
            'external_url': self.external_url,
            'github_run_id': self.github_run_id
        }
    
    def __repr__(self):
        return f'<JobExecution {self.id} - {self.status}>'
