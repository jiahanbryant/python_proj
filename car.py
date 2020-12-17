# to practice importing class
# by tony

from myclass import Car, Ecar

my_car = Ecar('tesla', 'model x', 2020)
print(my_car.get_descriptive_name())
my_car.describe_battery()

# using python standard library
from collections import OrderedDict

favorite_lang = OrderedDict()

favorite_lang['jen'] = 'python'
favorite_lang['sarah'] = 'C'
favorite_lang['edward'] = 'ruby'
favorite_lang['phil'] = 'python'

for name, language in favorite_lang.items():
	print(name.title() + "'s favorite language is " + language.title() + '.')
