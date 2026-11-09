import sqlite3
import json

conn = sqlite3.connect("rosterdb.sqlite")

cur = conn.cursor()

cur.executescript("""
    DROP TABLE IF EXISTS User;
    DROP TABLE IF EXISTS Course;
    DROP TABLE IF EXISTS Member;

    CREATE TABLE User (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT UNIQUE);
    
    CREATE TABLE Course (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE);

    CREATE TABLE Member (
        user_id INTEGER,
        course_id INTEGER,
        role INTEGER,
        PRIMARY KEY (user_id, course_id)
    );

""")

fname = input("Enter file name: ")

# Якщо нічого не введено, використовуємо файл за замовчуванням
if len(fname) < 1:
    fname = "roster_data.json"

with open(fname) as file:
    data = json.load(file)
    for row in data:
        #print(row)
        user_name = row[0]
        course_title = row[1]
        course_role = row[2]

        cur.execute("""
        INSERT OR IGNORE INTO User (name)
        VALUES (?)
        """,
        (user_name,),
        )
        cur.execute("SELECT id FROM User WHERE name = ?", (user_name,),)
        user_id = cur.fetchone()[0]

        cur.execute("""
        INSERT OR IGNORE INTO Course (title)
        VALUES (?)
        """,
        (course_title,),
        )
        cur.execute("SELECT id FROM Course WHERE title = ?", (course_title,),)
        course_id = cur.fetchone()[0]

        cur.execute("""
        INSERT OR REPLACE INTO Member (user_id, course_id, role)
        VALUES (?, ?, ?)
        """,
        (user_id, course_id, course_role),
        )
conn.commit()
conn.close()