def darken(colour, amount):
	"""
	Darken a colur by a given amount.

	The amount ranges from 0 to 1, with 0
	being black and 1 being unchanged.
	"""
	r, g, b = colour
	return r*amount, g*amount, b*amount

def lighten(colour, amount):
	"""
	Lighten a colour by a given amount.

	The amount ranges from 0 to 1, with 0
	being unchanged and 1 being white.
	"""
	r, g, b = colour
	return r + amount*(255 - r), g + amount*(255 - g), b + amount*(255 - b)