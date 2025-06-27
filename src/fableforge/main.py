#!/usr/bin/env python3

import sqlite3
import random
from src.fableforge.utilities import clear_console, exiting, setup_logging
from database_manager import DatabaseManager
from src.fableforge.quests import quest_menu

class Console:
    @staticmethod
    def menu_handler(title, options):
        while True:
            clear_console()
            Console.print_menu(title, options)
            choice = input("\n\033[93mChoose an option: \033[0m").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                action = options[int(choice) - 1]["action"]
                if action is None:
                    return
                action()
            else:
                Console.invalid_choice()

    @staticmethod
    def print_menu(title, options):
        print(f"\033[1m\033[94m{title}\033[0m\n")
        for i, option in enumerate(options, start=1):
            print(f"\033[1m\033[91m{i}. {option['label']}\033[0m")

    @staticmethod
    def invalid_choice():
        print("\033[91mInvalid choice. Please try again.\033[0m")
        input("\033[1mPress Enter to continue...\033[0m")

class CharacterCreator:
    @staticmethod
    def get_character_name():
        clear_console()
        print("\033[94mFableForge - Character Creation!\033[0m")
        return input("\n\033[93mEnter your character's name: \033[0m").strip()

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
            race_input = input(f"\n\033[93mEnter your race: \033[0m").strip().title()
            if race_input in races:
                return CharacterCreator.select_subrace(race_input, races[race_input])
            else:
                Console.invalid_choice()

    @staticmethod
    def print_races(races):
        print("\033[94mFableForge - Available Races:\033[0m\n")
        for race, subraces in races.items():
            print(f"\033[91m{race}\033[0m")
            for subrace in subraces:
                print(f"  \033[94m- {subrace}\033[0m")

    @staticmethod
    def select_subrace(race, subraces):
        if not subraces:
            return race, None
        while True:
            clear_console()
            print(f"\033[94mAvailable Subraces for {race}:\033[0m\n")
            for subrace in subraces:
                print(f"  \033[91m- {subrace}\033[0m")
            subrace_input = input(f"\n\033[93mEnter your subrace: \033[0m").strip().title()
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
            class_input = input(f"\n\033[93mChoose your class: \033[0m").strip().capitalize()
            if class_input in basic_classes + adv_classes:
                return class_input
            else:
                Console.invalid_choice()

    @staticmethod
    def print_classes(basic_classes, adv_classes):
        print("\033[94mFableForge - Available Classes:\033[0m\n")
        print(f"\033[94m{'Basic Classes:':<20} {'Advanced Classes:':<20}\033[0m\n")
        max_len = max(len(basic_classes), len(adv_classes))
        for i in range(max_len):
            basic = basic_classes[i] if i < len(basic_classes) else ""
            advanced = adv_classes[i] if i < len(adv_classes) else ""
            print(f"\033[91m{basic:<20} {advanced:<20}\033[0m")

    @staticmethod
    def generate_stats():
        options = {"1": "manual", "2": "random"}
        while True:
            clear_console()
            print("\033[94mFableForge - Stat generation method:\033[0m\n")
            print("\033[91m1. Manually distribute points\033[0m")
            print("\033[91m2. Generate random stats\033[0m")
            choice = input("\n\033[93mEnter your choice: \033[0m").strip()
            if choice in options:
                return CharacterCreator.manual_stats() if options[choice] == "manual" else CharacterCreator.random_stats()
            else:
                Console.invalid_choice()

    @staticmethod
    def manual_stats():
        stats = {key: 0 for key in ["strength", "dexterity", "intelligence", "charisma", "wisdom", "constitution"]}
        total_points = 75
        print(f"You have {total_points} points to distribute (8-18 per stat):")
        for stat in stats:
            while True:
                try:
                    allocation = int(input(f"Allocate to {stat.capitalize()} (remaining: {total_points}): "))
                    if 8 <= allocation <= 18 and allocation <= total_points:
                        stats[stat] = allocation
                        total_points -= allocation
                        break
                    else:
                        print("Invalid allocation. Try again.")
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
    print("\033[94mFableForge - Character Summary!\033[0m")
    print("\033[94mCharacter Details:\033[0m\n")
    print(f"\033[91mName:\033[0m {name}")
    print(f"\033[91mRace:\033[0m {race} {'(' + subrace + ')' if subrace else ''}")
    print(f"\033[91mClass:\033[0m {char_class}")
    print("\033[94mStats:\033[0m")
    for stat, value in stats.items():
        print(f"  \033[91m{stat.capitalize()}\033[0m: {value}")
    
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
        print("\n\033[94mCharacter saved to database!\033[0m")
        input("\n\033[93mPress Enter to continue...\033[0m")

