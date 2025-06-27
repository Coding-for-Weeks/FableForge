from fableforge.utilities import clear_console
from fableforge.style import CYAN, YELLOW, BLUE, GREEN, RED, RESET

def quest_one(character):
    """Play the opening quest with short branching choices."""

    clear_console()
    name = character[1] if character else "Adventurer"

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
    elif choice == "2":
        print(f"{name} ignores the whispers and focuses on the bustling market around them.")
    elif choice == "3":
        print(f"{name} seeks out the city guards, hoping they know more about the hooded figure or the shard.")
    elif choice == "4":
        print(f"{name} searches their memory for stories and legends that match the whispers.")
    elif choice == "5":
        print(f"{name} stands frozen, trying to make sense of everything. The crowd moves around them like a river.")

    input(f"\n{YELLOW}Press Enter to continue...{RESET}")
