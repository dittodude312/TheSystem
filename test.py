from csv import reader

with open("colossus_victims/victims.csv", "r") as file:
    thing = reader(file)
    for line in thing:print(line)