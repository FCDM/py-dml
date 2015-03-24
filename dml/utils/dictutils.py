def mergeDicts(*dicts):
	"""Merge a set of dictionaries."""
	result = {}
	for dict in dicts:
		result.update(dict)
	return result