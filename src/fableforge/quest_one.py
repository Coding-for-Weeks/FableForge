from fableforge.utilities import clear_console
from fableforge.style import CYAN, YELLOW, BLUE, GREEN, RED, RESET
from fableforge.database_manager import DatabaseManager



def quest_one(character, character_id, db, progress=None):

    clear_console()
    name = character[1] if character else "Adventurer"

    if progress:

        print(f"{BLUE}FableForge - Whispers of the Crystal Shard - Resuming Quest{RESET}\n")
        print(f"{CYAN}Resuming saved quest progress...{RESET}")
        if progress == "followed_hooded_figure":
            resume_followed_figure(character, character_id, db, progress)
        elif progress == "ignored_whispers":
            resume_ignored_whispers(character, character_id, db, progress)
        elif progress == "sought_guards":
            resume_sought_guards(character, character_id, db, progress)
        elif progress == "recalled_lore":
            resume_recalled_lore(character, character_id, db, progress)
        elif progress == "remained_still":
            resume_remained_still(character, character_id, db, progress)
        else:
            print(f"{RED}Unknown quest state. Starting fresh.{RESET}")
            quest_one(character, character_id, db, None)
        return
    
    """Play the opening quest with short branching choices."""

    intro_text = f"""
{BLUE}FableForge - Whispers of the Crystal Shard{RESET}

A chilling wind sweeps through the bustling market of Lyrinhold, carrying an
eerie melody that only a few can hear. Among them is {name}. The haunting tune
is laced with whispers in a forgotten tongue, yet you sense the message is
meant for you.

As the whispers grow louder, a hooded figure draws near.
"You've heard it, haven't you? The shard calls to you. But beware... those who
seek it will stop at nothing." With that warning, the figure melts into the
crowd, leaving you at a crossroads.
"""

    print(intro_text.strip())

    print(f"\n{GREEN}1.{RESET} Follow the hooded figure")
    print(f"{GREEN}2.{RESET} Stay in the market")
    print(f"{GREEN}3.{RESET} Search for guards")
    print(f"{GREEN}4.{RESET} Try to recall any lore about the shard")
    print(f"{GREEN}5.{RESET} Do nothing, remain still")

    valid_choices = {"1", "2", "3", "4", "5"}
    choice = ""

    while choice not in valid_choices:
        choice = input(f"\n{YELLOW}Choose your path: {RESET}").strip()

    print()

    if choice == "1":
        print(f"{name} pushes through the crowd, trying to catch another glimpse of the mysterious stranger.")
        resume_followed_figure(character, character_id, db, None)
        db.save_quest_progress(character_id, "Whispers of the Crystal Shard", "followed_hooded_figure")
    
    elif choice == "2":
        print(f"{name} ignores the whispers and focuses on the bustling market around them.")
        resume_ignored_whispers(character, character_id, db, None)
        db.save_quest_progress(character_id, "Whispers of the Crystal Shard", "ignored_whispers")    
    
    elif choice == "3":
        print(f"{name} seeks out the city guards, hoping they know more about the hooded figure or the shard.")
        resume_sought_guards(character, character_id, db, None)
        db.save_quest_progress(character_id, "Whispers of the Crystal Shard", "sought_guards")
    
    elif choice == "4":
        print(f"{name} searches their memory for stories and legends that match the whispers.")
        resume_recalled_lore(character, character_id, db, None)
        db.save_quest_progress(character_id, "Whispers of the Crystal Shard", "recalled_lore")
    
    elif choice == "5":
        print(f"{name} stands frozen, trying to make sense of everything. The crowd moves around them like a river.")
        resume_remained_still(character, character_id, db, None)
        db.save_quest_progress(character_id, "Whispers of the Crystal Shard", "remained_still")

# Resume functions for each choice
# These functions will be called when resuming the quest from a saved state.

def resume_followed_figure(character, character_id, db, progress):
    name = character[1] if character else "Adventurer"

    clear_console()
    print(f"{name} follows the hooded figure through the crowded market, weaving between stalls and people.")
    print(f"{CYAN}Press Enter to continue...{RESET}")
    input()
    clear_console()

def resume_ignored_whispers(character, character_id, db, progress):
    name = character[1] if character else "Adventurer"

    clear_console()
    print(f"{name} decides to ignore the whispers and focus on the market, but the eerie melody lingers in their mind.")
    print(f"{CYAN}Press Enter to continue...{RESET}")
    input()
    clear_console()

def resume_sought_guards(character, character_id, db, progress):
    name = character[1] if character else "Adventurer"

    clear_console()
    print(f"{name} approaches a group of city guards, hoping they can shed light on the hooded figure and the shard.")
    print(f"{CYAN}Press Enter to continue...{RESET}")
    input()
    clear_console()

def resume_recalled_lore(character, character_id, db, progress):
    name = character[1] if character else "Adventurer"

    clear_console()
    print(f"This action requires a INT check, would you like to roll a d20? (yes/no)")
    choice = input(f"{YELLOW}Your choice: {RESET}").strip().lower()
    if choice == "yes":
        import random
        roll = random.randint(1, 20)
        if roll >= 10:
            print(f"{name} recalls a legend about the Crystal Shard, realizing its immense power and the dangers it poses.")
        else:
            print(f"{name} struggles to remember the lore, feeling a sense of unease as the whispers grow louder.")
    elif choice == "no":
        print(f"{name} decides not to roll, feeling uncertain about the lore.")
    else:
        print(f"{name} hesitates, unsure of what to do next as the whispers continue to echo in their mind.")
    
    print(f"{CYAN}Press Enter to continue...{RESET}")
    input()
    clear_console()

def resume_remained_still(character, character_id, db, progress):
    name = character[1] if character else "Adventurer"

    clear_console()
    print(f"{name} stands still, trying to make sense of the situation, but the crowd continues to move around them.")
    print(f"{CYAN}Press Enter to continue...{RESET}")
    input()
    clear_console()

