import pygame
import random
import math

from ..utils import mergeDicts
from ..core  import globalSystem
from ..maths import *

from .utils  import *
from .core   import *

class LinearShooter(Component):

	"""
	A component that allows a bullet to fire other bullets linearly.
	"""

	def initialize(self, **config):
		# The type of bullet to be spawned.
		self.bulletType = config["bulletType"]

		# The direction at which to spawn bullets.
		self.direction = getDirectionOrAngle(config)

		# Any extra configuration for each bullet.
		self._extra_config = config.get("bulletConfig", {})

	def rotate(self, amount, radians=True):
		"""Rotate the direction in which to shoot."""
		self.direction = self.direction.rotate(amount, radians=radians)

	def fire(self, **extra_config):
		"""Spawn a new bullet in the given direction and return it."""
		config = mergeDicts(self._extra_config, extra_config)
		new_bullet = self.bulletType(self.bullet.position, direction=self.direction, **config)
		return new_bullet

