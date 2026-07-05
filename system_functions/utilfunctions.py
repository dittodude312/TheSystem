"""
    File containing general use functions used by other modules in package.
"""
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

    stop = 0
    words = []
    space_number = 0
    string = string.strip()
    string = string[:-1] if string[len(string) - 1] == "." else string

    for char in string:
        if char == " ": space_number += 1
    
    string += " "

    for _ in range(space_number + 1):
        stop = string.index(" ")
        word = string[:stop]

        string = string[stop + 1:]
        words.append(word)
    
    words = [x.lower().capitalize() for x in words]
    for element in words:
        if element.lower() == "ii" or element.lower() == "iii":
            words[words.index(element)] = element.upper()
    for element in words:
        words[words.index(element)] = element.upper() if "." in element else element
    for element in words:
        words[words.index(element)] = element.upper() if "/" in element else element
    string = ""

    for element in words:
        string += (element + " ")

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


if __name__ == "__main__":
    print("Running utilfunctions.py")