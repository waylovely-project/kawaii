import asyncio
import hashlib
import urllib
from hashlib import algorithms_available
from os import path
import os
from pathlib import Path
import subprocess
from urllib.parse import urlparse
import requests
import click
import urllib
import tarfile
import zipfile

from .checksum import file_checksum, get_checksum, get_checksum_config


def download_source(source_name, sourcee, sources_location, config):
            if "url" not in sourcee:
                raise Exception(f"The URl for {source_name} is missing!!")
            source = sourcee["url"]
            url = urlparse(source)
            paths = url.path.split("/")
            checksum = get_checksum_config(source, sourcee)
            install_path = path.join(sources_location, source_name.split("/")[-1])
          
            url = urlparse(source)
            ext = list(filter(lambda a : not a.isdigit(), url.path.split("/")[-1:][0].split('.')[1:]))
            
            tarball_path = Path(install_path).joinpath( f"{source_name}.{'.'.join(ext)}")
         
           
            
            if tarball_path.exists() and file_checksum(checksum[1], tarball_path) == checksum[0]:
                return

            folder_path = Path(install_path).joinpath(source_name)

      
            if url.scheme.startswith("git+"):
                source = source.removeprefix("git+")
                place_git = path.join(sources_location, ".git-bares", source_name)
                if not path.exists(place_git):
                    subprocess.run(
                        ["git", "clone", source, place_git, "--bare", "--depth=1"], text=True,
                        check=True
                    )
                if url.fragment:
                    checkout_to = url.fragment
                else:
                    checkout_to = subprocess.check_output(
                        ["git", "ls-remote", source, "HEAD"],
                        text=True
                    )[:-1].split(" ")[0]
                
                if not folder_path.exists():
                    folder_path.mkdir( parents=True)
                   
                   
                subprocess.run(
                    ["git", "checkout", checkout_to],
                    env={
                        "GIT_DIR": place_git
                    },
                    cwd=folder_path
                )

            subprocess.run(["wget", source, "--output-document", tarball_path], check=True)
                    
            if checksum[1] not in config.checksums:
                click(f"{checksum[1]} is not ", err=True)

            if  checksum_found != checksum[0]:
                        os.remove(tarball_path)
                        click.echo(f"Found checksum {checksum_found} for source {source_name}!! Different than checksum {checksum[0]} written in the manifest", err=True)
                        exit(1)
                     
    

def unpack_source(tarball_path, folder_path, ext, callback):
        if not folder_path.exists():
            folder_path.mkdir(parents=True)    

        if ext[-1] == "zip":
                    subprocess.run(["unzip", "-j", tarball_path, "-d", folder_path], check=True)
        elif ext[-2] == "tar":
            if ext[-1] == "gz":
                extfortar = "gzip"
            else:
                extfortar = ext[-1]
                    
            subprocess.run(["tar", "xf", tarball_path, f"--{extfortar}", "--strip-components", "1", "-C", folder_path])
async def download_all_sources(sources, sources_location): 
    
    for source in sources.keys():
        
        asyncio.create_task(download_source(source, sources[source], sources_location))
    
