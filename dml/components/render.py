import pygame
import math

from ..maths import Vector2D
from ..utils import lighten, darken
from ..core import globalSystem
from .core import *


class Render(Component):
	"""Represents anything that can be rendered."""

	def render(self):
		"""Render the bullet."""
		raise NotImplementedError()


class Circle(Render):
	"""Represents a coloured circle."""

	def initialize(self, **config):
		self.radius = config["radius"]
		self.colour = config["colour"]
		self._orig_radius = self.radius
		self._orig_colour = self.colour

	def scale(self, amount):
		"""Scale the renderer by the given amount."""
		self.radius = math.ceil(amount*self.radius)

	def setRadius(self, new_radius):
		"""Set a new radius."""
		self.radius = new_radius

	def resetRadius(self):
		"""Reset the radius to its original value."""
		self.radius = self._orig_radius

	def darken(self, amount):
		"""Darken the colour by a given amount."""
		self.colour = darken(self.colour, amount)

	def lighten(self, amount): 
		"""Lighten the colour by a given amount."""
		self.colour = lighten(self.colour, amount)

	def resetColour(self):
		"""Reset the colour."""
		self.colour = self._orig_colour

	def reset(self):
		"""Completely reset this renderer's attributes."""
		self.radius = self._orig_radius
		self.colour = self._orig_colour

	def render(self, offset=None):
		if offset is None:
			offset = Vector2D.origin
		else:
			offset = Vector2D(*offset)
		pygame.draw.circle(
			globalSystem.screen,
			self.colour,
			tuple((self.bullet.position + offset).floor()),
			self.radius
		)


class GlowingCircle(Circle):
	"""Represents a white circle with a coloured glow surrounding it."""

	def initialize(self, **config):
		super().initialize(**config)
		self.interior_colour = config.get("interiorColour", (255, 255, 255))
		self.glow_radius = config.get("glowRadius", 2)
		self._orig_glow_radius = self.glow_radius
		self._orig_interior = self.interior_colour

	def scale(self, amount):
		"""Scale the renderer by the given amount."""
		super().scale(amount)
		self.glow_radius = math.ceil(self.glow_radius*amount)

	def resetRadius(self):
		"""Reset the radius to its original value."""
		self.radius = self._orig_radius

	def darken(self, amount):
		"""Darken the colour by a given amount."""
		super().darken(amount)
		self.interior_colour = darken(self.interior_colour, amount)

	def lighten(self, amount):
		"""Lighten the colour by a given amount."""
		super().lighten(amount)
		self.interior_colour = lighten(self.interior_colour, amount)

	def resetColour(self):
		"""Reset the colour."""
		super().resetColour()
		self.interior_colour = self._orig_interior

	def reset(self):
		super().reset()
		self.glow_radius = self._orig_glow_radius
		self.interior_colour = self._orig_interior

	def render(self, offset=None):
		if offset is None:
			offset = Vector2D.origin
		else:
			offset = Vector2D(*offset)
		position = tuple((self.bullet.position - offset).floor())
		pygame.draw.circle(
			globalSystem.screen, self.colour, position, self.radius + self.glow_radius)
		pygame.draw.circle(
			globalSystem.screen, self.interior_colour, position, self.radius)