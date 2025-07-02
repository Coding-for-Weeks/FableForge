from rich.console import Console

from fableforge.utils.utilities import clear_console

console = Console()


def run(quest):
    """End scene summarizing the outcome."""
    clear_console()
    name = quest.character[1] if quest.character else "Adventurer"

    if quest.flags.get("solved_riddle"):
        console.print(f"With the riddle solved, {name} retrieves the glowing Crystal Shard. Power hums beneath its surface.")
    else:
        console.print(f"Unable to solve the riddle, {name} leaves the ruins empty-handed, the whispers fading to memory.")

    console.input("[cyan]Press Enter to end the quest...[/cyan]")
    quest.db.reset_quest_progress(quest.character_id, quest.QUEST_NAME)
    return None
