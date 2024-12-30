# 🐉 DnD Campaign Game

Welcome to the **DnD Campaign Game**, a Python-based, text-driven adventure inspired by Dungeons & Dragons! Create characters, complete quests, and explore a world full of possibilities. 🧙‍♂️✨

---

## 🌟 Features

- **🎭 Character Creation**:
  - Choose from various races, subraces, and classes.
  - Manually distribute or randomly generate character stats.
- **📦 Database Integration**:
  - Stores characters, quests, and inventory in a SQLite database (`dnd_game.db`).
  - Automatically initializes database tables on startup.
- **💻 Dynamic Console Interaction**:
  - User-friendly menu navigation with options for creating characters, playing the game, or exiting.
- **🔧 Custom Utilities**:
  - Cross-platform console clearing.
  - Logging setup for error tracking.

---

## 🏗️ Project Structure

### 🛠️ Classes and Functions

- **Utility Functions**:
  - `clear_console()`: Clears the console based on the OS.
  - `exiting()`: Clears the console and exits the game.
  - `setup_logging()`: Sets up error logging to `game.log`.

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

---

## 🚀 Getting Started

### 📋 Prerequisites

- Python 3.8 or later
- SQLite (bundled with Python)

### ▶️ Running the Game

1. Clone the repository or copy the script.
2. Run the script using Python:

   ```bash
   python main.py
   ```

### 📝 Logging

- Errors and warnings are logged to `game.log`. Ensure the script has write permissions for the log file.

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

✨ **Enjoy your adventure in the DnD campaign game!** 🎲
