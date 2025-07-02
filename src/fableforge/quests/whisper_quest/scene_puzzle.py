from rich.console import Console
import random

from fableforge.utils.utilities import clear_console

console = Console()


def run(quest):
    """Simple riddle gate to the shard."""
    clear_console()
    name = quest.character[1] if quest.character else "Adventurer"

    console.print(f"At the entrance to the ruins, a stone door blocks {name}'s path.")
    console.print("\nA riddle is carved into the stone: \"I speak without a mouth and hear without ears. What am I?\"")
    answer = console.input("\n[bold yellow]Your answer: [/bold yellow]").strip().lower()

    if "echo" in answer:
        console.print("[green]The door slides open with a low rumble.[/green]")
        quest.flags["solved_riddle"] = True
    else:
        console.print("[red]Nothing happens. Perhaps that was not it...[/red]")
        quest.flags["solved_riddle"] = False

    console.input("[cyan]Press Enter to continue...[/cyan]")
    return "conclusion"
