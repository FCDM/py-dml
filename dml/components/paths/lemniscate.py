from ...maths import parametricLGerono, parametricLBernoulli
from .arc import ArclikePathElement

class _LemniscatePathElement(ArclikePathElement):

	"""
	Base PathElement for lemniscates.
	"""

	_PARAMETRIC_FUNCTION = None

	def initialize(self, **config):
		super().initialize(**config)
		self.radius = config["radius"]

	def updateDisplacement(self):
		self.displacement = self._PARAMETRIC_FUNCTION(self.radius, self.current_angle)
		self.current_angle += self.speed

		self._transition()

		self._checkDone()

class LemniscateGeronoPathElement(ArclikePathElement):

	"""
	A PathElement that represents motion in the shape of the Lemniscate of 
	Gerono.
	"""

	_PARAMETRIC_FUNCTION = parametricLGerono

class LemniscateBernoulliPathElement(ArclikePathElement):

	"""
	A PathElement that represents motion in the shape of the Lemniscate of
	Bernoulli.
	"""

	_PARAMETRIC_FUNCTION = parametricLBernoulli