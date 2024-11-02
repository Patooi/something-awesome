from termcolor import colored
import os
from modules import add_user
import getpass
import string
import pyperclip

from modules.database import (
    add_password,
    delete_password,
    delete_user,
    get_master_password,
    get_password,
    get_password_names,
    get_userID,
)
from modules.password_security import (
    compare_master_password,
    decrypt_password,
    encrypt_password,
    hash_master_password,
)
from modules.password_strength import generate_password, is_valid_master


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def create_account():
    clear_screen()

    user = input(colored("Please enter your username\n", "green"))
    check_if_exists = get_userID(user)
    while check_if_exists is not None:
        print(
            colored(
                "User already exists. Please use a different username\n",
                "black",
                "on_red",
            )
        )
        user = input(colored("Please enter your username\n", "green"))
        check_if_exists = get_userID(user)
    while True:
        master_password = getpass.getpass(
            colored("Please enter your password\n", "red")
            + colored(
                "It should be at least 14 characters, have one upper-case + lower-case character, one number and one special character.\n",
                "blue",
            )
        )
        valid, string = is_valid_master(master_password)
        if not valid:
            clear_screen()
            print(colored(string + " Please try again", "red"))
            continue
        check = getpass.getpass(
            colored("Please enter your password again\n", "light_blue")
        )
        if check == master_password:
            break
        clear_screen()
        print(colored("These passwords did not match, please try again\n"))

    hashed_password, salt = hash_master_password(master_password)
    add_user(user, hashed_password, salt)
    logged_in(user, master_password)


def login():
    clear_screen()
    username = input(
        colored("Please enter your username\n", "green")
        + colored("Type 'quit' to exit\n", "blue")
    )
    if username == "quit":
        return

    while True:
        master_password = get_master_password(username)
        if master_password is not None:
            hashed_password, salt = master_password
            break
        username = input(
            colored("User not Found. Please try again\n", "black", "on_red")
            + colored("Type 'quit' to go back\n", "blue")
        )
        if username.lower() == "quit":
            return
    while True:
        master_password = getpass.getpass(
            colored("Please enter your password\n", "light_red")
        )
        if compare_master_password(hashed_password, master_password, salt):
            logged_in(username, master_password)
            break
        clear_screen()
        print(colored("Wrong Password. Please try again.\n", "black", "on_red"))


def logged_in(user, master_password):
    clear_screen()
    print("Logged in!")
    while True:
        user_input = input(
            colored("What would you like to do?\n", "magenta")
            + colored("(1) Add a password\n", "blue")
            + colored("(2) Retrieve a password\n", "cyan")
            + colored("(3) See what passwords are saved\n", "green")
            + colored("(4) Delete a password\n", "yellow")
            + colored("(5) Delete the account\n", "grey")
            + colored("Type 'quit' to quit\n", "white")
        )
        if user_input == "quit":
            print(colored("See ya! I'll keep your passwords safe."))
            break
        elif user_input == "1":
            insert_password(user, master_password)
        elif user_input == "2":
            retrieve_password(user, master_password)
        elif user_input == "3":
            retrieve_passwords(user)
        elif user_input == "4":
            remove_password(user)
        elif user_input == "5":
            remove_account(user, master_password)
            print(f"Account {user} deleted! See ya.")
            break
        else:
            clear_screen()
            print(colored("Choose one of the options below\n", "black", "on_red"))


def create_password():
    clear_screen()
    print(colored("How long do you want your password to be?", "green"))
    length = input(colored("Please choose a number from 14-26\n", "blue"))
    print(colored("What would you like your password to consist of?", "cyan"))
    choices = [
        ("Lower-Case Letters: [a-z]", string.ascii_lowercase),
        ("Upper-Case Letters: [A-Z]", string.ascii_uppercase),
        ("Numbers: [0-9]", string.digits),
        ("Special Characters: [!@#$%^]", "!@#$%^"),
    ]
    choice_string = ""
    while len(choices) != 0:
        for i, choice in enumerate(choices):
            print(colored(f"({i + 1}): {choice[0]}\n", "green"))
        user_input = input(colored("Type 'done' to finish selection\n", "magenta"))
        if user_input.lower() == "done":
            if len(choice_string) == 0:
                print(colored("Please choose at least one option.\n", "red"))
            else:
                break
        elif int(user_input) <= len(choices):
            choice_string = choice_string + choices[int(user_input) - 1][1]
            choices.remove(choices[int(user_input) - 1])
        else:
            print(colored("Please choose from the above choices.\n", "red"))
    password = generate_password(int(length), choice_string)
    return password


