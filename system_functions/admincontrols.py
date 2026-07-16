"""
    File containing functionality for admin panel.
    Only availible for admin user.
"""

from .utilfunctions import *

from random import randint


def unicast_notif(recipient:str, message:str) -> None:
    """
    Adds message to notification value of user's JSON object.
    :param recipient: Username of user to recieve message.
    :type recipient: str
    :param message: Message to send to recipient.
    :type message: str
    :return: None
    :rtype: None
    """
    with open(f"x_mans_files/profiles/{recipient}.json", "r") as file:
        data = load(file)
    data["Notifications"].append(message)
    with open(f"x_mans_files/profiles/{recipient}.json", "w") as file:
        dump(data, file)


def new_student() -> None:
    """
    Gets name, grade, and schedule for student and adds it to proper files and directories.
    :return: None
    :rtype: None
    """
    def add_hour():
        """
        Gets one valid subject from category.
        :return: Single existing subject for student.
        :rtype: str, None if cancel.
        """
        display_categories()
        # Get category for class
        while True:
            category = to_title_case(input("Enter the category of the class: "))

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
                subject = to_title_case(input("Enter the class name: "))

                if subject.lower() == "q" or subject.lower() == "quit":
                    display_categories()
                    break
                
                if subject not in classes:
                    print("Class does not exist.")
                    continue

                if subject in schedule:
                    print("Student already has this class.")
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


def new_user() -> None:
    """
    Gets information of user and adds it to proper files and directories.
    :return: None
    :rtype: None
    """
    # Getch existing user data
    with open("references/users.json", "r") as file:
        contents = load(file)
    existing_users = contents.keys()

    # Get username
    while True:
        new_username = input("Enter the username: ")
        if new_username.lower() == "q" or new_username.lower() == "quit":
            return None

        if not new_username:
            print("Field cannot be empty.")
            continue

        if new_username in existing_users:
            print("Username already in use.")
            continue

        if len(new_username) < 3:
            print("Username must be at least 4 characters.")
            continue
        break

    # Get names
    while True:
        first_name = input("Enter the user's first name: ").capitalize()
        if first_name.lower() == "q" or first_name.lower() == "quit": return None
        last_name = input("Enter the user's last name: ").capitalize()
        if last_name.lower() == "q" or last_name.lower() == "quit": return None
        nick_name = input("Enter the user's nickname: ")
        if nick_name.lower() == "q" or nick_name.lower() == "quit": return None

        if not first_name or not last_name or not nick_name:
            print("All fields must be filled out.")
            continue
        break

    # Save to x-mans list
    nick_name = to_title_case(nick_name)
    with open("x_mans_files/x_men_list.csv", "a", newline="") as file:
        _ = writer(file)
        _.writerow([first_name, last_name, nick_name, new_username])
    
    # Generate password
    password = ""
    for _ in range(4):
        password += str(randint(0,9))
    
    with open("x_mans_files/profiles/admin.json", "r") as file:
        admin_data = load(file)
        admin_data["Notifications"].append(f"{nick_name}'s password is {password}.")
    with open("x_mans_files/profiles/admin.json", "w") as file:
        dump(admin_data, file)
    
    # Save username and password
    load_dotenv()
    key = getenv("KEY").split(",")
    password = encrypt(password, key)
    contents.update({new_username:password})
    with open("references/users.json", "w") as file:
        dump(contents, file)

    # Add user to existing mission logs
    for path in listdir("x_mans_files/mission_logs"):
        for file in listdir(f"x_mans_files/mission_logs/{path}"):
            with open(f"x_mans_files/mission_logs/{path}/{file}", "a", newline="") as file:
                _ = writer(file)
                _.writerow([first_name, last_name, nick_name, 0, 0])

    # Add profile file
    with open(f"x_mans_files/profiles/{new_username}.json", "w") as file:
        dump({"Username": new_username, "First Name": first_name, "Last Name": last_name,
              "Nickname": nick_name, "Monthly Hours": "", "Monthly Mission Count": "",
              "All Time Hours": 0, "All Time Missions": 0, "Notifications": ["Welcome to The System."]}, file)
    
    print("User created successfully.")


def approve_supply_requests() -> None:
    """
    Moves approved request to orders file.
    :return: None
    :rtype: None
    """
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

    unicast_notif(request[0], f"Your request for {request[2]} {request[1]} was approved.")

    print("\nOrder placed successfully.")
    return None


