from graphlib import TopologicalSorter
from typing import Callable, List, Optional
from .project import Project

def sort_deps(projects: List[Project]):
    
    dicty = dict()
    for project in projects:
        dicty[project.id] = map(lambda project : project.id, project.deps or [])

    sorter = TopologicalSorter(dicty)
    
    return sorter

