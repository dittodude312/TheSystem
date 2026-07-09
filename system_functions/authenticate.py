"""
    File containing functionality for users logging in.
"""

from .utilfunctions import decrypt

from json import load
from dotenv import load_dotenv
from os import getenv


def fetch_data() -> dict:
    """
    Reads username and password data from file and returns dictionary.
    :return: Dictionary of {username:password} pairs.
    :rtype: dict
    """
    try:
        with open("references/users.json", "r") as file:
            contents = load(file)
    except FileNotFoundError:
        print("Failed to fetch user data. Terminating Session.")
        print("If issue persists, please contact admin.")
        print("Tip - Make sure you are using TheSystem directory when executing main.py.")
        exit(1)
    else:
        return contents 


def login() -> tuple[str]:
    """
    Gets input from user of username and password and returns inputs.
    :return: Tuple with 2 elements of username input and password input.
    :rtype: tuple[str]
    """
    while True:
        username = input("Username: ")
        password = input("Password: ")
        if not username or not password: print("Username or password fields cannot be blank.")
        else: return username, password


def main() -> str:
    """
    Calls login and fetch_data functions and checks if username and password are pairing in dictionary.
    :return: Valid username given that password matches in dictionary.
    :rtype: str
    """
    print("Welcome to the System. Please enter your credentials.")

    contents = fetch_data()
    load_dotenv()
    key = getenv("KEY").split(",")
    while True:
        username, password = login()
        if username in contents.keys() and password == decrypt(contents.get(username), key): return username
        else: print("Incorrect username or password.\n")


if __name__ == "__main__":
    print("Running authenticate.py")