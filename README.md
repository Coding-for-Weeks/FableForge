# 🔱 FableForge

Welcome to **FableForge**, a Python-based, text-driven adventure inspired by Dungeons & Dragons! Create characters, complete quests, and explore a world full of possibilities. 🧙‍♂️✨

---

## 🌟 Features

- **🎭 Character Creation**:
  - Choose from various races, subraces, and classes.
  - Manually distribute or randomly generate character stats.
- **📦 Database Integration**:
  - Stores characters, quests, and inventory in a SQLite database (`data/dnd_game.db`).
  - Automatically initializes database tables on startup.
- **💻 Dynamic Console Interaction**:
  - User-friendly menu navigation with options for creating characters, playing the game, or exiting.
- **🔧 Custom Utilities**:
  - Cross-platform console clearing.
  - Logging setup for error tracking.

---

## 🔧 Project Structure

### 🛠️ Classes and Functions

- **Utility Functions**:
  - `clear_console()`: Clears the console based on the OS.
  - `exiting()`: Clears the console and exits the game.
  - `setup_logging()`: Sets up error logging to `logs/game.log`.

- **DatabaseManager**:
  - Handles database connection and initialization.
  - Creates tables for characters, quests, and inventory.

- **Console**:
  - Provides methods for menu handling and displaying options.
  - Includes feedback for invalid user input.

- **CharacterCreator**:
  - Guides users through creating a character with options for races, subraces, classes, and stats.
  - Supports manual and random stat allocation.

- **Main Functions**:
  - `main_menu()`: Displays the main menu and navigates through options.
  - `create_character()`: Handles the character creation process.
  - `play_game()`: Placeholder for the game loop (to be implemented).

### 📚 Files

- **`main.py`**: The entry point of the application. It handles the main menu, character creation, and initialization.
- **`database_manager.py`**: Manages the SQLite database, including connection handling and table initialization.
- **`utilities.py`**: Contains utility functions for logging, console management, and exiting the application.

---

## 🚀 Getting Started

### 📋 Prerequisites

- Python 3.8 or later
- SQLite (bundled with Python)

### ▶️ Running the Game

1. Clone the repository or copy the script.
2. From the project root, launch the game module with Python:

```bash
python -m fableforge.main
```

### 🧪 Running Tests

Install the development extras and run pytest:

```bash
pip install -e .[dev]       # install with pytest
pytest                      # run tests
```

### 🖍️ Logging

- Errors and warnings are logged to `logs/game.log`. Ensure the script has write permissions for the log file.

### ✨ Customization

- Modify the database structure or add new tables by editing `DatabaseManager.initialize_tables()`.
- Add new game features by expanding `play_game()` or creating additional menu options.

---

## 🌟 Future Enhancements

- ⚔️ Expand the gameplay loop with quests and battles.
- 💾 Add a save/load game feature.
- 🤝 Introduce multiplayer functionality.

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

✨ **Enjoy your adventure in FableForge!** 🎲
