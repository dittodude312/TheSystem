# TODO: add choosing years for making hours request, userlog viewing, and x mans logs/requests
# TODO: games?
# TODO: notifications (would have to go back to like 6 different functions)
# TODO: x mans profiles
# TODO: fault tolerance thing
# TODO: optimize stuff ig
# TODO: fix add user function
# TODO: add function to create month entries


from system_functions import *
from json import load
from datetime import datetime, timedelta


def fetch_data():
    try:
        with open("references/users.json", "r") as file:
            contents = load(file)
    except FileNotFoundError:
        print("Failed to fetch user data. Terminating Session.")
        print("If issue persists, please contact admin.")
        print("Tip - Make sure you are using TheSystem directory when executing main.py.")
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


def start_menu(username):
    def prompt():
        print("*"*30)
        print("1 - Grades\n" \
              "2 - Test Scores\n"
              "3 - X-Mans\n" \
              "4 - Supplies\n" \
              "5 - Byclops\n" \
              "6 - Colosssus Victims\n"
              "7 - Log Missions\n"
              "8 - Change password")
        if username == "admin":
            print("9 - Admin Panel\n" \
                  "10 - Exit")
        else:
            print("9 - Exit")
        print("*"*30)

        return None

    prompt()

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
                menuchoices.log_missions(username)
            case "8":
                menuchoices.change_password(username)
            case "9":
                if username == "admin":
                    print("Initializing admin panel...")
                    admin_panel()
                else: return None
            case "10":
                if username == "admin": return None
                else: print("Invalid input.")
            case _:
                print("Invalid input.")
        print()
        prompt()


def admin_panel():
    def prompt():
        print("*"*30)
        print("1 - Add student\n" \
              "2 - Create new user\n" \
              "3 - Subjects Manager\n" \
              "4 - Approve supply requests\n" \
              "5 - Add test scores\n" \
              "6 - View logs\n" \
              "7 - View students\n" \
              "8 - Approve mission hours\n" \
              "9 - Exit")
        print("*"*30)
    
    prompt()
    while True:
        selection = input("Enter your selection: ")

        match selection:
            case "1":
                admincontrols.new_student()
            case "2":
                admincontrols.create_user()
            case "3":
                subjects.main()
            case "4":
                admincontrols.approve_supply_requests()
            case "5":
                admincontrols.add_test_scores()
            case "6":
                admincontrols.userlog()
            case "7":
                admincontrols.view_students()
            case "8":
                admincontrols.approve_hours()
            case "9":
                return None
            case _:
                print("Invalid selection.")
                continue
        print()
        prompt()
            

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

    #menuchoices.x_mans()
    #admincontrols.approve_hours() 