"""
Azure Function: Trigger Workflow

This function triggers a workflow_dispatch event in a GitHub repository.
It is called after an approval is granted to initiate the approved workflow.

Expected Request Payload:
{
    "repository": "owner/repo",
    "workflow_id": "deploy.yml",  // Can be workflow ID or filename
    "ref": "main",                 // Branch/tag to run workflow on
    "inputs": {                    // Optional workflow inputs
        "environment": "production",
        "version": "1.2.3"
    }
}

Response:
{
    "success": true,
    "workflow_run_id": "12345",
    "message": "Workflow triggered successfully"
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
    Trigger a GitHub workflow_dispatch event.
    
    This function:
    1. Validates the incoming request
    2. Authenticates with GitHub using a PAT
    3. Triggers the workflow_dispatch event via GitHub API
    4. Returns the workflow run information
    """
    logging.info('Trigger workflow function called')

    try:
        # Parse request body
        req_body = req.get_json()
        
        # Validate required fields
        required_fields = ['repository', 'workflow_id', 'ref']
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
        
        # Extract parameters
        repository = req_body['repository']
        workflow_id = req_body['workflow_id']
        ref = req_body['ref']
        inputs = req_body.get('inputs', {})
        
        # Validate repository format (should be owner/repo)
        if '/' not in repository:
            return func.HttpResponse(
                json.dumps({
                    "error": "Invalid repository format",
                    "details": "Repository must be in format 'owner/repo'"
                }),
                status_code=400,
                mimetype="application/json"
            )
        
        # Get GitHub token from environment
        github_token = os.environ.get('GITHUB_TOKEN')
        
        if not github_token:
            logging.error('GITHUB_TOKEN not configured')
            return func.HttpResponse(
                json.dumps({
                    "error": "Function not properly configured",
                    "details": "GITHUB_TOKEN environment variable not set"
                }),
                status_code=500,
                mimetype="application/json"
            )
        
        # Prepare GitHub API request
        api_url = f'https://api.github.com/repos/{repository}/actions/workflows/{workflow_id}/dispatches'
        
        headers = {
            'Authorization': f'Bearer {github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
        
        payload = {
            'ref': ref,
            'inputs': inputs
        }
        
        logging.info(f'Triggering workflow {workflow_id} in {repository} on ref {ref}')
        
        # Trigger the workflow
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 204:
            # Success - workflow triggered (GitHub returns 204 No Content)
            logging.info(f'Workflow triggered successfully: {workflow_id} in {repository}')
            
            # Try to get the latest run ID for this workflow
            # Note: There may be a slight delay before the run appears
            runs_url = f'https://api.github.com/repos/{repository}/actions/workflows/{workflow_id}/runs'
            runs_response = requests.get(
                runs_url,
                headers=headers,
                params={'per_page': 1},
                timeout=30
            )
            
            workflow_run_id = None
            if runs_response.status_code == 200:
                runs_data = runs_response.json()
                if runs_data.get('workflow_runs'):
                    workflow_run_id = runs_data['workflow_runs'][0]['id']
            
            return func.HttpResponse(
                json.dumps({
                    "success": True,
                    "workflow_run_id": workflow_run_id,
                    "message": f"Workflow '{workflow_id}' triggered successfully in {repository}",
                    "repository": repository,
                    "workflow": workflow_id,
                    "ref": ref
                }),
                status_code=200,
                mimetype="application/json"
            )
        elif response.status_code == 404:
            # Workflow not found
            logging.error(f'Workflow not found: {workflow_id} in {repository}')
            return func.HttpResponse(
                json.dumps({
                    "error": "Workflow not found",
                    "details": f"Workflow '{workflow_id}' not found in repository '{repository}'"
                }),
                status_code=404,
                mimetype="application/json"
            )
        elif response.status_code == 422:
            # Validation error (e.g., workflow doesn't have workflow_dispatch trigger)
            logging.error(f'Workflow validation error: {response.text}')
            return func.HttpResponse(
                json.dumps({
                    "error": "Workflow validation failed",
                    "details": "Workflow may not have workflow_dispatch trigger configured"
                }),
                status_code=422,
                mimetype="application/json"
            )
        else:
            # Other error
            logging.error(f'GitHub API error: {response.status_code} - {response.text}')
            return func.HttpResponse(
                json.dumps({
                    "error": "Failed to trigger workflow",
                    "status_code": response.status_code,
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
        logging.error(f'Error communicating with GitHub API: {str(e)}')
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
