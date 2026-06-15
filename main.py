import menuchoices
import admincontrols

from json import load
from datetime import datetime, timedelta

def fetch_data():
    try:
        with open("users.json", "r") as file:
            contents = load(file)
    except FileNotFoundError:
        print("Failed to fetch user data. Terminating Session.")
        print("If issue persists, please contact admin.")
        exit(1)
    else:
        return contents 

              
def login():
    while True:
        username = input("Username: ")
        password = input("Password: ")
        if not username or not password: print("Username or password fields cannot be blank.")
        else: return username, password


def authenticate():
    print("Welcome to the System. Please enter your credentials.")

    while True:
        username, password = login()
        contents = fetch_data()
        if username in contents.keys() and password == contents.get(username): return username
        else: print("Incorrect username or password.\n")


def display_start_options(username):
    print("*"*30)
    print("1 - Grades\n" \
          "2 - Test Scores\n"
          "3 - X-Mans\n" \
          "4 - Supplies\n" \
          "5 - Byclops\n" \
          "6 - Colosssus Victims")
    print("7 - Admin Panel" if username == "admin" else "", end="\n" if username == "admin" else "")
    print("*"*30)

    return None


def display_admin_options():
    print("*"*30)
    print("1 - Add student\n" \
          "2 - Create new user\n" \
          "3 - Subjects Manager\n" \
          "4 - Exit")
    print("*"*30)

    return None


def start_menu(username):
    display_start_options(username)

    while True:
        selection = input("Enter your selection: ")
        print("_"*30)
        match selection:
            case "1":
                menuchoices.grades()
            case "2":
                menuchoices.test_scores()
            case "3":
                menuchoices.x_mans()
            case "4":
                menuchoices.supplies(username)
            case "5":
                menuchoices.byclops()
            case "6":
                menuchoices.colossus_victims()
            case "7":
                print("Invalid input." if username != "admin" else "Initializing admin panel...\n" + "."*30)
                if username != "admin": pass
                else: admin_panel()
            case "q":
                return None
            case _:
                print("Invalid input.")
        print()
        display_start_options(username)


def admin_panel():
    display_admin_options()

    while True:
        selection = input("Enter your selection: ")

        match selection:
            case "1":
                admincontrols.create_student()
            case "2":
                admincontrols.create_user()
            case "3":
                admincontrols.subjects_mananger()
            case "4":
                return None
            case _:
                print("Invalid selection.")
                continue
        print()
        display_admin_options()
            

def log_user_access(username, start_time):
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


def main():
    start_time = datetime.now()
    print()
    username = authenticate()
    print("-"*30)
    print(f"Logged in successfully. Welcome {username}.")
    print("-"*30)

    start_menu(username)

    print("Thank you for using the System.\n" \
          "Terminating Session...")
    print()

    log_user_access(username, start_time)
   


if __name__ == "__main__":
    main()

    #menuchoices.grades()
    #admincontrols.subjects_mananger()