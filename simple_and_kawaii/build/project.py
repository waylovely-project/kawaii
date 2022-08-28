
from os import path
from simple_and_kawaii.utils import top_level, get_config_key
def packages_folder(**kwargs):
    return path.join(
        get_config_key("libs-folder") or path.join(top_level, "prebuilt-libs"),
        get_config_key("android-abi"),
    )
class Project:
    def __init__(self, name: str, path: str, deps: list):
        self.name = name
        self.path = path
        self.deps = deps
        self.deps_left = deps





