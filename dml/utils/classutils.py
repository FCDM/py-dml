def getBases(cls, stop_at=object):
	"""Return a list of the tree of all base classes of a given class."""
	bases = [cls]

	if cls == stop_at:
		return bases

	for base in cls.__bases__:
		bases.extend(getBases(cls, stop_at))

	return bases

def getBasesLinear(cls, stop_at=object):
	"""Return a list of the linear tree of base classes of a given class."""
	bases = [cls]
	next_base = cls.__bases__[0]

	while next_base != stop_at:
		bases.append(next_base)
		next_base = next_base.__bases__[0]
		
	bases.append(next_base)
	return bases