from rich.console import Console as RichConsole
from rich.table import Table

from fableforge.utils.utilities import clear_console

console = RichConsole()

class Console:
    """Wrapper around ``rich`` console for simple menu handling."""

    @staticmethod
    def menu_handler(title, options):
        while True:
            clear_console()
            table = Table(title=title, show_header=False, title_style="bold blue")
            for idx, opt in enumerate(options, 1):
                table.add_row(f"[bold red]{idx}[/bold red]", opt["label"])
            console.print(table)
            choice = console.input("[bold yellow]Choose an option:[/bold yellow] ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                action = options[int(choice) - 1]["action"]
                if action is None:
                    return
                action()
            else:
                Console.invalid_choice()

    @staticmethod
    def invalid_choice():
        console.print("[red]Invalid choice. Please try again.[/red]")
        console.input("[bold]Press Enter to continue...[/bold]")


def play_game():
    """Display the play menu with character and quest options."""
    from fableforge.quests import quest_menu  # local import to avoid circular dependency
    from fableforge.engine import main as engine_main

    options = [
        {"label": "Character Menu", "action": engine_main.character},
        {"label": "Quest Menu", "action": quest_menu},
        {"label": "Back to main menu", "action": engine_main.main_menu},
    ]
    Console.menu_handler("FableForge - Play", options)