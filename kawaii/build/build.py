from .build_files import init_meson_crossfile
from .buildsystem import execute_buildsystem
from os import path
from pathlib import Path
from urllib.parse import urlparse
import click
from .lookup_deps import lookup_deps_project
from .buildsystem import run_build_command

from ast import Tuple
from graphlib import TopologicalSorter
from typing import List
from urllib.parse import urlparse
from .buildsystem import execute_buildsystem
import click
import asyncio
from os import path, listdir
from pathlib import Path
import toml

from .project import FullyInitedProject, UninitProject, packages_folder
from .buildsystem import run_build_command
from .download import download_all_sources
from .topological_sorting import sort_deps
def build_all(all_projects: List[FullyInitedProject], arch: str, app_id: str, main_config):
    projects_dict = dict()

 
    sorter: TopologicalSorter = sort_deps(all_projects)
    order = list(sorter.static_order())

    init_meson_crossfile(arch, main_config)
    
    click.echo(
    click.style(" START BUILDING ", bg="green", fg="white")
    + "".join(map(lambda project: f"\n  - {project}", order))
    + "\n"
    )
    for project in order: 
        project = projects_dict[project]
        _build_one(project, all_projects, arch, app_id, main_config)
    packages_folder_dir = packages_folder(arch, main_config)
    with click.progressbar(Path(packages_folder_dir).glob("*.so"), label="Removing old symbolic links") as progressbar:
        for libpath in progressbar:
            libpath.unlink()
    
    with click.progressbar(Path(packages_folder_dir).glob("**/*.so"), label="Installing symbolic links to the packages folder") as progressbar:
        for libpath in progressbar:
            dist_path = Path(packages_folder_dir, libpath.name)
            dist_path.symlink_to(libpath)

def build_one(project: UninitProject, all_projects: List[UninitProject], arch, app_id, main_config):
    
    deps = lookup_deps_project(project, all_projects)

    project.deps = list(deps)
    deps.append(project)
    build_all(deps, arch, app_id, main_config)

def _build_one(project: FullyInitedProject, projects: List[FullyInitedProject], arch, app_id, main_config):
    click.echo(click.style(" BUILDING ", bg="green", fg="white") + " " + project.id)
    folder_path = project.path.parent
    sources = project.config.get("sources")

    for source in sources:
        url = urlparse(sources[source]["url"])
        relative_path = url.netloc + url.path
        source_path = project.path.parent.joinpath(relative_path).resolve()
        folder_path = folder_path.joinpath(source_path if url.scheme == "file" else source)
        script_path = path.join(folder_path, source, "kawaii-build.sh")
    steps =  sources[source].get("steps")
    if steps:
        run_build_command(steps, arch, app_id, main_config, cwd=folder_path)
    elif path.exists(script_path):
        run_build_command([script_path], main_config, cwd=folder_path)
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

        execute_buildsystem(buildsystem, arch, app_id, main_config, cwd=folder_path)