import sqlite3
import os
import logging

class DatabaseManager:
    def __init__(self, db_name="dnd_game.db"):
        root_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        db_dir = os.path.join(root_dir, "data")
        os.makedirs(db_dir, exist_ok=True)
        self.db_name = os.path.join(db_dir, db_name)

    def connect(self):
        """Return a SQLite connection with foreign keys enabled."""
        try:
            conn = sqlite3.connect(self.db_name)
            #Ensure ON DELETE CASCADE and other FK constraints are active
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except sqlite3.Error as e:
            logging.error("Database connection failed: %s", e)
            raise

    def initialize_tables(self):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                tables = {
                "characters": """
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
                """,
                "quests": """
                    CREATE TABLE IF NOT EXISTS quests (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT,
                        completed BOOLEAN NOT NULL,
                        progress TEXT,
                        character_id INTEGER,
                        FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE
                    )
                """,
                "inventory": """
                    CREATE TABLE IF NOT EXISTS inventory (
                        id INTEGER PRIMARY KEY,
                        item_name TEXT NOT NULL,
                        quantity INTEGER,
                        character_id INTEGER,
                        FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE
                    )
                """,
            }
                for table, create_sql in tables.items():
                    cursor.execute(create_sql)

                conn.commit()
        except sqlite3.Error as e:
            logging.error("Failed to initialize database tables: %s", e)
            raise


    # Inventory management ---------------------------------------------

    def add_item(self, character_id, item_name, quantity=1):
        """Add ``quantity`` of ``item_name`` to ``character_id``'s inventory."""
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, quantity FROM inventory WHERE character_id = ? AND item_name = ?",
                    (character_id, item_name),
                )
                row = cursor.fetchone()
                if row:
                    # Item exists, update quantity
                    cursor.execute(
                        "UPDATE inventory SET quantity = ? WHERE id = ?",
                        (row[1] + quantity, row[0]),
                    )
                else:
                    cursor.execute(
                        "INSERT INTO inventory (item_name, quantity, character_id) VALUES (?, ?, ?)",
                        (item_name, quantity, character_id),
                    )
                conn.commit()
        except sqlite3.Error as e:
            logging.error("Error adding item: %s", e)
            raise

    def remove_item(self, character_id, item_name, quantity=1):
        """Remove ``quantity`` of ``item_name`` from ``character_id``'s inventory."""
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, quantity FROM inventory WHERE character_id = ? AND item_name = ?",
                    (character_id, item_name),
                )
                row = cursor.fetchone()
                if row:
                    remaining = row[1] - quantity
                    if remaining > 0:
                        cursor.execute(
                            "UPDATE inventory SET quantity = ? WHERE id = ?",
                            (remaining, row[0]),
                        )
                    else:
                        cursor.execute(
                            "DELETE FROM inventory WHERE id = ?",
                            (row[0],),
                        )
                    conn.commit()
        except sqlite3.Error as e:
            logging.error("Error removing item: %s", e)
            raise

    def get_inventory(self, character_id):
        """Return a list of ``(item_name, quantity)`` for ``character_id``."""
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT item_name, quantity FROM inventory WHERE character_id = ?",
                    (character_id,),
                )
                return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error("Error retrieving inventory: %s", e)
            raise

# End of inventory management ------------------------------------------

# Save quest progress --------------------------------------------------
    def save_quest_progress(self, character_id, quest_name, progress_step):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id FROM quests WHERE character_id = ? AND name = ?",
                    (character_id, quest_name)
                )
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(
                    "INSERT INTO quests (character_id, name, progress, completed) VALUES (?, ?, ?, ?)",
                    (character_id, quest_name, progress_step, 0)
                )
            else:
                cursor.execute(
                    "UPDATE quests SET progress = ? WHERE character_id = ? AND name = ?",
                    (progress_step, character_id, quest_name)
                )
            conn.commit()
        except sqlite3.Error as e:
            logging.error("Error saving quest progress: %s", e)
            raise
# End of save quest progress -------------------------------------------

# load quest progress --------------------------------------------------
    def load_quest_progress(self, character_id, quest_name):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT progress FROM quests WHERE character_id = ? AND name = ?",
                    (character_id, quest_name)
                )
                row = cursor.fetchone()
                return row[0] if row else None
        except sqlite3.Error as e:
            logging.error("Error loading quest progress: %s", e)
            raise
# End of load quest progress --------------------------------------------

# Delete quest progress -------------------------------------------------
    def reset_quest_progress(self, character_id, quest_name):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM quests WHERE character_id = ? AND name = ?",
                    (character_id, quest_name)
                )
                conn.commit()
        except sqlite3.Error as e:
            logging.error("Error resetting quest progress: %s", e)
            raise
# End of delete quest progress ------------------------------------------