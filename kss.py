import click, os

from storage import commands as storage_commands
from config import commands as user_commands
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = {}
    ctx.obj['pages_table'] = os.getenv('PAGES_TABLE')
    ctx.obj['username'] = os.getenv('KSS_USER') or None
    ctx.obj['passwd'] = os.getenv('KSS_PASSWD') or None

cli.add_command(storage_commands.all)
cli.add_command(user_commands.all)