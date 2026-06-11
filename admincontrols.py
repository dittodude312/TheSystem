from json import dump, load
from random import choice

#make it so that you can enter q on class selection to go back to category selection
def create_student():
    schedule = []
    grades = {}

    # Get student name
    while True:
        first_name = input("Enter student's first name: ").strip().capitalize()
        last_name = input("Enter student's last name: ").strip().capitalize()

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
            print("="*30)
            print("1 - Art and Music\n"
                "2 - Computer Science\n"
                "3 - Electives\n"
                "4 - History\n"
                "5 - World Languages\n"
                "6 - Math\n"
                "7 - Reading\n"
                "8 - Sciences")
            print("="*30)
            category = input("Enter category of class the student will take: ")
            match category:
                case "1": file_path = "artmusic.txt"
                case "2": file_path = "compscience.txt"
                case "3": file_path = "elective.txt"
                case "4": file_path = "history.txt"
                case "5": file_path = "language.txt"
                case "6": file_path = "math.txt"
                case "7": file_path = "reading.txt"
                case "8": file_path = "sciences.txt"
                case "q" | "quit": return None
                case _:
                    print("Invalid selection.")
                    continue
            break

        # Fetch classes belonging to class category
        print("- "*15)
        with open(f"school_classes/{file_path}", "r") as file:
            classes = file.readlines()
            classes = [x[:-1] for x in classes]
        

        print("="*30)
        for index, element in enumerate(classes):
            print(f"{index + 1} - {element}")
        print("="*30)

        # Get class student will take from category
        while True:
            hour = input("Enter the class the student will be taking: ")
            
            if hour.lower() == "q" or hour.lower() == "quit":
                return None
            
            if hour not in classes:
                print("Invalid selection.")
                continue
            else: break
        schedule.append(hour)
        print()

    # Save classes and grades into new .json file
    for i in range(len(schedule)):
        grades.update({schedule[i]:"A"})

    with open(f"student_grades/{first_name}{last_name}.json", "w") as file:
        dump(grades, file)
    
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


if __name__ == "__main__":
    print("Running admincontrols.py")
else:
    print("\nAdmin functions loaded successfully.\n" + "~"*35)