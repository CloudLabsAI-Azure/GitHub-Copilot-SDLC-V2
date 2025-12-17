"""Base GitHub Provider abstract class."""
from abc import ABC, abstractmethod


class GitHubProvider(ABC):
    """Abstract base class for GitHub API providers."""
    
    @abstractmethod
    def list_repositories(self):
        """
        List all accessible repositories.
        
        Returns:
            list[dict]: List of repository dictionaries
        """
        pass
    
    @abstractmethod
    def list_workflows(self, owner, repo):
        """
        List workflows for a repository.
        
        Args:
            owner (str): Repository owner
            repo (str): Repository name
            
        Returns:
            list[dict]: List of workflow dictionaries
        """
        pass
    
    @abstractmethod
    def list_workflow_runs(self, owner, repo, workflow_id=None):
        """
        List workflow runs for a repository.
        
        Args:
            owner (str): Repository owner
            repo (str): Repository name
            workflow_id (str, optional): Filter by workflow ID
            
        Returns:
            list[dict]: List of workflow run dictionaries
        """
        pass
    
    @abstractmethod
    def get_workflow_run(self, owner, repo, run_id):
        """
        Get detailed information about a workflow run.
        
        Args:
            owner (str): Repository owner
            repo (str): Repository name
            run_id (int): Workflow run ID
            
        Returns:
            dict: Workflow run details including jobs and steps
        """
        pass
    
    @abstractmethod
    def dispatch_workflow(self, owner, repo, workflow_id, ref, inputs):
        """
        Dispatch a workflow.
        
        Args:
            owner (str): Repository owner
            repo (str): Repository name
            workflow_id (str): Workflow ID or filename
            ref (str): Git reference (branch, tag, or SHA)
            inputs (dict): Workflow inputs
            
        Returns:
            dict: Dispatch result
        """
        pass
