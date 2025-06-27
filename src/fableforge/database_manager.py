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
