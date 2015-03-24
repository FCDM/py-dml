from ...maths import Vector2D
from ...core  import globalSystem

from ..utils import getDirectionOrAngle
from ..core  import *
from .core import PathElement
from .common import *

_INF = float('inf')

class LinearPathElement(AcceleratableElement):

	"""
	A PathElement that represents linear motion.
	"""

	def initialize(self, **config):
		direction = getDirectionOrAngle(config, return_none=True)

		# If ``duration`` is defined, then the path is determined by
		# a finite duration of time and a number determine how many
		# times to repeat. The path also has a fixed speed.
		# 
		# If ``duration`` is not defined, then the path is determined
		# by a direction, has a varying speed, and lasts an infinite
		# length of time until forceEnd or forceNext is called.
		duration = config.get("duration")

		# I'm just gonna assume you can figure out what's going on here
		# based on the exception messages.
		if duration is not None:
			repeats  = config.get("repeatCount", 1)

			finalPoint = config.get("finalPoint")

			if direction == finalPoint == None:
				raise ConfigurationError(
					"Either ``direction`` or ``finalPoint`` must be " \
					"defined if ``timeBased`` is True.")

			distance = config.get("distance")

			if direction is None and distance is not None:
				raise ConfigurationError(
					"``finalPoint`` and ``distance`` cannot both be " \
					"defined simultaneously.")
			elif finalPoint is None and distance is None:
				raise ConfigurationError(
					"``distance`` must be defined if ``direction`` is defined.")

			if finalPoint:
				speed = finalPoint.magnitude() / duration * globalSystem._timestep
				direction = finalPoint.normalize()
			else:
				speed = distance / duration * globalSystem._timestep

		else:
			repeats  = 1

			if direction is None:
				raise ConfigurationError(
					"If ``timeBased`` is False, ``direction`` must be defined.")
			if "speed" in config:
				speed = config["speed"]
			else:
				speed = config["initialSpeed"]

		self.speed = speed
		self.direction = direction

		self.duration = duration
		self.repeats  = repeats
		# The current iteration number increases up to the given number
		# of repeats.
		self._current_iteration = 0

		self._transition_time = 0
		self._transition_amount = 0

	def rotate(self, amount, radians=True):
		"""Rotate the direction."""
		self.direction = self.direction.rotate(amount, radians=radians)

	def changeDirection(self, direction):
		"""Change the direction."""
		self.direction = Vector2D(*direction).normalize()

	def takeAim(self):
		"""Aim directly at the player (the mouse)."""
		self.direction = (Vector2D(*pygame.mouse.get_pos()) - self.bullet.position).normalize()

	def updateDisplacement(self):
		"""
		Update this PathElement's displacement.
		"""
		self.displacement += self.speed * self.direction

		if self._transition_time > 1e-9:  # Accounts for floating point errors
			self.speed += self._transition_amount
			self._transition_time -= globalSystem._timestep

		if self.duration is not None:
			# If we have completed one iteration (from (0, 0) to finalPoint)
			if self.local_time > (self._current_iteration + 1) * self.duration:

				self._current_iteration += 1
				self.direction *= -1

			# If we have repeated as many times as desired, then we are finished.
			if self._current_iteration == self.repeats:
				self.done = True