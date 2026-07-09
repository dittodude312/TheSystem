"""
    File containing functionality for start menu.
    Availible to all users.
"""

from .utilfunctions import to_title_case, encrypt, decrypt

from dotenv import load_dotenv
from json import load, dump
from csv import reader, writer
from os import listdir, getenv


def grades() -> None:
    """
    Displays the grades for a student and allows for changing grades.
    :return: None
    :rtype: None
    """
    def prompt() -> None:
        """
        Displays action options for user.
        :return: None
        :rtype: None
        """
        print(student + " " + "*"*(30 - len(student) - 1))
        for subject, grade in contents.items():
            print(f"{subject:20}---{grade:>5}")
        print("*"*30)
        
        print("1 - Change Grade\n" \
              "2 - Exit")


    def change_grade() -> None:
        """
        Changes the grade of a class the student takes.
        :return: None
        :rtype: None
        """
        # Get grade and subject
        print()
        while True:
            subject = to_title_case(input("Enter class to change grade: "))

            if subject.lower() == "q" or subject.lower() == "quit":
                return None 
            
            if subject not in contents.keys():
                print("Student doesn't take this class.")
                continue
            break
        
        print()
        while True:
            new_grade = input("Enter new grade: ").upper()

            if new_grade.lower() == "q" or new_grade.lower() == "quit":
                return None
            
            if new_grade not in ("A", "B", "C", "D", "E", "F"):
                print("Invalid input.")
                continue
            break

        # Update grades
        contents.update({subject:new_grade})
        
        with open(f"student_grades/{file_name}.json", "w") as file:
            dump(contents, file)

        return None

    # Get student name
    while True:
        student = input("Enter student name: ")
        if student.lower() == "q" or student.lower() == "quit": return None
        student = student[:student.find(" ")].capitalize() + " " + student[student.find(" ") + 1:].capitalize()
        file_name = student[:student.find(" ")] + student[student.find(" ") + 1:]

    # Fetch grades
        try:
            with open(f"student_grades/{file_name}.json", "r") as file:
                contents = load(file)
        except FileNotFoundError:
            print("Grades could not be found. Check if student name was typed correctly. If so, contact admin if issue persists.")
            continue
        except Exception:
            print("An unknown error occurred. Contact admin if issue persists.")
            continue
        else: break
            

    # Change grade prompt
    prompt()

    while True:
        selection = input("Enter your selection: ")
        match selection:
            case "1":
                change_grade()
                print()
                prompt()
            case "2":
                return None
            case _:
                print("Invalid input.")


def test_scores() -> None:
    """
    Allows for viewing different test scores for a specified year.
    :return: None
    :rtype: None
    """
    def view_score(index:int) -> None:
        """
        Displays different test scores from a year depending on index.
        :param index: Index of 2-d list to get scores.
        :type index: int
        :return: None
        :rtype: None
        """
        values = []
        print(year + " " + "*"*25)
        for line in contents:
            print(f"{(line[1] + ", " + line[0]):25}---  {line[index]:>4}")
            values.append(int(line[index]))
        print(f"Average Score Across School: {(sum(values)/len(values)):.2f}")
        print("*"*30)
        input("PRESS ENTER TO CONTINUE ")

    contents = []

    # Fetch scores
    while True:
        year = input("Enter school year to view scores: ")
        if year.lower() == "q" or year.lower() == "quit": return None
        try:
            with open(f"student_testscores/testscores{year}.csv") as file:
                _ = reader(file)
                for line in _: contents.append(line)
                contents.remove(contents[0])
                del _
        except FileNotFoundError:
            print("Test scores could not be found. Check if the year was entered correctly. If so, contact admin if issue persists.")
            continue
        except Exception:
            print("An unknown error occurred. Contact admin if issue persists.")
        else: break
    
    # View score category
    while True:
        print()
        print("*"*30)
        print("1 - Fall Standardized Testing Scores\n" \
              "2 - Spring Standardized Testing Scores\n" \
              "3 - SAT Scores\n" \
              "4 - Exit")
        print("*"*30)
        
        selection = input("Enter your selection: ")
        match selection:
            case "1":
                view_score(2)
            case "2":
                view_score(3)
            case "3":
                view_score(4)
            case "4":
                return None
            case _:
                print("Invalid selection.")
                continue


