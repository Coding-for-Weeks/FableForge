from rich.console import Console

from fableforge.utils.utilities import clear_console
from fableforge.engine.dialogue import NPC, run_dialogue

console = Console()


def run(quest):
    """Encounter with the hooded figure."""
    clear_console()
    name = quest.character[1] if quest.character else "Adventurer"

    console.print(f"{name} slips through the crowd, trailing the hooded figure into a narrow alley.")

    npc = NPC(
        name="Hooded Figure",
        tree={
            "start": {
                "text": "You heard the call. The shard seeks those who listen.",
                "options": {"Where can I find it?": "where", "Who are you?": "who"},
            },
            "where": {"text": "In the ruins east of town. Beware its guardians.", "options": {"Thanks": None}},
            "who": {"text": "Merely a messenger of ancient powers.", "options": {"Farewell": None}},
        },
    )
    run_dialogue(npc)
    console.input("[cyan]Press Enter to continue...[/cyan]")
    return "puzzle"
