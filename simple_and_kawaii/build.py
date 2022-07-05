import json
from os import abort, path
import os
from pathlib import Path
import subprocess
import sys
from traceback import print_tb
from typing import Tuple
import click
from .utils import (
    get_config_key,
    get_cpu_info,
    get_host_arch,
    get_host_os,
    show_top_level,
)

def packages_folder(**kwargs):
    return path.join(
        get_config_key("libs-folder") or path.join(show_top_level(), "prebuilt-libs"),
        get_config_key("android-abi"),
    )
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
    This behavior can be changed by changing the "deps-location" path in kawaii/cache_config.json file.
    """
    deps_folder = get_config_key("deps-folder") or path.join(
        show_top_level(), "kawaii-deps"
    )

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

            __execute_buildsystem(buildsystem, cwd=folder_path)
    packages_folder_dir = packages_folder()
    with click.progressbar(Path(packages_folder_dir).glob("**/*.so"), label="Installing symbolic links to the packages folder") as progressbar:
        for libpath in progressbar:
            Path(packages_folder_dir, libpath.name).symlink_to(libpath)


def __execute_buildsystem(buildsystem: str, **kwargs):
    run_build_command(
        path.join(path.dirname(__file__), "scripts", buildsystem), **kwargs
    )


def run_build_command(command: str, **kwargs):
    cwd = kwargs.get("cwd") or os.getcwd()
    missing_config = False
    for required_config in [
        "android-abi",
        "android-sdk-root",
        "android-ndk-version",
        "android-platform",
    ]:
        if not get_config_key(required_config):
            click.echo(
                f"{required_config} is not present in the cache_config file! Please run kawaii init ^^",
                err=True,
            )

            missing_config = True

    if missing_config:
        exit(1)
    packages_folder_dir = packages_folder()

    prefix = path.join(packages_folder_dir, path.basename(cwd))

    pkgconfig_path = ":".join(
        map(lambda path: str(path), Path(packages_folder_dir).glob("**/pkgconfig"))
    )
    android_ndk_root = path.join(
        get_config_key("android-sdk-root"), "ndk", get_config_key("android-ndk-version")
    )

    android_toolchain = path.join(
        android_ndk_root,
        "toolchains",
        "llvm",
        "prebuilt",
        f"{get_host_os()}-{get_host_arch()}",
    )

    def toolchain_arch_script(script: str):
        return path.join(
            android_toolchain,
            "bin",
            f"{get_cpu_info(get_config_key('android-abi'))['triple']}{get_config_key('android-platform')}-{script}",
        )

    def toolchain_script(script: str):
        return path.join(android_toolchain, "bin", script)

    args = list(kwargs.get("args") or "")
    args.insert(0, command)
    env = {
        "ANDROID_ABI": get_config_key("android-abi"),
        "ANDROID_SDK_ROOT": get_config_key("android-sdk-root"),
        "ANDROID_NDK_ROOT": android_ndk_root,
        "ANDROID_PLATFORM": "android-" + get_config_key("android-platform"),
        "PATH": os.environ.get("PATH"),
        "PREFIX": prefix,
        "TOOLCHAIN": android_toolchain,
        "PACKAGES_FOLDER": packages_folder_dir,
        "PKG_CONFIG_PATH": pkgconfig_path,
        "PKG_CONFIG_SYSROOT_DIR": path.join(android_toolchain, "sysroot"),
        "ABI_TRIPLE": get_cpu_info(get_config_key("android-abi"))["triple"],
        "MESON_CROSSFILE": path.join(
            show_top_level(),
            "kawaii",
            "cache",
            f"meson-{get_config_key('android-abi')}.ini",
        ),
        # Cross-compiling configuration for Autoconf based buildsystems
        "CC": toolchain_arch_script("clang"),
        "AR": toolchain_script("llvm-ar"),
        "AS": toolchain_arch_script("clang"),
        "CXX": toolchain_arch_script("clang++"),
        "LD": toolchain_script("ld"),
        "RANLIB": toolchain_script("llvm-ranlib"),
        "STRIP": toolchain_script("llvm-strip"),
    }

    def excepthook(type, value, traceback):
        command_style = click.style(command, fg="yellow")
        cwd_style = click.style(cwd, fg="yellow")
        env_style = "\n".join([f"  {click.style(key, fg='yellow')}: {value}" for key, value in env.items()])
        error = click.style(" FATAL ERROR ", bg="red", fg="white")
        click.echo(
            f"\n{error} {type} {value} \n{click.style(path.basename(cwd), fg='blue')} failed building\n",
            err=True,
        )
        click.secho(" Command Information ", err=True, bg="bright_magenta", fg="black")
        click.echo(f"   Executed command: {command_style} {args}")
        click.echo(f"   Working directory: {cwd_style}")
        if f"{value}" != "Build command failed!":
            click.secho(" Traceback ", err=True, bg="bright_red", fg="black")
            print_tb(traceback)
        click.echo("")
        click.secho(" Debug information ", err=True, bg="blue", fg="bright_green")
        click.echo(env_style)

    sys.excepthook = excepthook

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


available_buildsystems = ["meson", "cmake", "autotools", "cargo-apk"]
