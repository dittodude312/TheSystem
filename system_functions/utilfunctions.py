"""
    File containing general use functions used by other modules in package.
    Additionally imports other functions from built-in modules to be used by other modules.
"""

from json import load, dump
from csv import reader, writer
from os import listdir, getenv
from dotenv import load_dotenv
from datetime import datetime


CATEGORIES:dict = {"Art & Music":"artmusic", "Computer Science":"compscience", "Electives":"elective", 
                   "History":"history", "World Languages":"language", "Math":"math", "Reading":"reading",
                   "Sciences":"sciences"}


def display_categories() -> None:
    """
    Displays all categories availble for classes.
    :return: None
    :rtype: None
    """
    print("*"*30)
    for element in CATEGORIES.keys(): print(element)
    print("*"*30)


def get_class_from_category(category_path:str) -> list[str]:
    """
    Returns all registered classes from a category.
    :param category_path: File name of category.
    :type category_path: str
    :return: List of classes in a subject category.
    :rtype: list[str]
    """
    with open(f"school_classes/{category_path}.txt", "r") as file:
        classes = [x[:-1] for x in file.readlines()]
    return classes


def to_title_case(string:str) -> str:
    """
    Returns string capatilized in title case. Words are separated by spaces. Words with / or . are fully capitalized. ii and iii are fully capitalized.
    :param string: String to be made title case.
    :type string: str
    """
    if not string: return ""
    
    words = [x.lower().capitalize() for x in string.strip().split(" ")]

    for element in words:
        if element.lower() == "ii" or element.lower() == "iii":
            words[words.index(element)] = element.upper()
    for element in words:
        words[words.index(element)] = element.upper() if "." in element else element
    for element in words:
        words[words.index(element)] = element.upper() if "/" in element else element
    string = ""

    for element in words: string += (element + " ")

    return string.strip()


def change_key(dictionary:dict, old_key:str, new_key:str) -> dict:
    """
    Takes dictionary and swaps out old_key for new_key. Raises ValueError if old_key cannot be found.
    :param dictionary: Dictionary to be changed.
    :type dictionary: dict
    :param old_key: Old key found in dictionary.
    :type old_key: str
    :param new_key: New key to replace old key.
    :type new_key: str
    """
    new_dict = {}

    keys = list(dictionary.keys())
    if old_key not in keys: raise ValueError("Key not found.")
    values = list(dictionary.values())

    keys.insert(keys.index(old_key), new_key)
    keys.remove(old_key)

    for i in range(len(keys)):
        new_dict.update({keys[i]:values[i]})
    
    return new_dict


def encrypt(plaintext:str, key:list[str]) -> str:
    """
    Encrypts plaintext based on shuffled key.
    :param plaintext: Plain text.
    :type plaintext: str
    :param key: Key shuffled from character list.
    :type key: list[str]
    :return: Encrypted string.
    :rtype: str
    """
    chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
             "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    ciphertext = ""
    for char in [key[chars.index(x)] for x in plaintext]: ciphertext += char
    return ciphertext


def decrypt(ciphertext:str, key:list[str]) -> str:
    """
    Decrypts ciphertext based on shuffled key.
    :param ciphertext: Text ciphered according to key.
    :type ciphertext: str
    :param key: Key shuffled from character list.
    :type key: list[str]
    :return: Decrypted string.
    :rtype: str
    """
    chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
             "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    plaintext = ""
    for char in [chars[key.index(x)] for x in ciphertext]:
        plaintext += char
    return plaintext


def update_user_month_data(username:str) -> None:
    """
    Updates the mission count and hour count in profile file of given username for the current month. 
    :param username: Username of person to update profile.
    :type username: str
    :return: None
    :rtype: None
    """
    # Get first name
    start_time = datetime.now()
    with open("x_mans_files/x_men_list.csv", "r") as file:
        _ = reader(file)
        for entry in _:
            if entry[3] == username: first_name = entry[0]
    
    # Fetch old profile data
    with open(f"x_mans_files/profiles/{username}.json", "r") as file:
        user_data = load(file)

    # Fetch mission count and hour data for current month
    month = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}[start_time.month]
    
    try:
        with open(f"x_mans_files/mission_logs/{start_time.year}logs/xmans{month}{start_time.year}.csv", "r") as file:
            _ = reader(file)
            for line in _: 
                if line[0] == first_name: hour_data = line
    # Update profile file
    except FileNotFoundError:
        user_data["Monthly Hours"] = 0
        user_data["Monthly Mission Count"] = 0
    else:
        user_data["Monthly Hours"] = int(hour_data[4])
        user_data["Monthly Mission Count"] = int(hour_data[3])

    with open(f"x_mans_files/profiles/{username}.json", "w") as file:
        dump(user_data, file)


def date_is_later(a:str, b:str) -> bool:
    """
    Operates on dates in m/d/y format. Returns True if a is a later date than b, False if not.
    :param a: First date.
    :type a: str
    :param b: Second date.
    :type b: str
    :return: Boolean of whether a is a later date than b.
    :rtype: bool
    """
    a_digits = [int(x) for x in a.split("/")]
    b_digits = [int(x) for x in b.split("/")]

    if a_digits[2] > b_digits[2]: return True

    if a_digits[0] > b_digits[0]: return True

    if a_digits[0] == b_digits[0]:
        return True if a_digits[1] > b_digits[1] else False
    
    return False


if __name__ == "__main__":
    print("Running utilfunctions.py")