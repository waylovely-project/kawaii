import json
import subprocess
from os import path

def get_config():
    return json.loads(open(path.join(build_path, "config.json")).read())
def get_cpu_info(abi: str):
    if abi == "arm64-v8a":
        return {"triple": "aarch64-linux-android", "family": "aarch64"}
    elif abi == "armv7a-eabi":
        return {"triple": "armv7a-linux-androideabi", "family": "arm"}
    elif abi == "x86_64":
        return {"triple": "x86_64-linux-android", "family": "x86"}
    elif abi == "x86":
        return {"triple": "x86_32-linux-android", "family": "x86"}


__version__ = "0.1.0"


def __show_top_level(path):
    return subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True, cwd=path
)[:-1]


def show_top_level():
    path = __show_top_level(os.getcwd())
    try:
        return __show_top_level(os.path.dirname(path))
    except subprocess.CalledProcessError:
        return path


build_path = path.join(show_top_level(), "kawaii")
cache_path = path.join(build_path, "cache")
