from datetime import datetime
from typing import *
from typing.io import *

STORAGE_LOCATION = "test/"

# Create students table
TABLE_STUDENTS = """
    CREATE TABLE IF NOT EXISTS students (
        id      INTEGER PRIMARY KEY,
        name    TEXT
    );
"""
# Create records table
TABLE_RECORDS = """
    CREATE TABLE IF NOT EXISTS records (
        time        INTEGER PRIMARY KEY,
        student_id  INTEGER
    );
"""

# Insert student into database
INSERT_STUDENT = """
    INSERT INTO students (id, name) VALUES (
        ?,
        ?
    );
"""
# Insert hall pass record into database
INSERT_RECORD = """
    INSERT INTO records (time, student_id) VALUES (
        strftime('%s', 'now'),
        ?
    );
"""

# Query student by ID
QUERY_STUDENT_ID = """
    SELECT * FROM students
    WHERE   id = ?;
"""
# Query all passes printed for student between two datetimes. To get all records, pass in 0 and "datetime('now')"
QUERY_RECORDS_STUDENT = """
    SELECT * FROM records
    WHERE   student_id = ?
    AND     time BETWEEN ? AND ?;
"""
# Query all passes between two datetimes. To get all records, pass in 0 and "datetime('now')"
QUERY_RECORDS_ALL = """
    SELECT * FROM records
    WHERE   time BETWEEN ? AND ?;
"""


FONT_FAMILY = "Helvetica"
FONT_SIZE = 20

def log(text: str, *args):
    """Prints to the console and to a log file, using format syntax to add additional arguments to message"""
    # TODO: Print to log file
    print(("{}: " + text).format(datetime.now(), *args))
