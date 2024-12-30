import sqlite3
import random
import logging
import os
import platform
import subprocess

# Utility Functions
def clear_console():
    commands = {
        "Windows": "cls",
        "Linux": "clear",
        "Darwin": "clear",  # macOS
    }
    command = commands.get(platform.system(), "clear")
    subprocess.run(command, shell=True)

def exiting():
    clear_console()
    os._exit(0)

def setup_logging():
    log_file = "game.log"
    logging.basicConfig(
        filename=log_file,
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    if not os.access(log_file, os.W_OK):
        print(f"Warning: Cannot write to log file {log_file}. Check file permissions.")

setup_logging()

class DatabaseManager:
    def __init__(self, db_name="dnd_game.db"):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

    def initialize_tables(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            tables = {
                "characters": """
                    CREATE TABLE IF NOT EXISTS characters (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        race TEXT NOT NULL,
                        class TEXT NOT NULL,
                        strength INTEGER,
                        dexterity INTEGER,
                        intelligence INTEGER,
                        charisma INTEGER,
                        wisdom INTEGER,
                        constitution INTEGER,
                        health INTEGER,
                        experience INTEGER
                    )
                """,
                "quests": """
                    CREATE TABLE IF NOT EXISTS quests (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT,
                        completed BOOLEAN NOT NULL,
                        character_id INTEGER,
                        FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE
                    )
                """,
                "inventory": """
                    CREATE TABLE IF NOT EXISTS inventory (
                        id INTEGER PRIMARY KEY,
                        item_name TEXT NOT NULL,
                        quantity INTEGER,
                        character_id INTEGER,
                        FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE
                    )
                """,
            }
            for table, create_sql in tables.items():
                cursor.execute(create_sql)


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
        print("\033[94mWelcome to Character Creation!\033[0m")
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
        print("\033[94mAvailable Races:\033[0m\n")
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
            print("\033[94mChoose stat generation method:\033[0m\n")
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
    Console.menu_handler("Main Menu", options)

# Display Character Creation Menu
def create_character():
    name = CharacterCreator.get_character_name()
    race, subrace = CharacterCreator.select_race()
    char_class = CharacterCreator.select_class()
    stats = CharacterCreator.generate_stats()

    clear_console()
    print("\033[94mCharacter creation complete! Here are your details:\033[0m\n")
    print(f"\033[91mName:\033[0m {name}")
    print(f"\033[91mRace:\033[0m {race} {'(' + subrace + ')' if subrace else ''}")
    print(f"\033[91mClass:\033[0m {char_class}")
    print("\033[94mStats:\033[0m")
    for stat, value in stats.items():
        print(f"  \033[91m{stat.capitalize()}\033[0m: {value}")
    input("\n\033[93mPress Enter to continue...\033[0m")
    
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

def play_game():
    clear_console()
    print("Starting game...")
    input("\n\033[93mPress Enter to continue...\033[0m")

if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.initialize_tables()
    main_menu()
