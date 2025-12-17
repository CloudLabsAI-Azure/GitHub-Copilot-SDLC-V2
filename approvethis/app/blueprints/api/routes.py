"""API blueprint for REST endpoints."""
from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.providers import get_provider
from app.models import Permission
from app.utils import permission_required

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/repos')
@login_required
@permission_required(Permission.VIEW_REPOS)
def list_repos():
    """List all repositories."""
    provider = get_provider()
    repos = provider.list_repositories()
    return jsonify({'repositories': repos})


@api_bp.route('/repos/<owner>/<repo>/workflows')
@login_required
@permission_required(Permission.VIEW_WORKFLOWS)
def list_workflows(owner, repo):
    """List workflows for a repository."""
    provider = get_provider()
    workflows = provider.list_workflows(owner, repo)
    return jsonify({'workflows': workflows})


@api_bp.route('/repos/<owner>/<repo>/runs')
@login_required
@permission_required(Permission.VIEW_RUNS)
def list_runs(owner, repo):
    """List workflow runs for a repository."""
    provider = get_provider()
    workflow_id = request.args.get('workflow_id')
    runs = provider.list_workflow_runs(owner, repo, workflow_id)
    return jsonify({'workflow_runs': runs})


@api_bp.route('/repos/<owner>/<repo>/runs/<int:run_id>')
@login_required
@permission_required(Permission.VIEW_RUNS)
def get_run(owner, repo, run_id):
    """Get detailed information about a workflow run."""
    provider = get_provider()
    run = provider.get_workflow_run(owner, repo, run_id)
    
    if not run:
        return jsonify({'error': 'Workflow run not found'}), 404
    
    return jsonify(run)


@api_bp.route('/repos/<owner>/<repo>/workflows/<workflow_id>/dispatch', methods=['POST'])
@login_required
@permission_required(Permission.DISPATCH_WORKFLOW)
def dispatch_workflow(owner, repo, workflow_id):
    """Dispatch a workflow."""
    provider = get_provider()
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    ref = data.get('ref')
    inputs = data.get('inputs', {})
    
    if not ref:
        return jsonify({'error': 'ref is required'}), 400
    
    try:
        result = provider.dispatch_workflow(owner, repo, workflow_id, ref, inputs)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.errorhandler(401)
def unauthorized(e):
    """Handle 401 errors."""
    return jsonify({'error': 'Unauthorized'}), 401


@api_bp.errorhandler(403)
def forbidden(e):
    """Handle 403 errors."""
    return jsonify({'error': 'Forbidden - insufficient permissions'}), 403


@api_bp.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404
