def to_title_case(string, seperator = " "):
    stop = 0
    words = []
    space_number = 0
    string = string.strip()

    for char in string:
        if char == seperator: space_number += 1
    
    string += seperator

    for _ in range(space_number + 1):
        try:
            stop = string.index(seperator)
        except ValueError: pass

        word = string[:stop]

        string = string[stop + 1:]
        #print("word: " + word)
        #print("string: " + string)
        words.append(word)
    
    words = [x.lower().capitalize() for x in words]
    for x in words:
        words[words.index(x)] = x.upper() if "." in x else x
    for element in words:
        if element.lower() == "ii" or element.lower() == "iii":
            words[words.index(element)] = element.upper()
    #print(words)
    string = ""

    for element in words:
        string += (element + seperator)

    return string[:-1]


string = "e.L.A. ii"
print(to_title_case(string))