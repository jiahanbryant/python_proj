# For tests

message = "hello world! this is 'tony'!"
print (message.title())
print (message.upper())
print (message.lower())

first_name = "tony"
last_name = "gao"
full_name = first_name + " " + last_name
print (full_name.title())

#strip spaces
string_1 = " strip "
print (string_1.rstrip())
print (string_1.rstrip().lstrip())
print (string_1.strip())


name = ['tony', 'tom', 'hannes', 'jordan']
print (name)
print (name[0].title())

#read from end
print (name[-1].title())
print (name[-2].title())

#appending element
name.append('jimmy')
print (name)

#inserting element
name.insert(2, 'kate')
print (name)

#remove element using 'del'
del name[4]  #jordan is removed
print (name)

#remove element using 'pop'
print (name.pop())
print (name)

#remove element using 'remove'
name.remove('tony')
print (name)




