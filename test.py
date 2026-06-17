from csv import writer

with open("student_testscores/testscores2026.csv", "a", newline = "") as file:
    thing = writer(file)
    thing.writerow(["a", "b", 90,90,1200])