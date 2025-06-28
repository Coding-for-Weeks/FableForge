from dataclasses import dataclass
from typing import Optional

@dataclass
class Stats:
    strength: int
    dexterity: int
    intelligence: int
    charisma: int
    wisdom: int
    constitution: int

@dataclass
class Character:
    id: int
    name: str
    race: str
    cls: str
    stats: Stats
    health: int = 100
    experience: int = 0

@dataclass
class Quest:
    id: int
    name: str
    description: str
    completed: bool
    progress: Optional[str]
    character_id: int

@dataclass
class InventoryItem:
    id: int
    item_name: str
    quantity: int
    character_id: int

@dataclass
class LogEntry:
    id: int
    message: str
    level: str
    timestamp: str
