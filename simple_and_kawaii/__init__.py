from pathlib import Path
from urllib.parse import urlparse
import click
import os
from simple_and_kawaii.group import OrderedGroup
from simple_and_kawaii.vscode import vscode_settings

import toml
from .init_project import init
from .build import build_deps
from .config import init_config
from .build.buildsystem import  available_buildsystems, execute_buildsystem
from .build.build import build_one
from .build.collections import get_packages, get_source_package
from .config import init_config
from . import config 
@click.group(cls=OrderedGroup, invoke_without_command=True)
@click.option("--arch", default="arm64-v8a", help="The architechture, supports")
@click.pass_context
def cli(ctx, arch):
    if ctx.invoked_subcommand is None:

        project = get_source_package(Path.cwd(), arch)
        config = project.config 
        config = init_config(config)
        cargo_manifest = Path.cwd().joinpath("Cargo.toml")
        
        if cargo_manifest.exists():
            manifest = toml.loads(open(cargo_manifest).read())
            config["app-id"] = manifest["package"]["metadata"]["android"]["package"]
        app_id = config["app-id"]
        packages = list()
        for collection in config["collections"]:
            url = urlparse(config["collections"][collection])
            if url.scheme != "file":
                click.echo("Needs to be  file://")
                exit(1)
            path = Path(url.hostname + url.path)
            collection_config = toml.loads(open(path.joinpath("kawaii.toml")).read())
            packages.extend( get_packages(collection_config, str(path), arch, app_id, config))
        build_one(project, packages, arch, app_id, config)
    pass


cli.add_command(init)
cli.add_command(build_deps)
cli.add_command(vscode_settings)

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
    execute_buildsystem("{buildsystem}", os.environ.get("ANDROID_ABI"),  "none", init_config(dict()), args=config_args)
    
cli.add_command(execute_{indentname})
    """
    )
