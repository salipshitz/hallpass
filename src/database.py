import sqlite3
from include import *


def open_connection(file: str) -> sqlite3.Connection:
    """Opens a connection to an SQL database with given file path"""
    try:
        conn = sqlite3.connect(file)
        log("Connected to SQLite database '{}'.", file)
        return conn
    except sqlite3.Error as e:
        log("Error connecting to SQLite database: {}.", e)
        return None


def close_connection(conn: sqlite3.Connection):
    """Closes an SQLite connection"""
    try:
        if conn is None:
            raise sqlite3.Error("connection does not exist.")
        conn.close()
        log("Closed connection to SQLite database.")
    except sqlite3.Error as e:
        log("Error closing SQLite connection: {}.", e)


def execute(conn: sqlite3.Connection, sql: str, *args: object) -> bool:
    """Executes an SQLite statement. Returns True if successful, and false if unsuccessful."""
    try:
        if conn is None:
            raise sqlite3.Error("connection does not exist")
        cursor = conn.cursor()
        cursor.execute(sql, args)
        return True
    except sqlite3.Error as e:
        log("Error executing SQL command: {}.", e)
        return False


def query(conn: sqlite3.Connection, sql: str, *args: object) -> List:
    """Executes an SQLite query. Returns an empty list if the query fails"""
    try:
        if conn is None:
            raise sqlite3.Error("connection does not exist")
        cursor = conn.cursor()
        cursor.execute(sql, args)
        return cursor.fetchall()
    except sqlite3.Error as e:
        log("Error executing SQL query {}.", e)
        return []


def commit(conn: sqlite3.Connection):
    try:
        if conn is None:
            raise sqlite3.Error("connection does not exist")
        conn.commit()
    except sqlite3.Error as e:
        log("Error committing to SQL database: {}.", e)


def test_database():
    """Tests the SQLite database"""
    conn = open_connection("test/test.db")
    execute(conn, """
        CREATE TABLE IF NOT EXISTS students (
            id    INTEGER PRIMARY KEY,
            name  STRING NOT NULL
		);
	""")
    execute(conn, """INSERT INTO students(id, name) VALUES (1514, "Johnny Appleseed")""")
    students = query(conn, """SELECT * FROM students""")
    for student in students:
        print(student)
    close_connection(conn)


if __name__ == '__main__':
    test_database()
