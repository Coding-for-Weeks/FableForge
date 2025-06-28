"""Quest launcher and inventory menu."""

from fableforge.utils.utilities import clear_console
from fableforge.data.database_manager import DatabaseManager
from fableforge.quests.quest_one import quest_one
from fableforge.quests.quest_two import quest_two
from fableforge.engine.main import Console, play_game
from rich.console import Console as RichConsole

console = RichConsole()


def choose_character():
    """Return the selected character row or ``None`` if selection fails."""
    clear_console()
    console.print("[blue]FableForge - Choose Character![/blue]")
    db_manager = DatabaseManager()
    with db_manager.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, race, class FROM characters")
        characters = cursor.fetchall()
        if not characters:
            console.print("\n[red]No characters found in the database.[/red]")
            console.input("[yellow]Press Enter to return...[/yellow]")
            return None
        console.print("\n[blue]Available Characters:[/blue]\n")
        for cid, name, race, char_class in characters:
            console.print(f"[red]{cid}.[/red] {name} | Race: {race} | Class: {char_class}")
        selected = console.input("\n[bold yellow]Enter character ID: [/bold yellow]").strip()
        if selected.isdigit():
            selected_id = int(selected)
            cursor.execute("SELECT * FROM characters WHERE id = ?", (selected_id,))
            character = cursor.fetchone()
            if character:
                return character
    console.print("[red]Invalid ID. Returning to the quest menu.[/red]")
    console.input("[yellow]Press Enter to continue...[/yellow]")
    return None


def launch_quest(quest_fn):
    """Wrapper that prompts for a character before running ``quest_fn``."""
    character = choose_character()
    if character:
        quest_fn(character)


def inventory_menu():
    """Allow adding, removing, or viewing a character's inventory."""
    character = choose_character()
    if not character:
        return
    character_id, name = character[0], character[1]
    db_manager = DatabaseManager()

    def view_inventory():
        clear_console()
        items = db_manager.get_inventory(character_id)
        if items:
            console.print(f"[blue]{name}'s Inventory:[/blue]\n")
            for item, qty in items:
                console.print(f"[red]{item}[/red] x{qty}")
        else:
            console.print("[red]Inventory is empty.[/red]")
        console.input("\n[yellow]Press Enter to continue...[/yellow]")

    def add_item():
        clear_console()
        item = console.input("Item name: ").strip()
        qty = console.input("Quantity: ").strip()
        try:
            qty = int(qty)
        except ValueError:
            qty = 1
        db_manager.add_item(character_id, item, qty)
        console.print("\nItem added!")
        console.input("[yellow]Press Enter to continue...[/yellow]")

    def remove_item():
        clear_console()
        item = console.input("Item name to remove: ").strip()
        qty = console.input("Quantity: ").strip()
        try:
            qty = int(qty)
        except ValueError:
            qty = 1
        db_manager.remove_item(character_id, item, qty)
        console.print("\nItem removed (if it existed).")
        console.input("[yellow]Press Enter to continue...[/yellow]")

    options = [
        {"label": "View Inventory", "action": view_inventory},
        {"label": "Add Item", "action": add_item},
        {"label": "Remove Item", "action": remove_item},
        {"label": "Back", "action": None},
    ]
    Console.menu_handler(f"Inventory Menu - {name}", options)


def quest_menu():
    options = [
        {"label": "List Quests", "action": list_quests},
        {"label": "Complete Quest", "action": complete_quest},
        {"label": "Manage Inventory", "action": inventory_menu},
        {"label": "Back to Play Menu", "action": play_game},
    ]
    Console.menu_handler("FableForge - Quest Menu", options)


def whisper_quest_entry(character):
    """Entry point for the 'Whispers of the Crystal Shard' quest."""
    db = DatabaseManager()
    character_id = character[0]

    clear_console()
    console.print("[blue]FableForge - Whispers of the Crystal Shard[/blue]\n")
    console.print("What would you like to do?")
    console.print("[red]1.[/red] Start the quest")
    console.print("[red]2.[/red] Resume Saved Quest")
    console.print("[red]3.[/red] Back")

    choice = console.input("\n[bold yellow]Choose an option: [/bold yellow]").strip()
    if choice == "1":
        db.reset_quest_progress(character_id, "Whispers of the Crystal Shard")
        quest_one(character, character_id, db)
    elif choice == "2":
        progress = db.load_quest_progress(character_id, "Whispers of the Crystal Shard")
        if not progress:
            console.print("[red]No saved progress found. Starting fresh.[/red]")
            quest_one(character, character_id, db)
        else:
            console.print("[blue]Resuming saved quest progress...[/blue]")
            console.print(f"[yellow]Progress: {progress}[/yellow]")
            quest_one(character, character_id, db, progress)
    else:
        console.print("[red]Returning to the quest menu.[/red]")
        console.input("[yellow]Press Enter to continue...[/yellow]")


# Quests

def list_quests():
    options = [
        {"label": "Whispers of the Crystal Shard", "action": lambda: launch_quest(whisper_quest_entry)},
        {"label": "The Forgotten Ember", "action": lambda: launch_quest(quest_two)},
        {"label": "Back to Previous Menu", "action": quest_menu},
    ]
    Console.menu_handler("FableForge - Quests", options)


def complete_quest():
    clear_console()
    console.print("Complete a Quest")
    console.input("Press Enter to continue...")
