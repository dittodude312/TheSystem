"""
    Main file for program using system_functions package. Contains functions for accessing system functionality.
"""

try: from dotenv import load_dotenv
except ModuleNotFoundError:
    print("The System is missing python-dotenv dependency.")
    print("Try running [py -m pip install python-dotenv].")
    exit(1)
try: import system_functions
except ModuleNotFoundError:
    print("The System is missing functionality package.")
    exit(1)

import games

from json import load
from datetime import datetime, timedelta


def game_menu() -> None:
    """
    Prompts and displays options for games to play.
    :return: None
    :rtype: None
    """
    def prompt() -> None:
        """
        Displays games for user to play.
        :return: None
        :rtype: None
        """
        print("*"*30)
        print("1 - Tic Tac Toe\n" \
              "2 - Russian Roulette\n" \
              "3 - Exit")
        print("*"*30)

    prompt()
    while True:
        selection = input("Enter your selection: ")
        match selection:
            case "1": games.tictactoe.main()
            case "2": games.russianroulette.main()
            case "3": return None
            case _:
                print("Invalid selection.")
                continue
        print()
        print()
        prompt()


def start_menu(username:str) -> None:
    """
    Prompts and displays options for normal users and calls corresponding function. Calls admin_panel function if username == admin.
    :param username: Username.
    :type username: str
    :return: None
    :rtype: None
    """
    def prompt() -> None:
        """
        Displys options for user and displays Admin Panel option if username == admin.
        :return: None
        :rtype: None
        """
        print("*"*30)
        print("1 - Grades\n" \
              "2 - Test Scores\n"
              "3 - X-Mans\n" \
              "4 - Supplies\n" \
              "5 - Byclops\n" \
              "6 - Colosssus Victims\n"
              "7 - Log Missions\n"
              "8 - Profile Manager")
        if username == "admin":
            print("9 - Admin Panel\n" \
                  "10 - Close System")
        else:
            print("9 - Close System")
        print("*"*30)

        return None

    prompt()

    while True:
        selection = input("Enter your selection: ")
        print("_"*30)
        match selection:
            case "1": system_functions.menuchoices.grades()
            case "2": system_functions.menuchoices.test_scores()
            case "3": system_functions.menuchoices.x_mans()
            case "4": system_functions.menuchoices.supplies(username)
            case "5": system_functions.menuchoices.byclops()
            case "6": system_functions.menuchoices.colossus_victims()
            case "7": system_functions.menuchoices.log_missions(username)
            case "8": system_functions.menuchoices.profile_manager(username)
            case "9":
                if username == "admin":
                    print("Initializing admin panel...")
                    admin_panel()
                else: return None
            case "10":
                if username == "admin": return None
                else: 
                    print("Invalid input.")
                    continue
            case _:
                print("Invalid input.")
                continue
        print()
        prompt()


def admin_panel() -> None:
    """
    Displays actions for admin and calls corresponding function.
    :return: None
    :rtype: None
    """
    def prompt() -> None:
        """
        Displays options for admin.
        :return: None
        :retype: None
        """
        print("*"*30)
        print("1 - Add student\n" \
              "2 - Create new user\n" \
              "3 - Subjects Manager\n" \
              "4 - Approve supply requests\n" \
              "5 - Add test scores\n" \
              "6 - View logs\n" \
              "7 - View students\n" \
              "8 - Approve mission hours\n" \
              "9 - Update month entries\n" \
              "10 - Send notifications\n" \
              "11 - Games\n" \
              "12 - Exit")
        print("*"*30)
    
    prompt()
    while True:
        selection = input("Enter your selection: ")
        print("_"*30)
        match selection:
            case "1": system_functions.admincontrols.new_student()
            case "2": system_functions.admincontrols.new_user()
            case "3": system_functions.subjects.main()
            case "4": system_functions.admincontrols.approve_supply_requests()
            case "5": system_functions.admincontrols.add_test_scores()
            case "6": system_functions.admincontrols.userlog()
            case "7": system_functions.admincontrols.view_students()
            case "8": system_functions.admincontrols.approve_hours()
            case "9": system_functions.admincontrols.new_month()
            case "10": system_functions.admincontrols.send_notif()
            case "11": game_menu()
            case "12": return None
            case _:
                print("Invalid selection.")
                continue
        print()
        prompt()


def log_user_access(username:str, start_time:datetime) -> None:
    """
    Calculates the runtime of the program and saves it to userlog.txt along with username.
    :param username: Username.
    :type username: str
    :param start_time: Time that program began running.
    :type start_time: datetime.datetime
    :return: None
    :rtype: None
    """
    date = datetime.today()
    date = datetime.strftime(date, "%m/%d/%Y at %H:%M:%S")
    uptime = datetime.now() - start_time
    uptime -= timedelta(microseconds = uptime.microseconds)

    try:
        with open("userlog.txt", "a") as file:
            file.write(f"{username} accessed The System on {date} for {uptime}\n")
    except FileNotFoundError:
        print("An error occured with logging user activity. Contacting admin. Don't go anywhere.")
        exit(1)
    else: return None


def main() -> None:
    """
    Main file that program execution stems from.
    :return: None
    :rtype: None
    """
    print("="*35)
    start_time = datetime.now()
    username = system_functions.authenticate.main()

    with open(f"x_mans_files/profiles/{username}.json", "r") as file:
        notifications_number = len(load(file)["Notifications"])    

    print("-"*30)
    print(f"Logged in successfully. Welcome {username}.")
    print(f"You have {notifications_number} notifications.")
    input("-"*30 + " ")

    start_menu(username)

    print("Thank you for using the System.\n" \
          "Terminating Session...")

    log_user_access(username, start_time)
    print("="*35)


if __name__ == "__main__":
    load_dotenv()
    print()
    main()
    print()