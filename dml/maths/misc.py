import math

def sgn(x):
	"""Return the sign of x."""
	return -1 if x < 0 else 1

def binomialCoefficient(n, k):
	"""Calculate the binomial coefficient at n and k."""
	return math.factorial(n)/math.factorial(k)/math.factorial(n-k)