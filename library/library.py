import sqlite3
import csv

conn = sqlite3.connect("librarydb.sqlite")

cur = conn.cursor()

cur.executescript("""
    DROP TABLE IF EXISTS Author;
    DROP TABLE IF EXISTS Book;

    CREATE TABLE Author (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE);

    CREATE TABLE Book (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    author_id INTEGER ,
    year INTEGER,
    pages INTEGER
    
    );

""")

fname = input("Enter file name: ")

if len(fname) < 1:
    fname = "books.csv" 

with open(fname, newline="", encoding="utf-8") as file:
    data = csv.reader(file)
    for row in data:
        title_book = row[0]
        author_book = row[1]
        year = row[2]
        page = row[3]

        cur.execute(""" INSERT OR IGNORE INTO Author (name) VALUES(?)""",(author_book,),
        )
        cur.execute("SELECT id FROM Author  WHERE name = ? ", (author_book,),)
        author_id = cur.fetchone()[0]

        cur.execute(""" INSERT OR IGNORE INTO Book (title, author_id, year, pages) VALUES(?, ?, ?, ?)""",(title_book, author_id, year, page),
                )

conn.commit()
conn.close()
