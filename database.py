import sqlite3


db = sqlite3.connect(
    "bot.db",
    check_same_thread=False
)

cursor = db.cursor()



def setup_database():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS files(
        code TEXT PRIMARY KEY,
        file_id TEXT NOT NULL
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS channels(
        username TEXT PRIMARY KEY
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS banner(
        id INTEGER PRIMARY KEY,
        text TEXT
    )
    """)


    db.commit()



# -------- Files --------


def save_file(code, file_id):

    cursor.execute(
        """
        INSERT OR REPLACE INTO files
        (code,file_id)
        VALUES (?,?)
        """,
        (
            code,
            file_id
        )
    )

    db.commit()



def find_file(code):

    cursor.execute(
        """
        SELECT file_id
        FROM files
        WHERE code=?
        """,
        (code,)
    )

    result = cursor.fetchone()

    if result:
        return result[0]

    return None



# -------- Channels --------


def add_channel(username):

    cursor.execute(
        """
        INSERT OR IGNORE INTO channels
        VALUES(?)
        """,
        (username,)
    )

    db.commit()



def delete_channel(username):

    cursor.execute(
        """
        DELETE FROM channels
        WHERE username=?
        """,
        (username,)
    )

    db.commit()



def get_channels():

    cursor.execute(
        "SELECT username FROM channels"
    )

    return [
        row[0]
        for row in cursor.fetchall()
]
