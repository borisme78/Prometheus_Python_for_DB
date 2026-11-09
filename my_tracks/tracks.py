import sqlite3
import csv

conn = sqlite3.connect("tracksdb.sqlite")
cur = conn.cursor()

cur.executescript("""
    DROP TABLE IF EXISTS Artist;
    DROP TABLE IF EXISTS Genre;
    DROP TABLE IF EXISTS Album;
    DROP TABLE IF EXISTS Track;

    CREATE TABLE Artist(
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name    TEXT UNIQUE
    );

    CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
    );  

    CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

    CREATE TABLE Track (
        id  INTEGER NOT NULL PRIMARY KEY 
            AUTOINCREMENT UNIQUE,
        title TEXT  UNIQUE,
        album_id  INTEGER,
        genre_id  INTEGER,
        len INTEGER, rating INTEGER, count INTEGER
);
""")

fname = input("Enter file name: ")

if len(fname) < 1:
    fname = "tracks.csv"

with open(fname, newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        #print(row)
        title = row[0]
        name = row[1]
        album = row[2]
        count = row[3]
        rating = row[4]
        length = row[5]
        genre = row[6]

        cur.execute(
        """
        INSERT OR IGNORE INTO Artist (name)
        VALUES (?)
        """,
        (name,),
        )
        cur.execute("SELECT id FROM Artist WHERE name = ?", (name,))
        artist_id = cur.fetchone()[0]

        cur.execute(
        """
        INSERT OR IGNORE INTO Genre (name)
        VALUES (?)
        """,
        (genre,),
        )
        cur.execute("SELECT id FROM Genre WHERE name = ?", (genre,))
        genre_id = cur.fetchone()[0]


        cur.execute(
            """
            INSERT OR IGNORE INTO Album (artist_id, title)
            VALUES (?, ?)
            """,
            (artist_id, album),
            )
        cur.execute("SELECT id FROM Album WHERE title = ?", (album,))
        album_id = cur.fetchone()[0]


        cur.execute(
        """
        INSERT OR REPLACE INTO Track (title, album_id, genre_id, len, rating, count)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title, album_id, genre_id, length, rating, count),
    )





conn.commit()
conn.close()
