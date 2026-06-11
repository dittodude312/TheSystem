from json import load
with open("users.json", "r") as file:
    contents = load(file)

print(contents.keys())
if 'admin' in contents.keys():
    print('rufhe')