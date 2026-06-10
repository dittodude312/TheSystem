from json import load, dump
from csv import reader, writer


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
    def view_score(index):
        values = []
        print(year + " " + "*"*25)
        for line in contents:
            print(f"{(line[1] + ", " + line[0]):25}---  {line[index]:>4}")
            values.append(int(line[index]))
        print(f"Average Score Across School: {(sum(values)/len(values)):.2f}")
        print("*"*30)


    contents = []

    # Fetch scores
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
    
    # View score category
    while True:
        print()
        print("1 - Fall Standardized Testing Scores\n" \
              "2 - Spring Standardized Testing Scores\n" \
              "3 - SAT Scores\n" \
              "4 - Exit")
        
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
    

def x_mans():
    contents = []

    # Fetch log data
    while True:
        try:
            month = input("Enter the month to view X-Mans logs: ")
            with open(f"x_mans_files/xmans{month}2026.csv") as file:
                _ = reader(file)
                for line in _: contents.append(line)
                contents.remove(contents[0])
                del _
        except FileNotFoundError:
            print("Files could not be found. Check if month was entered correctly. If so, contact admin if issue persists.")
            continue
        except Exception:
            print("An unknown error occurred.")
            continue
        else: break

    # Display data
    print(month.upper() + " " + "-"*32 + "|" + "Missions  |Hours")
    for line in contents:
        print(f"{(line[1] + ", " + line[0] + " (" + line[2] + ")"):35} | {line[3]:>8} | {line[4]:>6}")
    print("-"*55)

    return None


def supplies(username):
    def order_supplies():
        print("-"*15)
        print("What supplies do you want to request?")
        print("1 - Papers\n" \
              "2 - Staples\n" \
              "3 - Erasers\n" \
              "4 - Pencils\n" \
              "5 - Rulers\n" \
              "6 - Desks\n" \
              "7 - Tables\n" \
              "8 - Other")
        print("-"*15)
        # Get supply name
        while True:
            supply = input("Enter your desired supply: ")
            match supply.lower():
                case "1": supply = "Papers"
                case "2": supply = "Staples"
                case "3": supply = "Erasers"
                case "4": supply = "Pencils"
                case "5": supply = "Rulers"
                case "6": supply = "Desks"
                case "7": supply = "Tables"
                case "8":
                    supply = input("Enter name of supply: ")
                    if not supply:
                        print("Field cannot be empty.")
                        continue
                case "q" | "quit":
                    return None
                case _:
                    print("Invalid selection.")
                    continue
            break
        
        # Get supply quantity
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
                print("Value must be number.")
            else: break
        
        #Write data
        write_request(supply, username, quantity)
        return None

    
    def write_request(supply_name, requestor, supply_quantity):
        try:
            with open("supplies/supplyrequests.csv", "a", newline="") as file:
                _ = writer(file)
                _.writerow([requestor, supply_name, supply_quantity])
        except FileNotFoundError:
            print("An error occurred placing the request. Contact admin if issue persists.")
            exit(1)
        else:
            print("Request placed successsfully. Your supply request will be reviewed and potentially apporoved by admin.")
            return None


    def prompt():
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