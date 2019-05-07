import click

from storage.services import StorageServices
from storage.model import Pages
from tabulate import tabulate

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
@click.option('-p', '--password',
    type = str,
    prompt = True,
    help = 'Password account')
@click.pass_context
def create(ctx, name_page, address, user, password):
    pass

def delete():
    pass

def update():
    pass

def _update_credentials_flow():
    pass

def list():
    pass

all = storage