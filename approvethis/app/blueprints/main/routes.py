"""Main blueprint for UI routes."""
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from app.providers import get_provider
from app.models import Permission
from app.utils import permission_required

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def index():
    """Dashboard page."""
    provider = get_provider()
    repos = []
    
    if current_user.can(Permission.VIEW_REPOS):
        repos = provider.list_repositories()
    
    return render_template('main/index.html', repos=repos)


@main_bp.route('/repos/<owner>/<repo>/workflows')
@login_required
@permission_required(Permission.VIEW_WORKFLOWS)
def workflows(owner, repo):
    """Workflow list page."""
    provider = get_provider()
    
    # Get repository info
    repos = provider.list_repositories()
    current_repo = None
    for r in repos:
        if r['full_name'] == f"{owner}/{repo}":
            current_repo = r
            break
    
    if not current_repo:
        abort(404)
    
    workflows = provider.list_workflows(owner, repo)
    can_dispatch = current_user.can(Permission.DISPATCH_WORKFLOW)
    
    return render_template('main/workflows.html', 
                         owner=owner, 
                         repo=repo, 
                         current_repo=current_repo,
                         workflows=workflows,
                         can_dispatch=can_dispatch)


@main_bp.route('/repos/<owner>/<repo>/runs')
@login_required
@permission_required(Permission.VIEW_RUNS)
def runs(owner, repo):
    """Workflow runs list page."""
    provider = get_provider()
    
    # Get repository info
    repos = provider.list_repositories()
    current_repo = None
    for r in repos:
        if r['full_name'] == f"{owner}/{repo}":
            current_repo = r
            break
    
    if not current_repo:
        abort(404)
    
    workflow_runs = provider.list_workflow_runs(owner, repo)
    
    return render_template('main/runs.html',
                         owner=owner,
                         repo=repo,
                         current_repo=current_repo,
                         runs=workflow_runs)


@main_bp.route('/repos/<owner>/<repo>/runs/<int:run_id>')
@login_required
@permission_required(Permission.VIEW_RUNS)
def run_detail(owner, repo, run_id):
    """Workflow run detail page."""
    provider = get_provider()
    
    # Get repository info
    repos = provider.list_repositories()
    current_repo = None
    for r in repos:
        if r['full_name'] == f"{owner}/{repo}":
            current_repo = r
            break
    
    if not current_repo:
        abort(404)
    
    run = provider.get_workflow_run(owner, repo, run_id)
    
    if not run:
        abort(404)
    
    return render_template('main/run_detail.html',
                         owner=owner,
                         repo=repo,
                         current_repo=current_repo,
                         run=run)
