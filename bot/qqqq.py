import sqlite3

conn = sqlite3.connect("new.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS `main` (
	`Name`	TEXT NOT NULL UNIQUE,
	`test_group`	INTEGER DEFAULT 0,
	`quest_number`	INTEGER DEFAULT 0,
	`economic_point`	INTEGER DEFAULT 0,
	`social_point`	INTEGER DEFAULT 0,
	`national_point`	INTEGER DEFAULT 0,
	`traditional_point`	INTEGER DEFAULT 0,
	`revolution_point`	INTEGER DEFAULT 0,
	`ecological_point`	INTEGER DEFAULT 0
);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS `logs` (
	`Name`	INTEGER NOT NULL,
	`test_group`	INTEGER,
	`quest_number`	INTEGER,
	`point_diff`	INTEGER
);""")

