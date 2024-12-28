import sqlite3
import random

# Connect to SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect('dnd_game.db')
cursor = conn.cursor()

# Create the 'characters' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    race TEXT NOT NULL,
    class TEXT NOT NULL,
    strength INTEGER,
    dexterity INTEGER,
    intelligence INTEGER,
    health INTEGER,
    experience INTEGER
)
''')

# Create the 'quests' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS quests (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL,
    character_id INTEGER,
    FOREIGN KEY (character_id) REFERENCES characters(id)
)
''')

# Create the 'inventory' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY,
    item_name TEXT NOT NULL,
    quantity INTEGER,
    character_id INTEGER,
    FOREIGN KEY (character_id) REFERENCES characters(id)
)
''')

# Commit and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")

def create_character():
    # Ask for character details
    name = input("Enter your character's name: ")
    race = input("Choose your race (Human, Elf, Dwarf, Orc): ")
    character_class = input("Choose your class (Warrior, Mage, Rogue): ")

    # Randomly generate stats
    strength = random.randint(8, 18)
    dexterity = random.randint(8, 18)
    intelligence = random.randint(8, 18)
    health = 100  # Default starting health
    experience = 0  # Starting experience

    # Connect to SQLite database
    conn = sqlite3.connect('dnd_game.db')
    cursor = conn.cursor()

    # Insert new character into the database
    cursor.execute('''
    INSERT INTO characters (name, race, class, strength, dexterity, intelligence, health, experience)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, race, character_class, strength, dexterity, intelligence, health, experience))

    # Commit and close the connection
    conn.commit()
    conn.close()

    print(f"Character {name} created successfully!")

# Call the create_character function to start the character creation process
create_character()