def x_mans() -> None:
    """
    Allows for viewing different information about X-Mans.
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
        print("1 - View mission logs\n" \
              "2 - View X-Mans\n" \
              "3 - Exit")
        print("*"*30)
    
    
    def fetch_x_mans() -> list[str]:
        """
        Gets list of X-Mans from x_men_list.csv file.
        :return: Contents of x_men_list.csv file.
        :rtype: list[str]
        """
        contents = []
        with open("x_mans_files/x_men_list.csv", "r") as file:
            _ = reader(file)
            for line in _: contents.append(line)
            contents.remove(contents[0])
        return contents


    def view_mission_logs() -> None:
        """
        Displays logs for specified month from user.
        :return: None
        :rtype: None
        """
        contents = []

        # Fetch log data
        while True:
            try:
                year = input("Enter the year to view X-Mans logs: ")
                if year.lower() == "q" or year.lower() == "quit": return None
                month = input("Enter the month to view X-Mans logs: ")
                if month.lower() == "q" or month.lower() == "quit": return None
                with open(f"x_mans_files/mission_logs/{year}logs/xmans{month}{year}.csv") as file:
                    _ = reader(file)
                    for line in _: contents.append(line)
                    contents.remove(contents[0])
                    del _
            except FileNotFoundError:
                print("Files could not be found. Check if month and year were entered correctly. If so, contact admin if issue persists.")
                continue
            except Exception:
                print("An unknown error occurred.")
                continue
            else: break

        # Display data
        print(year + " - " + month.upper() + " " + "-"*25 + "|Missions  |Hours")
        for line in contents:
            print(f"{(line[1] + ", " + line[0] + " (" + line[2] + ")"):35} | {line[3]:>8} | {line[4]:>6}")
        print("-"*55)
        input("PRESS ENTER TO CONTINUE ")

    
    def view_x_mans() -> None:
        """
        Displays X-Mans in formatted table.
        :return: None
        :rtype: None
        """
        contents = fetch_x_mans()

        print("First Name     |Last Name      |Nickname        ")
        print("---------------+---------------+----------------")
        for line in contents:
            print(f"{line[0]:15}|{line[1]:15}|{line[2]:15}")
        
        input("PRESS ENTER TO CONTINUE ")
        

    prompt()

    while True:
        selection = input("Enter your selection: ")
        match selection:
            case "1":
                print()
                view_mission_logs()
            case "2":
                print()
                view_x_mans()
            case "3":
                return None
            case _:
                print("Invalid selection.")
                continue
        print()
        prompt()


def supplies(username:str) -> None:
    """
    Allows viewing supply inventory and requesting supplies.
    :return: None
    :rtype: None
    """
    def order_supplies() -> None:
        """
        Gets requests from user and writes it to supplyrequests.csv file.
        :return: None
        :rtype: None
        """
        # Get supply options
        supply_options = []
        with open("supplies/supplycosts.csv", "r") as file:
            _ = reader(file)
            for line in _: supply_options.append(line[0])
            supply_options.remove(supply_options[0])

        # Get supply name
        print("-"*15)
        print("What supplies do you want to request?")
        for item in supply_options: print(f"- {item}")
        print("-"*15)
        while True:
            supply = input("Enter your desired supply: ").capitalize()

            if supply.lower() == "q" or supply.lower() == "quit":
                return None

            if supply == "Other":
                supply = to_title_case(input("Enter other supply name: "))

                if supply.lower() == "q" or supply.lower() == "quit": 
                    print()
                    continue

                if not supply:
                    print("Field cannot be empty.")
                    print()
                    continue
                break

            if supply not in supply_options:
                print("Supply could not be found.")
                continue
            break
        
        # Get supply quantity
        print()
        while True:
            try:
                quantity = input("Enter the quantity of the supply: ")
                if quantity.lower() == "q" or quantity.lower() == "quit":
                    return None
                
                quantity = int(quantity)

                if quantity <= 0:
                    print("Quantity must be larger than 0.")
                    continue
            except ValueError:
                print("Invalid input.")
            else: break
        
        #Write data
        write_request(supply, username, quantity)
        return None

    
    def write_request(supply_name:str, requestor:str, supply_quantity:int) -> None:
        """
        Saves request to supplyrequests.csv file.
        :param supply_name: Name of supply to request.
        :type supply_name: str
        :param requestor: Username of user saving request.
        :type requestor: str
        :param supply_quantity: Quantity of supply_name to order.
        :type supply_quantity: int
        :return: None
        :rtype: None
        """
        try:
            with open("supplies/supplyrequests.csv", "a", newline="") as file:
                _ = writer(file)
                _.writerow([requestor, supply_name, supply_quantity])
        except FileNotFoundError:
            print("An error occurred placing the request. Contact admin if issue persists.")
            exit(1)
        else:
            print("Request placed successsfully. Your supply request will be reviewed and potentially apporoved by admin.")
            print()
            return None


    def prompt() -> None:
        """
        Displays action options for user.
        :return: None
        :rtype: None
        """
        print("*"*30)
        for line in contents:
            print(f"{line[0]:15} | {line[1]:5}")
        print("*"*30)

        print("1 - Order Supplies\n" \
              "2 - Exit")

    # Fetch supply inventory data
    contents = []
    try:
        with open("supplies/supplyinventory.csv", "r") as file:
            _ = reader(file)
            for line in _: contents.append(line)
    except FileNotFoundError:
        print("An error occurred when loading the supplies. Contact admin if issue persists.")
        exit(1)
    except Exception:
        print("An unknown error occurred.")
        exit(1)
    
    prompt()

   # Get user choice
    while True:
        selection = input("Enter your selection: ")
        match selection:
            case "1":
                order_supplies()
            case "2":
                return None
            case _:
                print("Invalid selection.")
                continue
        
        prompt()


def byclops() -> None:
    """
    Byclops.
    :return: None
    :rtype: None
    """
    print("byclops")
    return None


def colossus_victims() -> None:
    """
    Displays Colossus Victims from victims.csv file.
    :return: None
    :rtype: None
    """
    contents = []
    with open("colossus_victims/victims.csv", "r") as file:
        _ = reader(file)
        for line in _: contents.append(line)
        contents.remove(contents[0])
    
    print()
    print("First Name     |Last Name      |Date       |Description")
    print("---------------+---------------+-----------+-------------------------------------")
    for line in contents:
        print(f"{line[0]:15}|{line[1]:15}|{line[2]} | {line[3]}")
    print("---------------+---------------+-----------+-------------------------------------")

    input("PRESS ENTER TO CONTINUE ")


def log_missions(username:str) -> None:
    """
    Saves request for hours in a given month from user.
    :param username: User making request.
    :type username: str
    :return: None
    :rtype: None
    """
    # Get year
    years = [x[-8:-4] for x in listdir("x_mans_files/mission_logs")]
    while True:
        year = input("Enter year to log mission: ")
        if year.lower() == "q" or year.lower() == "quit":
            return None

        if len(year) != 4 or not year.isdigit():
            print("Invalid input.")
            continue
        
        if year not in years:
            print("Year doesn't have any entries.")
            continue
        break
    months = [x[-11:-8] for x in listdir(f"x_mans_files/mission_logs/{year}logs")]
    
    # Get month
    while True:
        month = input("Enter the month to log mission: ").capitalize()
        
        if month.lower() == "q" or month.lower() == "quit":
            return None
        
        if month not in months:
            print("Month does not have a log.")
            continue
        
        print()
        # Get amount of hours
        while True:
            try:
                hours = int(input("Enter the hours you want to log for this mission: "))
                if hours > 24 or hours < 0:
                    print("Value out of range.")
                    continue
            except ValueError:
                print("Invalid input.")
                continue
            else:
                # Save request
                with open("x_mans_files/hour_requests.csv", "a", newline="") as file:
                    _ = writer(file)
                    _.writerow([username, hours, month, year])
                print("Mission requested successfully. Admin will review it for approval to be logged.")
                return None


def profile_manager(username:str) -> None:
    def prompt() -> None:
        """
        Displays action options for user.
        :return: None
        :rtype: None
        """
        print("*"*30)
        print("1 - View Profile\n"
              "2 - Notifications\n"
              "3 - Change Password\n"
              "4 - Exit")
        print("*"*30)


    def view_profile() -> None:
        """
        Formats and displays data from user's profile file.
        :return: None
        :rtype: None 
        """
        print()
        with open(f"x_mans_files/profiles/{username}.json", "r") as file:
            user_data = load(file)
        
        print("="*35)
        for key, value in list(user_data.items())[:-1]:
            print(f"{key.upper():23}: {value}")
        
        tmp = len(user_data["Notifications"])
        print(f"NOTIFICATIONS          : {"No notifications" if tmp == 0 else str(tmp) + " notifications"}")
        print("="*35)
        input("PRESS ENTER TO CONTINUE ")


    def notifications() -> None:
        """
        Numbers and displays notifications from user's profile file.
        :return: None
        :rtype: None
        """
        print()
        with open(f"x_mans_files/profiles/{username}.json", "r") as file:
            user_data = load(file)
        
        if not user_data["Notifications"]:
            print("No notifications to view.")
        else:
            for index, element in enumerate(user_data["Notifications"]):
                print(f"[{index + 1}] {element}")
        
        input("PRESS ENTER TO CONTINUE ")

        user_data["Notifications"] = []
        with open(f"x_mans_files/profiles/{username}.json", "w") as file:
            dump(user_data, file)


    def change_password(username: str) -> None:
        """
        Allows user to change the password save in users.json file.
        :param username: User changing their password.
        :type username: str
        :return: None
        :rtype: None
        """
        # Fetch data
        load_dotenv()
        key = getenv("KEY").split(",")
        with open("references/users.json", "r") as file:
            contents = load(file)
        
        # Get old password
        print("Enter your current password to proceed.")
        while True:
            old_password = input("Password: ")
            if old_password.lower() == "q" or old_password.lower() == "quit":
                return None

            if old_password != decrypt(contents[username], key):
                print("Password incorrect.")
                continue
            else: break

        # Get new password
        print()
        while True:
            new_password = input("Enter your new password: ")
            if new_password.lower() == "q" or new_password.lower() == "quit":
                return None

            if not new_password:
                print("Field cannot be empty.")
                continue

            if new_password == old_password:
                print("New password cannot be the same as old password.")
                continue

            if not new_password.isalnum():
                print("Password must be alphanumeric only.")
                continue
            
            print()
            if input("Confirm password: ") == new_password: break
        
        # Save new password
        new_password = encrypt(new_password, key)
        contents.update({username:new_password})

        with open("references/users.json", "w") as file:
            dump(contents, file)
        
        print("\nPassword updated.")
        input("PRESS ENTER TO CONTINUE ")

    prompt()
    while True:
        selection = input("Enter your selection: ")
         
        match selection:
            case "1":
                view_profile()
            case "2":
                notifications()
            case "3":
                change_password(username)
            case "4":
                return None
            case _:
                print("Invalid selection.")
                continue
        print()
        prompt()


if __name__ == "__main__":
    print("Running menuchoices.py")