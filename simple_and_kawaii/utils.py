import json
import os
import subprocess
from os import path


def get_config():
    return json.loads(open(path.join(build_path, "config.json")).read())


def get_cache_config():
    return json.loads(open(path.join(build_path, "cache", "config.json")).read())


def get_cpu_info(abi: str):
    if abi == "arm64-v8a":
        return {"triple": "aarch64-linux-android", "family": "aarch64"}
    elif abi == "armv7a-eabi":
        return {"triple": "armv7a-linux-androideabi", "family": "arm"}
    elif abi == "x86_64":
        return {"triple": "x86_64-linux-android", "family": "x86"}
    elif abi == "x86":
        return {"triple": "i686-linux-android", "family": "x86"}

def get_host_arch():
    host_arch = platform.machine()

    if host_arch == "AMD64":
        host_arch = "x86_64"
        host_arch.lower()
    
    return host_arch

def get_host_os():
    if platform.system() == "Java":
        click.echo(
            "For the time being, kawaii init can't be use with Jython, as it exposes the operating system's name as 'Java'",
            err=True,
        )
    return platform.system().lower()


__version__ = "0.1.0"


def __show_top_level(path):
    return subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True, cwd=path,
        stderr=subprocess.DEVNULL
    )[:-1]


def show_top_level():
    path = __show_top_level(os.getcwd())
    try:
        return __show_top_level(os.path.dirname(path))
    except subprocess.CalledProcessError:
        return path


build_path = path.join(show_top_level(), "kawaii")
cache_path = path.join(build_path, "cache")
