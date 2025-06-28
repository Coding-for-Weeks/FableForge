import sqlite3
from fableforge.database_manager import DatabaseManager


def make_db(tmp_path):
    db_file = tmp_path / "test.db"
    manager = DatabaseManager()
    manager.db_name = str(db_file)
    manager.initialize_tables()
    return manager


def test_initialize_tables(tmp_path):
    manager = make_db(tmp_path)
    with sqlite3.connect(manager.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
    assert {"characters", "quests", "inventory"}.issubset(tables)


def test_inventory_methods(tmp_path):
    manager = make_db(tmp_path)
    with sqlite3.connect(manager.db_name) as conn:
        conn.execute(
            """
            INSERT INTO characters (
                id, name, race, class, strength, dexterity, intelligence,
                charisma, wisdom, constitution, health, experience
            ) VALUES (1, 'Hero', 'Human', 'Fighter', 10,10,10,10,10,10,100,0)
            """
        )
        conn.commit()

    manager.add_item(1, "Sword", 1)
    manager.add_item(1, "Sword", 2)
    items = manager.get_inventory(1)
    assert ("Sword", 3) in items

    manager.remove_item(1, "Sword", 1)
    items = manager.get_inventory(1)
    assert ("Sword", 2) in items

    manager.remove_item(1, "Sword", 2)
    items = manager.get_inventory(1)
    assert items == []
