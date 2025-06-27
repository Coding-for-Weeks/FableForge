import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="dnd_game.db"):
        root_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        db_dir = os.path.join(root_dir, "data")
        os.makedirs(db_dir, exist_ok=True)
        self.db_name = os.path.join(db_dir, db_name)

    def connect(self):
        return sqlite3.connect(self.db_name)

    def initialize_tables(self):
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


    # Inventory management -------------------------------------------------

    def add_item(self, character_id, item_name, quantity=1):
        """Add ``quantity`` of ``item_name`` to ``character_id``'s inventory."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, quantity FROM inventory WHERE character_id = ? AND item_name = ?",
                (character_id, item_name),
            )
            row = cursor.fetchone()
            if row:
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

    def remove_item(self, character_id, item_name, quantity=1):
        """Remove ``quantity`` of ``item_name`` from ``character_id``'s inventory."""
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

    def get_inventory(self, character_id):
        """Return a list of ``(item_name, quantity)`` for ``character_id``."""
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT item_name, quantity FROM inventory WHERE character_id = ?",
                (character_id,),
            )
            return cursor.fetchall()