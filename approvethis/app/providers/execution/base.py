"""Base execution provider abstract class."""
from abc import ABC, abstractmethod


class ExecutionProvider(ABC):
    """Abstract base class for job execution providers."""
    
    @abstractmethod
    def execute(self, target_config, job_config, inputs):
        """
        Execute a job.
        
        Args:
            target_config (dict): Execution target configuration
            job_config (dict): Job definition configuration
            inputs (dict): Job inputs
            
        Returns:
            dict: Execution result with keys:
                - external_id: ID in the external system
                - external_url: URL to view execution
                - status: Initial status
        """
        pass
    
    @abstractmethod
    def get_status(self, target_config, external_id):
        """
        Get execution status.
        
        Args:
            target_config (dict): Execution target configuration
            external_id (str): External execution ID
            
        Returns:
            dict: Status result with keys:
                - status: Current status
                - result: Execution result (if completed)
                - error_message: Error message (if failed)
        """
        pass
    
    @abstractmethod
    def cancel(self, target_config, external_id):
        """
        Cancel an execution.
        
        Args:
            target_config (dict): Execution target configuration
            external_id (str): External execution ID
            
        Returns:
            dict: Cancellation result with keys:
                - success: Boolean indicating success
                - message: Status message
        """
        pass
