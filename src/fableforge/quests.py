from fableforge.utilities import clear_console
from fableforge.database_manager import DatabaseManager
from fableforge.quest_one import quest_one
from fableforge.quest_two import quest_two
from fableforge.style import BLUE, RED, YELLOW, RESET

def choose_character():
    """Return the selected character row or ``None`` if selection fails."""

    clear_console()
    print(f"{BLUE}FableForge - Choose Character!{RESET}")

    db_manager = DatabaseManager()
    with db_manager.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, race, class FROM characters")
        characters = cursor.fetchall()

        if not characters:
            print(f"\n{RED}No characters found in the database.{RESET}")
            input(f"{YELLOW}Press Enter to return...{RESET}")
            return None

        print(f"\n{BLUE}Available Characters:{RESET}\n")
        for cid, name, race, char_class in characters:
            print(f"{RED}{cid}. {name}{RESET} | Race: {race} | Class: {char_class}")

        selected = input(f"\n{YELLOW}Enter character ID: {RESET}").strip()

        if selected.isdigit():
            selected_id = int(selected)
            cursor.execute("SELECT * FROM characters WHERE id = ?", (selected_id,))
            character = cursor.fetchone()
            if character:
                return character

    print(f"{RED}Invalid ID. Returning to the quest menu.{RESET}")
    input(f"{YELLOW}Press Enter to continue...{RESET}")
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
    char_id, name = character[0], character[1]
    db_manager = DatabaseManager()

    def view_inventory():
        clear_console()
        items = db_manager.get_inventory(char_id)
        if items:
            print(f"{BLUE}{name}'s Inventory:{RESET}\n")
            for item, qty in items:
                print(f"{RED}{item}{RESET} x{qty}")
        else:
            print(f"{RED}Inventory is empty.{RESET}")
        input(f"\n{YELLOW}Press Enter to continue...{RESET}")

    def add_item():
        clear_console()
        item = input("Item name: ").strip()
        qty = input("Quantity: ").strip()
        try:
            qty = int(qty)
        except ValueError:
            qty = 1
        db_manager.add_item(char_id, item, qty)
        print("\nItem added!")
        input(f"{YELLOW}Press Enter to continue...{RESET}")

    def remove_item():
        clear_console()
        item = input("Item name to remove: ").strip()
        qty = input("Quantity: ").strip()
        try:
            qty = int(qty)
        except ValueError:
            qty = 1
        db_manager.remove_item(char_id, item, qty)
        print("\nItem removed (if it existed).")
        input(f"{YELLOW}Press Enter to continue...{RESET}")

    from fableforge.main import Console
    options = [
        {"label": "View Inventory", "action": view_inventory},
        {"label": "Add Item", "action": add_item},
        {"label": "Remove Item", "action": remove_item},
        {"label": "Back", "action": None},
    ]
    Console.menu_handler(f"Inventory Menu - {name}", options)

def quest_menu():
    from fableforge.main import Console, play_game
    options = [
        {"label": "List Quests", "action": list_quests},
        {"label": "Complete Quest", "action": complete_quest},
        {"label": "Manage Inventory", "action": inventory_menu},
        {"label": "Back to Play Menu", "action": play_game},
    ]
    Console.menu_handler("FableForge - Quest Menu", options)

# Quests
def list_quests():
    options = [
        {"label": "Whispers of the Crystal Shard", "action": lambda: launch_quest(quest_one)},
        {"label": "The Forgotten Ember", "action": lambda: launch_quest(quest_two)},
        {"label": "Back to Previous Menu", "action": quest_menu}
    ]
    from fableforge.main import Console
    Console.menu_handler("FableForge - Quests", options)

def complete_quest():
    clear_console()
    print("Complete a Quest")
    input("Press Enter to continue...")
    

