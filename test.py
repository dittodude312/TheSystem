from csv import writer

with open("supplies/supplyrequests.csv", "a", newline="") as file:
    writ = writer(file)
    writ.writerow(["doodpool", "Erasers", "69"])