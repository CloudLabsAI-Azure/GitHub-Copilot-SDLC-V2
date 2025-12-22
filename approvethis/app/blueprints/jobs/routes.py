"""Jobs blueprint routes."""
import json
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.blueprints.jobs import jobs_bp
from app.extensions import db
from app.models import (
    JobDefinition, JobExecution, ExecutionTarget,
    ExecutionStatus, Permission
)
from app.providers.execution import get_execution_provider
from datetime import datetime


# UI Routes

@jobs_bp.route('/')
@login_required
def index():
    """List all job definitions."""
    jobs = JobDefinition.query.filter_by(is_active=True).all()
    
    # Group by category
    jobs_by_category = {}
    for job in jobs:
        category = job.category or 'other'
        if category not in jobs_by_category:
            jobs_by_category[category] = []
        jobs_by_category[category].append(job)
    
    return render_template('jobs/index.html', jobs_by_category=jobs_by_category)


@jobs_bp.route('/<int:job_id>')
@login_required
def detail(job_id):
    """Job detail page with execution form."""
    job = JobDefinition.query.get_or_404(job_id)
    
    # Get recent executions for this job
    recent_executions = JobExecution.query.filter_by(
        job_definition_id=job_id
    ).order_by(JobExecution.created_at.desc()).limit(10).all()
    
    # Parse input schema
    input_schema = json.loads(job.input_schema) if job.input_schema else {}
    default_inputs = json.loads(job.default_inputs) if job.default_inputs else {}
    
    return render_template(
        'jobs/detail.html',
        job=job,
        input_schema=input_schema,
        default_inputs=default_inputs,
        recent_executions=recent_executions
    )


@jobs_bp.route('/<int:job_id>/execute', methods=['POST'])
@login_required
def execute(job_id):
    """Execute a job."""
    job = JobDefinition.query.get_or_404(job_id)
    
    # Check permission
    if not current_user.can(job.required_permission):
        flash('You do not have permission to execute this job.', 'error')
        return redirect(url_for('jobs.detail', job_id=job_id))
    
    # Get inputs from form
    inputs = {}
    if job.input_schema:
        schema = json.loads(job.input_schema)
        for field_name, field_spec in schema.items():
            value = request.form.get(field_name)
            if field_spec.get('type') == 'checkbox':
                value = value == 'on' if value else False
            inputs[field_name] = value
    
    # Create execution record
    execution = JobExecution(
        job_definition_id=job.id,
        inputs=json.dumps(inputs),
        status=ExecutionStatus.PENDING_APPROVAL if job.requires_approval else ExecutionStatus.QUEUED,
        requested_by_id=current_user.id
    )
    db.session.add(execution)
    db.session.commit()
    
    # If requires approval, don't execute yet
    if job.requires_approval:
        flash('Job execution request submitted for approval.', 'info')
        return redirect(url_for('jobs.execution_detail', execution_id=execution.id))
    
    # Execute the job
    try:
        target_config = json.loads(job.execution_target.config) if job.execution_target.config else {}
        job_config = {
            'workflow_id': job.workflow_id,
            'default_ref': job.default_ref
        }
        
        provider = get_execution_provider(job.execution_target.target_type)
        result = provider.execute(target_config, job_config, inputs)
        
        # Update execution with result
        execution.status = result.get('status', ExecutionStatus.RUNNING)
        execution.external_id = result.get('external_id')
        execution.external_url = result.get('external_url')
        execution.started_at = datetime.utcnow()
        db.session.commit()
        
        flash('Job execution started successfully.', 'success')
    except Exception as e:
        execution.status = ExecutionStatus.FAILED
        execution.error_message = str(e)
        db.session.commit()
        flash(f'Failed to execute job: {str(e)}', 'error')
    
    return redirect(url_for('jobs.execution_detail', execution_id=execution.id))


