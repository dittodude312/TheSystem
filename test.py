from os import listdir
from csv import reader

def get_alltime_stats(username):
    names = []
    real_name = ""
    with open("X_mans_files/x_men_list.csv", "r") as file:
        _ = reader(file)
        for line in _: names.append(line)

    for line in names:
        if username == line[3]:
            real_name = line[0]

    contents = []
    hour_total = 0
    mission_total = 0
    for file_path in listdir("x_mans_files/mission_logs"):
        with open(f"x_mans_files/mission_logs/{file_path}", "r") as file:
            _ = reader(file)
            for line in _: contents.append(line)

        for entry in contents:
            if real_name == entry[0]:
                hour_total += int(entry[4])
                mission_total += int(entry[3])
        contents = []

    return hour_total, mission_total

#print(get_alltime_stats("doodpool"))

thing = [1,2,3,4,5]
a = 6
print(list(range(1, len(thing) + 1)))
if a not in range(1, len(thing) + 1):
    print("no")
else: print("yes")
thing2 = thing.copy()
print(thing2)

thing[0] = 69

print(thing)
print(thing2)