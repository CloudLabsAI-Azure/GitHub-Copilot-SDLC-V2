"""Execution Target model for job execution backends."""
from app.extensions import db


class ExecutionTargetType:
    """Execution target type constants."""
    GITHUB_ACTIONS = 'github_actions'
    AZURE_FUNCTION = 'azure_function'
    TERRAFORM_CLOUD = 'terraform_cloud'


class ExecutionTarget(db.Model):
    """Execution target model - defines where jobs run."""
    __tablename__ = 'execution_targets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.Text)
    target_type = db.Column(db.String(64), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    config = db.Column(db.Text)  # JSON configuration
    
    job_definitions = db.relationship('JobDefinition', backref='execution_target', lazy='dynamic')
    
    @staticmethod
    def seed_targets():
        """Create default execution targets."""
        import json
        
        targets = [
            {
                'name': 'Web App GitHub Actions',
                'description': 'GitHub Actions workflows for web application',
                'target_type': ExecutionTargetType.GITHUB_ACTIONS,
                'is_active': True,
                'config': json.dumps({
                    'owner': 'acme-corp',
                    'repo': 'web-app'
                })
            },
            {
                'name': 'Infrastructure GitHub Actions',
                'description': 'GitHub Actions workflows for infrastructure deployment',
                'target_type': ExecutionTargetType.GITHUB_ACTIONS,
                'is_active': True,
                'config': json.dumps({
                    'owner': 'acme-corp',
                    'repo': 'infrastructure'
                })
            },
            {
                'name': 'Azure Terraform Function',
                'description': 'Azure Function for Terraform execution',
                'target_type': ExecutionTargetType.AZURE_FUNCTION,
                'is_active': True,
                'config': json.dumps({
                    'function_url': 'https://placeholder.azurewebsites.net/api/terraform',
                    'timeout': 300
                })
            }
        ]
        
        for target_data in targets:
            target = ExecutionTarget.query.filter_by(name=target_data['name']).first()
            if target is None:
                target = ExecutionTarget(**target_data)
                db.session.add(target)
        
        db.session.commit()
    
    def __repr__(self):
        return f'<ExecutionTarget {self.name}>'