@jobs_bp.route('/executions')
@login_required
def executions():
    """List job executions."""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Filter by status if provided
    status_filter = request.args.get('status')
    job_filter = request.args.get('job_id', type=int)
    
    query = JobExecution.query
    
    # Non-admin users see only their own executions
    if not current_user.is_admin():
        query = query.filter_by(requested_by_id=current_user.id)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if job_filter:
        query = query.filter_by(job_definition_id=job_filter)
    
    pagination = query.order_by(JobExecution.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Get all jobs for filter dropdown
    jobs = JobDefinition.query.filter_by(is_active=True).all()
    
    return render_template(
        'jobs/executions.html',
        executions=pagination.items,
        pagination=pagination,
        jobs=jobs,
        status_filter=status_filter,
        job_filter=job_filter
    )


@jobs_bp.route('/executions/<int:execution_id>')
@login_required
def execution_detail(execution_id):
    """Execution detail page."""
    execution = JobExecution.query.get_or_404(execution_id)
    
    # Non-admin users can only view their own executions
    if not current_user.is_admin() and execution.requested_by_id != current_user.id:
        flash('You do not have permission to view this execution.', 'error')
        return redirect(url_for('jobs.executions'))
    
    # Parse inputs and result
    inputs = json.loads(execution.inputs) if execution.inputs else {}
    result = json.loads(execution.result) if execution.result else None
    
    return render_template(
        'jobs/execution_detail.html',
        execution=execution,
        inputs=inputs,
        result=result
    )


# API Routes

@jobs_bp.route('/api/jobs')
@login_required
def api_list_jobs():
    """List job definitions (JSON)."""
    jobs = JobDefinition.query.filter_by(is_active=True).all()
    
    return jsonify([{
        'id': job.id,
        'name': job.name,
        'description': job.description,
        'category': job.category,
        'requires_approval': job.requires_approval,
        'execution_target': job.execution_target.name if job.execution_target else None
    } for job in jobs])


@jobs_bp.route('/api/jobs/<int:job_id>')
@login_required
def api_get_job(job_id):
    """Get job definition (JSON)."""
    job = JobDefinition.query.get_or_404(job_id)
    
    return jsonify({
        'id': job.id,
        'name': job.name,
        'description': job.description,
        'category': job.category,
        'requires_approval': job.requires_approval,
        'execution_target': job.execution_target.name if job.execution_target else None,
        'input_schema': json.loads(job.input_schema) if job.input_schema else {},
        'default_inputs': json.loads(job.default_inputs) if job.default_inputs else {}
    })


@jobs_bp.route('/api/jobs/<int:job_id>/execute', methods=['POST'])
@login_required
def api_execute_job(job_id):
    """Execute job (JSON)."""
    job = JobDefinition.query.get_or_404(job_id)
    
    # Check permission
    if not current_user.can(job.required_permission):
        return jsonify({'error': 'Permission denied'}), 403
    
    data = request.get_json()
    inputs = data.get('inputs', {})
    
    # Create execution record
    execution = JobExecution(
        job_definition_id=job.id,
        inputs=json.dumps(inputs),
        status=ExecutionStatus.PENDING_APPROVAL if job.requires_approval else ExecutionStatus.QUEUED,
        requested_by_id=current_user.id
    )
    db.session.add(execution)
    db.session.commit()
    
    # If requires approval, don't execute yet
    if job.requires_approval:
        return jsonify({
            'execution_id': execution.id,
            'status': execution.status,
            'message': 'Execution submitted for approval'
        })
    
    # Execute the job
    try:
        target_config = json.loads(job.execution_target.config) if job.execution_target.config else {}
        job_config = {
            'workflow_id': job.workflow_id,
            'default_ref': job.default_ref
        }
        
        provider = get_execution_provider(job.execution_target.target_type)
        result = provider.execute(target_config, job_config, inputs)
        
        # Update execution with result
        execution.status = result.get('status', ExecutionStatus.RUNNING)
        execution.external_id = result.get('external_id')
        execution.external_url = result.get('external_url')
        execution.started_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(execution.to_dict())
    except Exception as e:
        execution.status = ExecutionStatus.FAILED
        execution.error_message = str(e)
        db.session.commit()
        return jsonify({'error': str(e)}), 500


@jobs_bp.route('/api/jobs/executions')
@login_required
def api_list_executions():
    """List executions (JSON)."""
    query = JobExecution.query
    
    # Non-admin users see only their own executions
    if not current_user.is_admin():
        query = query.filter_by(requested_by_id=current_user.id)
    
    executions = query.order_by(JobExecution.created_at.desc()).limit(50).all()
    
    return jsonify([execution.to_dict() for execution in executions])


@jobs_bp.route('/api/jobs/executions/<int:execution_id>')
@login_required
def api_get_execution(execution_id):
    """Get execution (JSON)."""
    execution = JobExecution.query.get_or_404(execution_id)
    
    # Non-admin users can only view their own executions
    if not current_user.is_admin() and execution.requested_by_id != current_user.id:
        return jsonify({'error': 'Permission denied'}), 403
    
    return jsonify(execution.to_dict())


@jobs_bp.route('/api/jobs/executions/<int:execution_id>/cancel', methods=['POST'])
@login_required
def api_cancel_execution(execution_id):
    """Cancel execution (JSON)."""
    execution = JobExecution.query.get_or_404(execution_id)
    
    # Only requester or admin can cancel
    if not current_user.is_admin() and execution.requested_by_id != current_user.id:
        return jsonify({'error': 'Permission denied'}), 403
    
    # Can only cancel running or queued executions
    if execution.status not in [ExecutionStatus.QUEUED, ExecutionStatus.RUNNING]:
        return jsonify({'error': 'Cannot cancel execution in current status'}), 400
    
    try:
        target_config = json.loads(execution.job_definition.execution_target.config) if execution.job_definition.execution_target.config else {}
        provider = get_execution_provider(execution.job_definition.execution_target.target_type)
        
        result = provider.cancel(target_config, execution.external_id)
        
        if result.get('success'):
            execution.status = ExecutionStatus.CANCELLED
            execution.completed_at = datetime.utcnow()
            db.session.commit()
            return jsonify({'message': 'Execution cancelled'})
        else:
            return jsonify({'error': result.get('message')}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
