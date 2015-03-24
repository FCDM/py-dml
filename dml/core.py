import pygame

from . import utils
from . import timeline


class DMLSystemError(Exception):
	pass


class _DMLSystem(object, metaclass=utils.SingletonMeta):
	"""
	The system which runs the simulation.

	All the bullets are stored here, and are created, updated
	and destroyed automatically as per the specified behaviour
	of the bullet.
	"""

	def __init__(self):
		self._dim = None
		self._fps = None
		self._timestep = None

		self.global_frame = 0
		self.global_time = 0

		self._running = False

		self._bullets = {}
		self._to_delete = []
		self._to_add = []
		self._timeline = timeline.Timeline()

		self.screen = None

	def _checkRunning(self):
		"""Check if the system is running and throw an error if so."""
		if self._running:
			raise DMLSystemError(
				"Cannot change system components when running.")

	def setDimensions(self, dimensions):
		"""Set the dimensions of the screen."""
		self._checkRunning()
		self._dim = dimensions

	def setFPS(self, integer):
		"""Set the FPS of the system."""
		self._checkRunning()
		self._fps = integer
		self._timestep = 1 / self._fps

	def getDimensions(self):
		"""Return the dimensions."""
		return self._dim

	def getFPS(self):
		"""Return the FPS."""
		return self._fps

	def addBullet(self, bullet):
		"""Add a bullet to the system."""
		if self._running:
			self._to_add.append(bullet)
		else:
			self._bullets[bullet.name] = bullet

	def deleteBullet(self, bullet_name):
		"""Delete a bullet from the system by its name."""
		if self._running:
			self._to_delete.append(bullet_name)
		else:
			del self._bullets[bullet_name]

	def getBullet(self, bullet_name):
		"""Retrieve a bullet by its name or None if it doesn't exist."""
		return self._bullets.get(bullet_name)

	def addTimestamp(self, timestamp):
		"""Add a timestamp to the system."""
		self._timeline.addTimestamp(timestamp)

	def run(self):
		"""Run the system."""
		self._timeline.begin()

		if not self._dim:
			raise DMLSystemError("Dimensions not set.")
		if not self._fps:
			raise DMLSystemError("FPS not set.")

		pygame.init()

		self.screen = pygame.display.set_mode(self._dim)
		clock = pygame.time.Clock()

		self._running = True

		while self._running:

			self.screen.fill((0, 0, 0))
			
			for evt in pygame.event.get():
				if evt.type == pygame.QUIT:
					self._running = False

			# Do the next event in the timeline.
			self._timeline.doNext(self.global_time)

			# Update the bullets
			for bullet in self._bullets.values():
				bullet._update()
				if bullet.isDead():
					self._to_delete.append(bullet.name)

			# Remove dead bullets
			for name in self._to_delete:
				del self._bullets[name]

			# Add new bullets
			for bullet in self._to_add:
				self._bullets[bullet.name] = bullet

			# Refresh deleted bullet and new bullet lists.
			self._to_delete = []
			self._to_add = []

			pygame.display.update()
			clock.tick(self._fps)

			self.global_frame += 1
			self.global_time += self._timestep

		pygame.quit()


globalSystem = _DMLSystem()
