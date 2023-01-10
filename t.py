import pickle
import pprint
import PyDest

with open('data/xur', 'rb') as filename:
    file_data = filename.read()

# Load data from read bytes
xur: dict = pickle.loads(file_data)

items = dict()

for val in xur.values():
    if (val['inventory']['tierTypeName'] == 'Exotic') and (val['itemType'] in [2, 3]):
        items.update({val['displayProperties']['name']: val['stats']['stats']})

for stats in items:
	pprint.pprint(items[stats])
	for stat in items[stats]:
		name = PyDest.PyDest.decode_hash(items[stats][stat]['statHash'], 'DestinyStatDefinition')
		val = items[stats][stat]['value']

		print(name + ": " + val)

	print()


# pprint.pprint(items)
