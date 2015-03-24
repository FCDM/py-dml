import math

from .geometry import Vector2D
from .misc import sgn

def parametricCircle(radius, time):
	"""
	Calculate a point on a parametric circle with the given radius at the
	given time.
	"""
	return radius * Vector2D(math.cos(time), math.sin(time))

def parametricEllipse(hradius, vradius, time):
	"""
	Calculate a point on a parametric ellipse with the given horizontal radius
	and vertical radius at the given time.
	"""
	return Vector2D(hradius*math.cos(time), vradius*math.sin(time))

def parametricSuperEllipse(hradius, vradius, exponent, time):
	"""
	Calculate a point on a parametric super-ellipse with the given horizontal
	radius, vertical radius, and exponent at the given time.
	"""
	n = 2/exponent
	cos_time = math.cos(time)
	sin_time = math.sin(time)
	return Vector2D(
		abs(cos_time**n)*hradius*sgn(cos_time),
		abs(sin_time**n)*vradius*sgn(sin_time)
		)

def parametricHippopede(hradius, vradius, time):
	"""
	Calculate a point on a parametric hippopede with the given horizontal radius
	and vertical radius at the given time.
	"""
	r = math.sqrt(hradius + (vradius - hradius)*math.sin(time)**2)
	return r * Vector2D(math.cos(time), math.sin(time))

def parametricCassiniOval(hradius, vradius, time):
	"""
	Calculate a point on a parametric Cassini oval with the given horizontal radius
	and vertical radius at the given time.
	"""
	c = math.cos(2*time)
	r = math.sqrt(hradius**2*c + math.sqrt(hradius**4*(c**2 - 1) + vradius**4))
	return r * Vector2D(math.cos(time), math.sin(time))

def parametricEpitrochoid(R, r, d, time):
	"""
	Calculate a point on a parametric epitrochoid with the given inner radius
	(R), outer radius (r), and arm length (d) at the given time.
	"""
	A = R + r
	B = A/r
	return Vector2D(
		A*math.cos(time) - d*math.cos(B*time),
		A*math.sin(time) - d*math.sin(B*time)
		)

def parametricHypotrochoid(R, r, d, time):
	"""
	Calculate a point on a parametric hypotrochoid with the given outer radius
	(R), inner radius (r), and arm length (d) at the given time.
	"""
	A = R - r
	B = A/r
	return Vector2D(
		A*math.cos(time) + d*math.cos(B*time),
		A*math.sin(time) - d*math.sin(B*time)
		)

def parametricRose(radius, k, time):
	"""
	Calculate a point on a parametric Rose curve with the given radius and
	number of petals at the given time.
	"""
	c = math.cos(k*time) * radius
	return c * Vector2D(math.cos(time), math.sin(time))

def parametricGear(radius, n, b, time):
	"""
	Calculate a point on a parametric Gear curve with the given radius,
	number of teeth, and tooth depth / gear offset at the given time.
	"""
	r = 1 + 1/b*math.tanh(b*math.sin(n*time))
	return r * Vector2D(math.cos(time), math.sin(time))

def parametricLGerono(radius, time):
	"""
	Calculate a point on a parametric Lemniscate of Gerono with the given 
	radius at the given time.
	"""
	return Vector2D(math.cos(time), math.sin(2*time)/2)

def parametricLBernoulli(radius, time):
	"""
	Calculate a point on a parametric Lemniscate of Bernoulli with the given
	radius at the given time.
	"""
	A = a*math.sqrt(2)*math.cos(time)/(math.sin(time)**2 + 1)
	return Vector2D(A, A*math.sin(time))