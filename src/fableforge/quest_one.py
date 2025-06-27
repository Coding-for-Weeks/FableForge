from fableforge.utilities import clear_console


def quest_one(character):
    """Play the opening quest with short branching choices."""

    clear_console()
    name = character[1] if character else "Adventurer"

    intro_text = f"""
\033[94mFableForge - Whispers of the Crystal Shard\033[0m

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
    print("\033[94m1.\033[0m Follow the hooded figure")
    print("\033[94m2.\033[0m Stay in the market")
    choice = input("\n\033[93mChoose your path: \033[0m").strip()
    
    if choice == "1":
        print(
            f"\n{name} pushes through the crowd, trying to catch another glimpse "
            "of the mysterious stranger."
    
        )
    elif choice == "2":
        print(
            f"\n{name} ignores the whispers and focuses on the bustling market "
            "around them."
        )
    else:
        print("\033[91mIndecision grips you, and the opportunity slips away.\033[0m")
    
    input("\033[93mPress Enter to continue...\033[0m")