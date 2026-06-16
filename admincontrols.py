from utilfunctions import *

from json import dump, load
from csv import reader, writer
from random import choice
from os import listdir


def display_subject_categories():
    print("="*30)
    print("1 - Art/Music\n"
          "2 - Computer Science\n"
          "3 - Electives\n"
          "4 - History\n"
          "5 - World Languages\n"
          "6 - Math\n"
          "7 - Reading\n"
          "8 - Sciences")
    print("="*30)


def display_classes(category):
    classes = get_class_from_category(category)     

    print("="*30)
    for index, element in enumerate(classes):
        print(f"{index + 1} - {element}")
    print("="*30)

    return classes


def get_class_from_category(category):
    with open(f"school_classes/{category}.txt", "r") as file:
        classes = file.readlines()
    classes = [x[:-1] for x in classes]

    return classes


def create_student():
    existing_names = [x[:-5] for x in listdir("student_grades")]
    schedule = []
    grades = {}

    # Get student name
    while True:
        first_name = input("Enter student's first name: ").strip().lower().capitalize()
        last_name = input("Enter student's last name: ").strip().lower().capitalize()

        if (first_name + last_name) in existing_names:
            print(f"Student {first_name} {last_name} is already registered in system.")
            continue

        if first_name.lower() == "q" or last_name.lower() == "quit":
            return None

        if not first_name or not last_name:
            print("Neither fields can be empty.")
            continue
        else: break
    
    print()

    for i in range(6):
        # Get category of student's class i
        print(f"Please enter student's information for Hour {i+1}.")
        while True:
            display_subject_categories()

            category = input("Enter category of class the student will take: ")
            match category:
                case "1": file_path = "artmusic"
                case "2": file_path = "compscience"
                case "3": file_path = "elective"
                case "4": file_path = "history"
                case "5": file_path = "language"
                case "6": file_path = "math"
                case "7": file_path = "reading"
                case "8": file_path = "sciences"
                case "q" | "quit": return None
                case _:
                    print("Invalid selection.")
                    continue
            

            # Fetch classes belonging to class category
            classes = display_classes(file_path)

            # Get class student will take from category
            hour = input("Enter the class the student will be taking: ")
                
            if hour.lower() == "q" or hour.lower() == "quit":
                continue
                
            if hour not in classes:
                print("Invalid selection.")
                continue
            else:
                schedule.append(hour)
                print()
                break

    # Save classes and grades into new .json file
    for i in range(len(schedule)):
        grades.update({schedule[i]:"A"})

    with open(f"student_grades/{first_name}{last_name}.json", "w") as file:
        dump(grades, file)
        print("Student created successfully.")
    
    return None


def create_user():
    # Fetch existing user data
    try:
        with open("users.json", "r") as file:
            contents = load(file)
    except FileNotFoundError:
        print("User data file could not be found.")
        exit(1)
    except Exception:
        print("An unknown error occurred.")
        exit(1)


    characters = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
    password = ""

    # Get new user's username
    while True:
        username = input("Enter new user's username: ")
        if not username:
            print("Username field cannot be blank.")
        elif username in contents.keys():
            print(f"User {username} already exists.")
        else: break

    # Create random password
    for _ in range(4):
        password += choice(characters)
    print(f"User's password is:  {password}")


    # Save new username and password
    contents.update({username:password})
    try:
        with open("users.json", "w") as file:
            dump(contents, file)
    except FileNotFoundError:
        print("The user data file could not be found.")
        exit(1)
    except Exception:
        print("An unknown error occurred.")
        exit(1)
    else:
        print(f"User {username} created successfully.")
    return None


