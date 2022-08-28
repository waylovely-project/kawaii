from ast import Tuple
from .buildsystem import execute_buildsystem
import click
import asyncio
from os import path, listdir
from pathlib import Path
import toml

from .project import Project, packages_folder
from .buildsystem import run_build_command
from .download import download_all_sources


def build_one(deps_folder: str):
    projects = dict()
    queue = []
    projects_order = []
    count = 0
    for file in listdir(deps_folder):

        file_path = path.join(deps_folder, file)
        if path.isdir(file_path):
            project_config_path = path.join(file_path, "build.kawaii")

            if path.exists(project_config_path):
              
                project_config = toml.loads(open(project_config_path).read())
          
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
    click.echo(
        click.style(" START BUILDING ", bg="green", fg="white")
        + "".join(map(lambda project: f"\n  - {project}", projects_order))
        + "\n"
    )
    for project in projects_order:
        click.echo(click.style(" BUILDING ", bg="green", fg="white") + " " + project)
        folder_path = projects[project].path
        script_path = path.join(folder_path, "kawaii-build.sh")

        if path.exists(script_path):
            run_build_command(script_path, cwd=folder_path)
        else:
            if path.exists(path.join(folder_path, "meson.build")):
                buildsystem = "meson"
            elif path.exists(path.join(folder_path, "CMakeLists.txt")):
                buildsystem = "cmake"
            elif path.exists(path.join(folder_path, "autogen.sh")):
                buildsystem = "autotools"
            else:
                click.echo(
                    f"The {folder_path} does not have a kawaii-build.sh file and we can't automatically decide the build system to use ^^",
                    err=True,
                )
                exit(1)

            execute_buildsystem(buildsystem, cwd=folder_path)
    packages_folder_dir = packages_folder()
    with click.progressbar(Path(packages_folder_dir).glob("*.so"), label="Removing old symbolic links") as progressbar:
        for libpath in progressbar:
            libpath.unlink()
    
    with click.progressbar(Path(packages_folder_dir).glob("**/*.so"), label="Installing symbolic links to the packages folder") as progressbar:
        for libpath in progressbar:
            dist_path = Path(packages_folder_dir, libpath.name)
            dist_path.symlink_to(libpath)