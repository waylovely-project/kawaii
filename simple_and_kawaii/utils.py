import subprocess
from os import path


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

root_source_dir = subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], text=True
)[:-1]
build_path = path.join(root_source_dir, "kawaii")
cache_path = path.join(build_path, "cache")
