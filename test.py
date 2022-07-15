import re

a = 'sadasdsaada123asdsadsadasd'

print(a.replace('123.*', ''))
print(re.sub('123*', '', a))
