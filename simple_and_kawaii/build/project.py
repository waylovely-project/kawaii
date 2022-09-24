from dataclasses import dataclass, field
from lib2to3.pgen2.tokenize import StopTokenizing
from os import path
from pathlib import Path
from typing import List, Optional
from simple_and_kawaii.utils import top_level
def packages_folder(arch, config):
    return path.join(
        config.get("install-path") or path.join(top_level, "prebuilt-libs"),
        arch,
    )

@dataclass
class ProjectSource:
    url: Optional[str]
    local: Optional[str]
    checksum: Optional[str]
    checksum_type: Optional[str]
    
@dataclass
class Project:
    name: str
    deps: Optional[List[str]]
    sources: List[ProjectSource]
    arch: str
    path: Path
    config: dict
    id: Optional[str]
    category: Optional[str]
