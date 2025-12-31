"""GitHub-specific Provider abstract class.

This module defines the GitHub-specific interface that extends the base
SourceControlProvider. It can include GitHub-specific methods that don't
apply to other platforms.
"""
from abc import abstractmethod
from app.providers.base import SourceControlProvider


class GitHubProvider(SourceControlProvider):
    """Abstract base class for GitHub API providers.
    
    Extends SourceControlProvider with GitHub-specific functionality.
    All GitHub implementations (real API, mock, etc.) should extend this class.
    """
    
    # GitHub-specific methods can be added here as needed.
    # For example:
    
    @abstractmethod
    def get_rate_limit(self):
        """
        Get current GitHub API rate limit status.
        
        Returns:
            dict: Rate limit information with:
                - limit: Maximum requests allowed
                - remaining: Requests remaining
                - reset: Unix timestamp when limit resets
        """
        pass
    
    # Additional GitHub-specific methods could include:
    # - get_actions_billing()
    # - list_workflow_artifacts()
    # - download_workflow_logs()
    # - cancel_workflow_run()
    # - re_run_workflow()
