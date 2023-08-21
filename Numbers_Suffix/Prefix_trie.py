import datrie 

import string


trie = datrie.Trie(string.digits)

def create_trie_numbers():

    with open("numbers.txt", "r", encoding="UTF-8") as f:
        reader = [number.strip("\n").lstrip("+").replace(" ", "") for number in f.readlines()]

        for number in reader:

            prefix = ""

            for digit in number:
                
                prefix += digit

                if prefix not in trie.keys():

                    trie[prefix] = trie.get(prefix, [number for number in reader if prefix[:len(prefix)] == number[:len(prefix)]]) 

                else:

                    continue
     
    trie.save('my.trie')

def search_trie(user_input):

    trie1 = datrie.Trie.load('my.trie')

    key_set = set(trie1.keys())

    matching_key = [key for key in key_set if user_input in key]

    if matching_key != []:

        matched_key = sorted(matching_key, key=len)[0]

        return trie1[matched_key]
    
    return False