"""Job Definition model for executable jobs."""
from app.extensions import db
from app.models.role import Permission


class JobDefinition(db.Model):
    """Job definition model - defines executable jobs."""
    __tablename__ = 'job_definitions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(64))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    execution_target_id = db.Column(db.Integer, db.ForeignKey('execution_targets.id'))
    workflow_id = db.Column(db.String(128))  # For GitHub Actions targets
    default_ref = db.Column(db.String(64), default='main')
    input_schema = db.Column(db.Text)  # JSON schema for inputs
    default_inputs = db.Column(db.Text)  # JSON default values
    required_permission = db.Column(db.Integer, default=Permission.DISPATCH_WORKFLOW)
    requires_approval = db.Column(db.Boolean, default=False, nullable=False)
    approval_roles = db.Column(db.Text)  # JSON array of role names
    
    executions = db.relationship('JobExecution', backref='job_definition', lazy='dynamic')
    
    @staticmethod
    def seed_jobs():
        """Create default job definitions."""
        import json
        from app.models.execution_target import ExecutionTarget
        
        # Get execution targets
        github_infra = ExecutionTarget.query.filter_by(name='Infrastructure GitHub Actions').first()
        azure_function = ExecutionTarget.query.filter_by(name='Azure Terraform Function').first()
        
        if not github_infra or not azure_function:
            # Targets need to be seeded first
            return
        
        jobs = [
            {
                'name': 'Terraform Plan',
                'description': 'Run Terraform plan to preview infrastructure changes',
                'category': 'infrastructure',
                'execution_target_id': github_infra.id,
                'workflow_id': '301',
                'default_ref': 'main',
                'input_schema': json.dumps({
                    'environment': {
                        'type': 'select',
                        'label': 'Environment',
                        'required': True,
                        'options': ['dev', 'staging', 'production']
                    }
                }),
                'default_inputs': json.dumps({'environment': 'dev'}),
                'required_permission': Permission.DISPATCH_WORKFLOW,
                'requires_approval': False,
                'approval_roles': json.dumps([])
            },
            {
                'name': 'Terraform Apply',
                'description': 'Apply Terraform changes to infrastructure',
                'category': 'infrastructure',
                'execution_target_id': github_infra.id,
                'workflow_id': '302',
                'default_ref': 'main',
                'input_schema': json.dumps({
                    'environment': {
                        'type': 'select',
                        'label': 'Environment',
                        'required': True,
                        'options': ['dev', 'staging', 'production']
                    },
                    'auto_approve': {
                        'type': 'checkbox',
                        'label': 'Auto-approve',
                        'required': False,
                        'default': False
                    }
                }),
                'default_inputs': json.dumps({'environment': 'dev', 'auto_approve': False}),
                'required_permission': Permission.DISPATCH_WORKFLOW,
                'requires_approval': True,
                'approval_roles': json.dumps(['GlobalAdmin'])
            },
            {
                'name': 'Azure Function Terraform',
                'description': 'Execute Terraform via Azure Function',
                'category': 'infrastructure',
                'execution_target_id': azure_function.id,
                'workflow_id': None,
                'default_ref': 'main',
                'input_schema': json.dumps({
                    'action': {
                        'type': 'select',
                        'label': 'Action',
                        'required': True,
                        'options': ['plan', 'apply', 'destroy']
                    },
                    'environment': {
                        'type': 'select',
                        'label': 'Environment',
                        'required': True,
                        'options': ['dev', 'staging', 'production']
                    }
                }),
                'default_inputs': json.dumps({'action': 'plan', 'environment': 'dev'}),
                'required_permission': Permission.DISPATCH_WORKFLOW,
                'requires_approval': True,
                'approval_roles': json.dumps(['GlobalAdmin'])
            }
        ]
        
        for job_data in jobs:
            job = JobDefinition.query.filter_by(name=job_data['name']).first()
            if job is None:
                job = JobDefinition(**job_data)
                db.session.add(job)
        
        db.session.commit()
    
    def __repr__(self):
        return f'<JobDefinition {self.name}>'
