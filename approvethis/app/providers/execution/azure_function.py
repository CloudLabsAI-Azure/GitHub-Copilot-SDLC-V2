"""Azure Function execution provider (placeholder for future implementation)."""
from app.providers.execution.base import ExecutionProvider


class AzureFunctionProvider(ExecutionProvider):
    """
    Azure Function execution provider for Terraform.
    
    This provider will call an Azure Function to execute Terraform operations.
    
    Expected Azure Function Contract:
    
    POST /api/terraform
    Request:
        {
            "action": "plan|apply|destroy",
            "environment": "dev|production",
            "inputs": {...}
        }
    
    Response:
        {
            "execution_id": "unique-execution-id",
            "status": "queued|running|completed|failed",
            "message": "Status message"
        }
    
    GET /api/terraform/{execution_id}
    Response:
        {
            "execution_id": "...",
            "status": "queued|running|completed|failed",
            "result": {...},
            "error_message": "Error if failed",
            "logs_url": "URL to logs"
        }
    
    DELETE /api/terraform/{execution_id}
    Response:
        {
            "success": true,
            "message": "Cancellation message"
        }
    """
    
    def execute(self, target_config, job_config, inputs):
        """
        Execute Terraform via Azure Function.
        
        Args:
            target_config (dict): Target configuration with:
                - function_url: Azure Function URL
                - function_key: Optional function key for authentication
            job_config (dict): Job configuration
            inputs (dict): Job inputs
            
        Returns:
            dict: Execution result
            
        Raises:
            NotImplementedError: This provider is not yet implemented
        """
        raise NotImplementedError(
            "Azure Function provider not yet implemented. "
            "This will be implemented in future lab exercises."
        )
    
    def get_status(self, target_config, external_id):
        """
        Get execution status from Azure Function.
        
        Args:
            target_config (dict): Target configuration
            external_id (str): Execution ID from Azure Function
            
        Returns:
            dict: Status result
            
        Raises:
            NotImplementedError: This provider is not yet implemented
        """
        raise NotImplementedError(
            "Azure Function provider not yet implemented. "
            "This will be implemented in future lab exercises."
        )
    
    def cancel(self, target_config, external_id):
        """
        Cancel execution via Azure Function.
        
        Args:
            target_config (dict): Target configuration
            external_id (str): Execution ID from Azure Function
            
        Returns:
            dict: Cancellation result
            
        Raises:
            NotImplementedError: This provider is not yet implemented
        """
        raise NotImplementedError(
            "Azure Function provider not yet implemented. "
            "This will be implemented in future lab exercises."
        )
