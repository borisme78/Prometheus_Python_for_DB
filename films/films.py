import sqlite3
import json

conn = sqlite3.connect("movies.sqlite")
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS Director;
DROP TABLE IF EXISTS Movie;
DROP TABLE IF EXISTS MovieDirector;
DROP VIEW IF EXISTS MovieDirectorView;

CREATE TABLE Director (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE);

CREATE TABLE Movie (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE);

CREATE TABLE MovieDirector (
    director_id INTEGER,
    movie_id INTEGER,
    year INTEGER,
    PRIMARY KEY (director_id, movie_id)
);

CREATE VIEW MovieDirectorView AS
SELECT Director.name AS director_name,
       Movie.title AS movie_title,
       MovieDirector.year AS year
FROM MovieDirector
JOIN Director ON MovieDirector.director_id = Director.id
JOIN Movie ON MovieDirector.movie_id = Movie.id;
""")

# Просимо користувача ввести ім'я файлу
fname = input("Enter file name: ")

# Якщо нічого не введено, використовуємо файл за замовчуванням
if len(fname) < 1:
    fname = "movies.json"

str_data = open(fname).read()
json_data = json.loads(str_data)

for entry in json_data:
    name = entry[0]
    title = entry[1]
    year = entry[2]
    print(name, title, year)

    cur.execute(
        """
        INSERT OR IGNORE INTO Director (name)
        VALUES (?)
        """,
        (name,),
    )
    cur.execute("SELECT id FROM Director WHERE name = ?", (name,))
    director_id = cur.fetchone()[0]

    cur.execute(
        """
        INSERT OR IGNORE INTO Movie (title)
        VALUES (?)
        """,
        (title,),
    )
    cur.execute("SELECT id FROM Movie WHERE title = ?", (title,))
    movie_id = cur.fetchone()[0]

    cur.execute(
        """
        INSERT OR IGNORE INTO MovieDirector (director_id, movie_id, year)
        VALUES (?, ?, ?)
        """,
        (director_id, movie_id, year),
    )

# Зберігаємо всі зміни в базі даних
conn.commit()

# Закриваємо з'єднання з базою даних
conn.close()