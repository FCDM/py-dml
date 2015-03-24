import math

def clampf(f, x_min, x_max):
	"""
	Return a new function that is the given function clamped on its domain
	between the given x_min and x_max values.
	"""
	return lambda t : f(x_max if t > x_max else x_min if t < x_min else t)

def compose(func_a, func_b):
	"""
	Return a new function that is the composition of the first one with the second.
	"""
	return lambda x : func_a(func_b(x))


def periodic(f, period):
	"""
	Return a new function that is the given one periodic over the given period.
	"""
	return lambda x : f(x % period)

def periodicReflected(f, period):
	"""
	Return a new function F(t) such that it has the following properties.

	Define P as the given period, and f as the initial function. Then

			/ f(t), 0 <= t < P/2
	F(t) = | 
			\ f(P - t), P/2 <= t < P

	F(t) also satisfies F(t + n*P) = F(t) for all integers n.
	"""
	half_period = period/2
	def _f(t):
		t %= period
		if t > half_period:
			return f(period - t)
		return f(t)
	return _f

def piecewise(functions, conditions, fallback=lambda x : 0):
	"""
	Return a piecewise function such that if condition ``i`` in the given list
	of conditions is true, then the function at index ``i`` is executed. 

	If none of the conditions are satisfied, then the given fallback function
	is used (default is lambda x : 0).
	"""
	def _f(x):
		for i, condition in enumerate(conditions):
			if condition(x):
				return functions[i](x)
		return fallback(x)
	return _f

def transform(f, a, b, c, d):
	"""
	Transform a given function linearly.

	If f(t) is the original function, and a, b, c, and d are the parameters in
	order, then the return value is the function

	F(t) = af(cx + d) + b
	"""
	return lambda x: a * f(c * x + d) + b

def polynomial(coefficients):
	"""
	Create a polynomial from the given list of coefficients.

	For example, if the coefficients are [1, 0, 3, 5], then
	the polynomial returned is

	P(t) = t^3 + 3t + 5

	If the coefficients are [3, 2, -2, 9, 4, 0, 1, 0], then
	the polynomial returned is

	P(t) = 3t^7 + 2t^6 - 2t^5 + 9t^4 + 4t^3 + t
	"""
	def _f(x):
		result = 0
		for coefficient in coefficients:
			result = result * x + coefficient
		return result
	return _f