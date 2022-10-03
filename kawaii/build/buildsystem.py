from os import environ 
from pathlib import Path
from traceback import print_tb
import click
from .utils import get_envvars
from os import path
import subprocess
import sys


def run_build_command(commands: list[str], arch, app_id, main_config, **kwargs):
    (env, cwd) = get_envvars("", arch, app_id, main_config, **kwargs)

    def excepthook(type, value, traceback):
        command_style = click.style(commands, fg="yellow")
        cwd_style = click.style(cwd, fg="yellow")
        env_style = "\n".join([f"  {click.style(key, fg='yellow')}: {value}" for key, value in env.items()])

        error = click.style(" FATAL ERROR ", bg="red", fg="white")
        
        if environ.get("KAWAII_VERBOSE") == "1":
            click.secho(" Command Information ", err=True, bg="bright_magenta", fg="black")
            click.echo(f"   Executed command: {command_style} {args}")
            click.echo(f"   Working directory: {cwd_style}")
            if f"{value}" != "Build command failed!":
                click.secho(" Traceback ", err=True, bg="bright_red", fg="black")
                print_tb(traceback)
            click.echo("")
            click.secho(" Debug information ", err=True, bg="blue", fg="bright_green")
            click.echo(env_style)
            click.echo(
            f"\n{error} {type} {value} \n{click.style(path.basename(cwd), fg='blue')} failed building\n",
            err=True,
        )
        click.echo(f"{error} {click.style(Path(cwd).name, fg='blue')} failed building")
    sys.excepthook = excepthook
 
    for args in commands:
        args = args.split(" ")
    
        process = subprocess.run(
            args,
            executable=args[0],
            stdin=sys.stdin,
            stderr=sys.stderr,
            stdout=sys.stdout,
            env=env["env"],
            cwd=cwd,
        )

        if process.returncode != 0:
            raise Exception("Build command failed!")

def execute_buildsystem(buildsystem: str, arch, app_id, main_config, **kwargs):
    run_build_command(
        [str(Path(__file__).parent.parent.joinpath("scripts", buildsystem)), *(kwargs.get("args") or [])], arch, app_id, main_config, **kwargs
    )

        
available_buildsystems = ["meson", "cmake", "autotools", "cargo-apk"]