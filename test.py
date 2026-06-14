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

string = "the cat sat on the mat"
string = string.strip()
stop = 0
words = []

while True:
    try:
        stop = string.index(" ")
        word = string[:stop]
        string = string[stop + 1:]
        words.append(word)
    except ValueError:
        break
    