from graphlib import TopologicalSorter
from typing import Callable, List, Optional
from .project import FullyInitedProject

def sort_deps(projects: List[FullyInitedProject]):
    
    dicty = dict()
    for project in projects:
        dicty[project.id] = list(map(lambda project : project.id, project.deps or []))
  
    sorter = TopologicalSorter(dicty)
    
    return sorter

