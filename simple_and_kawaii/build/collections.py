import toml
from pathlib import Path
from os import listdir, path
from simple_and_kawaii.utils import top_level
def get_packages(config): 
    packages = list()
    for deps_folder in config["collection"]["collections"]:
        deps_folder = Path(top_level).joinpath(deps_folder)
        for file_path in deps_folder.iterdir():
            file_path = deps_folder.joinpath(file_path)
            if file_path.is_file() and file_path.suffix == ".kawaii":
                project_config = toml.loads(open(file_path).read())
                packages.append({
                    "path": file_path,
                    "config": project_config
                })

    return packages

                


#  if "sources" in project_config:
# sources = project_config["sources"]
#                sources_location = path.join(deps_folder, ".sources")
 #               
  #              download_all_sources(sources, sources_location)
        #   else: 
           #     click.echo(f"Can't get the sources for {file_path}!!", err=True)
           #     exit(1)