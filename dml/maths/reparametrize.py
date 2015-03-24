"""
This file includes a set of functions and classes that aid in
reparametrizing parametric curves.
"""
import scipy.integrate

from .newton import approximateInverse
from .rkode import RKODE

def normalizeArclengthParametrization(parametrization, derivative, t_min, t_max):
	"""
	Normalize an arclength parametrization of a curve.
	"""
	arclength = scipy.integrate(lambda t : derivative(t).magnitude(), t_min, t_max)
	return lambda t : arclength * parametrization

class ArclengthReparametrizer(RKODE):

	"""
	An RKODE that reparaemtrizes a 2-dimensional parametric curve with an
	arclenght parametrization.
	"""

	def __init__(self, curve, derivative, reparametrization, step_size):
		initial_distance = reparametrization(0)
		# To find the initial time value we have to use a different method of approximating
		# the inverse of the arclength function. Otherwise we would have to use another RKODE,
		# which would be infinite recursion.
		initial_time = approximateInverse(lambda t : t)
		super().__init__(lambda y, t : 1/derivative(y).magnitude(), step_size, initial_distance)
		self._reparam = reparametrization
