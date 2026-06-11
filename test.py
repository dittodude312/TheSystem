from os import listdir

print(listdir("student_grades"))

names = [x[:-5] for x in listdir("student_grades")]
print(names)