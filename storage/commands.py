import click, getpass

from storage.services import StorageService
from storage.model import Container
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
    help = 'User account')
@click.password_option()
@click.pass_context
def create(ctx, name_page, address, user, password):
    """Create a new container of credentials."""
    container = Container(name_page, address, user,password)
    storage_service = StorageService(ctx.obj['pages_table'])
    storage_service.create_container(container)
    click.echo('Container created...')


@storage.command()
@click.option('--available/--permanent', default = False, help = 'Pending...')
@click.argument('container_uid', type = str)
@click.pass_context
def delete(ctx, available, container_uid):
    """Delete a container"""
    storage_service = StorageService(ctx.obj['pages_table'])
    container_list = storage_service.list_containers(False)
    container = [container for container in container_list if container['uid'] == container_uid]
    if click.confirm(f'Are you sure you want to delete the container with uid: {container_uid}') and container:
        if available:
            container = _soft_delete_credentials_flow(Container(**container[0]))
            storage_service.update_container(container)
            click.echo('Container deleted...')
        else:
            storage_service.delete_container(Container(**container[0]))
            click.echo('Container deleted permanent...')
    else:
        click.echo('Container not found...')


def _soft_delete_credentials_flow(container):
    container.deleted_at = datetime.now()
    return container


@storage.command()
@click.argument('container_uid', type = str)
@click.pass_context
def update(ctx, container_uid):
    """Update a container"""
    storage_service = StorageService(ctx.obj['pages_table'])
    container_list = storage_service.list_containers(True)
    container = [container for container in container_list if container['uid'] == container_uid]
    if container:
        container = _update_credentials_flow(Container(**container[0]))
        storage_service.update_container(container)
        click.echo('Container updated...')
    else:
        click.echo('Container not found...')


def _update_credentials_flow(container):
    click.echo('Leave empty if you don\'t want to modify the value?')
    container.name_page = click.prompt('New name page', type = str, default = container.name_page)
    container.address = click.prompt('New address', type = str, default = container.address)
    container.user = click.prompt('New user', type = str, default = container.user)
    tmp_pass = getpass.getpass()
    if tmp_pass == getpass.getpass('Confirm password:'):
        container.password = tmp_pass
    else:
        click.echo('Your password has not been updated...')
    container.updated_at = datetime.now()
    return container


@storage.command()
@click.option('--current/--all', default = False, help = 'Pending...')
@click.pass_context
def list(ctx, current):
    """List the stored data"""
    storage_service = StorageService(ctx.obj['pages_table'])
    container_list = storage_service.list_containers(current)
    if container_list:
        click.echo(tabulate(container_list, headers = 'keys', tablefmt='fancy_grid'))
    else:
        click.echo('No containers available...')


@storage.command()
@click.argument('name_page', type = str)
@click.pass_context
def search(ctx, name_page):
    """Search container for name page"""
    storage_service = StorageService(ctx.obj['pages_table'])
    containers = storage_service.search(name_page)
    if containers:
        click.echo(tabulate(containers, headers = 'keys', tablefmt='fancy_grid'))
    else:
        click.echo('Container not found...')


all = storage