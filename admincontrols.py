from utilfunctions import *

from json import dump, load
from csv import reader, writer
from random import choice
from os import listdir


def display_subject_categories():
    print("="*30)
    print("1 - Art & Music\n"
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
    def prompt():
        print("*"*30)
        print("1 - Add student score\n"
              "2 - Create new year entry\n"
              "3 - Exit")
        print("*"*30)


    def valid_score(prompt, max):
        while True:
            try:
                score = int(input(prompt))

                if score <= 0 or score > max:
                    print("Score out of range.")
                    continue
                else: break

            except ValueError:
                print("Invalid input.")
                continue
        return score            


    def add_score():
        students = [x[:-5] for x in listdir("student_grades")]
        existing_students = []

        while True:
            year = input("Enter the year: ")
            if year.lower() == "q" or year.lower() == "quit":
                return None

            try:
                with open(f"student_testscores/testscores{year}.csv", "r") as file:
                    _ = reader(file)
                    for line in _: existing_students.append(line[0] + line[1])
                    existing_students.remove(existing_students[0])
            except FileNotFoundError:
                print("Could not find test score entry for that year. Check if that year exists or was entered correctly.")
                continue
            else: break
        
        while True:
            student_name = input("Enter the name of the student: ")
            if student_name.lower() == "q" or student_name.lower() == "quit":
                return None
            
            if not student_name:
                print("Field cannot be empty.")
                continue

            student_name = to_title_case(student_name)
            try:
                compare = student_name[:student_name.index(" ")] + student_name[student_name.index(" ") + 1:]
            except ValueError:
                print("Student does not exist. Check if name was spelled correctly.")
                continue
            if compare not in students:
                print("Student does not exist. Check if name was spelled correctly.")
                continue
            if compare in existing_students:
                print("Student already has a test score entry.")
                continue
            break

        print()
        fallscore = valid_score("Enter student's Fall Score: ", 100)
        springscore = valid_score("Enter student's Spring Score: ", 100)
        satscore = valid_score("Enter the student's SAT Score: ", 1600)
        
        print()
        print(f"Score entry will be [{student_name.replace(" ", ",")},{fallscore},{springscore},{satscore}]")

        confirm = input("Is the information correct: ")
        if confirm.lower() == "y" or confirm.lower() == "yes":
            with open(f"student_testscores/testscores{year}.csv", "a", newline="") as file:
                _ = writer(file)
                _.writerow([student_name[:student_name.index(" ")], student_name[student_name.index(" ") + 1:], fallscore, springscore, satscore])
            print("Score added successfully.")
            return None
        else: return None


    prompt()

    while True:
        selection = input("Enter your selection: ")
        match selection:
            case "1":
                add_score()
            case "2":
                pass
            case "3":
                return None
            case _:
                print("Invalid selection.")
                continue
        print()
        prompt()


def userlog():
    def prompt():
        print("*"*30)
        print("1 - View user log\n"
              "2 - View log by day\n"
              "3 - Clear user log\n"
              "4 - Exit")
        print("*"*30)

    def fetch_data():
        with open("userlog.txt", "r") as file:
            contents = file.readlines()
            contents = [x[:-1] for x in contents]
            
        return contents
    
    def display_logs(log_data):
        if not log_data:
            print("NO LOGS TO DISPLAY")
            return None
        
        for index, line in enumerate(log_data):
            print(f"[{index + 1}] {line}")
        input("PRESS ENTER TO CONTINUE ")
        return None
    
    prompt()
    
    while True:
        selection = input("Enter your selection: ")

        match selection:
            case "1":
                print()
                display_logs(fetch_data())
            case "2":
                logs = fetch_data()
                while True:
                    date = input("Enter the date (m/d): ")
                    if date.lower() == "q" or date.lower() == "quit": break
                    try:
                        day = date[date.index("/") + 1:]
                        month = date[:date.index("/")]
                    except ValueError:
                        print("Invalid input.")
                        continue
                    if not day.isdigit() or not month.isdigit():
                        print("Invalid input.")
                        continue
                    if int(day) > 31 or int(month) > 12 or int(day) <= 0 or int(month) <= 0:
                        print("Invalid input.")
                        continue
                
                    logs = list(filter(lambda x: f"{month:>02}/{day:>02}/" in x, logs))

                    print()
                    display_logs(logs)
                    break
            case "3":
                print("THIS WILL CLEAR ALL LOG HISTORY")
                confirm = input("Are you sure you want to clear ALL log history: ")
                if confirm.lower() == "y" or confirm.lower() == "yes":
                    with open("users.json", "r") as file:
                        contents = load(file)
                        admin_password = contents["admin"]
                    
                    password = input("Enter admin password to proceed: ")

                    if password != admin_password:
                        print("Incorrect password.")
                    else:
                        with open("userlog.txt", "w") as file:
                            file.write("")
                        
                        print()
                        print("User log has been cleared.")
                        input("PRESS ENTER TO CONTINUE ")
            case "4":
                return None
            case _:
                print("Invalid selection.")
                continue

        print()
        prompt()


if __name__ == "__main__":
    print("Running admincontrols.py")