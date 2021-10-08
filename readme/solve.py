with open("readme", "r") as file:
    data = file.read()
split_data = data.split("-------------")
enc_story = split_data[1].strip()
story = split_data[2].strip()

def check_key(key, key_checker_data):
    """ returns True is the key is correct.
        Usage:
        check_key('{I_think_this_is_the_key}', key_checker_data)
    """
    arc4 = ARC4.new(("CSA" + key).encode())
    return arc4.decrypt(key_checker_data) == b'success'

flags_option = []

def rec(options, flag="", index=0):
    if index == 28:
        flags_option.append(flag)
        return
    for o in options[index]:
        rec(options, flag + o, index + 1)

mapping = dict()
mapping["_"] = {'_'}
flag_map = []
for i, char in enumerate(story.lower()):
    mapping[char] = mapping.get(char, set())
    mapping[char].add(enc_story[i])
for i in "hey_that_is_the_great_puzzle":
    flag_map.append(list(mapping[i]))
rec(flag_map)

for flag in flags_option:
    if check_key(f"{{{flag}}}", b"\xE0\x33\x70\x95\xA1\xE5\x31"):
        print(f"CSA{{{flag}}}")
        break