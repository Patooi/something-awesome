import sqlite3
from contextlib import contextmanager

"""
Connects to the database and creates the database file, if it does not exist. Context manager ensures that 
the connection is always closed after process is done and/or exits due to errors.
"""


@contextmanager
def connect_db():
    conn = sqlite3.connect("../password_manager.db")
    try:
        yield conn
    finally:
        conn.close()


def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users(
        userID INTEGER PRIMARY KEY,
        user TEXT UNIQUE,
        master_password TEXT,
        salt TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Passwords(
        passwordID INTEGER PRIMARY KEY,
        userID INTEGER,
        name TEXT,
        password TEXT UNIQUE,
        salt TEXT,
        FOREIGN KEY(userID) REFERENCES Users(userID)
    )
    """)


def add_user(user, hashed_master, salt):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            create_tables(cursor)

            cursor.execute(
                "INSERT into Users (user, master_password, salt) VALUES (?, ?, ?)",
                (user, hashed_master, salt),
            )
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while adding the user: {e}")


def add_password(encrypted_password, userID, salt, name):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            create_tables(cursor)

            cursor.execute(
                "INSERT into Passwords (userID, password, salt, name) VALUES (?, ?, ?, ?)",
                (userID, encrypted_password, salt, name),
            )
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while adding the password: {e}")


def get_userID(user):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()

            userID = cursor.execute(
                "SELECT UserID FROM Users WHERE user is ?", (user,)
            ).fetchone()
            return userID
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while retrieving userID: {e}")


def get_passwordID(userID, name):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()

            passID = cursor.execute(
                "SELECT passwordID FROM Passwords WHERE passwordID is ? and name is ?",
                (
                    userID,
                    name,
                ),
            ).fetchone()
            return passID
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while retrieving passID: {e}")


def get_password(passwordID):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()

            password = cursor.execute(
                "SELECT password, salt FROM Passwords WHERE passwordID is ?",
                (passwordID,),
            ).fetchone()

            return password
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while retrieving Password: {e}")


def get_all_passwords(userID):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()

            passwords = cursor.execute(
                "SELECT password, salt FROM Passwords WHERE userID is ?", (userID,)
            ).fetchall()

            return passwords
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while retrieving Passwords: {e}")


def delete_password(passwordID):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Passwords WHERE passwordID is ?", (passwordID,))
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while deleting the password: {e}")


def delete_all_passwords(userID):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Passwords WHERE userID is ?", (userID,))
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while deleting the user's passwords: {e}")


def delete_user(userID):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Users WHERE userID is ?", (userID,))

            delete_all_passwords(userID)
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while deleting the user: {e}")
