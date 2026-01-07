# ApproveThis Azure Functions

This directory contains Azure Functions that facilitate communication between GitHub Actions and the ApproveThis application for the approval workflow system.

## Functions

### 1. request-approval

**Endpoint:** `POST /api/approval/request`

Receives workflow dispatch requests from GitHub Actions and forwards them to the ApproveThis application for approval.

**Request Payload:**
```json
{
    "workflow": "deploy-production",
    "repository": "org/repo",
    "branch": "main",
    "requestor": "username",
    "run_id": "12345",
    "callback_url": "https://api.github.com/repos/org/repo/actions/runs/12345",
    "inputs": {}
}
```

**Response:**
```json
{
    "approval_id": "uuid",
    "status": "pending",
    "message": "Approval request submitted successfully"
}
```

### 2. approval-response

**Endpoint:** `POST /api/approval/response`

Receives approval/denial decisions from the ApproveThis application and communicates them back to GitHub Actions.

**Request Payload:**
```json
{
    "approval_id": "uuid",
    "status": "approved",
    "approved_by": "username",
    "reason": "optional reason",
    "github_run_id": "12345",
    "callback_url": "https://api.github.com/repos/org/repo/actions/runs/12345"
}
```

**Response:**
```json
{
    "success": true,
    "message": "GitHub Actions notified successfully",
    "approval_id": "uuid",
    "github_run_id": "12345",
    "status": "approved"
}
```

### 3. trigger-workflow

**Endpoint:** `POST /api/workflow/trigger`

Triggers a workflow_dispatch event in a GitHub repository. This is called after an approval is granted to initiate the approved workflow.

**Request Payload:**
```json
{
    "repository": "owner/repo",
    "workflow_id": "deploy.yml",
    "ref": "main",
    "inputs": {
        "environment": "production",
        "version": "1.2.3"
    }
}
```

**Response:**
```json
{
    "success": true,
    "workflow_run_id": "12345",
    "message": "Workflow 'deploy.yml' triggered successfully in owner/repo",
    "repository": "owner/repo",
    "workflow": "deploy.yml",
    "ref": "main"
}
```

## Configuration

The functions require the following environment variables:

- `APPROVETHIS_API_URL`: The base URL of the ApproveThis application API
- `APPROVETHIS_API_KEY`: API key for authenticating with ApproveThis (optional)
- `GITHUB_TOKEN`: GitHub Personal Access Token for API communication

These are configured via Application Settings in the Azure Function App.

## Development

### Local Development

1. Install Azure Functions Core Tools:
   ```bash
   npm install -g azure-functions-core-tools@4
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `local.settings.json`:
   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "AzureWebJobsStorage": "UseDevelopmentStorage=true",
       "FUNCTIONS_WORKER_RUNTIME": "python",
       "APPROVETHIS_API_URL": "http://localhost:5000",
       "APPROVETHIS_API_KEY": "your-api-key",
       "GITHUB_TOKEN": "your-github-token"
     }
   }
   ```

4. Run locally:
   ```bash
   func start
   ```

### Testing

Test the request-approval function:
```bash
curl -X POST http://localhost:7071/api/approval/request \
  -H "Content-Type: application/json" \
  -d '{
    "workflow": "deploy-production",
    "repository": "org/repo",
    "branch": "main",
    "requestor": "username",
    "run_id": "12345"
  }'
```

Test the approval-response function:
```bash
curl -X POST http://localhost:7071/api/approval/response \
  -H "Content-Type: application/json" \
  -d '{
    "approval_id": "uuid",
    "status": "approved",
    "approved_by": "admin",
    "github_run_id": "12345"
  }'
```

Test the trigger-workflow function:
```bash
curl -X POST http://localhost:7071/api/workflow/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "repository": "owner/repo",
    "workflow_id": "deploy.yml",
    "ref": "main",
    "inputs": {
      "environment": "production"
    }
  }'
```

## Deployment

The functions are deployed using:
1. Terraform (provisions the Function App infrastructure)
2. Azure Functions VS Code extension (deploys the function code)

See Lab 7 instructions for detailed deployment steps.

## Architecture

```
GitHub Actions Workflow (waiting)
        |
        | (1) Request approval
        v
request-approval Function
        |
        | (2) Forward request
        v
ApproveThis Application
        |
        | (3) User approves/denies
        v
approval-response Function
        |
        | (4a) If approved
        v
trigger-workflow Function
        |
        | (4b) Trigger workflow_dispatch
        v
GitHub Actions Workflow (continues)
```

## Security

- Functions use function-level authentication (`authLevel: "function"`)
- Communication with ApproveThis uses API key authentication
- Communication with GitHub uses Personal Access Token
- All sensitive credentials are stored in Azure Key Vault (in production)

## Logging

Functions log to Application Insights for monitoring and debugging:
- Request payloads (sanitized)
- Response status codes
- Errors and exceptions
- Integration points (ApproveThis, GitHub API)
