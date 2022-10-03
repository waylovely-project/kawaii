import os
import platform
import json
import click
from os import path
from .utils import  get_cpu_info, get_host_arch, get_host_os
from jinja2 import Environment, PackageLoader, select_autoescape
from pathlib import Path
def init_meson_crossfile(arch, config):
    app_dir = Path(click.get_app_dir("kawaii-build"))
    if not app_dir.exists():
        app_dir.mkdir(parents=True)
    crossfile_file = open(app_dir.joinpath(f"meson-{arch}.ini"), mode="w")
    env = Environment(
        loader=PackageLoader("simple_and_kawaii"),
        autoescape=select_autoescape(),
    )
    crossfile = env.get_template("crossfile.ini")

    cpu_info = get_cpu_info(arch)
    crossfile_file.write(
        crossfile.render(
            ndk_version=config["android"]["ndk"],
            cpu_info=cpu_info,
            abi=arch,
            sdk_version=config["android"]["sdk"],
            host_arch=get_host_arch(),
            host_os=get_host_os(),
            sdk_root=config["android"]["sdk-root"]
            
        )
    )
