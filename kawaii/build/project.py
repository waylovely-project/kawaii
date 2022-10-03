from typing_extensions import Self


from typing import ClassVar, Type

from marshmallow_dataclass import dataclass
from marshmallow import Schema
from pathlib import Path
from typing import List, Optional
from kawaii.utils import top_level
def packages_folder(arch, config):
    path = Path(
        config.get("install-path") or Path(top_level).joinpath(".kawaii-libs")).joinpath(
        arch)
    
    if not path.exists():
        path.mkdir(parents=True)
    
    return path

@dataclass
class ProjectSource:
    url: Optional[str]
    local: Optional[str]
    checksum: Optional[str]
    checksum_type: Optional[str]
    
@dataclass
class UninitProject:
    name: str
    deps: Optional[List[str]]
    sources: List[ProjectSource]    
    Schema: ClassVar[Type[Schema]] = Schema

@dataclass
class HalfInitedProject(UninitProject):
    id: Optional[str]
    arch: str
    category: Optional[str]
    """ Path to the project's manifest: eg '~/wrap-packages/glib.kawaii' """
    path: Path
    """ The dependencies that """
    deps: List[str]
    Schema: ClassVar[Type[Schema]] = Schema
        
@dataclass
class FullyInitedProject(HalfInitedProject):
    deps: List[Self]
    
