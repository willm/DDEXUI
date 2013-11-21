def enum(**enums):
	reverse = dict((value, key) for key, value in enums.items())
	enums['reverse_mapping'] = reverse
	return type('Enum', (), enums)

