# to practice file manipulation
# by Tony

filename = 'test_file.txt'
filename_w = 'test_file_w.txt'

with open(filename) as file_object:
    contents = file_object.read()
    print(contents.rstrip()) # using rstrip to remove white space to the
                             # right of the string
                             
with open(filename) as file_object:
    for line in file_object:
        print(line.rstrip())

# to store lines in to list:
with open(filename) as file_object:
    lines = file_object.readlines()

for line in lines:
    print(line.rstrip())

pi_string = ''
for line in lines:
    pi_string += line.strip()  # to strip both right and left whitespace

print(pi_string)
print(len(pi_string))

# to check if your bithday is in the digits:
birthday = input("Enter your birthday, in the form of mmdd: ")
print("Your birthday is: " + str(birthday))
if birthday in pi_string:
    print("Yay, your birthday is here.")
else:
    print("Sorry, you're without luck!")
    

# to write to a file:
# if the file doesn't exist, it will be created.
with open(filename_w, 'w') as file_object:
    file_object.write("I love python programming. 123\r")
    file_object.write("I don't eat rice.\r")  # will be appended

with open(filename_w) as file_object:
    contents = file_object.read()
    print("Here's what you've written to the file: \n")
    print(contents)
    
# to append to a file
with open(filename_w, 'a') as file_object:
    file_object.write('appending 1st line.\n')
    file_object.write('appending 2nd line.\n')

with open(filename_w) as file_object:
    contents = file_object.read()
    print("Here's what you've written to the file: \n")
    print(contents)
    

    
    
    
