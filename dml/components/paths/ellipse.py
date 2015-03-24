from ...maths import (
	parametricEllipse, parametricSuperEllipse, 
	parametricHippopede, parametricCassini)
from .arc import ArclikePathElement

class _EllipticPathElement(ArclikePathElement):

	"""
	Base PathElement for elliptic shapes.
	"""

	def initialize(self, **config):
		super().initialize(**config)
		self.hradius = config["hradius"]
		self.vradius = config["vradius"]

		self.pivot = self._PARAMETRIC_FUNCTION(
			self.hradius, self.vradius, self.initial_angle)

	def updateDisplacement(self):
		"""
		Update this PathElement's displacement.
		"""
		self.displacement = self._PARAMETRIC_FUNCTION(
			self.hradius, self.vradius, self.current_angle) - self.pivot
		self.current_angle += self.speed

		self._transition()

		self._checkDone()

class EllipsePathElement(_EllipticPathElement):

	"""
	A PathElement that represents motion in an ellipse.
	"""

	_PARAMETRIC_FUNCTION = parametricEllipse

class SuperEllipsePathElement(_EllipticPathElement):

	"""
	A PathElement that represents motion in a super-ellipse.
	"""

	def initialize(self, **config):
		super().initialize(**config)
		self.exponent = config["exponent"]

		self.pivot = parametricSuperEllipse(
			self.hradius, self.vradius, self.exponent, self.current_angle)

	def updateDisplacement(self):
		"""
		Update this PathElement's displacement.
		"""
		self.displacement = parametricSuperEllipse(
			self.hradius, self.vradius, self.exponent, self.current_angle) - self.pivot
		self.current_angle += self.speed

		self._transition()

		self._checkDone()


class HippopedePathElement(_EllipticPathElement):

	"""
	A PathElement that represents motion in a hippopede.
	"""

	_PARAMETRIC_FUNCTION = parametricHippopede


class CassiniOvalPathElement(_EllipticPathElement):

	"""
	A PathElement that represents motion in a Cassini oval.
	"""

	_PARAMETRIC_FUNCTION = parametricCassini