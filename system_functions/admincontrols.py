from .utilfunctions import *

from json import dump, load
from csv import reader, writer
from random import choice
from os import listdir


def display_classes(category):
    classes = get_class_from_category(CATEGORIES[category])     

    print("="*30)
    for index, element in enumerate(classes):
        print(f"{index + 1} - {element}")
    print("="*30)

    return classes


def new_student():
    def add_hour():
        display_categories()
        # Get category for class
        while True:
            category = input("Enter the category of the class: ")

            if category.lower() == "q" or category.lower() == "quit":
                confirm = input("Are you sure you want to cancel: ")
                if confirm == "y" or confirm == "yes": return None
                else: continue

            if category not in CATEGORIES.keys():
                print("Category does not exist.")
                continue
            
            print()
            classes = get_class_from_category(CATEGORIES[category])
            print("*"*30)
            for element in classes: print(element)
            print("*"*30)
            # Get class name
            while True:
                subject = input("Enter the class name: ")

                if subject.lower() == "q" or subject.lower() == "quit":
                    display_categories()
                    break
                
                if subject not in classes:
                    print("Class does not exist.")
                    continue

                return subject
    
    # Fetch existing students
    existing_students = []
    with open("references/students.csv", "r") as file:
        _ = reader(file)
        for line in _: existing_students.append(line[:-1])
        existing_students.remove(existing_students[0])
    
    schedule = []
    grades = {}

    # Get basic student information
    while True:
        first_name = input("Enter the student's first name: ").lower().capitalize()
        if first_name.lower() == "q" or first_name.lower() == "quit": return None
        last_name = input("Enter the student's last name: ").lower().capitalize()
        if last_name.lower() == "q" or last_name.lower() == "quit": return None
        grade = input("Enter the student's grade level: ")
        if grade.lower() == "q" or grade.lower() == "quit": return None

        if [first_name, last_name] in existing_students:
            print(f"{first_name} {last_name} is already registered.")
            continue

        if not first_name or not last_name:
            print("Neither fields can be empty.")
            continue

        if grade not in ("9", "10", "11", "12"):
            print("Invalid grade entry. Must be between 9 and 12.")
            continue
        break
    
    # Create schedule
    for i in range(6):
        print(f"Enter the class the student will have for hour {i + 1}.")
        subject = add_hour()
        
        if subject is None: return None
        else: schedule.append(subject)
        
        print()
    
    # Display information
    print("="*30)
    print(f"{first_name} {last_name}")
    print(f"\tGrade {grade}")
    for index, element in enumerate(schedule):
        print(f"{index + 1}. {element}")
    print("="*30)

    # Format grades and save student information
    for element in schedule: grades.update({element:"A"})

    with open(f"student_grades/{first_name}{last_name}.json", "w") as file:
        dump(grades, file)
    
    with open("references/students.csv", "a", newline="") as file:
        _ = writer(file)
        _.writerow([first_name, last_name, grade])

    print("Student registered successfully.")

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
    with open("references/schoolbudget.txt", "r") as file: budget = float(file.read())

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
    with open("supplies/supplycosts.csv", "r") as file:
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
    with open("references/schoolbudget.txt", "w") as file:
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
            # Get year for text scores
            year = input("Enter the year: ")
            if year.lower() == "q" or year.lower() == "quit":
                return None

            # Get students who already have a score for the year
            try:
                with open(f"student_testscores/testscores{year}.csv", "r") as file:
                    _ = reader(file)
                    for line in _: existing_students.append(line[0] + line[1])
                    existing_students.remove(existing_students[0])
            except FileNotFoundError:
                print("Could not find test score entry for that year. Check if that year exists or was entered correctly.")
                continue
            else: break
        
        # Get name of student
        while True:
            student_name = input("Enter the name of the student: ")
            if student_name.lower() == "q" or student_name.lower() == "quit":
                return None
            
            if not student_name:
                print("Field cannot be empty.")
                continue

            if len(student_name.strip().split(" ")) != 2:
                print("Must include both first and last name.")
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
        
        # Get each score
        print()
        fallscore = valid_score("Enter student's Fall Score: ", 100)
        springscore = valid_score("Enter student's Spring Score: ", 100)
        satscore = valid_score("Enter the student's SAT Score: ", 1600)
        
        print()
        print(f"Score entry will be [{student_name.replace(" ", ",")},{fallscore},{springscore},{satscore}]")
        confirm = input("Is the information correct: ")

        # Save scores
        if confirm.lower() == "y" or confirm.lower() == "yes":
            with open(f"student_testscores/testscores{year}.csv", "a", newline="") as file:
                _ = writer(file)
                _.writerow([student_name[:student_name.index(" ")], student_name[student_name.index(" ") + 1:], fallscore, springscore, satscore])
            print("Score added successfully.")
            return None
        else: return None


    def add_entry():
        while True:
            existing_years = [x[-8:-4] for x in listdir("student_testscores")]
            year = input("Enter the year: ")

            if year.lower() == "q" or year.lower() == "quit":
                return None
            
            if year in existing_years:
                print("An entry already exists for that year.")
                continue

            if not year.isdigit() or len(year) != 4:
                print("Invalid input.")
                continue

            if int(year) > 2100 or int(year) < 2000:
                print("Year out of range.")
                continue

            with open(f"student_testscores/testscores{year}.csv", "w", newline="") as file:
                _ = writer(file)
                _.writerow(["FirstName","Lastname","FallScore","SpringScore","SATScore"])

            print("Entry created successfully.")
            return None


    prompt()

    while True:
        selection = input("Enter your selection: ")
        match selection:
            case "1":
                add_score()
            case "2":
                add_entry()
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
                # Get date
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
                # Confirm delete
                print("THIS WILL CLEAR ALL LOG HISTORY")
                confirm = input("Are you sure you want to clear ALL log history: ")
                if confirm.lower() == "y" or confirm.lower() == "yes":
                    with open("users.json", "r") as file:
                        contents = load(file)
                        admin_password = contents["admin"]
                    
                    # Confirm password
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


