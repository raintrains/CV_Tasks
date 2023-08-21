from  db_utils import user_query, create_and_db_filling

from Prefix_trie import search_trie

create_and_db_filling()

print("Hi if you want to get out enter: q")
print()

while True:
    
    user_data = str(input("Enter the numbers than begin the phone youre looking for: "))

    print()


    if user_data == 'q':
        break

    trie_response = search_trie(user_data)
    
    # print(trie_response)

    if trie_response:
        
        print(user_query(trie_response))

        print()
         
    else:
        
        print("No matches found!")
        
        print()