from dotenv import load_dotenv
from os import getenv
from system_functions import utilfunctions


string = "   t.h.e. cat sat c/c++ c/c# on the mat c++  "

print(utilfunctions.to_title_case(string) + "|")

utilfunctions.update_user_month_data("byclopss")
number = 12
print(f"{number:0>2}")

numbers = (1,4,2,6,3,4,2)

print(sorted(numbers))

print(utilfunctions.date_is_later("4/10/2026", "1/10/2026"))

lis = ["a", "b", "c", "d"]
lis.insert(2, "E")
print(lis )

#print([x for x in range(10) if x%2==0])