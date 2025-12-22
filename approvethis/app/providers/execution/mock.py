"""Mock execution provider for testing."""
import uuid
import time
from app.providers.execution.base import ExecutionProvider
from app.models.job_execution import ExecutionStatus


class MockExecutionProvider(ExecutionProvider):
    """Mock execution provider for development and testing."""
    
    # Class-level storage for mock executions
    _executions = {}
    
    def execute(self, target_config, job_config, inputs):
        """Execute a mock job."""
        execution_id = str(uuid.uuid4())
        
        self._executions[execution_id] = {
            'status': ExecutionStatus.RUNNING,
            'created_at': time.time(),
            'inputs': inputs,
            'result': None,
            'error_message': None
        }
        
        return {
            'external_id': execution_id,
            'external_url': f'https://mock-execution.example.com/runs/{execution_id}',
            'status': ExecutionStatus.RUNNING
        }
    
    def get_status(self, target_config, external_id):
        """Get mock execution status."""
        if external_id not in self._executions:
            return {
                'status': ExecutionStatus.FAILED,
                'result': None,
                'error_message': 'Execution not found'
            }
        
        execution = self._executions[external_id]
        elapsed = time.time() - execution['created_at']
        
        # Simulate execution progression
        if elapsed < 5:
            status = ExecutionStatus.RUNNING
        elif elapsed < 10:
            # Randomly succeed or fail
            status = ExecutionStatus.COMPLETED
            execution['status'] = status
            execution['result'] = {
                'output': 'Mock execution completed successfully',
                'duration': elapsed
            }
        else:
            status = execution['status']
        
        return {
            'status': status,
            'result': execution.get('result'),
            'error_message': execution.get('error_message')
        }
    
    def cancel(self, target_config, external_id):
        """Cancel a mock execution."""
        if external_id not in self._executions:
            return {
                'success': False,
                'message': 'Execution not found'
            }
        
        self._executions[external_id]['status'] = ExecutionStatus.CANCELLED
        
        return {
            'success': True,
            'message': 'Execution cancelled'
        }
