# 🧠 agent.md — FableForge Game Agent

This document helps ChatGPT Codex and future developers navigate and extend the FableForge game.

📌 Overview

FableForge is a single-player, fantasy role-playing game where players create characters, engage in interactive quests, and save progress in a SQLite database.

🎯 Agent Responsibilities

Component | Purpose | Key Classes/Functions
----------|---------|-----------------------
Menus     | Navigation & input | `Console.menu_handler`, `Play.play_game` (in `main.py`, `quests.py`)
Characters| Creation & stats   | `CharacterCreator` (in `main.py`)
Quests    | Interactive stories| `quest_menu()`, `quest_one()`, `quest_two()`
Database  | Data persistence   | `DatabaseManager` (in `database_manager.py`)
Utility   | Console + logging  | `clear_console()`, `setup_logging()` (in `utilities.py`)

📂 File Structure

FableForge/
├── data/                # SQLite database file
├── logs/                # Logging output
├── src/
│   └── fableforge/
│       ├── main.py
│       ├── quests.py
│       ├── quest_one.py
│       ├── quest_two.py
│       ├── database_manager.py
│       └── utilities.py

🗺️ Runtime Flow

1. Start game → `python -m fableforge.main`
2. `main_menu()` appears
3. User picks:
   - 🎭 Create Character → save to DB
   - 🎮 Play → Character menu or Quest menu
   - ❌ Exit
4. Quests execute `quest_one()` or `quest_two()` stories

🗃️ SQLite Schema Summary

Table | Description
------|-------------
`characters` | Stores name, race, class, stats, health, XP
`quests`     | Quest completion & descriptions
`inventory`  | Items held by each character

Tables are created by `DatabaseManager.initialize_tables()` at launch.

➕ Extension Guide

- **Add a quest**: Create `quest_<name>.py` → define `quest_<name>()` → add it to `quests.py`.
- **New classes/races**: Update lists in `CharacterCreator`.
- **Stats or mechanics**: Expand DB schema and display logic.

✅ Updated: 27 Jun 2025
