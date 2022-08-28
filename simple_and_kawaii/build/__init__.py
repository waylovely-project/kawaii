from .download import download_source
from .collections import get_packages
from .build_one import build_one 
import asyncio
from hashlib import algorithms_available
import zipfile
import urllib
import tarfile 
import requests
import toml
import json
from os import abort, path
import os
from pathlib import Path
import subprocess
import sys
from traceback import print_tb
from typing import Tuple
import click

from simple_and_kawaii.utils import top_level, get_config


@click.command()
def build_deps():    
    """Build native libraries required for Waylovely and Portals.\n
    Mostly they are written in C/C++. They'll get installed to the '' folder of the root directory of the Git repository!
    This behavior can be changed by changing the "deps-location" path in kawaii/cache_config.json file."""
    config = get_config()

    packages = get_packages(config)

    sources = list()
    for package in packages:
        package_config = package["config"]
        
        if "sources" in package_config:
            for source in package_config["sources"].keys():
                sources.append((source, package_config["sources"][source]))

    with click.progressbar(length=len(sources), label="Downloading sources") as bar:
        for source in sources:
            download_source(source[0], source[1], path.join(top_level, ".kawaii-sources"), bar)
