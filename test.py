from json import load

with open("student_grades/BillyBob.json", "r") as file:
    contents = load(file)
    print(contents.keys())
    if "Chinese" in contents.keys():
        print('evkje')