"""Database seeding commands."""
import click
from flask.cli import with_appcontext
from app.extensions import db
from app.models import Role, User, ExecutionTarget, JobDefinition


@click.group()
def seed():
    """Database seeding commands."""
    pass


@seed.command()
@with_appcontext
def roles():
    """Seed roles into the database."""
    click.echo('Seeding roles...')
    Role.insert_roles()
    click.echo('Roles seeded successfully!')


@seed.command()
@with_appcontext
def users():
    """Seed default users into the database."""
    click.echo('Seeding users...')
    User.insert_default_users()
    click.echo('Users seeded successfully!')


@seed.command()
@with_appcontext
def targets():
    """Seed execution targets into the database."""
    click.echo('Seeding execution targets...')
    ExecutionTarget.seed_targets()
    click.echo('Execution targets seeded successfully!')


@seed.command()
@with_appcontext
def jobs():
    """Seed job definitions into the database."""
    click.echo('Seeding job definitions...')
    JobDefinition.seed_jobs()
    click.echo('Job definitions seeded successfully!')


@seed.command()
@with_appcontext
def all():
    """Seed roles, users, targets, and jobs."""
    click.echo('Seeding all data...')
    Role.insert_roles()
    User.insert_default_users()
    ExecutionTarget.seed_targets()
    JobDefinition.seed_jobs()
    click.echo('All data seeded successfully!')
    click.echo('\nDefault users:')
    click.echo('  - viewer/viewer123 (Viewer role)')
    click.echo('  - developer/developer123 (LeadDeveloper role)')
    click.echo('  - admin/admin123 (GlobalAdmin role)')
    click.echo('\nExecution targets and job definitions have been created.')
