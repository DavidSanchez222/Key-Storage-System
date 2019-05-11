import click

from config.model import User
from config.services import AuthService

@click.group()
def user():
    """Create an update user"""
    pass

@user.command()
@click.option('-u', '--username',
    type = str,
    prompt = True,
    confirmation_prompt = True,
    hide_input = True,
    help = 'Teh user name.')
@click.password_option()
@click.pass_context
def create(ctx, username, password):
    """Create the user for key storage."""
    if ctx.obj['username'] == None and ctx.obj['passwd'] == None:
        user = User(username, password)
        auth_services = AuthService(ctx.obj['username'], ctx.obj['passwd'])
        auth_services.create_user(user)
        click.echo(click.style('User created...', fg = 'green'))
    else:
        click.echo(click.style('User already exists...', fg = 'red'))


@user.command()
@click.pass_context
def update(ctx):
    """Update username and / or password."""
    auth_service = AuthService(ctx.obj['username'], ctx.obj['passwd'])
    username = click.prompt('Username', type = str, hide_input = True, show_default = False)
    password = click.prompt('Password', type = str, hide_input = True, show_default = False)
    auth = auth_service.verify_user(username, password)
    if auth == None:
        click.echo(click.style('Please, create your user with command \'kss user create\'.', fg = 'yellow'))
        return
    elif auth:
        auth_services = AuthService(ctx.obj['username'], ctx.obj['passwd'])
        user = _update_credentials_flow(User(ctx.obj['username'], ctx.obj['passwd']))
        auth_services.update_user(user)
        click.echo(click.style('User updated...', fg = 'green'))
    else:
        click.echo(click.style('Invalid credentials...', fg = 'red'))


def _update_credentials_flow(user):
    click.echo(click.style('Leave empty if you don\'t want to modify the value?', fg = 'yellow'))
    username = click.prompt('New username', type = str, default = user.username, hide_input = True,
        show_default = False, confirmation_prompt = True)
    password = click.prompt('New password', type = str, hide_input = True, default = user.password,
        show_default = False, confirmation_prompt = True)
    return User(username, password)


all = user