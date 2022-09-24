from os import path
import click
from pathlib import Path
from .build.project import packages_folder
from .build.utils import get_envvars
from .utils import get_host_arch, get_host_os, show_top_level
import commentjson

@click.command()
def vscode_settings(arch):
    settings_path = path.join(show_top_level(), ".vscode", "settings.json")

    settings = commentjson.loads(open(settings_path).read())
    android_ndk_root = path.join(
        main_config["android"]["sdk-root"], "ndk", main_config["android"]["ndk"]
    )

    android_toolchain = path.join(
        android_ndk_root,
        "toolchains",
        "llvm",
        "prebuilt",
        f"{get_host_os()}-{get_host_arch()}",
    )
    packages_folder_dir = packages_folder(arch)

    pkgconfig_path = ":".join(
        map(lambda path: str(path), Path(packages_folder_dir).glob("**/pkgconfig"))
    )
    (env, cwd, args) = get_envvars("", arch)
    settings['rust-analyzer.server.extraEnv'] = env
    
    settings_file = open(settings_path, mode="w")
    settings_file.write(commentjson.dumps(settings, sort_keys=True, indent=4))
    