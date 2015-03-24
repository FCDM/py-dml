import scipy.integrate

# from .reparametrize import Reparametrizer
from .geometry import Vector2D
from .rkode import RKODE
from .gquad import gaussianQuadrature
from .misc import binomialCoefficient

def bezier(control_points, time):
	"""Calculate a point on a bezier curve."""
	sum = Vector2D.origin
	n = len(control_points)
	t2 = 1 - time
	for k in range(n):
		sum += time**k*t2**(n - 1 - k)*binomialCoefficient(n - 1, k) * control_points[k]
	return sum

def bezierDerivative(control_points, time):
	"""Calculate the derivative of a bezier curve at the given time."""
	return (len(control_points) - 1)*(bezier(control_points[1:], time) - bezier(control_points[:-1], time))

def bezierArclength(control_points, time=1):
	"""Calculate the arclength of a bezier curve from the start to the given time."""
	f = lambda t: bezierDerivative(control_points, t).magnitude()
	return gaussianQuadrature(f, 0, time)

def compositeBezierArclength(control_polygon, weight_polygon):
	"""
	Calculate the total arclength of a composite cubic bezier curve.
	"""
	total_distance = 0
	for i in range(len(control_polygon) - 1):
		total_distance += bezierArclength([
				control_polygon[i],
				control_polygon[i] + weight_polygon[i],
				control_polygon[i + 1] - weight_polygon[i + 1],
				control_polygon[i + 1]
			])
	return total_distance