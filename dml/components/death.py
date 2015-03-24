from ..core import globalSystem
from .core import *

class DieIfOffscreen(Component):

	"""
	An automatic component that kills the bullet if it goes
	off-screen.
	"""

	AUTOMATIC = True

	def initialize(self, **config):
		# The amount of leeway the bullet has when determining if it is
		# offscreen or not. If its value is 100, then the bullet can move
		# 100 pixels offscreen before dying.
		self.leeway = config.get("leeway", 10)

		# Remember the dimensions so we don't keep recalculating them every frame.
		dimensions = globalSystem.getDimensions()
		self._xrange = (-self.leeway, dimensions[0] + self.leeway)
		self._yrange = (-self.leeway, dimensions[1] + self.leeway)

	def _auto(self):
		x, y = self.bullet.position
		if not (self._xrange[0] <= x <= self._xrange[1] and \
				self._yrange[0] <= y <= self._yrange[1]):
			self.bullet.kill()

class DieIfAfter(Component):

	"""
	An automatic component that kills the bullet after a
	given amount of time.
	"""

	AUTOMATIC = True

	def initialize(self, **config):
		# The time after which to kill the bullet.
		self.time = config["time"]

	def _auto(self):
		if self.bullet.local_time > self.time:
			self.bullet.kill()