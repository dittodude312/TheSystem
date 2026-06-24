CATEGORIES = {"Art & Music":"artmusic", "Computer Science":"compscience", "Electives":"elective", 
              "History":"history", "World Languages":"language", "Math":"math", "Reading":"reading",
              "Sciences":"sciences"}


def display_categories():
    print("*"*30)
    for element in CATEGORIES.keys(): print(element)
    print("*"*30)


def get_class_from_category(category_path):
    with open(f"school_classes/{category_path}.txt", "r") as file:
        classes = [x[:-1] for x in file.readlines()]
    return classes


def to_title_case(string):
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


def change_key(dictionary, old_key, new_key):
    new_dict = {}

    keys = list(dictionary.keys())
    values = list(dictionary.values())

    keys.insert(keys.index(old_key), new_key)
    keys.remove(old_key)

    for i in range(len(keys)):
        new_dict.update({keys[i]:values[i]})
    
    return new_dict


if __name__ == "__main__":
    print("Running utilfunctions.py")