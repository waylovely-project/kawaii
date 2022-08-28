from traceback import print_tb
import click
from .utils import get_envvars
from os import path
import subprocess
import sys


def run_build_command(command: str, **kwargs):
    (env, cwd, args) = get_envvars(command, **kwargs)

    def excepthook(type, value, traceback):
        command_style = click.style(command, fg="yellow")
        cwd_style = click.style(cwd, fg="yellow")
        env_style = "\n".join([f"  {click.style(key, fg='yellow')}: {value}" for key, value in env.items()])
        click.secho(" Command Information ", err=True, bg="bright_magenta", fg="black")
        click.echo(f"   Executed command: {command_style} {args}")
        click.echo(f"   Working directory: {cwd_style}")
        if f"{value}" != "Build command failed!":
            click.secho(" Traceback ", err=True, bg="bright_red", fg="black")
            print_tb(traceback)
        click.echo("")
        click.secho(" Debug information ", err=True, bg="blue", fg="bright_green")
        click.echo(env_style)
        error = click.style(" FATAL ERROR ", bg="red", fg="white")
        click.echo(
            f"\n{error} {type} {value} \n{click.style(path.basename(cwd), fg='blue')} failed building\n",
            err=True,
        )

    sys.excepthook = excepthook
    print(args)
    process = subprocess.run(
        args,
        executable=command,
        stdin=sys.stdin,
        stderr=sys.stderr,
        stdout=sys.stdout,
        env=env,
        cwd=cwd,
    )

    if process.returncode != 0:
        raise Exception("Build command failed!")

def execute_buildsystem(buildsystem: str, **kwargs):
    run_build_command(
        path.join(path.dirname(__file__), "scripts", buildsystem), **kwargs
    )

        
available_buildsystems = ["meson", "cmake", "autotools", "cargo-apk"]