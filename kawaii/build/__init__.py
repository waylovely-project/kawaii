
from tkinter import E
from urllib.parse import urlparse
from .download import download_source
from .collections import get_packages
from .build import build_all
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
from kawaii.utils import top_level

@click.option("--experimental-sources-feature", is_flag=True)
@click.option("--arch", default="arm64-v8a", help="The architechture, supports")
@click.option("--sdk-version", default="29", help="")
@click.option("--ndk-version", default="23.2.8568313", help="")
@click.option("--sdk-root", default=f"{os.environ.get('HOME')}/Android/Sdk", help="")
@click.option("--app-id", type=str, default="none", help="The ID of t")
@click.command()
def build_deps(experimental_sources_feature, arch: str, sdk_version, ndk_version, sdk_root, app_id):    
    """Build native libraries required for Waylovely and Portals.\n
    Mostly they are written in C/C++. They'll get installed to the '' folder of the root directory of the Git repository!
    This behavior can be changed by changing the "deps-location" path in kawaii/cache_config.json file."""
    
    main_config["arch"] = arch.split(",")
    android_config = main_config["android"]
    
  
    packages = dict()
    
    for arch in config["arch"]: 
        packages[arch] = get_packages(config, top_level, arch, app_id)

    sources = list()
    for arch in packages:
        for package in packages[arch]:
          
            package_config = package["config"]
            
            if "sources" in package_config:
                for source in package_config["sources"].keys():
                    sources.append((source, package_config["sources"][source]))
        
    sources = filter(lambda source: len(dict(filter(lambda another_source: another_source is source, sources))) == 1, sources) 
    for source in sources:
       
        url = urlparse(source[1]["url"])
        if url.scheme == "file":
            relative_path = url.netloc + url.path
            path = Path(package["path"]).parent.joinpath(relative_path).resolve()
            if not path.is_dir():
                click.echo(f"Can't continue: {path} is not a folder!!!", err=True)
                exit(1)
        elif experimental_sources_feature:
             download_source(source[0], source[1], path.join(top_level, ".kawaii-sources"), config)
        else:
                click.echo(f"Skipping {package['path']}#{source[1]['url']}", err=True)
    
    for arch in main_config["arch"]:
        build_all(packages[arch], arch, app_id, main_config)
        
