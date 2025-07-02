from rich.console import Console

from fableforge.utils.utilities import clear_console

console = Console()


def run(quest):
    """Initial scene presenting the mysterious call."""
    clear_console()
    name = quest.character[1] if quest.character else "Adventurer"

    intro = (
        "[bold blue]FableForge - The Withering Veil[/bold blue]\n"
        "\n[bold]You awaken not with sunlight, but with the weight of stillness.[/bold]\n"
        "A pale mist clings to the earth, coiling like fingers around your boots as you arrive on the outskirts of [cyan]Greymire[/cyan]. "
        "The morning is silent—too silent. No birdsong, no cartwheels, just the soft creak of a weathered sign swinging in the breeze. "
        "[yellow]GREYMIRE[/yellow] – the name is carved in rotting oak, the letters warped as if melted by time. "
        "From the forest nearby, a wind howls. But it doesn’t sound like wind. It sounds like... [red]laughing[/red]. "
        "Ahead, an old woman in a dark shawl watches you from a porch. She doesn’t blink. Doesn’t move. Just stares—and when you glance again... "
        "[bold]…she’s gone.[/bold] "
        "The village gate lies open. The dirt road ahead is marked with fresh prints—some human, some not. "
        "As you take your first step into [cyan]Greymire[/cyan], you hear a soft voice behind you, carried on the wind: \n[bold red]“They’re already watching you.”[/bold red]"
    )


    console.print(intro)
    console.print("\n[bold white] What do you do?[/bold white]")
    console.print("\n[green]1.[/green] Follow the strange footprints into the village")
    console.print("[green]2.[/green] Approach the house where the old woman vanished")
    console.print("[green]3.[/green] Call out into the fog")
    console.print("[green]4.[/green] Light a torch to push back the mist")

    # Wait for valid input
    valid = {"1", "2", "3", "4"}
    choice = ""
    while choice not in valid:
        choice = console.input("\n[bold yellow]Choose your path: [/bold yellow]").strip()

    if choice == "1":
        return "encounter1"
    elif choice == "2":
        return "encounter2"
    elif choice == "3":
        return "encounter3"
    elif choice == "4":
        return "encounter4"
    return "scene_intro"
