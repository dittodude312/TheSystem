from dotenv import load_dotenv
from os import getenv
from system_functions import utilfunctions


string = "   t.h.e. cat sat c/c++ c/c# on the mat c++  "

print(utilfunctions.to_title_case(string) + "|")
utilfunctions.update_user_month_data("byclopss")
#print([x for x in range(10) if x%2==0])