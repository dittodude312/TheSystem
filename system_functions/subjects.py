"""
    File containing functionality for managing school classes.
    Only availible for admin user.
"""

from .utilfunctions import *


def view_classes() -> None:
    """
    Formats and displays all classes under their category.
    :return: None
    :rtype: None
    """
    for category in CATEGORIES.keys():
        print(category.upper())
        for element in get_class_from_category(CATEGORIES[category]):
            print("\t" + element)


def add_class() -> None:
    """
    Adds new class to given category.
    :return: None
    :rtype: None
    """
    # Display categories
    display_categories()

    # Get new class's category
    while True:
        category = to_title_case(input("Enter the category for the class: "))
        
        if category.lower() == "q" or category.lower() == "quit":
            return None

        if category not in CATEGORIES.keys():
            print("Category does not exist.")
            continue
        
        existing_classes = get_class_from_category(CATEGORIES[category])
        print()

        # Get new class name
        while True:
            new_class = input("Enter the name of the class: ")

            if not new_class:
                print("Field cannot be empty.")
                continue

            new_class = to_title_case(new_class)

            if new_class.lower() == "q" or new_class.lower() == "quit":
                display_categories()
                break

            if new_class in existing_classes:
                print(f"{new_class} already exists.")
                continue
            
            # Save new class
            with open(f"school_classes/{CATEGORIES[category]}.txt", "a", newline="") as file:
                file.write(new_class + "\n") 
            print("Class registered successfully.")
            return None


def remove_class() -> None:
    """
    Remove class from given category if no students take the class.
    :return: None
    :rtype: None
    """
    # Display categories
    display_categories()

    # Get category of the class
    while True:
        category = to_title_case(input("Enter the category of the class to remove: "))

        if category.lower() == "q" or category.lower() == "quit":
            return None
        
        if category not in CATEGORIES.keys():
            print("Category does not exist.")
            continue
        
        classes = get_class_from_category(CATEGORIES[category])
        print("*"*30)
        for element in classes: print(element)
        print("*"*30)
        # Get name of the class to remove
        while True:
            delete_class = to_title_case(input("Enter the name of the class: "))

            if delete_class.lower() == "q" or delete_class.lower() == "quit":
                display_categories()
                break

            if delete_class not in classes:
                print("Class does not exist.")
                continue
            
            # Check if students are taking the class
            for student in listdir("student_grades"):
                with open(f"student_grades/{student}", "r") as file:
                    contents = load(file)
                    if delete_class in contents.keys():
                        print("A student is currently taking this class. The class cannot be removed.")
                        return None       
            
            # Remove class
            classes.remove(delete_class)

            with open(f"school_classes/{CATEGORIES[category]}.txt", "w") as file:
                classes = [x + "\n" for x in classes]
                file.writelines(classes)

            print("Class removed successfully.")
            return None


def rename_class() -> None:
    """
    Renames class found in given category.
    :return: None
    :rtype: None
    """
    display_categories()

    # Get class category
    while True:
        category = to_title_case(input("Enter the category of the class to rename: "))

        if category.lower() == "q" or category.lower() == "quit":
            return None

        if category not in CATEGORIES.keys():
            print("Category does not exist.")
            continue
        
        classes = get_class_from_category(CATEGORIES[category])
        print("*"*30)
        for element in classes: print(element)
        print("*"*30)
        # Get old name
        while True:
            old_name = to_title_case(input("Enter the class name: "))

            if old_name.lower() == "q" or old_name.lower() == "quit":
                display_categories()
                break

            if old_name not in classes:
                print("Class does not exist.")
                continue
            
            # Get new name
            while True:
                new_name = to_title_case(input("Enter the class's new name: "))

                if not new_name:
                    print("Field cannot be empty.")

                if new_name.lower() == "q" or new_name.lower() == "quit":
                    break

                if new_name in classes:
                    print("Name already in use.")
                    continue
                
                # Save new name
                classes.insert(classes.index(old_name), new_name)
                classes.remove(old_name)
                classes = [x + "\n" for x in classes]

                with open(f"school_classes/{CATEGORIES[category]}.txt", "w") as file:
                    file.writelines(classes)

                for student in listdir("student_grades"):
                    with open(f"student_grades/{student}", "r") as file:
                        contents = load(file)
                    if old_name in contents.keys():
                        contents = change_key(contents, old_name, new_name)
                        with open(f"student_grades/{student}", "w") as file:
                            dump(contents, file)
                    else: continue
                
                print("Class renamed successfully.")
                return None


def move_class() -> None:
    """
    Moves given class from one category to another given category.
    :return: None
    :rtype: None
    """
    display_categories()

    # Get class category
    while True:
        category = to_title_case(input("Enter the category of the class to move: "))
        if category.lower() == "q" or category.lower() == "quit":
            return None
        
        if category not in CATEGORIES.keys():
            print("Category doesn't exist.")
            continue
        
        classes = get_class_from_category(CATEGORIES[category])
        print("*"*30)
        for element in classes: print(element)
        print("*"*30)
        # Get class name
        while True:
            relocate_class = to_title_case(input("Enter the class name: "))
            
            if relocate_class.lower() == "q" or relocate_class.lower() == "quit":
                display_categories()
                break

            if relocate_class not in classes:
                print("Class doesn't exist.")
                continue
            
            # Get new category
            while True:
                new_category = to_title_case(input("Enter the new category: "))

                if new_category.lower() == "q" or new_category.lower() == "quit":
                    print("*"*30)
                    for element in classes: print(element)
                    print("*"*30)
                    break

                if new_category not in CATEGORIES.keys():
                    print("Category doesn't exist.")
                    continue

                if new_category == category:
                    print("Invalid input.")
                    continue

                if relocate_class in get_class_from_category(CATEGORIES[new_category]):
                    print("The class is already in the category.")
                    continue
                
                # Remove class from old category
                contents = get_class_from_category(CATEGORIES[category])
                contents.remove(relocate_class)
                contents = [x + "\n" for x in contents]
                with open(f"school_classes/{CATEGORIES[category]}.txt", "w") as file:
                    file.writelines(contents)

                # Add class to new category
                with open(f"school_classes/{CATEGORIES[new_category]}.txt", "a", newline="") as file:
                    file.write(relocate_class + "\n")
                
                print("Class moved successfully.")
                return None


def main() -> None:
    """
    Main function for accessing other functionality for mananging classes.
    :return: None
    :rtype: None
    """
    def prompt():
        print("*"*30)
        print("1 - View classes\n" \
              "2 - Add class\n" \
              "3 - Rename class\n" \
              "4 - Change class category\n" \
              "5 - Remove class\n" \
              "6 - Exit")
        print("*"*30)
    
    prompt()

    while True:
        selection = input("Enter your selection: ")
        match selection:
            case "1":
                print()
                view_classes()
                input("PRESS ENTER TO CONTINUE ")
            case "2":
                add_class()
            case "3":
                rename_class()
            case "4":
                move_class()
            case "5":
                remove_class()
            case "6":
                return None
            case _:
                print("Invalid selection.")
                continue

        print()
        prompt()


if __name__ == "__main__":
    print("Running subjects.py")