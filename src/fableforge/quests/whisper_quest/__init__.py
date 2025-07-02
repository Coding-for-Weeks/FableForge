"""Whispers of the Crystal Shard quest package."""

from rich.console import Console

from fableforge.utils.utilities import clear_console
from . import scene_intro, scene_encounter, scene_puzzle, scene_conclusion

console = Console()


class WhisperQuest:
    """Coordinator for the quest scenes."""

    QUEST_NAME = "Whispers of the Crystal Shard"

    def __init__(self, character, character_id, db, progress=None):
        self.character = character
        self.character_id = character_id
        self.db = db
        self.flags = {}
        self.progress = progress or "intro"

    def start(self):
        """Run scenes sequentially based on ``self.progress``."""
        scene_map = {
            "intro": scene_intro.run,
            "encounter": scene_encounter.run,
            "puzzle": scene_puzzle.run,
            "conclusion": scene_conclusion.run,
        }

        current = self.progress
        while current:
            run_scene = scene_map[current]
            next_scene = run_scene(self)
            if next_scene:
                self.db.save_quest_progress(self.character_id, self.QUEST_NAME, next_scene)
            current = next_scene

