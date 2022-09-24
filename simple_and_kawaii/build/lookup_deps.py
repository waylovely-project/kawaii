import click 
from pathlib import Path
from typing import Dict, List

from .project import Project

def lookup_deps_projects(projects: List[Project]):
    for project in projects:
        lookup_deps_project(project, projects)

def lookup_deps_project(project: Project, all_projects: List[Project]):
    
    deps = list()
    for dep in project.deps:
        dep = lookup_dep(dep, all_projects)
        try: 
            iter(dep)
        except TypeError:
            deps.append(dep)
        else: 
            deps.extend(dep)

        for dep in dep:
            depdep = lookup_deps_project(dep, all_projects)
            dep.deps = depdep
            deps.extend(depdep)

    return deps

def lookup_dep(dep: str, all_projects: List[Project], **kwargs):
    if dep.endswith("/*"):
        category = dep.removesuffix("/*")
        projects = filter(lambda project : project.category == category, all_projects)

    else:
        allow_multiple = dep.startswith("**/")
        
        dep = dep.removeprefix("**/")
        projects = list(filter(lambda project : project.path.name.removesuffix(".kawaii") == dep,  all_projects))

        if not allow_multiple and len(projects) > 1:
            click.echo(f"{click.style(' ERROR ')} Multiple dependencies for {kwargs.get('project_name') or 'unknown'}: {list(projects)}")
            exit(1)
            
    return list(projects)
        
            