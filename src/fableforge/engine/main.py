#!/usr/bin/env python3

"""Entry point and CLI for FableForge."""

import random
from rich.console import Console as RichConsole

from fableforge.utils.utilities import clear_console, exiting, setup_logging
from fableforge.data.database_manager import DatabaseManager
from fableforge.data.models import Stats
from fableforge.menus import Console, play_game


console = RichConsole()

class CharacterCreator:
    """Utility class for interactive character creation."""

    @staticmethod
    def get_character_name():
        clear_console()
        console.print("[blue]FableForge - Character Creation![/blue]")
        return console.input("\n[bold yellow]Enter your character's name:[/bold yellow] ").strip()

    @staticmethod
    def select_race():
        races = {
            "Gnome": ["Rock Gnome", "Forest Gnome", "Deep Gnome"],
            "Dwarf": ["Hill Dwarf", "Mountain Dwarf", "Duergar"],
            "Elf": ["High Elf", "Wood Elf", "Dark Elf"],
        }
        additional = ["Half-Orc", "Goliath", "Human", "Dragonborn", "Kobold", "Tiefling"]
        for race in additional:
            races[race] = []
        while True:
            clear_console()
            CharacterCreator.print_races(races)
            race_input = console.input("\n[bold yellow]Enter your race:[/bold yellow] ").strip().title()
            if race_input in races:
                return CharacterCreator.select_subrace(race_input, races[race_input])
            Console.invalid_choice()

    @staticmethod
    def print_races(races):
        console.print("[blue]FableForge - Available Races:[/blue]\n")
        for race, subraces in races.items():
            console.print(f"[red]{race}[/red]")
            for sr in subraces:
                console.print(f"  [blue]- {sr}[/blue]")

    @staticmethod
    def select_subrace(race, subraces):
        if not subraces:
            return race, None
        while True:
            clear_console()
            console.print(f"[blue]Available Subraces for {race}:[/blue]\n")
            for sr in subraces:
                console.print(f"  [red]- {sr}[/red]")
            choice = console.input("\n[bold yellow]Enter your subrace:[/bold yellow] ").strip().title()
            if choice in subraces:
                return race, choice
            Console.invalid_choice()

    @staticmethod
    def select_class():
        basic = [
            "Fighter",
            "Wizard",
            "Rogue",
            "Cleric",
            "Bard",
            "Warlock",
            "Druid",
            "Barbarian",
            "Monk",
            "Ranger",
            "Paladin",
            "Sorcerer",
        ]
        advanced = ["Artificer", "Hexblade", "Psion", "Warlord", "Swashbuckler"]
        while True:
            clear_console()
            CharacterCreator.print_classes(basic, advanced)
            choice = console.input("\n[bold yellow]Choose your class:[/bold yellow] ").strip().capitalize()
            if choice in basic + advanced:
                return choice
            Console.invalid_choice()

    @staticmethod
    def print_classes(basic, advanced):
        console.print("[blue]FableForge - Available Classes:[/blue]\n")
        header = f"{'Basic Classes:':<20} {'Advanced Classes:':<20}"
        console.print(f"[blue]{header}[/blue]\n")
        max_len = max(len(basic), len(advanced))
        for i in range(max_len):
            b = basic[i] if i < len(basic) else ""
            a = advanced[i] if i < len(advanced) else ""
            console.print(f"[red]{b:<20} {a:<20}[/red]")

    @staticmethod
    def generate_stats():
        options = {"1": "manual", "2": "random"}
        while True:
            clear_console()
            console.print("[blue]FableForge - Stat generation method:[/blue]\n")
            console.print("[red]1.[/red] Manually distribute points")
            console.print("[red]2.[/red] Generate random stats")
            choice = console.input("\n[bold yellow]Enter your choice:[/bold yellow] ").strip()
            if choice in options:
                if options[choice] == "manual":
                    return CharacterCreator.manual_stats()
                return CharacterCreator.random_stats()
            Console.invalid_choice()

    @staticmethod
    def manual_stats():
        stats = {k: 0 for k in [
            "strength",
            "dexterity",
            "intelligence",
            "charisma",
            "wisdom",
            "constitution",
        ]}
        total = 75
        console.print(f"You have {total} points to distribute (8-18 per stat):")
        names = list(stats.keys())
        for idx, stat in enumerate(names):
            remaining = len(names) - idx
            while True:
                try:
                    max_alloc = min(18, total - 8 * (remaining - 1))
                    alloc = int(console.input(
                        f"Allocate to {stat.capitalize()} (remaining: {total}, max {max_alloc}): "
                    ))
                    if 8 <= alloc <= max_alloc:
                        stats[stat] = alloc
                        total -= alloc
                        break
                    console.print(f"Invalid allocation. Enter a value between 8 and {max_alloc}.")
                except ValueError:
                    console.print("Enter a valid number.")
        return Stats(**stats)

    @staticmethod
    def random_stats():
        values = {k: random.randint(8, 18) for k in [
            "strength",
            "dexterity",
            "intelligence",
            "charisma",
            "wisdom",
            "constitution",
        ]}
        return Stats(**values)


def main_menu():
    options = [
        {"label": "Create a new character", "action": create_character},
        {"label": "Play", "action": play_game},
        {"label": "Exit", "action": exiting},
    ]
    Console.menu_handler("FableForge - Main Menu", options)


