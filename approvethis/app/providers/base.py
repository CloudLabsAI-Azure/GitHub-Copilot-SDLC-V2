"""Base Source Control Provider abstract class.

This module defines the abstract interface that all source control providers
must implement. This allows for platform-agnostic code that can work with
GitHub, GitLab, Bitbucket, Azure DevOps, or any other source control platform.
"""
from abc import ABC, abstractmethod


class SourceControlProvider(ABC):
    """Abstract base class for source control API providers.
    
    This interface defines the common operations that any source control
    platform must support for workflow/pipeline management.
    """
    
    @abstractmethod
    def list_repositories(self):
        """
        List all accessible repositories.
        
        Returns:
            list[dict]: List of repository dictionaries with at minimum:
                - id: Unique identifier
                - name: Repository name
                - full_name: Full repository path (e.g., owner/repo)
        """
        pass
    
    @abstractmethod
    def list_workflows(self, owner, repo):
        """
        List workflows/pipelines for a repository.
        
        Args:
            owner (str): Repository owner/organization
            repo (str): Repository name
            
        Returns:
            list[dict]: List of workflow dictionaries with at minimum:
                - id: Unique identifier
                - name: Workflow name
                - path: Path to workflow definition file
        """
        pass
    
    @abstractmethod
    def list_workflow_runs(self, owner, repo, workflow_id=None):
        """
        List workflow/pipeline runs for a repository.
        
        Args:
            owner (str): Repository owner/organization
            repo (str): Repository name
            workflow_id (str, optional): Filter by workflow ID
            
        Returns:
            list[dict]: List of workflow run dictionaries with at minimum:
                - id: Unique identifier
                - status: Current status
                - conclusion: Final result (if completed)
        """
        pass
    
    @abstractmethod
    def get_workflow_run(self, owner, repo, run_id):
        """
        Get detailed information about a workflow/pipeline run.
        
        Args:
            owner (str): Repository owner/organization
            repo (str): Repository name
            run_id (int): Workflow run ID
            
        Returns:
            dict: Workflow run details including jobs and steps
        """
        pass
    
    @abstractmethod
    def dispatch_workflow(self, owner, repo, workflow_id, ref, inputs):
        """
        Dispatch/trigger a workflow or pipeline.
        
        Args:
            owner (str): Repository owner/organization
            repo (str): Repository name
            workflow_id (str): Workflow ID or filename
            ref (str): Git reference (branch, tag, or SHA)
            inputs (dict): Workflow inputs/parameters
            
        Returns:
            dict: Dispatch result with at minimum:
                - success: Boolean indicating success
                - message: Human-readable message
        """
        pass
