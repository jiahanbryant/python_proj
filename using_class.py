# practice for using classes
# bt Tony

# define a class Dog:
class Dog():
	"""A simple attempt to model a dog."""
	def __init__(self, name, age):
		"""Initialize name and age attributes."""
		self.name = name
		self.age = age
		
	def sit(self):
		""" Simulate a dog sitting in response to a command """
		print(self.name.title() + " is now sitting.")
		
	def roll_over(self):
		""" Simulate a dog rolling over """
		print(self.name.title() + " is now rolling over.")
		
# using the Dog class		
my_dog = Dog("Jime", 6)

print("My dog's name is " + my_dog.name.title() + ".")
print("My dog is " + str(my_dog.age) + " years old.")

my_dog.sit()
my_dog.roll_over()

# define a class Car
class Car():
	"""A simple attempt to model a car."""
	def __init__(self, make, model, year):
		"""Initialize attributes to describe a car."""
		self.make = make
		self.model = model
		self.year = year
		self.odometer_reading = 0
		
	def get_descriptive_name(self):
		""" Return a neatly formatted descriptive name. """
		long_name = str(self.year) + ' ' + self.make.upper() + ' ' + self.model
		return long_name
		
	def read_odometer(self):
		"""Reading back the odometer. """
		print("This car has " + str(self.odometer_reading) + " miles on it.")
	
	def update_odometer(self, mileage):
		""" to update the mileage on odometer. """
		if mileage > self.odometer_reading:
			self.odometer_reading = mileage
		else:
			print ("You can't roll back an odometer!")
			
	def increment_odometer(self, miles):
		""" To increment a mileage."""
		self.odometer_reading += miles
		
		
# using the class Car
my_new_car = Car('audi', 'A8', 2020)
print(my_new_car.get_descriptive_name())
my_new_car.read_odometer()

# changing an attribute directly
my_new_car.odometer_reading = 30
my_new_car.read_odometer()

# changing an attribute by using method
my_new_car.update_odometer(100)
my_new_car.read_odometer()

# trying to roll back
my_new_car.update_odometer(20)
my_new_car.read_odometer()

# to increment 30 miles
my_new_car.increment_odometer(30)
my_new_car.read_odometer()

# to inherit Car class
class Ecar(Car):
	"""Represent aspects of a car, specific to electric cars."""
	def __init__(self, make, model, year):
		"""Initialize attributes of the parent class.
		   Then adding more attributes. """
		super().__init__(make, model, year)
		
		self.battery_size = 70
	
	def describe_battery(self):
		""" Printing the size of battery. """
		print("This car has a " + str(self.battery_size) + "-KWh battery")
		
		

# using of Ecar
my_tesla = Ecar("Tesla", "Model S", 2020)
print(my_tesla.get_descriptive_name())
my_tesla.describe_battery()
