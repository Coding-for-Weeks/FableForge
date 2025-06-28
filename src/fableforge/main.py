#!/usr/bin/env python3

import random
from fableforge.utilities import clear_console, exiting, setup_logging
from fableforge.database_manager import DatabaseManager
from fableforge.quests import quest_menu
from fableforge.style import BOLD, BLUE, RED, YELLOW, RESET

class Console:
    @staticmethod
    def menu_handler(title, options):
        while True:
            clear_console()
            Console.print_menu(title, options)
            choice = input(f"\n{YELLOW}Choose an option: {RESET}").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                action = options[int(choice) - 1]["action"]
                if action is None:
                    return
                action()
            else:
                Console.invalid_choice()

    @staticmethod
    def print_menu(title, options):
        print(f"{BOLD}{BLUE}{title}{RESET}\n")
        for i, option in enumerate(options, start=1):
            print(f"{BOLD}{RED}{i}. {option['label']}{RESET}")

    @staticmethod
    def invalid_choice():
        print(f"{RED}Invalid choice. Please try again.{RESET}")
        input(f"{BOLD}Press Enter to continue...{RESET}")

class CharacterCreator:
    @staticmethod
    def get_character_name():
        clear_console()
        print(f"{BLUE}FableForge - Character Creation!{RESET}")
        return input(f"\n{YELLOW}Enter your character's name: {RESET}").strip()

    @staticmethod
    def select_race():
        races = {
            "Gnome": ["Rock Gnome", "Forest Gnome", "Deep Gnome"],
            "Dwarf": ["Hill Dwarf", "Mountain Dwarf", "Duergar"],
            "Elf": ["High Elf", "Wood Elf", "Dark Elf"],
        }
        additional_races = [
            "Half-Orc", "Goliath", "Human",
            "Dragonborn", "Kobold", "Tiefling",
        ]
        for race in additional_races:
            races[race] = []

        while True:
            clear_console()
            CharacterCreator.print_races(races)
            race_input = input(f"\n{YELLOW}Enter your race: {RESET}").strip().title()
            if race_input in races:
                return CharacterCreator.select_subrace(race_input, races[race_input])
            else:
                Console.invalid_choice()

    @staticmethod
    def print_races(races):
        print(f"{BLUE}FableForge - Available Races:{RESET}\n")
        for race, subraces in races.items():
            print(f"{RED}{race}{RESET}")
            for subrace in subraces:
                print(f"  {BLUE}- {subrace}{RESET}")

    @staticmethod
    def select_subrace(race, subraces):
        if not subraces:
            return race, None
        while True:
            clear_console()
            print(f"{BLUE}Available Subraces for {race}:{RESET}\n")
            for subrace in subraces:
                print(f"  {RED}- {subrace}{RESET}")
            subrace_input = input(f"\n{YELLOW}Enter your subrace: {RESET}").strip().title()
            if subrace_input in subraces:
                return race, subrace_input
            else:
                Console.invalid_choice()

    @staticmethod
    def select_class():
        basic_classes = ["Fighter", "Wizard", "Rogue", "Cleric",
                         "Bard", "Warlock", "Druid", "Barbarian",
                         "Monk", "Ranger", "Paladin", "Sorcerer"]
        adv_classes = ["Artificer", "Hexblade", "Psion", "Warlord", "Swashbuckler"]

        while True:
            clear_console()
            CharacterCreator.print_classes(basic_classes, adv_classes)
            class_input = input(f"\n{YELLOW}Choose your class: {RESET}").strip().capitalize()
            if class_input in basic_classes + adv_classes:
                return class_input
            else:
                Console.invalid_choice()

    @staticmethod
    def print_classes(basic_classes, adv_classes):
        print(f"{BLUE}FableForge - Available Classes:{RESET}\n")
        print(f"{BLUE}{'Basic Classes:':<20} {'Advanced Classes:':<20}{RESET}\n")
        max_len = max(len(basic_classes), len(adv_classes))
        for i in range(max_len):
            basic = basic_classes[i] if i < len(basic_classes) else ""
            advanced = adv_classes[i] if i < len(adv_classes) else ""
            print(f"{RED}{basic:<20} {advanced:<20}{RESET}")

    @staticmethod
    def generate_stats():
        options = {"1": "manual", "2": "random"}
        while True:
            clear_console()
            print(f"{BLUE}FableForge - Stat generation method:{RESET}\n")
            print(f"{RED}1. Manually distribute points{RESET}")
            print(f"{RED}2. Generate random stats{RESET}")
            choice = input(f"\n{YELLOW}Enter your choice: {RESET}").strip()
            if choice in options:
                return CharacterCreator.manual_stats() if options[choice] == "manual" else CharacterCreator.random_stats()
            else:
                Console.invalid_choice()

    @staticmethod
    def manual_stats():
        stats = {
            key: 0
            for key in [
                "strength",
                "dexterity",
                "intelligence",
                "charisma",
                "wisdom",
                "constitution",
            ]
        }
        total_points = 75
        print(f"You have {total_points} points to distribute (8-18 per stat):")
        stat_names = list(stats.keys())
        for index, stat in enumerate(stat_names):
            remaining = len(stat_names) - index
            while True:
                try:
                    max_alloc = min(18, total_points - 8 * (remaining - 1))
                    allocation = int(
                        input(
                            f"Allocate to {stat.capitalize()} "
                            f"(remaining: {total_points}, max {max_alloc}): "
                        )
                    )
                    if 8 <= allocation <= max_alloc:
                        stats[stat] = allocation
                        total_points -= allocation
                        break
                    else:
                        print(
                            f"Invalid allocation. Enter a value between 8 and {max_alloc}."
                        )
                except ValueError:
                    print("Enter a valid number.")
        return stats

    @staticmethod
    def random_stats():
        return {key: random.randint(8, 18) for key in ["strength", "dexterity", "intelligence", "charisma", "wisdom", "constitution"]}

