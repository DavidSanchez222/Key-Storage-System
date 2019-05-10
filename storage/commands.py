import click, getpass, os

from storage.services import StorageService
from storage.model import Container
from config.services import AuthService
from tabulate import tabulate
from datetime import datetime

@click.group()
def storage():
    """Manages access credentials containers"""
    pass

@storage.command()
@click.option('-n', '--name_page', 
    type = str,
    prompt = True,
    help = 'The page name')
@click.option('-a', '--address',
    type = str,
    prompt = True,
    help = 'The page address')
@click.option('-u', '--user',
    type = str,
    prompt = True,
    hide_input = True,
    confirmation_prompt = True,
    help = 'User account')
@click.password_option()
@click.pass_context
def create(ctx, name_page, address, user, password):
    """Create a new container of credentials."""
    container = Container(name_page.capitalize(), address, user,password)
    storage_service = StorageService(ctx.obj['pages_table'])
    storage_service.create_container(container)
    click.echo(click.style('Container created...', fg = 'green'))


@storage.command()
@click.option('--available/--permanent', default = False, help = 'Pending...')
@click.argument('container_uid', type = str)
@click.pass_context
def delete(ctx, available, container_uid):
    """Delete a container"""
    auth_service = AuthService(ctx.obj['username'], ctx.obj['passwd'])
    username = click.prompt('Username', type = str, hide_input = True, show_default = False)
    password = click.prompt('Password', type = str, hide_input = True, show_default = False)
    auth = auth_service.verify_user(username, password)
    if auth == None:
        click.echo(click.style('Please, create your user with command \'kss user create\'.', fg = 'yellow'))
        return
    elif auth:
        storage_service = StorageService(ctx.obj['pages_table'])
        container_list = storage_service.list_containers(False)
        container = [container for container in container_list if container['uid'] == container_uid]
        if click.confirm(click.style(f'Are you sure you want to delete the container with uid: {container_uid}', fg = 'yellow')) and container:
            if available:
                container = _soft_delete_credentials_flow(Container(**container[0]))
                storage_service.update_container(container)
                click.echo(click.style('Container deleted...', fg = 'green'))
            else:
                storage_service.delete_container(Container(**container[0]))
                click.echo(click.style('Container deleted permanent...', fg = 'green'))
        else:
            click.echo(click.style('Container not found...', fg = 'yellow'))
    else:
        click.echo(click.style('Invalid credentials...', fg = 'red'))


def _soft_delete_credentials_flow(container):
    container.deleted_at = datetime.now()
    return container


@storage.command()
@click.argument('container_uid', type = str)
@click.pass_context
def update(ctx, container_uid):
    """Update a container"""
    auth_service = AuthService(ctx.obj['username'], ctx.obj['passwd'])
    username = click.prompt('Username', type = str, hide_input = True, show_default = False)
    password = click.prompt('Password', type = str, hide_input = True, show_default = False)
    auth = auth_service.verify_user(username, password)
    if auth == None:
        click.echo(click.style('Please, create your user with command \'kss user create\'.', fg = 'yellow'))
        return
    elif auth:
        storage_service = StorageService(ctx.obj['pages_table'])
        container_list = storage_service.list_containers(True)
        container = [container for container in container_list if container['uid'] == container_uid]
        if container:
            container = _update_credentials_flow(Container(**container[0]))
            storage_service.update_container(container)
            click.echo(click.style('Container updated...', fg = 'green'))
        else:
            click.echo(click.style('Container not found...', fg = 'yellow'))
    else:
        click.echo(click.style('Invalid credentials...', fg = 'red'))


def _update_credentials_flow(container):
    click.echo(click.style('Leave empty if you don\'t want to modify the value.', fg = 'yellow'))
    container.name_page = click.prompt('New name page', type = str, default = container.name_page)
    container.address = click.prompt('New address', type = str, default = container.address)
    container.user = click.prompt('New user', type = str, default = container.user, hide_input = True, 
        confirmation_prompt = True, show_default = False)
    container.password = click.prompt('New password', type = str, default = container.password, 
        hide_input = True, confirmation_prompt = True, show_default = False)
    container.updated_at = datetime.now()
    return container


@storage.command()
@click.option('--current/--all', default = False, help = 'Pending...')
@click.option('-v/-n', default = False,help = 'Pending...')
@click.pass_context
def list(ctx, current, v):
    """List the stored data"""
    storage_service = StorageService(ctx.obj['pages_table'])
    if v:
        auth_service = AuthService(ctx.obj['username'], ctx.obj['passwd'])
        username = click.prompt('Username', type = str, hide_input = True, show_default = False)
        password = click.prompt('Password', type = str, hide_input = True, show_default = False)
        auth = auth_service.verify_user(username, password)
        if auth == None:
            click.echo(click.style('Please, create your user with command \'kss user create\'.', fg = 'yellow'))
            return
        elif auth:
            container_list = storage_service.list_containers(current)
            if container_list:
                click.echo(tabulate(container_list, headers = 'keys', tablefmt='fancy_grid'))
                click.pause(info = click.style('Press any key to continue ...', fg = 'yellow'))
                _clear_screen()
            else:
                click.echo(click.style('No containers availables...', fg = 'yellow'))
        else:
            click.echo(click.style('Invalid credentials...', fg = 'red'))
    else:
        container_list = storage_service.list_containers_without_credentials(current)
        if container_list:
            click.echo(tabulate(container_list, headers = 'keys', tablefmt='fancy_grid'))
            click.pause(info = click.style('Press any key to continue ...', fg = 'yellow'))
            _clear_screen()
        else:
            click.echo(click.style('No containers availables...', fg = 'yellow'))


@storage.command()
@click.argument('name_page', type = str)
@click.option('-v/-n', default = False,help = 'Pending...')
@click.pass_context
def search(ctx, v, name_page):
    """Search container for name page"""
    storage_service = StorageService(ctx.obj['pages_table'])
    if v:
        auth_service = AuthService(ctx.obj['username'], ctx.obj['passwd'])
        username = click.prompt('Username', type = str, hide_input = True, show_default = False)
        password = click.prompt('Password', type = str, hide_input = True, show_default = False)
        auth = auth_service.verify_user(username, password)
        if auth == None:
            click.echo(click.style('Please, create your user with command \'kss user create\'.', fg = 'yellow'))
            return
        elif auth:
            containers = storage_service.search(name_page.capitalize())
            if containers:
                click.echo(tabulate(containers, headers = 'keys', tablefmt='fancy_grid'))
                click.pause(info = click.style('Press any key to continue ...', fg = 'yellow'))
                _clear_screen()
            else:
                click.echo(click.style('Container not found...', fg = 'yellow'))
        else:
            click.echo(click.style('Invalid credentials...', fg = 'red'))
    else:
        containers = storage_service.search_without_credentials(name_page.capitalize())
        if containers:
            click.echo(tabulate(containers, headers = 'keys', tablefmt='fancy_grid'))
            click.pause(info = click.style('Press any key to continue ...', fg = 'yellow'))
            _clear_screen()
        else:
            click.echo(click.style('Container not found...', fg = 'yellow'))


def _clear_screen():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system('cls')


all = storage