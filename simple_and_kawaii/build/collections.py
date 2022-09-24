from urllib.parse import urlparse
import click
from jinja2 import Environment, DictLoader, select_autoescape
from .project import Project, ProjectSource
import toml
from pathlib import Path
from os import listdir, path
from simple_and_kawaii.build.utils import get_envvars
from simple_and_kawaii.utils import top_level
def get_packages(config, path, arch, app_id, main_config, **kwargs): 
    packages = list()
 
    for deps_folder in config["collection"]["collections"]:
        deps_folder = Path(path).joinpath(deps_folder)
        for file_path in deps_folder.iterdir():
            if file_path.is_file() and file_path.suffix == ".kawaii":
                config_str = open(file_path).read()
                env = Environment(
                    loader=DictLoader({file_path.name: config_str}),
                    autoescape=select_autoescape(),
                )
                manifest = env.get_template(file_path.name)
           
                (env, _,) = get_envvars("", arch, app_id, main_config, **kwargs)
                        

                config = toml.loads(manifest.render(env))
                
                
                packages.append(Project(file_path.name.removesuffix(".kawaii"), config.get("deps") or [], [map(lambda source: ProjectSource(source.get("url"), source.get("local"), source.get("checksum-type")), config["sources"])],  arch, file_path, config, None, file_path.parent.name))



    return packages


def get_source_package(path: Path, arch: str):
    config_file = path.joinpath("build.kawaii")    
    if not config_file.exists():
        click.echo("build.kawaii does not exist")
        exit(1)
    if not config_file.is_file():  
        click.echo(f"{str(config_file)} is not a regular file")  
        exit(1)

    config = toml.loads(open(config_file).read())

    return Project(path.name, config.get("deps"), [ProjectSource(None, path,None, None)], arch, config_file, config, path.name, None)




def get_remote_collections(config):
    for remote in config["remote"].keys():
        url = urlparse(config["remote"][remote])

        if url["scheme"] != "file":
            click.echo("At the moment, non-local sources are not supported!!")
            exit(1)
        


#  if "sources" in project_config:
# sources = project_config["sources"]
#                sources_location = path.join(deps_folder, ".sources")
 #               
  #              download_all_sources(sources, sources_location)
        #   else: 
           #     click.echo(f"Can't get the sources for {file_path}!!", err=True)
           #     exit(1)