from os import listdir

for path in listdir("x_mans_files/mission_logs"):
    for file in listdir(f"x_mans_files/mission_logs/{path}"):
        print(file)