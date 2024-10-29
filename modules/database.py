import sqlite3
import os


def connect_db():
    conn = sqlite3.connect("../db/password_manager.db")
    return conn


def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users(
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        master_password TEXT,
        salt TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Passwords(
        PasswordID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER
        Password TEXT,
        salt TEXT,
        FOREIGN KEY(UserID) REFERENCES Users(UserID)
    )
    """)


conn = connect_db()
cursor = conn.cursor()
create_tables(cursor)
conn.close()
print("hello")
