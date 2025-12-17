"""Mock GitHub Provider implementation."""
import json
from pathlib import Path
from app.providers.base import GitHubProvider


class MockGitHubProvider(GitHubProvider):
    """Mock implementation of GitHub Provider using JSON files."""
    
    def __init__(self):
        """Initialize mock provider with data directory."""
        self.data_dir = Path(__file__).parent.parent / 'mock_data'
    
    def _load_json(self, filename):
        """Load JSON data from file."""
        filepath = self.data_dir / filename
        if filepath.exists():
            with open(filepath, 'r') as f:
                return json.load(f)
        return None
    
    def list_repositories(self):
        """List all repositories from mock data."""
        data = self._load_json('repositories.json')
        return data.get('repositories', []) if data else []
    
    def list_workflows(self, owner, repo):
        """List workflows for a repository from mock data."""
        data = self._load_json('workflows.json')
        if not data:
            return []
        
        repo_key = f"{owner}/{repo}"
        workflows = data.get(repo_key, [])
        return workflows
    
    def list_workflow_runs(self, owner, repo, workflow_id=None):
        """List workflow runs from mock data."""
        data = self._load_json('workflow_runs.json')
        if not data:
            return []
        
        runs = data.get('workflow_runs', [])
        
        # Filter by repo
        runs = [r for r in runs if r.get('repository', {}).get('full_name') == f"{owner}/{repo}"]
        
        # Filter by workflow_id if provided
        if workflow_id:
            runs = [r for r in runs if str(r.get('workflow_id')) == str(workflow_id)]
        
        return runs
    
    def get_workflow_run(self, owner, repo, run_id):
        """Get detailed workflow run information."""
        # First check if we have a detailed file
        detail_file = f"run_{run_id}.json"
        detailed_data = self._load_json(f'workflow_run_details/{detail_file}')
        
        if detailed_data:
            return detailed_data
        
        # Fallback to basic run data
        runs = self.list_workflow_runs(owner, repo)
        for run in runs:
            if run.get('id') == run_id:
                return run
        
        return None
    
    def dispatch_workflow(self, owner, repo, workflow_id, ref, inputs):
        """
        Dispatch a workflow (mock implementation).
        
        Creates a DispatchRequest in the database and returns success.
        """
        from app.models.dispatch_request import DispatchRequest
        from app.extensions import db
        from flask_login import current_user
        
        # Find workflow name
        workflows = self.list_workflows(owner, repo)
        workflow_name = None
        for workflow in workflows:
            if str(workflow.get('id')) == str(workflow_id) or workflow.get('path', '').endswith(workflow_id):
                workflow_name = workflow.get('name')
                break
        
        # Create dispatch request
        dispatch_request = DispatchRequest(
            owner=owner,
            repo=repo,
            workflow_id=str(workflow_id),
            workflow_name=workflow_name or 'Unknown Workflow',
            ref=ref,
            inputs=json.dumps(inputs) if inputs else None,
            status='success',
            user_id=current_user.id
        )
        
        db.session.add(dispatch_request)
        db.session.commit()
        
        return {
            'success': True,
            'message': 'Workflow dispatch request created successfully',
            'dispatch_request_id': dispatch_request.id
        }
