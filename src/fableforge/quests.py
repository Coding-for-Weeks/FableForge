from fableforge.utilities import clear_console
from fableforge.database_manager import DatabaseManager
from fableforge.quest_one import quest_one
from fableforge.quest_two import quest_two

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

def quest_menu():
    from fableforge.main import play_game
    options = [
        {"label": "List Quests", "action": list_quests},
        {"label": "Complete Quest", "action": complete_quest},
        {"label": "Back to Play Menu", "action": play_game},
    ]
    Play.play_game("FableForge - Quest Menu", options)

# Quests
def list_quests():
    options = [
        {"label": "Whispers of the Crystal Shard", "action": quest_one},
        {"label": "The Forgotten Ember", "action": quest_two},
        {"label": "Back to Previous Menu", "action": quest_menu}
    ]
    Play.play_game("FableForge - Quests", options)

def complete_quest():
    clear_console()
    print("Complete a Quest")
    input("Press Enter to continue...")
    