class Play:
    @staticmethod
    def play_game(title, options):
        while True:
            clear_console()
            Play.print_menu(title, options)
            choice = input("\n\033[93mChoose an option: \033[0m").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                action = options[int(choice) - 1]["action"]
                if action is None:
                    return
                action()
            else:
                Play.invalid_choice()

    @staticmethod
    def print_menu(title, options):
        print(f"\033[1m\033[94m{title}\033[0m\n")
        for i, option in enumerate(options, start=1):
            print(f"\033[1m\033[91m{i}. {option['label']}\033[0m")

    @staticmethod
    def invalid_choice():
        print("\033[91mInvalid choice. Please try again.\033[0m")
        input("\033[1mPress Enter to continue...\033[0m")

def play_game():
    options = [
        {"label": "Character Menu", "action": character},
        {"label": "Quest Menu", "action": quest_menu},
        {"label": "Back to main menu", "action": main_menu},
    ]
    Play.play_game("FableForge - Play", options)

def character():
    clear_console()
    options = [
        {"label": "Choose Character", "action": character_choice},
        {"label": "Delete Character", "action": delete_character},
        {"label": "Back to Play Menu", "action": play_game},
    ]
    Play.play_game("FableForge - Character Menu", options)


def character_choice():
    clear_console()
    print("\033[94mFableForge - Choose Character!\033[0m")
    
    db_manager = DatabaseManager()
    with db_manager.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, race, class FROM characters")
        characters = cursor.fetchall()
        
        if not characters:
            print("\n\033[91mNo characters found in the database.\033[0m")
            input("\033[93mPress Enter to return to the main menu...\033[0m")
            return
        
        print("\n\033[94mAvailable Characters:\033[0m\n")
        for char in characters:
            name, race, char_class = char
            print(f"\033[91mName:\033[0m {name} | \033[91mRace:\033[0m {race} | \033[91mClass:\033[0m {char_class}")
        
        print("\n\033[94mSelect a character by entering their name.\033[0m")
        selected_name = input("\033[93mEnter character name: \033[0m").strip()
        
        cursor.execute("SELECT * FROM characters WHERE name = ? COLLATE NOCASE", (selected_name,))
        character = cursor.fetchone()
        
    if character:
        clear_console()
        print("\033[94mCharacter Details:\033[0m\n")
        print(f"\033[91mName:\033[0m {character[1]}")
        print(f"\033[91mRace:\033[0m {character[2]}")
        print(f"\033[91mClass:\033[0m {character[3]}")
        print(f"\033[94mStats:\033[0m")
        for stat, value in zip(
            ["Strength", "Dexterity", "Intelligence", "Charisma", "Wisdom", "Constitution"], character[4:10]
        ):
            print(f"  \033[91m{stat}\033[0m: {value}")
        print(f"\033[91mHealth:\033[0m {character[10]}")
        print(f"\033[91mExperience:\033[0m {character[11]}")
    else:
        print("\033[91mInvalid Name. Returning to the main menu.\033[0m")
    input("\n\033[93mPress Enter to continue...\033[0m")

def delete_character():
    clear_console()
    print("\033[94mFableForge - Delete Character!\033[0m")
    
    db_manager = DatabaseManager()
    with db_manager.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, race, class FROM characters")
        characters = cursor.fetchall()
        
        if not characters:
            print("\n\033[91mNo characters found in the database.\033[0m")
            input("\033[93mPress Enter to return to the main menu...\033[0m")
            return
        
        print("\n\033[94mAvailable Characters:\033[0m\n")
        for char in characters:
            name, race, char_class = char
            print(f"\033[91mName:\033[0m {name} | \033[91mRace:\033[0m {race} | \033[91mClass:\033[0m {char_class}")
        
        print("\n\033[94mSelect a character to delete by entering their name.\033[0m")
        selected_name = input("\033[93mEnter character name: \033[0m").strip()
        
        cursor.execute("SELECT * FROM characters WHERE name = ? COLLATE NOCASE", (selected_name,))
        character = cursor.fetchone()
        
        if character:
            cursor.execute("DELETE FROM characters WHERE name = ? COLLATE NOCASE", (selected_name,))
            conn.commit()
            clear_console()
            print(f"\033[91mCharacter {selected_name} has been deleted.\033[0m")
        else:
            print("\033[91mInvalid Name. Returning to the main menu.\033[0m")
    input("\n\033[93mPress Enter to continue...\033[0m")

if __name__ == "__main__":
    setup_logging()
    db_manager = DatabaseManager()
    db_manager.initialize_tables()
    main_menu()
