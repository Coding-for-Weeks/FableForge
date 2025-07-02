"""Compatibility wrapper for the 'Whispers of the Crystal Shard' quest."""

from fableforge.quests.whisper_quest import WhisperQuest


def quest_one(character, character_id, db, progress=None):
    """Launch the refactored quest using ``WhisperQuest``."""
    quest = WhisperQuest(character, character_id, db, progress)
    quest.start()

