import json
from os import path
import os
from typing import Dict
import click
from .utils import get_cache_config, show_top_level


class Project:
    def __init__(self, name: str, path: str, deps: list):
        self.name = name
        self.path = path
        self.deps = deps
        self.deps_left = deps


@click.command()
def build_deps():
    """Build native libraries required for Waylovely and Portals.\n
    Mostly they are written in C/C++. They'll get installed to the '' folder of the root directory of the Git repository!
    This behavior can be changed by changing the "deps-location" path in kawaii/config.json file. 
    """
    config = get_cache_config()
    if "deps-location" in config:
        deps_folder = config["deps-location"]
    else:
        deps_folder = path.join(show_top_level(), "deps")
    projects = dict()
    queue = []
    projects_order = []
    count = 0
    for file in os.listdir(deps_folder):
        file_path = path.join(deps_folder, file)
        if path.isdir(file_path):
            project_config_path = path.join(file_path, "kawaii.config.json")

            if path.exists(project_config_path):
                try:
                project_config = json.loads(open(project_config_path).read())
                except json.JSONDecodeError as error:
                    click.echo(
                        f"Oh nooo! We found an error while processing {project_config_path}! {error}",
                        err=True,
                    )
                    exit(1)

                if "deps" in project_config:
                    projects[file] = Project(file, file_path, project_config["deps"])
                    if len(project_config["deps"]) == 0:
                        queue.append(file)

    while queue:
        current = queue.pop()
        projects_order.append(current)
        for (name, config) in projects.items():
            if current in config.deps_left:

                config.deps_left.remove(current)

                if len(config.deps_left) == 0:

                    queue.append(name)
        count += 1

    projects_with_deps = [
        project
        for project in filter(
            lambda project: len(project[1].deps_left) != 0, projects.items()
        )
    ]
    deps_missing = False
    for project in projects_with_deps:
        for dep in project[1].deps:
            if not dep in projects:
                click.echo(f"Missing dependency for {project[0]}: {dep}", err=True)
                deps_missing = True
                
    if deps_missing:
        exit(1)

    if count != len(projects):

        def output_deps(project: Tuple[str, Project]):
            name = f" {project.name} "
            if projects in projects_with_deps:
                name = click.style(name, fg="white", bg="red")

            return name + " ⇒  " + " ".join(project.deps)

        tree = "\n".join(map(output_deps, projects.values()))
        click.echo(
            f"Oh nooo! Found some cyclic dependencies. \n\nHere is the dependency tree:\n{tree}",
        )
        exit(1)

    for project in projects_order:
        print(project.path)