def add_test_scores() -> None:
    """
    Adds valid testscores for student or year.
    :return: None
    :rtype: None
    """
    def prompt() -> None:
        """
        Displays action options for user.
        :return: None
        :rtype: None
        """
        print("*"*30)
        print("1 - Add student score\n"
              "2 - Create new year entry\n"
              "3 - Exit")
        print("*"*30)


    def valid_score(prompt: str, max:int) -> int:
        """
        Get valid input from user within specified range.
        :param prompt: Input prompt for user.
        :type prompt: str
        :param max: Maximum value user is allowed to enter inside function.
        :type max: int
        :return: Valid score within range.
        :rtype: int
        """
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


    def add_score() -> None:
        """
        Add single yearly entry for one student with test scores.
        :return: None
        :rtype: None
        """
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


    def add_entry() -> None:
        """
        Create new file for new year entry of test scores.
        :return: None
        :rtype: None
        """
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


def userlog() -> None:
    """
    Allows viewing userlog and clearing it from terminal.
    :return: None
    :rtype: None
    """
    def prompt() -> None:
        """
        Displays action options for user.
        :return: None
        :rtype: None
        """
        print("*"*30)
        print("1 - View user log\n"
              "2 - View log by date\n"
              "3 - Clear user log\n"
              "4 - Exit")
        print("*"*30)


    def fetch_data() -> list[str]:
        """
        Read data from userlog.txt and return list of each line.
        :return: List where each element is a line/entry in userlog.
        :rtype: list[str]
        """
        with open("userlog.txt", "r") as file:
            contents = file.readlines()
            contents = [x[:-1] for x in contents]
            
        return contents

    
    def display_logs(log_data) -> None:
        """
        Displays message if log data is empty. If not, displays data by each formatted line.
        :return: None
        :rtype: None
        """
        if not log_data:
            print("NO LOGS TO DISPLAY")
        
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
                    date = input("Enter the date (m/d/y): ")
                    if date.lower() == "q" or date.lower() == "quit": break
                    try:
                        month, day, year = date.split("/")
                    except ValueError:
                        print("Invalid input.")
                        continue
                    if not day.isdigit() or not month.isdigit() or not year.isdigit():
                        print("Invalid input.")
                        continue
                    if int(day) > 31 or int(month) > 12 or int(day) <= 0 or int(month) <= 0 or len(year) != 4:
                        print("Invalid input.")
                        continue
                
                    logs = list(filter(lambda x: f"{month:>02}/{day:>02}/{year}" in x, logs))

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


def view_students() -> None:
    """
    Reads and displays table data from students.csv.
    :return: None
    :rtype: None
    """
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


def approve_hours() -> None:
    """
    Approve request and update hour and mission amounts in correct files.
    :return: None
    :rtype: None
    """
    # Get all requests
    requests = []
    with open("x_mans_files/hour_requests.csv", "r") as file:
        _ = reader(file)
        for line in _: requests.append(line)
        requests.remove(requests[0])

    for index, line in enumerate(requests):
        print(f"[{index + 1}] {(line[0] + ":"):15} {line[1]:2} hour(s) for {line[2]}, {line[3]}")
    
    # Get request to approve
    tmp = range(1, len(requests) + 1)
    while True:
        try:
            to_approve = input("Enter request number to approve: ")

            if to_approve.lower() == "q" or to_approve.lower() == "quit":
                return None
            
            if int(to_approve) not in tmp:
                print("Request number out of range.")
                continue
        except ValueError:
            print("Invalid input.")
            continue
        else: break

    to_approve = requests[int(to_approve) - 1]
    del tmp

    # Remove request from requests list
    requests.remove(to_approve)
    requests.insert(0, ["Username", "HoursRequested", "MissionMonth", "MissionYear"])
    with open("x_mans_files/hour_requests.csv", "w", newline="") as file:
        _ = writer(file)
        _.writerows(requests)
    
    # Update requestor's profile
    with open(f"x_mans_files/profiles/{to_approve[0]}.json", "r") as file:
        profile_data = load(file)
    profile_data.update({"All Time Hours": profile_data["All Time Hours"] + int(to_approve[1])})
    profile_data.update({"All Time Missions": profile_data["All Time Missions"] + 1})
    with open(f"x_mans_files/profiles/{to_approve[0]}.json", "w") as file:
        dump(profile_data, file)
        
    # Update monthly entry for requestor
    all_entries = []
    with open(f"x_mans_files/mission_logs/{to_approve[3]}logs/xmans{to_approve[2]}{to_approve[3]}.csv", "r") as file:
        _ = reader(file)
        for line in _: all_entries.append(line)
        all_entries.remove(all_entries[0])
    
    for line in all_entries:
        if line[2] == profile_data["Nickname"]:
            line[3] = str(int(line[3]) + 1)
            line[4] = str(int(line[4]) + int(to_approve[1]))
    
    all_entries.insert(0, ["FirstName", "LastName", "Nickname", "MissionCount", "HoursLogged"])
    with open(f"x_mans_files/mission_logs/{to_approve[3]}logs/xmans{to_approve[2]}{to_approve[3]}.csv", "w", newline="") as file:
        _ = writer(file)
        _.writerows(all_entries)

    unicast_notif(profile_data["Username"], f"Your request for {to_approve[1]} hours was approved.")
    
    print("Hours updated successfully.")


