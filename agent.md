🧠 agent.md — FableForge Game Agent

This document tells ChatGPT Codex (and any future contributors) what the FableForge agent does, where to find core logic, and how to extend the project safely. Keep this file updated whenever you refactor or add major features—Codex will use it as a quick map of the codebase.

📌 Purpose

A single‑player, text‑driven fantasy adventure that lets users create D&D‑style characters, embark on quests, and persist progress in a SQLite database—all from the command line.

🎯 Agent Responsibilities

Area

What the agent handles

Main Classes / Functions

Menu navigation

Print menus, capture & validate input, route to the correct action

Console.menu_handler (main.py)  /  Play.play_game (main.py & quests.py)

Character creation

Prompt for name, race, class, and stats (manual or random)

CharacterCreator (main.py)

Quest flow

List quests, launch story scripts, mark completion (future)

quest_menu (quests.py)  /  quest_one, quest_two

Persistence

SQLite connection & table setup

DatabaseManager (database_manager.py)

Utilities

Clear console, exit cleanly, configure logging

utilities.py

🗂️ Project Structure at a Glance

.
├── main.py              # Entry point & top‑level menus
├── quests.py            # Quest menu wrapper
├── quest_one.py         # "Whispers of the Crystal Shard"
├── quest_two.py         # "Shadows of the Lost Keep"
├── database_manager.py  # SQLite helper
├── utilities.py         # OS / logging helpers
├── data/                # dnd_game.db lives here
└── logs/                # game.log lives here (auto‑created)

🔄 Typical Interaction Flow

Startup → python main.py calls main_menu()

Player chooses:

Create Character → CharacterCreator → DB insert

Play → play_game() ➜ (a) Character Menu or (b) Quest Menu

Exit

When a quest is selected, its narrative function (quest_one() etc.) runs; future versions will update the quests table.

🗃️ Database Schema (simplified)

Table

Core Columns

characters

id, name, race, class, strength, dexterity, intelligence, charisma, wisdom, constitution, health, experience

quests

id, name, description, completed, character_id (FK)

inventory

id, item_name, quantity, character_id (FK)

All tables are created automatically inside DatabaseManager.initialize_tables() if they don’t exist.

➕ Extension Points

Add a new quest

Create quest_<slug>.py with a function quest_<slug>() that prints the narrative.

Import & register it in quests.list_quests().

Add new character races / classes: Edit CharacterCreator.select_race() / .select_class() arrays.

Add new stats or mechanics: Update DB schema and display logic in CharacterCreator.generate_stats() and character summary.

💡 Tips for ChatGPT Codex

Look here first when suggesting new functions or refactoring.

Mirror exact function names and menu labels defined above to stay consistent.

When creating code examples, import from the modules listed under Project Structure.

✅ Agent Behavior Checklist (kept in sync with code)



Last Updated: 27 Jun 2025

