# for practicing exception handling
# by Tony

# using try-except blocks:
try:
	divider = input("Input a number: ")
	print(5/int(divider))
	
except ZeroDivisionError:
	print("You can't divide by Zero! Change to another number and try again.")
	
except ValueError:
	print("Please input a number, not characters.")
	

# file not found:
filename = 'test.txt'

try:
	with open(filename) as file_object:
		contents = file_object.read()
		
except FileNotFoundError:
	msg = "Sorry. the file" + filename + " does not exists."
	print(msg)
	
else:
	print(contents)
