"""Application factory."""
import os
from flask import Flask, render_template
from config import config
from app.extensions import init_extensions


def create_app(config_name=None):
    """
    Application factory pattern.
    
    Args:
        config_name (str): Configuration name (development, testing, production)
        
    Returns:
        Flask: Configured Flask application
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register template context processors
    register_template_context(app)
    
    # Register CLI commands
    register_cli_commands(app)
    
    return app


def register_blueprints(app):
    """Register Flask blueprints."""
    from app.blueprints.auth import auth_bp
    from app.blueprints.main import main_bp
    from app.blueprints.api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)


def register_error_handlers(app):
    """Register error handlers."""
    
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(500)
    def internal_error(e):
        return render_template('errors/500.html'), 500


def register_template_context(app):
    """Register template context processors."""
    from app.models import Permission
    
    @app.context_processor
    def inject_permissions():
        return dict(Permission=Permission)


def register_cli_commands(app):
    """Register CLI commands."""
    from app.cli import seed
    
    app.cli.add_command(seed)