def new_month() -> None:
    """
    Creates new file for month if current month doesn't already have a file.
    :return: None
    :rtype: None
    """
    # Find current month and year
    MONTHS = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
    current_month = datetime.today().month
    current_month = MONTHS[current_month]
    current_year = datetime.today().year

    if f"xmans{current_month}{current_year}.csv" in listdir(f"x_mans_files/mission_logs/{current_year}logs"):
        print("Entry already exists for this month.")
        return None
    
    # Fetch x_mans data
    x_men = []
    with open("x_mans_files/x_men_list.csv", "r") as file:
        _ = reader(file)
        for line in _: x_men.append([line[0], line[1], line[2], 0, 0])
        x_men.remove(x_men[0])

    # Create month entry
    with open(f"x_mans_files/mission_logs/{current_year}logs/xmans{current_month}{current_year}.csv", "w", newline="") as file:
        _ = writer(file)
        x_men.insert(0, ["FirstName", "LastName", "Nickname", "MissionCount", "HoursLogged"])
        _.writerows(x_men)

    print("Entry created successfully.")
    input("PRESS ENTER TO CONTINUE ")


def send_notif() -> None:
    """
    Allows for sending broadcast or unicast messages to different users.
    :return: None
    :rtype: None
    """
    def prompt() -> None:
        """
        Displays action options for user.
        :return: None
        :rtype: None
        """
        print("*"*30)
        print("1 - Unicast\n" \
              "2 - Broadcast\n" \
              "3 - Exit")
        print("*"*30)
    
    
    def unicast() -> None:
        """
        Sends message to single profile given by user.
        :return: None
        :rtype: None
        """
        users = [x[:-5] for x in listdir("x_mans_files/profiles")]
        
        while True:
            recipient = input("Enter user to notify: ")

            if recipient.lower() == "q" or recipient.lower() == "quit":
                return None

            if recipient not in users:
                print("User does not exist.")
                continue

            print()
            while True:
                message = input("Enter message for notification: ")

                if message.lower() == "q" or message.lower() == "quit":
                    print()
                    break
                
                if not message:
                    print("Field cannot be empty.")
                    continue

                unicast_notif(recipient, message)

                print("User notified successfully.")
                return None


    def broadcast() -> None:
        """
        Sends message to all existing users.
        :return: None
        :rtype: None
        """
        while True:
            message = input("Enter message for notification: ")
            
            if message.lower() == "q" or message.lower() == "quit":
                return None
            
            if not message:
                print("Field cannot be empty.")
                continue
            break
            
        for profile in listdir("x_mans_files/profiles")[:4]:
            with open(f"x_mans_files/profiles/{profile}", "r") as file:
                data = load(file)
                if data["Username"] == "admin": continue
                data["Notifications"].append(message)
            
            with open(f"x_mans_files/profiles/{profile}", "w") as file:
                dump(data, file)
        
        print("All X-Mans notified successfully.")

    prompt()
    while True:
        selection = input("Enter your selection: ")
        match selection.lower():
            case "1":
                unicast()
            case "2":
                broadcast()
            case "3":
                return None
            case _:
                print("Invalid selection.")
                continue
        print()
        prompt()


if __name__ == "__main__":
    print("Running admincontrols.py")