def subjects_mananger():
    #add/edit/remove/view classes but then also have to check if any student has the deleted class and reassign them omg
    def prompt():
        print("*"*30)
        print("1 - View classes\n" \
              "2 - Add class\n" \
              "3 - Edit class\n" \
              "4 - Remove class\n" \
              "5 - Exit")
        print("*"*30)

    def register_class(category, class_name):
        with open(f"school_classes/{category}.txt", "a") as file:
            file.write(class_name + "\n")
    

    categories = ("Art/Music", "Computer Science", "Electives", "History", "World Language", "Math", "Reading", "Sciences")
    file_paths = ("artmusic", "compscience", "elective", "history", "language", "math", "reading", "sciences")

    prompt()

    while True:
        selection = input("Enter your selection: ")
        match selection:
            case "1":
                # Display all classes by categories
                print()
                for i in range(len(categories)):
                    print(f"{categories[i].upper()} - ")
                    classes = get_class_from_category(file_paths[i])
                    for element in classes:
                        print(f"\t- {element}")  
                input("PRESS ENTER TO CONTINUE ")  
            case "2":
                # Get category to put class in
                print("*"*30)
                for element in categories: print(element)
                print("*"*30)
                while True:
                    new_class_category = input("Enter the category the class will be put in: ")
                    if new_class_category.lower() == "q" or new_class_category.lower() == "quit": break
                    if new_class_category not in categories:
                        print("Invalid selection.")
                        continue
                    
                    classes = get_class_from_category(file_paths[categories.index(new_class_category)])
                    # Enter name of new class
                    while True:   
                        new_class = input("Enter the new class: ")
                        if new_class == "q" or new_class == "quit": break
                        if new_class in classes:
                            print(f"{to_title_case(new_class)} already exists.")
                            continue
                        if not new_class:
                            print("Class name cannot be empty.")
                            continue
                        
                        # Format and save new class
                        new_class = to_title_case(new_class)
                        register_class(file_paths[categories.index(new_class_category)], new_class)
                        break
                    break
            case "3":
                # Get category of class to be changed
                print("*"*30)
                for element in categories: print(element)
                print("*"*30)
                while True:
                    class_category = input("Enter the category of the class to edit: ")
                    if class_category == "q" or class_category == "quit": break
                    if class_category not in categories:
                        print("Invalid selection.")
                        continue
                    
                    # Get class to change
                    while True:
                        classes = get_class_from_category(file_paths[categories.index(class_category)])
                        print("*"*30)
                        for element in classes: print(element)
                        print("*"*30)

                        edit_class = input("Enter the class to edit: ")
                        if edit_class == "q" or edit_class == "quit": break
                        if edit_class not in classes:
                            print("Invalid selection.")
                            continue
                        else:
                            # Change class
                            class_editor(class_category, edit_class)
                            break
                    break
            case "4":
                print("*"*30)
                for element in categories: print(element)
                print("*"*30)
                while True:
                    remove_category = input("Enter the category of the class to remove: ")
                    if remove_category.lower() == "q" or remove_category.lower() == "quit":
                        break
                    if remove_category not in categories:
                        print("Invalid selection.")
                        continue

                    classes = get_class_from_category(file_paths[categories.index(remove_category)])

                    print("*"*30)
                    for element in classes: print(element)
                    print("*"*30)

                    remove_class = input("Enter class to remove: ")
                    if remove_class.lower() == "q" or remove_class.lower() == "quit":
                        break
                    if remove_class not in classes:
                        print("Invalid selection.")
                        continue
                    else:
                        classes.remove(remove_class)
                        classes = [x + "\n" for x in classes]
                        with open(f"school_classes/{file_paths[categories.index(remove_category)]}.txt", "w") as file:
                            file.writelines(classes)
                        break
            case "5":
                return None
            case _:
                print("Invalid selection.")
                continue
        print()
        prompt()


