from rich.console import Console
import random

from fableforge.utils.utilities import clear_console
from fableforge.engine.dialogue import NPC, run_dialogue

console = Console()


def quest_one(character, character_id, db, progress=None):
    """Play the opening quest with short branching choices."""
    clear_console()
    name = character[1] if character else "Adventurer"

    if progress:
        console.print("[blue]FableForge - Whispers of the Crystal Shard - Resuming Quest[/blue]\n")
        console.print("[cyan]Resuming saved quest progress...[/cyan]")
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
            console.print("[red]Unknown quest state. Starting fresh.[/red]")
            quest_one(character, character_id, db, None)
        return

    intro_text = f"""
[blue]FableForge - Whispers of the Crystal Shard[/blue]

A chilling wind sweeps through the bustling market of Lyrinhold, carrying an eerie melody that only a few can hear. Among them is {name}. The haunting tune is laced with whispers in a forgotten tongue, yet you sense the message is meant for you.

As the whispers grow louder, a hooded figure draws near. "You've heard it, haven't you? The shard calls to you. But beware... those who seek it will stop at nothing." With that warning, the figure melts into the crowd, leaving you at a crossroads.
"""
    console.print(intro_text.strip())
    console.print("\n[green]1.[/green] Follow the hooded figure")
    console.print("[green]2.[/green] Stay in the market")
    console.print("[green]3.[/green] Search for guards")
    console.print("[green]4.[/green] Try to recall any lore about the shard")
    console.print("[green]5.[/green] Do nothing, remain still")

    valid_choices = {"1", "2", "3", "4", "5"}
    choice = ""
    while choice not in valid_choices:
        choice = console.input("\n[bold yellow]Choose your path: [/bold yellow]").strip()

    if choice == "1":
        console.print(f"{name} pushes through the crowd, trying to catch another glimpse of the mysterious stranger.")
        resume_followed_figure(character, character_id, db, None)
        db.save_quest_progress(character_id, "Whispers of the Crystal Shard", "followed_hooded_figure")
    elif choice == "2":
        console.print(f"{name} ignores the whispers and focuses on the bustling market around them.")
        resume_ignored_whispers(character, character_id, db, None)
        db.save_quest_progress(character_id, "Whispers of the Crystal Shard", "ignored_whispers")
    elif choice == "3":
        console.print(f"{name} seeks out the city guards, hoping they know more about the hooded figure or the shard.")
        resume_sought_guards(character, character_id, db, None)
        db.save_quest_progress(character_id, "Whispers of the Crystal Shard", "sought_guards")
    elif choice == "4":
        console.print(f"{name} searches their memory for stories and legends that match the whispers.")
        resume_recalled_lore(character, character_id, db, None)
        db.save_quest_progress(character_id, "Whispers of the Crystal Shard", "recalled_lore")
    elif choice == "5":
        console.print(f"{name} stands frozen, trying to make sense of everything. The crowd moves around them like a river.")
        resume_remained_still(character, character_id, db, None)
        db.save_quest_progress(character_id, "Whispers of the Crystal Shard", "remained_still")


def resume_followed_figure(character, character_id, db, progress):
    name = character[1] if character else "Adventurer"
    clear_console()
    console.print(f"{name} follows the hooded figure through the crowded market, weaving between stalls and people.")
    npc = NPC(
        name="Hooded Figure",
        tree={
            "start": {
                "text": "You were wise to follow. Do you seek the shard?",
                "options": {"Who are you?": "who", "Where is it?": "where"},
            },
            "who": {"text": "Merely a messenger of its power.", "options": {"Continue": None}},
            "where": {"text": "Beyond the eastern ruins. Be cautious.", "options": {"Thanks": None}},
        },
    )
    run_dialogue(npc)
    console.input("[cyan]Press Enter to continue...[/cyan]")
    clear_console()


def resume_ignored_whispers(character, character_id, db, progress):
    name = character[1] if character else "Adventurer"
    clear_console()
    console.print(f"{name} decides to ignore the whispers and focus on the market, but the eerie melody lingers in their mind.")
    console.input("[cyan]Press Enter to continue...[/cyan]")
    clear_console()


def resume_sought_guards(character, character_id, db, progress):
    name = character[1] if character else "Adventurer"
    clear_console()
    console.print(f"{name} approaches a group of city guards, hoping they can shed light on the hooded figure and the shard.")
    console.input("[cyan]Press Enter to continue...[/cyan]")
    clear_console()


def resume_recalled_lore(character, character_id, db, progress):
    name = character[1] if character else "Adventurer"
    clear_console()
    console.print("This action requires an INT check, would you like to roll a d20? (yes/no)")
    choice = console.input("[yellow]Your choice: [/yellow]").strip().lower()
    if choice == "yes":
        roll = random.randint(1, 20)
        if roll >= 10:
            console.print(f"{name} recalls a legend about the Crystal Shard, realizing its immense power and the dangers it poses.")
        else:
            console.print(f"{name} struggles to remember the lore, feeling a sense of unease as the whispers grow louder.")
    elif choice == "no":
        console.print(f"{name} decides not to roll, feeling uncertain about the lore.")
    else:
        console.print(f"{name} hesitates, unsure of what to do next as the whispers continue to echo in their mind.")
    console.input("[cyan]Press Enter to continue...[/cyan]")
    clear_console()


def resume_remained_still(character, character_id, db, progress):
    name = character[1] if character else "Adventurer"
    clear_console()
    console.print(f"{name} stands still, trying to make sense of the situation, but the crowd continues to move around them.")
    console.input("[cyan]Press Enter to continue...[/cyan]")
    clear_console()