def create_character():
    name = CharacterCreator.get_character_name()
    race, subrace = CharacterCreator.select_race()
    char_class = CharacterCreator.select_class()
    stats = CharacterCreator.generate_stats()

    clear_console()
    console.print("[blue]FableForge - Character Summary![/blue]")
    console.print("[blue]Character Details:[/blue]\n")
    console.print(f"[red]Name:[/red] {name}")
    console.print(f"[red]Race:[/red] {race} {'(' + subrace + ')' if subrace else ''}")
    console.print(f"[red]Class:[/red] {char_class}")
    console.print("[blue]Stats:[/blue]")
    for field, value in stats.__dict__.items():
        console.print(f"  [red]{field.capitalize()}[/red]: {value}")

    db_manager = DatabaseManager()
    with db_manager.connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO characters (
                name, race, class, strength, dexterity, intelligence,
                charisma, wisdom, constitution, health, experience
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                f"{race} ({subrace})" if subrace else race,
                char_class,
                stats.strength,
                stats.dexterity,
                stats.intelligence,
                stats.charisma,
                stats.wisdom,
                stats.constitution,
                100,
                0,
            ),
        )
        conn.commit()
        console.print("\n[blue]Character saved to database![/blue]")
        console.input("\n[bold yellow]Press Enter to continue...[/bold yellow]")


def character():
    clear_console()
    options = [
        {"label": "Choose Character", "action": character_choice},
        {"label": "Delete Character", "action": delete_character},
        {"label": "Back to Play Menu", "action": play_game},
    ]
    Console.menu_handler("FableForge - Character Menu", options)


def character_choice():
    clear_console()
    console.print("[blue]FableForge - Choose Character![/blue]")

    db_manager = DatabaseManager()
    with db_manager.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, race, class FROM characters")
        characters = cursor.fetchall()

        if not characters:
            console.print("\n[red]No characters found in the database.[/red]")
            console.input("[yellow]Press Enter to return to the main menu...[/yellow]")
            return

        console.print("\n[blue]Available Characters:[/blue]\n")
        for char in characters:
            name, race, char_class = char
            console.print(f"[red]Name:[/red] {name} | [red]Race:[/red] {race} | [red]Class:[/red] {char_class}")

        console.print("\n[blue]Select a character by entering their name.[/blue]")
        selected_name = console.input("[bold yellow]Enter character name: [/bold yellow]").strip()

        cursor.execute("SELECT * FROM characters WHERE name = ? COLLATE NOCASE", (selected_name,))
        character = cursor.fetchone()

    if character:
        clear_console()
        console.print("[blue]Character Details:[/blue]\n")
        console.print(f"[red]Name:[/red] {character[1]}")
        console.print(f"[red]Race:[/red] {character[2]}")
        console.print(f"[red]Class:[/red] {character[3]}")
        console.print("[blue]Stats:[/blue]")
        for stat, value in zip([
            "Strength",
            "Dexterity",
            "Intelligence",
            "Charisma",
            "Wisdom",
            "Constitution",
        ], character[4:10]):
            console.print(f"  [red]{stat}[/red]: {value}")
        console.print(f"[red]Health:[/red] {character[10]}")
        console.print(f"[red]Experience:[/red] {character[11]}")
        inventory = db_manager.get_inventory(character[0])
        if inventory:
            console.print("\n[blue]Inventory:[/blue]")
            for item, qty in inventory:
                console.print(f"  [red]{item}[/red] x{qty}")
    else:
        console.print("[red]Invalid Name. Returning to the main menu.[/red]")
    console.input("\n[bold yellow]Press Enter to continue...[/bold yellow]")


def delete_character():
    clear_console()
    console.print("[blue]FableForge - Delete Character![/blue]")

    db_manager = DatabaseManager()
    with db_manager.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, race, class FROM characters")
        characters = cursor.fetchall()

        if not characters:
            console.print("\n[red]No characters found in the database.[/red]")
            console.input("[yellow]Press Enter to return to the main menu...[/yellow]")
            return

        console.print("\n[blue]Available Characters:[/blue]\n")
        for char in characters:
            name, race, char_class = char
            console.print(f"[red]Name:[/red] {name} | [red]Race:[/red] {race} | [red]Class:[/red] {char_class}")

        console.print("\n[blue]Select a character to delete by entering their name.[/blue]")
        selected_name = console.input("[bold yellow]Enter character name: [/bold yellow]").strip()

        cursor.execute("SELECT * FROM characters WHERE name = ? COLLATE NOCASE", (selected_name,))
        character = cursor.fetchone()

        if character:
            cursor.execute("DELETE FROM characters WHERE name = ? COLLATE NOCASE", (selected_name,))
            conn.commit()
            clear_console()
            console.print(f"[red]Character {selected_name} has been deleted.[/red]")
        else:
            console.print("[red]Invalid Name. Returning to the main menu.[/red]")
    console.input("\n[bold yellow]Press Enter to continue...[/bold yellow]")


def main():
    """Program entry point."""
    setup_logging()
    db_manager = DatabaseManager()
    db_manager.initialize_tables()
    main_menu()


if __name__ == "__main__":
    main()
