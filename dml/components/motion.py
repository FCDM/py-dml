import warnings
import pygame
import math

from ..maths import *
from ..core import globalSystem
from .core import *


class Motion(Component):

	"""
	Base motion component that alone does nothing. It is meant
	to be inherited by other components.
	"""

	def initialize(self, **config):
		self.displacement = Vector2D.origin

	def moveBullet(self):
		"""Move this component's associated bullet by the current displacement."""
		self.bullet._current_displacement += self.displacement
		self._move()

	def _move(self):
		"""Update this motion component (Internal)."""
		pass

class LinearAccelerator(Motion):

	"""
	A component describing the motion of a bullet as a straight line. It
	maintains a ``direction`` and ``speed`` attribute, which can both
	be altered at run-time.
	"""

	def initialize(self, **config):
		super().initialize(**config)
		self.speed = config["initialSpeed"]
		self.direction = Vector2D(*config["direction"]).normalize()

		# Auxiliary fields for transitioning to new speeds.
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

	def stop(self):
		"""Completely hault all motion."""
		self.speed = 0
		self._transition_time = 0

	def setSpeed(self, speed):
		"""Set a new speed."""
		self.speed = speed
		self._transition_time = 0

	def transitionToSpeed(self, new_speed, time):
		"""Smoothly transition to a new speed over a given period of time."""
		self._transition_amount = (
			new_speed - self.speed) / time * globalSystem._timestep
		self._transition_time = time

	def reverse(self):
		"""Reverse the direction of motion."""
		self.speed *= -1

	def _move(self):
		self.displacement += self.speed * self.direction
		
		if self._transition_time > 1e-9:  # Accounts for floating point errors
			self.speed += self._transition_amount
			self._transition_time -= globalSystem._timestep