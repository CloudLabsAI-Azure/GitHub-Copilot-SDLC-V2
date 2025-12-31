"""GitHub Provider (placeholder for future implementation)."""
from app.providers.github_base import GitHubProvider


class RealGitHubProvider(GitHubProvider):
    """Real GitHub API provider (to be implemented)."""
    
    def __init__(self, token=None):
        """Initialize with GitHub token."""
        self.token = token
        # TODO: Initialize GitHub API client
    
    def list_repositories(self):
        """List repositories via GitHub API."""
        raise NotImplementedError("Real GitHub provider not yet implemented")
    
    def list_workflows(self, owner, repo):
        """List workflows via GitHub API."""
        raise NotImplementedError("Real GitHub provider not yet implemented")
    
    def list_workflow_runs(self, owner, repo, workflow_id=None):
        """List workflow runs via GitHub API."""
        raise NotImplementedError("Real GitHub provider not yet implemented")
    
    def get_workflow_run(self, owner, repo, run_id):
        """Get workflow run details via GitHub API."""
        raise NotImplementedError("Real GitHub provider not yet implemented")
    
    def dispatch_workflow(self, owner, repo, workflow_id, ref, inputs):
        """Dispatch workflow via GitHub API."""
        raise NotImplementedError("Real GitHub provider not yet implemented")
    
    def get_rate_limit(self):
        """Get rate limit via GitHub API."""
        raise NotImplementedError("Real GitHub provider not yet implemented")
