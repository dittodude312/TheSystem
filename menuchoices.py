from json import load, dump
from csv import reader


def input_check(prompt, acceptable_values):
    while True:
        selection = input(prompt)
        if selection.lower() == "q" or selection.lower() == "quit":
            return "QUIT"
        elif selection not in acceptable_values:
            print("Invalid input.")
            continue
        else: return selection


def grades():
    def prompt():
        print(student + " " + "*"*(30 - len(student) - 1))
        for subject, grade in contents.items():
            print(f"{subject:20}---{grade:>5}")
        print("*"*30)
        
        print("1 - Change Grade\n" \
          "2 - Exit")


    def change_grade():
        # Get grade and subject
        subject = input_check("Enter subject to change grade: ", contents.keys())
        if subject == "QUIT": return None

        new_grade = input_check("Enter new grade: ", ("A", "B", "C", "D", "E", "F"))
        if new_grade == "QUIT": return None

        # Update grades
        contents.update({subject:new_grade})
        
        with open(f"student_grades/{file_name}.json", "w") as file:
            dump(contents, file)

        return None


    # Get student name
    while True:
        student = input("Enter student name: ")
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
                

def test_scores():
    def prompt():
        print(year + " " + "*"*25)
        for line in contents:
            print(f"{(line[1] + ", " + line[0]):25}---")

    contents = []
    while True:
        year = input("Enter school year to view scores: ")
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

    prompt()
    exit()
    
    
    

def x_mans():
    pass

def supplies():
    pass

def byclops():
    pass

def colossus_victims():
    pass

def admin_panel():
    pass

if __name__ == "__main__":
    print("Running menuchoices.py")
else:
    print("\nSystem functions loaded successfully.\n" + "~"*35)