from rich.console import Console

from fableforge.utils.utilities import clear_console

console = Console()


def run(quest):
    """Initial scene presenting the mysterious call."""
    clear_console()
    name = quest.character[1] if quest.character else "Adventurer"

    intro = (
        "[blue]FableForge - Whispers of the Crystal Shard[/blue]\n\n"
        f"A haunting melody brushes past {name}. In the corner of the market, a hooded figure watches."
    )
    console.print(intro)
    console.print("\n[green]1.[/green] Follow the figure")
    console.print("[green]2.[/green] Investigate the strange whispers")
    console.print("[green]3.[/green] Ignore everything and continue on")

    valid = {"1", "2", "3"}
    choice = ""
    while choice not in valid:
        choice = console.input("\n[bold yellow]Choose your path: [/bold yellow]").strip()

    if choice == "1":
        quest.flags["followed"] = True
        return "encounter"
    if choice == "2":
        return "puzzle"
    return "conclusion"
