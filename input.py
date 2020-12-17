# for practicing user inputs
# by Tony

message = input("Tell me your name: ")
print("Your name is: " + message.title())

prompt = "\nTell me something, and I will repeat it back to you: "
prompt += "\nEnter 'quit' to end the program. "

message = ""
while message != 'quit':
	message = input(prompt)
	if message != 'quit':
		print(message)

