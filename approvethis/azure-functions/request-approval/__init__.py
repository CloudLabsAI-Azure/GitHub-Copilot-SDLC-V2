"""
Azure Function: Request Approval

This function receives workflow dispatch requests from GitHub Actions
and forwards them to the ApproveThis application for approval.

Expected Request Payload from GitHub Actions:
{
    "workflow": "deploy-production",
    "repository": "org/repo",
    "branch": "main",
    "requestor": "username",
    "run_id": "12345",
    "callback_url": "https://api.github.com/repos/org/repo/actions/runs/12345"
}

Response to GitHub Actions:
{
    "approval_id": "uuid",
    "status": "pending",
    "message": "Approval request submitted successfully"
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
    Process approval request from GitHub Actions.
    
    This function:
    1. Validates the incoming request from GitHub Actions
    2. Forwards the approval request to ApproveThis application
    3. Returns the approval request ID to GitHub Actions
    """
    logging.info('Request approval function triggered')

    try:
        # Parse request body
        req_body = req.get_json()
        
        # Validate required fields
        required_fields = ['workflow', 'repository', 'branch', 'requestor', 'run_id']
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
        
        # Get ApproveThis API endpoint from environment
        approvethis_url = os.environ.get('APPROVETHIS_API_URL')
        approvethis_api_key = os.environ.get('APPROVETHIS_API_KEY')
        
        if not approvethis_url:
            logging.error('APPROVETHIS_API_URL not configured')
            return func.HttpResponse(
                json.dumps({
                    "error": "Function not properly configured"
                }),
                status_code=500,
                mimetype="application/json"
            )
        
        # Prepare payload for ApproveThis
        approval_payload = {
            "workflow_name": req_body['workflow'],
            "repository": req_body['repository'],
            "branch": req_body['branch'],
            "requested_by": req_body['requestor'],
            "github_run_id": req_body['run_id'],
            "callback_url": req_body.get('callback_url', ''),
            "inputs": req_body.get('inputs', {}),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Forward request to ApproveThis application
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': approvethis_api_key
        } if approvethis_api_key else {
            'Content-Type': 'application/json'
        }
        
        logging.info(f'Forwarding approval request to ApproveThis: {approvethis_url}')
        
        response = requests.post(
            f'{approvethis_url}/api/approvals/requests',
            json=approval_payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 201:
            # Successfully created approval request
            approval_data = response.json()
            logging.info(f'Approval request created: {approval_data.get("id")}')
            
            return func.HttpResponse(
                json.dumps({
                    "approval_id": approval_data.get('id'),
                    "status": "pending",
                    "message": "Approval request submitted successfully"
                }),
                status_code=201,
                mimetype="application/json"
            )
        else:
            # Error from ApproveThis
            logging.error(f'ApproveThis returned error: {response.status_code}')
            return func.HttpResponse(
                json.dumps({
                    "error": "Failed to create approval request",
                    "details": response.text
                }),
                status_code=response.status_code,
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
        logging.error(f'Error communicating with ApproveThis: {str(e)}')
        return func.HttpResponse(
            json.dumps({
                "error": "Failed to communicate with ApproveThis",
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
