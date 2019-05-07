import click

from storage.services import StorageService
from storage.model import Container
from tabulate import tabulate
from datetime import datetime
from simplecrypt import encrypt, decrypt

@click.group()
def storage():
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


def delete():
    pass

def update():
    pass

def _update_credentials_flow():
    pass

@storage.command()
@click.argument('option', type = str)
@click.pass_context
def list(ctx, option = '-s'):
    storage_service = StorageService(ctx.obj['pages_table'])
    container_list = storage_service.list_containers(option)
    click.echo(tabulate(container_list, headers = 'keys', tablefmt='fancy_grid'))


all = storage