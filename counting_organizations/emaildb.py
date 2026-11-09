import sqlite3

conn = sqlite3.connect("emaildb.sqlite")
cur = conn.cursor()

cur.executescript("""  
    DROP TABLE IF EXISTS Counts;

    CREATE TABLE Counts (
        org TEXT,
        count INTEGER);

""")

fname = input("Enter file name: ")

if len(fname) < 1:
    fname = "mbox.txt"

with open(fname) as file:

    for line in file:

        if not line.startswith("From "):
            continue
        words = line.split()
        email = words[1]
        domain = email.split("@")[1]

        # print(domain)
        cur.execute("SELECT count FROM Counts WHERE org = ?", (domain,))
        row = cur.fetchone()
        # print(row)
        if row is None:
            cur.execute(
                """
            INSERT INTO Counts (org, count)
            VALUES(?, ?)""",
                (
                    domain,
                    1,
                ),
            )
        else:
            cur.execute(
                """
            UPDATE Counts SET count = count + 1 WHERE org = ?""",
                (domain,),
            )

conn.commit()
conn.close()