def insert_password(user, master_password):
    clear_screen()
    name = input(colored("What will you name this password?\n", "magenta"))
    check = get_password(name, user)
    while check is not None:
        clear_screen()
        print(
            colored(
                "Name already exists for another one of your passwords. Please try another.",
                "black",
                "on_red",
            )
        )
        name = input(colored("What will you name this password?", "magenta"))
        check = get_password(name, user)
    password = create_password()
    ciphertext, salt, tag, iv = encrypt_password(master_password, password)
    add_password(ciphertext, user, salt, name, iv, tag)
    clear_screen()
    print(colored(f"Password added! Your password is {password}", "cyan"))


def retrieve_password(user, master_password):
    clear_screen()
    while True:
        print(
            colored("What is the name of the password you want to retrieve?", "green")
        )
        name = input(colored("Type 'quit' to go back\n", "blue"))
        if name.lower() == "quit":
            return
        password = get_password(name, user)
        if password is None:
            print(
                colored(
                    "That name does not belong to any of your passwords. Please try again",
                    "black",
                    "on_red",
                )
            )
            continue
        break
    ciphertext, iv, salt, tag = password
    decrypted_password = decrypt_password(iv, salt, tag, ciphertext, master_password)
    clear_screen()
    print(
        colored(
            f"Your password named {name} is {decrypted_password.decode('utf-8')}\n",
            "black",
            "on_green",
        )
        + colored("The password has also been copied to your clipboard\n", "blue")
    )
    pyperclip.copy(f"{decrypted_password.decode('utf-8')}")


def retrieve_passwords(user):
    clear_screen()
    password_names = get_password_names(user)
    if len(password_names) == 0:
        print("No passwords were saved\n")
    for i, password in enumerate(password_names):
        print(f"({i + 1}): {password[0]}")
    input(colored("Press enter to return\n", "blue"))
    return


def remove_password(user):
    clear_screen()
    while True:
        name = print(
            colored("What is the name of the password you want removed?\n", "green")
        )
        name = input(colored("Type 'quit' to go back\n", "blue"))
        if name.lower() == "quit":
            return
        password = get_password(name, user)
        if password is None:
            print(colored("Password does not exist. Please try again.\n", "red"))
        break
    confirmation = input(colored(f"Are you sure you want to remove {name}? (y/n)\n"))
    if confirmation.lower() == "n":
        return
    delete_password(name, user)
    clear_screen()
    print(colored(f"Password {name} has been deleted!\n", "cyan"))


def remove_account(user, master_password):
    clear_screen()
    confirmation = input(
        colored(
            "Are you sure you want to delete your account? All passwords will be removed. (y/n)\n",
            "red",
        )
    )

    if confirmation == "n":
        return

    while True:
        print("Please enter your master password\n")
        password = getpass.getpass(colored("Type 'quit' to go back.\n", "blue"))
        if password.lower() == "quit":
            return
        elif password != master_password:
            print(colored("Incorrect. Please try again.\n", "red"))
        break

    delete_user(user)


if __name__ == "__main__":
    welcome = "Welcome to the password manager! What would you like to do?"
    print(colored(welcome, "blue"))

    def prompt_func():
        prompt = (
            colored("(1) Log in to existing account\n", "green")
            + colored("(2) Create a new account\n", "light_red")
            + colored("Type 'quit' to quit\n", "white")
        )
        user_input = input(prompt)
        if user_input.lower() == "quit":
            print(colored("See ya! I'll keep your passwords safe."))
        elif user_input == "1":
            login()
        elif user_input == "2":
            create_account()
        else:
            clear_screen()
            print(colored("Invalid input. Please try again", "black", "on_red"))
            prompt_func()

    prompt_func()
