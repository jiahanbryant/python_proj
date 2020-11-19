# For practicing dictionary topics
# by Tony

alien_0 = {'color': 'green', 'points': 5}

print(alien_0['color'])
print(alien_0['points'])

# now add more key-valule pairs to the dictionary
alien_0['x_position'] = 0
alien_0['y_position'] = 25

print(alien_0)

# deleting a key-value pair
del alien_0['color']
print(alien_0)

# changing key values
alien_0['color'] = 'yellow'
print(alien_0)

# an example
alien_0 = {'x_position': 0, 'y_position': 25, 'speed': 'medium'}
print("Original x-position: " + str(alien_0['x_position']))

if alien_0['speed'] == 'medium':
    x_increment = 2
elif alien_0['speed'] == 'slow':
    x_increment = 1
else:
    x_increment = 3

alien_0['x_position'] = alien_0['x_position'] + x_increment
print("New x-position: " + str(alien_0['x_position']))

# looping thru dictionary
user_0 = {
    'username': 'tony',
    'first': 'tony',
    'last': 'gao',
}

for key, value in user_0.items():
    print("\nKey: " + key)
    print("\nValue: " + value)

# using key()
print("All the keys: \n")
for key in user_0.keys():
    print(key.title())
