# practice for loops
# by Tony

nums = [1, 4, 22, 21, 5, 2]
new_nums = []
print("numbers in the list:" )
for num in nums:
	print (num)
	new_nums.insert(0, num)
print("numbers in the new list:")
print(new_nums)

#make numberial list using 'list'
nums = list(range(1,5))
print(nums)

#usnig 'range' with a step
nums = list(range(1, 11, 2)) #2 as step, ending element < 11
print(nums)

#squaring
squares = []
for value in range(1, 11):
	square = value ** 2  ##** means square
	squares.append(square)

print(squares)
print(min(squares))
print(max(squares))
print(sum(squares))

#a more concise option, using list comprehension
print("using list comprehension:")
squares = [value ** 2 for value in range(1, 11)]
print(squares)

#Slicing list
print("the first two elements of the list: ")
print(squares[0:2]) #print only the first two elemments

