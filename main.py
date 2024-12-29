import sqlite3
import random
import logging
import os
import platform
import subprocess

def clear_console():
    def run_command(command):
        subprocess.run(command, shell=True)

    commands = {
        "Windows": "cls",
        "Linux": "clear",
        "Darwin": "clear",  # macOS
    }
    platform_name = platform.system()
    command = commands.get(platform_name, "clear")
    run_command(command)

def setup_logging():
    log_file = "game.log"
    if not os.access(log_file, os.W_OK):
        print(f"Warning: Cannot write to log file {log_file}. Check file permissions.")
    logging.basicConfig(
        filename=log_file,
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

setup_logging()

class DatabaseManager:
    def __init__(self, db_name="dnd_game.db"):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

    def initialize_tables(self):
        with self.connect() as conn:
            cursor = conn.cursor()

            # Create the 'characters' table
            cursor.execute(
                """
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
                """
            )

            # Create the 'quests' table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS quests (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    completed BOOLEAN NOT NULL,
                    character_id INTEGER,
                    FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE
                )
                """
            )

            # Create the 'inventory' table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY,
                    item_name TEXT NOT NULL,
                    quantity INTEGER,
                    character_id INTEGER,
                    FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE
                )
                """
            )

class Console:
    @staticmethod
    def menu_handler(title, options):
        while True:
            clear_console()
            print(title)
            for i, option in enumerate(options, start=1):
                print(f"{i}. {option['label']}")
            choice = input("Choose an option: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                action = options[int(choice) - 1]["action"]
                if action is None:
                    return  # Exit the menu loop
                action()
            else:
                print("Invalid choice. Please try again.")

def get_character_name():
    clear_console()
    print("Welcome to Character Creation!")
    print("--------------------------------")
    name = input("\nEnter your character's name: ").strip()
    return name

def select_race():
    races = {
        "Gnome": ["Rock Gnome", "Forest Gnome", "Deep Gnome"],
        "Dwarf": ["Hill Dwarf", "Mountain Dwarf", "Duergar"],
        "Elf": ["High Elf", "Wood Elf", "Dark Elf"],
    }
    additional_races = [
        "Half-Orc",
        "Goliath",
        "Human",
        "Dragonborn",
        "Kobold",
        "Tiefling",
    ]
    for race in additional_races:
        races[race] = []
    clear_console()
    print("\nAvailable Races:\n")
    for race, subraces in races.items():
        if subraces:
            print(f"{race}: {', '.join(subraces)}")
        else:
            print(race)

    race = None
    subrace = None
    while not race:
        race_input = input(f"\nChoose your race: ").strip()
        if race_input in races:
            race = race_input
            subraces = races[race]
            if subraces:
                while not subrace:
                    clear_console()
                    print(f"Available subraces for {race}:")
                    for sub in subraces:
                        print(sub)
                    subrace_input = input(f"\nChoose your subrace: ").strip()
                    if subrace_input in subraces:
                        subrace = subrace_input
                    else:
                        print("Invalid subrace. Please choose a valid option.")
        else:
            print("Invalid race. Please choose a valid option.")

    return race, subrace

def select_class():
    classes = [
        "Fighter",
        "Wizard",
        "Rogue",
        "Cleric",
        "Bard",
        "Warlock",
        "Druid",
        "Barbarian",
        "Paladin",
        "Sorcerer",
    ]
    character_class = None
    while not character_class:
        clear_console()
        print("\nAvailable Classes:\n")
        for char_class in classes:
            print(char_class)

        class_input = input(f"\nChoose your class: ").strip()
        if class_input in classes:
            character_class = class_input
        else:
            print("Invalid class. Please choose a valid option.")

    return character_class

def generate_stats():
    def manual_stats():
        stats = {
            "strength": 0,
            "dexterity": 0,
            "intelligence": 0,
            "charisma": 0,
            "wisdom": 0,
            "constitution": 0,
        }
        total_points = 75
        print(
            f"You have {total_points} points to distribute among the following stats:"
        )
        for stat in stats:
            allocated = False
            while not allocated:
                try:
                    allocation = int(
                        input(
                            f"Allocate points to {stat.capitalize()} (remaining points: {total_points}): "
                        )
                    )
                    if 0 <= allocation <= total_points:
                        stats[stat] = allocation
                        total_points -= allocation
                        allocated = True
                    else:
                        print(
                            "Invalid allocation. Please enter a value within the remaining points."
                        )
                except ValueError:
                    print("Please enter a valid integer.")
        return stats

    predefined_stats = [
        {
            "strength": 15,
            "dexterity": 14,
            "intelligence": 13,
            "charisma": 12,
            "wisdom": 10,
            "constitution": 8,
        },
        {
            "strength": 10,
            "dexterity": 10,
            "intelligence": 15,
            "charisma": 12,
            "wisdom": 14,
            "constitution": 10,
        },
    ]

    def random_stats():
        return {
            "strength": random.randint(8, 18),
            "dexterity": random.randint(8, 18),
            "intelligence": random.randint(8, 18),
            "charisma": random.randint(8, 18),
            "wisdom": random.randint(8, 18),
            "constitution": random.randint(8, 18),
        }

    stats = None
    while not stats:
        clear_console()
        print("\nChoose stat generation method:\n")
        print("1. Manually distribute points")
        print("2. Choose predefined stats")
        print("3. Generate random stats")
        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            stats = manual_stats()
        elif choice == "2":
            clear_console()
            print("Predefined stat options:")
            for i, option in enumerate(predefined_stats, start=1):
                print(f"{i}: {option}")
            selected = input("Select an option (1 or 2): ").strip()
            if selected in ["1", "2"]:
                stats = predefined_stats[int(selected) - 1]
        elif choice == "3":
            stats = random_stats()
        else:
            print("Invalid choice. Please try again.")

    return stats

def create_character():
    try:
        name = get_character_name()
        race, subrace = select_race()
        character_class = select_class()
        stats = generate_stats()

        health = 100
        experience = 0

        print("Generated stats:")
        for stat, value in stats.items():
            print(f"{stat.capitalize()}: {value}")

        db_manager = DatabaseManager()
        with db_manager.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO characters (name, race, class, strength, dexterity, intelligence, charisma, wisdom, constitution, health, experience)
                VALUES (:name, :race, :class, :strength, :dexterity, :intelligence, :charisma, :wisdom, :constitution, :health, :experience)
                """,
                {
                    "name": name,
                    "race": f"{race} ({subrace})" if subrace else race,
                    "class": character_class,
                    "strength": stats["strength"],
                    "dexterity": stats["dexterity"],
                    "intelligence": stats["intelligence"],
                    "charisma": stats["charisma"],
                    "wisdom": stats["wisdom"],
                    "constitution": stats["constitution"],
                    "health": health,
                    "experience": experience,
                },
            )

        clear_console()
        print("Character Created Successfully!")
        print("--------------------------------")
        print(f"Name: {name}")
        print(f"Race: {race}")
        if subrace:
            print(f"Subrace: {subrace}")
        print(f"Class: {character_class}")
        print("Stats:")
        for stat, value in stats.items():
            print(f"  {stat.capitalize()}: {value}")
        print("--------------------------------")
        input("Press Enter to return to the menu...")
    except sqlite3.IntegrityError as e:
        logging.error(f"Integrity error in create_character: {e}")
        print(
            "A database integrity error occurred. Please ensure all fields are correctly filled."
        )
    except sqlite3.OperationalError as e:
        logging.error(f"Operational error in create_character: {e}")
        print(
            "A database operational error occurred. Please check the database connection or schema."
        )
    except Exception as e:
        logging.error(f"Unexpected error in create_character: {e}")
        print(
            "An unexpected error occurred while creating the character. Please try again."
        )

def main_menu():
    options = [
        {"label": "Create a new character", "action": create_character},
        {"label": "Play", "action": play_game},
        {"label": "Exit", "action": lambda: os._exit(0)},
    ]
    while True:
        Console.menu_handler("Main Menu", options)

def play_game():
    options = [
        {"label": "View Character", "action": lambda: print("Displaying character information...")},
        {"label": "Go on a Quest", "action": lambda: print("Starting a quest...")},
        {"label": "View Inventory", "action": lambda: print("Viewing inventory...")},
        {"label": "Exit to Main Menu", "action": None},
    ]
    while True:
        Console.menu_handler("Game Menu", options)

if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.initialize_tables()
    main_menu()