import math

from ...core import globalSystem
from ..core import ComponentError, ConfigurationError
from .core import PathElement

class TimeBasedElement(PathElement):
	"""
	A PathElement that is either based off of time or not.
	"""

	def _timeBasedError(self):
		if self.duration is not None:
			raise ComponentError(
				"Cannot change the speed of time-based ArcPathElement.")

class AcceleratableElement(TimeBasedElement):
	"""
	A PathElement that has an acceleratable speed.
	"""

	def stop(self):
		"""Completely hault all motion."""
		self._timeBasedError()

		self.speed = 0
		self._transition_time = 0

	def setSpeed(self, speed):
		"""Set a new speed."""
		self._timeBasedError()

		self.speed = speed
		self._transition_time = 0

	def transitionToSpeed(self, new_speed, time):
		"""Smoothly transition to a new speed over a given period of time."""
		self._timeBasedError()

		self._transition_amount = (
			new_speed - self.speed) / time * globalSystem._timestep
		self._transition_time = time

	def reverse(self):
		"""Reverse the direction of motion."""
		self._timeBasedError()
		self.speed *= -1

	def _transition(self):
		"""
		Update the speed if we are in the middle of transitioning.
		"""
		if self._transition_time > 1e-9:  # Accounts for floating point errors
			self.speed += self._transition_amount
			self._transition_time -= globalSystem._timestep

def getArcConfig(config):
	"""
	Parse the configuration for an arc-like PathElement.

	The return value is a 5-tuple containing the initial angle, the final 
	angle, the duration, the speed, and the repeat count in that order.
	"""
	# The configuration scheme is as follows:
	# radius & initialAngle & (speed | (duration & (finalAngle | arcLength)))
	radians = config.get("radians", True)
	initial_angle = config.get("initialAngle", 0)
	if not radians:
		initial_angle = math.radians(initial_angle)

	duration = config.get("duration")
	if duration is not None:
		repeats  = config.get("repeatCount", 1)
		
		final_angle = config.get("finalAngle")
		arc_length  = config.get("arcLength")

		if (final_angle is None) == (arc_length is None):
			raise ConfigurationError(
				"Either only ``final_angle`` or ``arc_length`` must be "\
				"defined if ``duration`` is defined.")

		if final_angle is not None:
			if not radians:
				final_angle = math.radians(final_angle)
			speed = (final_angle - initial_angle) / duration
		else:
			if not radians:
				arc_length = math.radians(arc_length)
			speed = arc_length / duration
			final_angle = arc_length - initial_angle
		speed *=  globalSystem._timestep
	else:
		if "speed" in config:
			speed = config["speed"]
		else:
			speed = config["initialSpeed"]
		# It seems arbitrary to divide by 100, but this approximately normalizes
		# the speed so that a speed of 1 in an ArcPathElement has the same velocity
		# as a speed of 1 in a LinearPathElement.
		speed /= 100
		repeats = 1
		final_angle = None
	return initial_angle, final_angle, duration, speed, repeats