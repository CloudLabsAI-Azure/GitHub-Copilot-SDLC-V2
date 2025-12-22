"""Execution provider factory and adapters."""
from app.models.execution_target import ExecutionTargetType
from app.providers.execution.base import ExecutionProvider
from app.providers.execution.mock import MockExecutionProvider
from app.providers.execution.azure_function import AzureFunctionProvider


def get_execution_provider(target_type):
    """
    Factory function to get execution provider by target type.
    
    Args:
        target_type (str): Type of execution target
        
    Returns:
        ExecutionProvider: Provider instance
    """
    if target_type == ExecutionTargetType.GITHUB_ACTIONS:
        return GitHubActionsExecutionAdapter()
    elif target_type == ExecutionTargetType.AZURE_FUNCTION:
        return AzureFunctionProvider()
    elif target_type == ExecutionTargetType.TERRAFORM_CLOUD:
        # Future: Terraform Cloud provider
        raise NotImplementedError("Terraform Cloud provider not yet implemented")
    else:
        # Default to mock provider for development
        return MockExecutionProvider()


class GitHubActionsExecutionAdapter(ExecutionProvider):
    """
    Adapter to wrap GitHub provider for execution interface.
    
    This adapter translates between the ExecutionProvider interface
    and the existing GitHubProvider interface.
    """
    
    def __init__(self):
        """Initialize with GitHub provider."""
        # Import here to avoid circular dependencies
        from app.providers import get_provider
        self.github_provider = get_provider()
    
    def execute(self, target_config, job_config, inputs):
        """
        Execute workflow via GitHub Actions.
        
        Args:
            target_config (dict): Target config with 'owner' and 'repo'
            job_config (dict): Job config with 'workflow_id' and 'default_ref'
            inputs (dict): Workflow inputs
            
        Returns:
            dict: Execution result
        """
        owner = target_config.get('owner')
        repo = target_config.get('repo')
        workflow_id = job_config.get('workflow_id')
        ref = job_config.get('default_ref', 'main')
        
        result = self.github_provider.dispatch_workflow(
            owner=owner,
            repo=repo,
            workflow_id=workflow_id,
            ref=ref,
            inputs=inputs
        )
        
        # Map GitHub result to standard execution result
        return {
            'external_id': result.get('run_id', 'pending'),
            'external_url': result.get('url', ''),
            'status': 'queued'
        }
    
    def get_status(self, target_config, external_id):
        """
        Get workflow run status from GitHub.
        
        Args:
            target_config (dict): Target config with 'owner' and 'repo'
            external_id (str): GitHub run ID
            
        Returns:
            dict: Status result
        """
        if external_id == 'pending':
            return {
                'status': 'queued',
                'result': None,
                'error_message': None
            }
        
        owner = target_config.get('owner')
        repo = target_config.get('repo')
        
        try:
            run = self.github_provider.get_workflow_run(
                owner=owner,
                repo=repo,
                run_id=int(external_id)
            )
            
            # Map GitHub status to our status
            github_status = run.get('status')
            github_conclusion = run.get('conclusion')
            
            if github_status == 'completed':
                if github_conclusion == 'success':
                    status = 'completed'
                elif github_conclusion == 'cancelled':
                    status = 'cancelled'
                else:
                    status = 'failed'
            elif github_status in ['queued', 'waiting']:
                status = 'queued'
            else:
                status = 'running'
            
            return {
                'status': status,
                'result': run if status == 'completed' else None,
                'error_message': github_conclusion if status == 'failed' else None
            }
        except Exception as e:
            return {
                'status': 'failed',
                'result': None,
                'error_message': str(e)
            }
    
    def cancel(self, target_config, external_id):
        """
        Cancel workflow run (not implemented in base GitHub provider).
        
        Args:
            target_config (dict): Target config
            external_id (str): GitHub run ID
            
        Returns:
            dict: Cancellation result
        """
        # GitHub API supports cancellation but our provider doesn't implement it yet
        return {
            'success': False,
            'message': 'Cancellation not yet supported for GitHub Actions'
        }


__all__ = [
    'ExecutionProvider',
    'get_execution_provider',
    'GitHubActionsExecutionAdapter',
    'MockExecutionProvider',
    'AzureFunctionProvider'
]
