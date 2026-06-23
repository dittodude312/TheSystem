from csv import writer

with open("students.csv", 'a', newline="") as file:
    w = writer(file)
    w.writerow(["e", "e", 12])