import sqlite3

for i in range(10):
    conn = sqlite3.connect("./data/news{}.db".format(i+5))
    c = conn.cursor()

    c.execute('''CREATE TABLE news
                (
                    url text,
                    title text,
                    cluster text)''')

    conn.commit()
    conn.close()