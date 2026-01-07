"""
Azure Function: Approval Response

This function receives approval/denial decisions from the ApproveThis application
and communicates them back to the GitHub Actions workflow run.

Expected Request Payload from ApproveThis:
{
    "approval_id": "uuid",
    "status": "approved" | "denied",
    "approved_by": "username",
    "reason": "optional reason for denial",
    "github_run_id": "12345",
    "callback_url": "https://api.github.com/repos/org/repo/actions/runs/12345"
}

Response to ApproveThis:
{
    "success": true,
    "message": "GitHub Actions notified successfully"
}
"""

import logging
import json
import os
import requests
from datetime import datetime
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Process approval response from ApproveThis application.
    
    This function:
    1. Validates the approval/denial decision from ApproveThis
    2. Communicates the decision back to GitHub Actions
    3. Updates the workflow run status or triggers continuation
    """
    logging.info('Approval response function triggered')

    try:
        # Parse request body
        req_body = req.get_json()
        
        # Validate required fields
        required_fields = ['approval_id', 'status', 'github_run_id']
        missing_fields = [field for field in required_fields if field not in req_body]
        
        if missing_fields:
            return func.HttpResponse(
                json.dumps({
                    "error": "Missing required fields",
                    "missing": missing_fields
                }),
                status_code=400,
                mimetype="application/json"
            )
        
        # Validate status
        if req_body['status'] not in ['approved', 'denied']:
            return func.HttpResponse(
                json.dumps({
                    "error": "Invalid status",
                    "details": "Status must be 'approved' or 'denied'"
                }),
                status_code=400,
                mimetype="application/json"
            )
        
        # Get GitHub configuration from environment
        github_token = os.environ.get('GITHUB_TOKEN')
        
        if not github_token:
            logging.error('GITHUB_TOKEN not configured')
            return func.HttpResponse(
                json.dumps({
                    "error": "Function not properly configured"
                }),
                status_code=500,
                mimetype="application/json"
            )
        
        # Prepare the response for GitHub
        approval_status = req_body['status']
        approval_id = req_body['approval_id']
        run_id = req_body['github_run_id']
        
        logging.info(f'Processing {approval_status} for approval {approval_id}, run {run_id}')
        
        # For approved requests, we could trigger a workflow_dispatch or update a deployment status
        # For denied requests, we could cancel the workflow run or update status
        
        callback_url = req_body.get('callback_url', '')
        
        if callback_url:
            # Use the callback URL to communicate with GitHub
            headers = {
                'Authorization': f'Bearer {github_token}',
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json'
            }
            
            # Prepare status update
            status_payload = {
                "state": "success" if approval_status == "approved" else "failure",
                "description": (
                    f"Approved by {req_body.get('approved_by', 'unknown')}"
                    if approval_status == "approved"
                    else f"Denied: {req_body.get('reason', 'No reason provided')}"
                ),
                "context": "ApproveThis/approval"
            }
            
            # Note: In a real implementation, you would use the GitHub API
            # to either continue the workflow, update status, or cancel the run
            # The exact mechanism depends on how the workflow is structured
            
            logging.info(f'Would notify GitHub at {callback_url} with status: {approval_status}')
            
            # For Lab 7, we'll document this approach without making actual GitHub API calls
            # since the workflow integration will be built in Lab 8
            
        # Return success response to ApproveThis
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "message": f"Approval {approval_status} processed for run {run_id}",
                "approval_id": approval_id,
                "github_run_id": run_id,
                "status": approval_status
            }),
            status_code=200,
            mimetype="application/json"
        )
            
    except ValueError as e:
        logging.error(f'Invalid JSON in request: {str(e)}')
        return func.HttpResponse(
            json.dumps({
                "error": "Invalid request body",
                "details": str(e)
            }),
            status_code=400,
            mimetype="application/json"
        )
    except requests.RequestException as e:
        logging.error(f'Error communicating with GitHub: {str(e)}')
        return func.HttpResponse(
            json.dumps({
                "error": "Failed to communicate with GitHub",
                "details": str(e)
            }),
            status_code=502,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f'Unexpected error: {str(e)}')
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "details": str(e)
            }),
            status_code=500,
            mimetype="application/json"
        )
