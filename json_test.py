# to practice json files
# by Tony

import json

try:
    numbers = [2, 3, 23, 5, 9, 20]
    filename = 'numbers.json'
    with open(filename, 'w') as f_object:
        json.dump(numbers, f_object)  # dump numbers to a file
        
except FileNotFoundError:
    print("File does not exists, try to create the file first.")
    
    
with open(filename) as f_obj:
    numbers = json.load(f_obj)

print("The numbers written: ")
print(numbers)

userfile = 'username.json'

# to try if username exists
try: 
    with open(userfile) as f_obj:
        username = json.load(f_obj)
except FileNotFoundError:
    username = input("input your username: ")
    with open(userfile, 'w') as f_obj:
        json.dump(username, f_obj)
        print("We'll remember you when you come back, " + username + "!")
else:
    print("Welcome back, " + username + "!")
