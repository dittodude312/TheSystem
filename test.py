"""string = " onCe uPOn a tiME  "
stop = 0
words = []
string = string.strip()

num = 0
for char in string:
    if char == " ":
        num += 1
string += " "

for i in range(num + 1):
    stop = string.index(" ")
    word = string[:stop]
    string = string[stop + 1:]
    words.append(word)
words = [x.lower().capitalize() for x in words]
string = ""
for thing in words:
    string += (thing + " ")

string = string.strip()


print(string + "|")"""

diction = {"a":1, "b":2, "c":3}
new_dict = {}
keys = list(diction.keys())
values = list(diction.values())
old = "b"
new = "bee"
keys.insert(keys.index(old), new)
keys.remove(old)

for i in range(len(keys)):
    new_dict.update({keys[i]:values[i]})

print(new_dict)
