string = "The Cat"

string = string[:string.find(" ")].capitalize() + " " + string[string.find(" ") + 1:].capitalize()
print(string)