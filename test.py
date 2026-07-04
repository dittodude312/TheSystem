from random import shuffle
"""
def gen_key():
    chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    key = chars.copy()
    shuffle(key)
    return key


def encrypt(plaintext, key):
    chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    return [key[chars.index(x)] for x in plaintext]


def decrypt(ciphertext, key):
    chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    return [chars[key.index(x)] for x in ciphertext]

key = gen_key()
password = "password"

password = encrypt(password, key)
print(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"])
print(key)
print(password)
print(decrypt(password, key))"""


from system_functions import utilfunctions

print(utilfunctions.to_title_case("w w w"))