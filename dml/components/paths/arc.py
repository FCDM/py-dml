import math

from ...maths import *
from ...core  import globalSystem
from ..core import *
from .core import PathElement
from .common import *

class ArclikePathElement(AcceleratableElement):

	"""
	Base class for arc-like PathElements.
	"""

	def initialize(self, **config):
		# Parse the config and unpack it.
		initial_angle, final_angle, duration, speed, repeats = getArcConfig(config)

		self.current_angle = initial_angle
		self.initial_angle = initial_angle
		self.final_angle = final_angle

		self.duration = duration
		self.speed = speed

		self.repeats = repeats
		# The current iteration number increases up to the given number
		# of repeats.
		self._current_iteration = 0

		self._transition_time = 0
		self._transition_amount = 0

	# We have to override setSpeed and transitionToSpeed because we have
	# to divide the speed by 100 to normalize it. For more information,
	# see the second comment in getArcConfig.

	def setSpeed(self, speed):
		"""Set a new speed."""
		self._timeBasedError()

		self.speed = speed/100
		self._transition_time = 0

	def transitionToSpeed(self, new_speed, time):
		"""Smoothly transition to a new speed over a given period of time."""
		self._timeBasedError()

		self._transition_amount = (
			new_speed/100 - self.speed) / time * globalSystem._timestep
		self._transition_time = time

	def _checkDone(self):
		if self.duration is not None:
			# If we've completed one iteration.
			if self.current_angle >= self.final_angle or self.current_angle <= self.initial_angle:
				self._current_iteration += 1
				self.speed *= -1

			# If we've completed all iterations.
			if self._current_iteration == self.repeats:
				self.done = True

class ArcPathElement(ArclikePathElement):

	"""
	A PathElement that represents motion in an arc (circle sector).
	"""

	def initialize(self, **config):
		super().initialize(**config)
		
		radius = config["radius"]
		self.radius = radius

		self.pivot = parametricCircle(radius, self.initial_angle)

	def updateDisplacement(self):
		"""
		Update this PathElement's displacement.
		"""
		self.displacement = parametricCircle(self.radius, self.current_angle) - self.pivot
		self.current_angle += self.speed

		# Transition the speed (if necessary)
		self._transition()

		self._checkDone()


class EpitrochoidPathElement(ArclikePathElement):

	"""
	A PathElement that represents motion in an epitrochoid sector.
	"""

	def initialize(self, **config):
		super().initialize(**config)

		self._R = config["innerRadius"]
		self._r = config["outerRadius"]
		self._d = config["armRadius"]

		self.pivot = parametricEpitrochoid(self._R, self._r, self._d, self.initial_angle)

		# This part normalizes the speed relative to the periodicity of the
		# epitrochoid. An epitrochoid is periodic in 2*ri*pi, where ri is the
		# numerator of r as an integer ratio.
		duration = self.duration
		if duration is not None:
			arclength = self.final_angle - self.initial_angle
			periodicity = float(self._r).as_integer_ratio()[0]
			self.speed = arclength / duration * periodicity * globalSystem._timestep


	def updateDisplacement(self):
		"""
		Update this PathElement's displacement.
		"""
		self.displacement = parametricEpitrochoid(
			self._R, self._r, self._d, self.current_angle) - self.pivot
		self.current_angle += self.speed

		# Transition the speed (if necessary)
		self._transition()

		self._checkDone()


class LimaconPathElement(EpitrochoidPathElement):

	"""
	A PathElement that represents motion in a Limaçon sector.
	"""

	def initialize(self, **config):
		# A Limaçon is just an epitrochoid with outer radius = inner radius.
		config["outerRadius"] = config["radius"]
		config["innerRadius"] = config["radius"]
		super().initialize(**config)


class EpicycloidPathElement(EpitrochoidPathElement):

	"""
	A PathElement that represents motion in an epicycloid sector.
	"""

	def initialize(self, **config):
		# An epicycloid is just an epitrochoid with arm length = outer radius.
		config["armRadius"] = config["outerRadius"]
		super().initialize(**config)


class HypotrochoidPathElement(ArclikePathElement):

	"""
	A PathElement that represents motion in a hypotrochoid sector.
	"""

	def initialize(self, **config):
		super().initialize(**config)

		self._R = config["outerRadius"]
		self._r = config["innerRadius"]
		self._d = config["armRadius"]

		self.pivot = parametricHypotrochoid(self._R, self._r, self._d, self.initial_angle)

		# This part normalizes the speed relative to the periodicity of the
		# hypotrochoid. A hypotrochoid is periodic in 2*ri*pi, where ri is the
		# numerator of r as an integer ratio.
		duration = self.duration
		if duration is not None:
			arclength = self.final_angle - self.initial_angle
			periodicity = float(self._r).as_integer_ratio()[0]
			self.speed = arclength / duration * periodicity * globalSystem._timestep

	def updateDisplacement(self):
		"""
		Update this PathElement's displacement.
		"""
		self.displacement = parametricHypotrochoid(
			self._R, self._r, self._d, self.current_angle) - self.pivot
		self.current_angle += self.speed

		# Transition the speed (if necessary)
		self._transition()

		self._checkDone()


class HypocycloidPathElement(HypotrochoidPathElement):

	"""
	A PathElement that represents motion in a hypocycloid sector.
	"""

	def initialize(self, **config):
		# A hypocycloid is just a hypotrochoid with arm length = inner radius.
		config["armRadius"] = config["innerRadius"]
		super().initialize(**config)


class RosePathElement(ArclikePathElement):

	"""
	A PathElement that represents motion in a rose curve.
	"""

	def initialize(self, **config):
		super().initialize(**config)
		self.radius = config["radius"]
		self.petals = config["petals"]

		self.pivot = parametricRose(self.radius, self.petals, self.initial_angle)

	def updateDisplacement(self):
		"""
		Update this PathElement's displacement.
		"""
		self.displacement = parametricRose(
			self.radius, self.petals, self.current_angle) - self.pivot
		self.current_angle += self.speed

		self._transition()

		self._checkDone()


class GearPathElement(ArclikePathElement):

	"""
	A PathElement that represents motion in a gear curve.
	"""

	def initialize(self, **config):
		super().initialize(**config)
		self.radius = config["radius"]
		self.gear_teeth  = config["gearTeath"]
		self.gear_offset = config.get("gearOffset", 10)

		self.pivot = parametricGear(
			self.radius, self.gear_teeth, self.gear_offset, self.initial_angle)

	def updateDisplacement(self):
		"""
		Update this PathElement's displacement.
		"""
		self.displacement = parametricGear(
			self.radius, self.gear_teeth, self.gear_offset, self.current_angle) - self.pivot
		self.current_angle += self.speed

		self._transition()

		self._checkDone()