def view_students():
    # Fetch data
    contents = []
    with open("references/students.csv", "r") as file:
        _ = reader(file)
        for line in _: contents.append(line)
        contents.remove(contents[0])

    # Display data
    print()
    print("First Name   |Last Name    |Grade    \n" \
          "-------------+-------------+---------")
    for line in contents:
        print(f"{line[0]:13}|{line[1]:13}|{line[2]:>8}")

    input("PRESS ENTER TO CONTINUE ")


def approve_hours():
    requests = []
    # Fetch all requests
    with open("x_mans_files/requests/hour_requests.csv", "r") as file:
        _ = reader(file)
        for line in _: requests.append(line)
        requests.remove(requests[0])

    # Display requests
    if not requests:
        print("NO HOUR REQUESTS TO REVIEW")
        input("PRESS ENTER TO CONTINUE ")
        return None
    else:
        for index, line in enumerate(requests):
            print(f"[{index + 1}] {line[0]} {line[1]} hour(s) for {line[2]}")

    # Get request to approve
    while True:
        try:
            selection = input("Enter request number to approve: ")

            if selection.lower() == "q" or selection.lower() == "quit":
                return None

            selection = int(selection)
            if selection not in range(1, len(requests) + 1):
                print("Invalid selection")
                continue
        except ValueError:
            print("Invalid selection.")
            continue
        else: break
    # Remove approved request from requests file
    to_approve = requests[selection - 1]
    requests.remove(to_approve)
    requests.insert(0, ["Username", "HoursRequested", "MissionMonth"])
    with open("x_mans_files/requests/hour_requests.csv", "w", newline="") as file:
        _ = writer(file)
        _.writerows(requests)

    # Map username attached to request to name
    contents = []
    requestor = []
    with open("x_mans_files/x_men_list.csv", "r") as file:
        _ = reader(file)
        for line in _: contents.append(line)
        contents.remove(contents[0])
    
    for person in contents:
        if person[3] == to_approve[0]:
            requestor = person[:-1]

    # Get month entry for requestor
    month_entries = []
    mission_report = []
    with open(f"x_mans_files/mission_logs/xmans{to_approve[2]}2026.csv") as file:
        _ = reader(file)
        for line in _: month_entries.append(line)
        month_entries.remove(month_entries[0])
    
    for entry in month_entries:
        if requestor[0] == entry[0]:
            mission_report = entry
    

    # Update mission report
    hours = int(mission_report[4]) + int(to_approve[1])
    mission_count = int(mission_report[3]) + 1

    upd_mission_report = [mission_report[0], mission_report[1], mission_report[2], mission_count, hours]

    # Save updated mission report
    month_entries.insert(month_entries.index(mission_report), upd_mission_report)
    month_entries.remove(mission_report)
    month_entries.insert(0, ["FirstName","LastName","Nickname","MissionCount","HoursLogged"])
    with open(f"x_mans_files/mission_logs/xmans{to_approve[2]}2026.csv", "w", newline="") as file:
        _ = writer(file)
        _.writerows(month_entries)
    
    print("Hours updated successfully.")


    

    


if __name__ == "__main__":
    #add hour/misson logging for normal users and approval for admin panel.
    print("Running admincontrols.py")