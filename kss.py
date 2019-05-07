import click

from storage import commands as storage_commands
from searchs import commands as searchs_commands

PAGES_TABLE = '.pages.csv'

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = {}
    ctx.obj['pages_table'] = PAGES_TABLE

cli.add_command(storage_commands.all)
cli.add_command(searchs_commands.all)