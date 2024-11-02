import sqlite3


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
        password BLOB,
        iv BLOB,
        salt TEXT,
        tag BLOB,
        FOREIGN KEY(userID) REFERENCES Users(userID)
    )
    """)


def add_user(user, hashed_master, salt):
    try:
        with sqlite3.connect("password_manager.db") as conn:
            cursor = conn.cursor()
            create_tables(cursor)

            cursor.execute(
                "INSERT into Users (user, master_password, salt) VALUES (?, ?, ?)",
                (user, hashed_master, salt),
            )
            conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while adding the user: {e}")


def add_password(encrypted_password, user, salt, name, iv, tag):
    try:
        with sqlite3.connect("password_manager.db") as conn:
            cursor = conn.cursor()
            create_tables(cursor)

            userID = get_userID(user)

            find_existing = cursor.execute(
                "SELECT * from Passwords WHERE userID = ? and name = ?",
                (userID, name),
            ).fetchone()
            if find_existing is not None:
                raise ValueError(
                    "A password with this name already exists for this user"
                )

            cursor.execute(
                "INSERT into Passwords (userID, password, salt, name, iv, tag) VALUES (?, ?, ?, ?, ?, ?)",
                (userID, encrypted_password, salt, name, iv, tag),
            )
            conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while adding the password: {e}")


def get_userID(user):
    try:
        with sqlite3.connect("password_manager.db") as conn:
            cursor = conn.cursor()

            userID = cursor.execute(
                "SELECT UserID FROM Users WHERE user = ?", (user,)
            ).fetchone()
            return userID[0]
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while retrieving userID: {e}")


def get_master_password(user):
    try:
        with sqlite3.connect("password_manager.db") as conn:
            cursor = conn.cursor()

            master_password = cursor.execute(
                "SELECT master_password, salt FROM Users WHERE user = ?", (user,)
            ).fetchone()
            return master_password
    except sqlite3.Error as e:
        raise RuntimeError(
            f"An error occured while retrieving the master password: {e}"
        )


def get_passwordID(userID, name):
    try:
        with sqlite3.connect("password_manager.db") as conn:
            cursor = conn.cursor()

            passID = cursor.execute(
                "SELECT passwordID FROM Passwords WHERE userID = ? and name = ?",
                (
                    userID,
                    name,
                ),
            ).fetchone()
            return passID
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while retrieving passID: {e}")


def get_password(name, user):
    try:
        with sqlite3.connect("password_manager.db") as conn:
            cursor = conn.cursor()

            userID = get_userID(user)

            password = cursor.execute(
                "SELECT password, iv, salt, tag FROM Passwords WHERE userID = ? and name = ?",
                (userID, name),
            ).fetchone()
            return password
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while retrieving Password: {e}")


def get_password_names(user):
    try:
        with sqlite3.connect("password_manager.db") as conn:
            cursor = conn.cursor()

            userID = get_userID(user)

            passwords = cursor.execute(
                "SELECT name FROM Passwords WHERE userID = ?", (userID,)
            ).fetchall()
            return passwords
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while retrieving Passwords: {e}")


def delete_password(name, user):
    try:
        with sqlite3.connect("password_manager.db") as conn:
            cursor = conn.cursor()

            userID = get_userID(user)

            passwordID = get_passwordID(userID, name)[0]
            cursor.execute("DELETE FROM Passwords WHERE passwordID = ?", (passwordID,))
            conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while deleting the password: {e}")


def delete_all_passwords(userID):
    try:
        with sqlite3.connect("password_manager.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Passwords WHERE userID = ?", (userID,))
            conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while deleting the user's passwords: {e}")


def delete_user(user):
    try:
        with sqlite3.connect("password_manager.db") as conn:
            cursor = conn.cursor()

            userID = get_userID(user)

            cursor.execute("DELETE FROM Users WHERE userID = ?", (userID,))
            conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f"An error occured while deleting the user: {e}")

    delete_all_passwords(userID)
