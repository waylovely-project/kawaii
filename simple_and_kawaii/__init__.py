import click
from .init_project import init;
from .build import build_deps
@click.group()
def cli():
    pass

cli.add_command(init)
cli.add_command(build_deps)

