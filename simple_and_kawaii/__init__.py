import click

from simple_and_kawaii.group import OrderedGroup
from .init_project import init
from .build import build_deps, __execute_buildsystem, available_buildsystems


@click.group(cls=OrderedGroup)
def cli():
    pass


cli.add_command(init)
cli.add_command(build_deps)


@click.group()
def buildsystems():
    pass


for buildsystem in available_buildsystems:
    indentname = buildsystem.replace("-", "_")
    exec(
        f"""@click.command(buildsystem, context_settings=dict(
        ignore_unknown_options=True
        ),
        help="Run {buildsystem} with Kawaii configurations")
@click.argument("config_args", nargs=-1, type=click.UNPROCESSED)
def execute_{indentname}(config_args):
    __execute_buildsystem("{buildsystem}", args=config_args)
    
cli.add_command(execute_{indentname})
    """
    )
