import json
from os import path
import os
from typing import Dict
import click
from utils import build_path, root_source_dir


@click.command()
def build_deps():
    """ Build native libraries required for Waylovely and Portals.\n
    Mostly they are written in C/C++. They'll get installed to the '' folder of the root directory of the Git repository!
    This behavior can be changed by changing the "deps-location" path in kawaii/config.json file. 
    """
    config = json.loads(open(path.join(build_path, "config.json")).read())
    if hasattr(config, "deps-location"):
        deps_folder = config["deps-location"]
    else:
        deps_folder = path.join(root_source_dir, "deps")
    projects = dict()
    queue = []
    projects_order = []
    for file in os.listdir(deps_folder):
        file_path = path.join(deps_folder, file)
        if path.isdir(file):
            project_config_path = path.join(file_path, "kawaii.config.json")
            build_script_path = path.join(file_path, "kawaii-build.sh")
            if path.exists():
                project_config = json.loads(open(project_config_path).read())

                if hasattr(project_config, "deps"):

                    projects.add(file, {"path": file_path, "deps": project_config.deps})

                    if project_config.deps.len() == 0:
                        queue.push(file)

    while queue:
        current = queue.pop()
        projects_order.append(current)
        for (name, config) in projects.items():
            config.deps.remove(name)
            if config.deps.len() == 0:
                queue.append(name)
                
    projects_with_deps = [project for project in filter(
        lambda project: project[1].deps.len() != 0, projects.items()
    ) ]

    if len(projects_with_deps) != 0:
        raise Exception(
            f"Oh no!!! It seems we are left with some cylic dependencies!! {projects_with_deps}"
        )

    for project in projects_order:
        print(project.path)