def class_editor(category, edit_class):
    def prompt():
        print("*"*30)
        print("1 - Rename class\n" \
              "2 - Move class to different category\n" \
              "3 - Exit")
        print("*"*30)
    
    categories = ("Art/Music", "Computer Science", "Electives", "History", "World Language", "Math", "Reading", "Sciences")
    file_paths = ("artmusic", "compscience", "elective", "history", "language", "math", "reading", "sciences")
    classes = get_class_from_category(file_paths[categories.index(category)])

    prompt()
    while True:
        selection = input("Enter your selection: ")
        match selection:
            case "1":
                # Get new name of class
                while True:
                    new_name = input(f"Enter the new name of {edit_class}: ")
                    if new_name.lower() == "q" or new_name.lower() == "quit": break
                    if new_name in classes:
                        print(f"{to_title_case(new_name)} already exists.")
                        continue
                    if not new_name:
                        print("Class name cannot be empty.")
                        continue
                    else:
                        # Update classes file with new name
                        classes.insert(classes.index(edit_class), new_name)
                        classes.remove(edit_class)

                        classes = [x + "\n" for x in classes]

                        with open(f"school_classes/{file_paths[categories.index(category)]}.txt", "w") as file:
                            file.writelines(classes)

                        # Update schedule for any students with updated class name
                        for student in listdir("student_grades"):
                            with open(f"student_grades/{student}", "r") as file:
                                contents = load(file)
                            
                            if edit_class in contents.keys():
                                contents = change_key(contents, edit_class, new_name)
                                with open(f"student_grades/{student}", "w") as file:
                                    dump(contents, file)
                        print("Class updated successfully.")
                        break
            case "2":
                print("*"*30)
                for element in categories: print(element)
                print("*"*30)
                while True:
                    # Get new category for class
                    new_category = input(f"Enter the new location for {edit_class}: ")
                    if new_category.lower() == "q" or new_category.lower() == "quit":
                        break
                    if new_category not in categories:
                        print("Invalid selection.")
                        continue

                    # Remove class from old category
                    with open(f"school_classes/{file_paths[categories.index(category)]}.txt", "r") as file:
                        contents = file.readlines()
                        contents.remove(edit_class + "\n")
                    with open(f"school_classes/{file_paths[categories.index(category)]}.txt", "w") as file:
                        file.writelines(contents)

                    # Add class to new category
                    with open(f"school_classes/{file_paths[categories.index(new_category)]}.txt", "a") as file:
                        file.writelines(edit_class + "\n")
                    
                    category = new_category
                    break
            case "3":
                return None
            case _:
                print("Invalid selection.")
                continue
        print()
        prompt()


def approve_supply_requests():
    requests = []
    items = []
    costs = []
    with open("schoolbudget.txt", "r") as file: budget = float(file.read())

    # Display current budget
    print(f"The current school budget is: ${budget:,.2f}")
    input("PRESS ENTER TO CONTINUE ")
    print()
    
    # Fetch and display all requests
    with open("supplies/supplyrequests.csv", "r") as file:
        _ = reader(file)
        requests = [x for x in _]
        requests = list(enumerate(requests[1:]))

    print("   |Username       |Supply              |Quantity")
    print("---+---------------+--------------------+-----------")
    for index, line in requests: 
        print(f"{index + 1:3}|{line[0]:15}|{line[1]:20}|{line[2]:>11}")

    # Get valid request to approve
    while True:
        try:
            approve = input("Enter the request number to approve: ")

            if approve.lower() == "q" or approve.lower() == "quit":
                return None
            
            approve = int(approve)

            if approve <= 0 or approve > len(requests):
                print("Invalid input.")
                continue
            else:
                request = requests[approve - 1][1]
                print(f"The request is: {request[2]} {request[1]} from {request[0]}.")
                confirm = input("Are you sure you want to approve the supply request: ")
                if confirm.lower() == "y" or confirm.lower() == "yes":
                    break
                else: continue
        except ValueError:
            print("Invalid input.")
            continue

    # Get list of items and their costs
    with open("supplycosts.csv", "r") as file:
        _ = reader(file)
        for line in _: 
            items.append(line[0])
            costs.append(line[1])
        items.remove(items[0])
        costs.remove(costs[0])

    # Get price of the order
    if request[1] in items:
        order_cost = float(costs[items.index(request[1])])
        order_cost *= int(request[2])
    else:
        print("Request is custom made. Price could not be found.")
        while True:
            try:
                order_cost = float(input("Enter the cost of the order: "))
            except ValueError:
                print("Invalid input")
                continue
            else: break
    
    # Bankruptcy check
    budget -= order_cost
    if budget < 0:
        print("Insufficient funds to complete the order. Cancelling approval...")
        return None

    print()
    print(f"The cost of the order will be: {order_cost:,.2f}")
    print(f"The remaining money in budget is {budget}")

    # Update budget
    with open("schoolbudget.txt", "w") as file:
        file.write(f"{budget:.2f}")
    
    # Update requests
    requests = [x[1] for x in requests]
    requests.remove(request)
    with open("supplies/supplyrequests.csv", "w", newline="") as file:
        _ = writer(file)
        _.writerow(["Username", "Supply", "Quantity"])
        _.writerows(requests)
    
    # Add order to orders file
    request.append(f"{order_cost:.2f}")
    with open("supplies/supplyorders.csv", "a", newline="") as file:
        _ = writer(file)
        _.writerow(request)

    print("\nOrder placed successfully.")
    return None


def add_test_scores():
    #add test scores or something
    pass


if __name__ == "__main__":
    print("Running admincontrols.py")
else:
    print("\nAdmin functions loaded successfully.\n" + "~"*35)