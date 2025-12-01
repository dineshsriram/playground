from dataclasses import dataclass, field
from typing import ClassVar

@dataclass(frozen=True)
class Coordinate:
    x: float
    y: float



@dataclass
class ClubMember:
    name: str
    guests: list[str] = field(default_factory=list)


@dataclass
class HackerClubMember(ClubMember):
    all_handles: ClassVar[set[str]] = set()
    handle: str = ''

    def __post_init__(self):
        if self.handle == '':
            self.handle = self.name.split()[0]
        
        cls= self.__class__
        if self.handle in cls.all_handles:
            raise ValueError("Duplicate handle found")

        cls.all_handles.add(self.handle)