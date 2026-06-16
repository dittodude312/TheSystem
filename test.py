from csv import writer

with open("tests.csv", "a",newline="") as file:
    wr = writer(file)
    wr.writerow(["z",109])