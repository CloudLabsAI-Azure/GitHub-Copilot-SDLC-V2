"""Database seeding commands."""
import click
from flask.cli import with_appcontext
from app.extensions import db
from app.models import Role, User


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
def all():
    """Seed roles and users."""
    click.echo('Seeding all data...')
    Role.insert_roles()
    User.insert_default_users()
    click.echo('All data seeded successfully!')
    click.echo('\nDefault users:')
    click.echo('  - viewer/viewer123 (Viewer role)')
    click.echo('  - developer/developer123 (LeadDeveloper role)')
    click.echo('  - admin/admin123 (GlobalAdmin role)')