def main_menu():
    options = [
        {"label": "Create a new character", "action": create_character},
        {"label": "Play", "action": play_game},
        {"label": "Exit", "action": exiting},
    ]
    Console.menu_handler("FableForge - Main Menu", options)

# Display Character Creation Menu
def create_character():
    name = CharacterCreator.get_character_name()
    race, subrace = CharacterCreator.select_race()
    char_class = CharacterCreator.select_class()
    stats = CharacterCreator.generate_stats()

    clear_console()
    print(f"{BLUE}FableForge - Character Summary!{RESET}")
    print(f"{BLUE}Character Details:{RESET}\n")
    print(f"{RED}Name:{RESET} {name}")
    print(f"{RED}Race:{RESET} {race} {'(' + subrace + ')' if subrace else ''}")
    print(f"{RED}Class:{RESET} {char_class}")
    print(f"{BLUE}Stats:{RESET}")
    for stat, value in stats.items():
        print(f"  {RED}{stat.capitalize()}{RESET}: {value}")
    
    # Save character to database
    db_manager = DatabaseManager()
    with db_manager.connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO characters (name, race, class, strength, dexterity, intelligence, charisma, wisdom, constitution, health, experience)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                f"{race} ({subrace})" if subrace else race,
                char_class,
                stats["strength"],
                stats["dexterity"],
                stats["intelligence"],
                stats["charisma"],
                stats["wisdom"],
                stats["constitution"],
                100,  # Default health
                0,    # Default experience
            ),
        )
        conn.commit()
        print(f"\n{BLUE}Character saved to database!{RESET}")
        input(f"\n{YELLOW}Press Enter to continue...{RESET}")

def play_game():
    options = [
        {"label": "Character Menu", "action": character},
        {"label": "Quest Menu", "action": quest_menu},
        {"label": "Back to main menu", "action": main_menu},
    ]
    Console.menu_handler("FableForge - Play", options)

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
    print(f"{BLUE}FableForge - Choose Character!{RESET}")
    
    db_manager = DatabaseManager()
    with db_manager.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, race, class FROM characters")
        characters = cursor.fetchall()
        
        if not characters:
            print(f"\n{RED}No characters found in the database.{RESET}")
            input(f"{YELLOW}Press Enter to return to the main menu...{RESET}")
            return
        
        print(f"\n{BLUE}Available Characters:{RESET}\n")
        for char in characters:
            name, race, char_class = char
            print(f"{RED}Name:{RESET} {name} | {RED}Race:{RESET} {race} | {RED}Class:{RESET} {char_class}")
        
        print(f"\n{BLUE}Select a character by entering their name.{RESET}")
        selected_name = input(f"{YELLOW}Enter character name: {RESET}").strip()
        
        cursor.execute("SELECT * FROM characters WHERE name = ? COLLATE NOCASE", (selected_name,))
        character = cursor.fetchone()
        
    if character:
        clear_console()
        print(f"{BLUE}Character Details:{RESET}\n")
        print(f"{RED}Name:{RESET} {character[1]}")
        print(f"{RED}Race:{RESET} {character[2]}")
        print(f"{RED}Class:{RESET} {character[3]}")
        print(f"{BLUE}Stats:{RESET}")
        for stat, value in zip(
            ["Strength", "Dexterity", "Intelligence", "Charisma", "Wisdom", "Constitution"], character[4:10]
        ):
            print(f"  {RED}{stat}{RESET}: {value}")
        print(f"{RED}Health:{RESET} {character[10]}")
        print(f"{RED}Experience:{RESET} {character[11]}")
        inventory = db_manager.get_inventory(character[0])
        if inventory:
            print(f"\n{BLUE}Inventory:{RESET}")
            for item, qty in inventory:
                print(f"  {RED}{item}{RESET} x{qty}")
    else:
        print(f"{RED}Invalid Name. Returning to the main menu.{RESET}")
    input(f"\n{YELLOW}Press Enter to continue...{RESET}")

def delete_character():
    clear_console()
    print(f"{BLUE}FableForge - Delete Character!{RESET}")
    
    db_manager = DatabaseManager()
    with db_manager.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, race, class FROM characters")
        characters = cursor.fetchall()
        
        if not characters:
            print(f"\n{RED}No characters found in the database.{RESET}")
            input(f"{YELLOW}Press Enter to return to the main menu...{RESET}")
            return
        
        print(f"\n{BLUE}Available Characters:{RESET}\n")
        for char in characters:
            name, race, char_class = char
            print(f"{RED}Name:{RESET} {name} | {RED}Race:{RESET} {race} | {RED}Class:{RESET} {char_class}")
        
        print(f"\n{BLUE}Select a character to delete by entering their name.{RESET}")
        selected_name = input(f"{YELLOW}Enter character name: {RESET}").strip()
        
        cursor.execute("SELECT * FROM characters WHERE name = ? COLLATE NOCASE", (selected_name,))
        character = cursor.fetchone()
        
        if character:
            cursor.execute("DELETE FROM characters WHERE name = ? COLLATE NOCASE", (selected_name,))
            conn.commit()
            clear_console()
            print(f"{RED}Character {selected_name} has been deleted.{RESET}")
        else:
            print(f"{RED}Invalid Name. Returning to the main menu.{RESET}")
    input(f"\n{YELLOW}Press Enter to continue...{RESET}")

def main():
    """Entry point for the FableForge command line interface."""
    setup_logging()
    db_manager = DatabaseManager()
    db_manager.initialize_tables()
    main_menu()


if __name__ == "__main__":
    main()
