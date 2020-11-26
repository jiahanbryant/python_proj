# for practicing functions
#  by Tony

def greet_user(username):
    """"Display a simple greeting"""
    print("hello, " + username.title() + "!")

# call the function
greet_user('tony')

# passing arbitrary number of arguments
def hello_to(*names):
    """ Print as many names as you want """
    print(names)
hello_to('tony', 'jimmy')



