def newtonRaphson(function, derivative, initial_guess=1, error=1e-5):
	"""
	Perform the Newton-Raphson root-finding algorithm on a given function and
	its derivative.
	"""
	px = initial_guess
	nx = initial_guess - function(initial_guess)/derivative(initial_guess)
	while abs(nx - px)/abs(nx) > error:
		px = nx
		nx = nx - function(nx)/derivative(nx)
	return nx

def approximateInverse(function, derivative, value):
	"""
	Approximate the inverse of a function at the desired value.
	"""
	return newtonRaphson(lambda x : function(x) - value, derivative)