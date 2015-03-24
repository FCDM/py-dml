import pygame
import math
import enum

from ..core   import globalSystem
from ..bullet import *
from ..maths  import *
from ..components import *

def _getFromConfig(name, main_config, auxiliary_config, default=None, strict=True):
	if name in main_config:
		return main_config[name]
	elif name in auxiliary_config:
		return auxiliary_config[name]
	if strict:
		raise ConfigurationError(
			"Parameter %s not defined in static configuration "\
			"or instance configuration." % name)
	return default

def _getDirectionOrAngle(main_config, auxiliary_config, direction_name="direction", angle_name="angle"):
	direction = _getFromConfig(direction_name, main_config, auxiliary_config, strict=False)
	angle = _getFromConfig(angle_name, main_config, auxiliary_config, strict=False)
	return getDirectionOrAngle({direction_name : direction, angle_name : angle}, direction_name, angle_name)


class CircleShot(Bullet):

	"""
	A basic bullet that has a glowing circle component and dies if offscreen.
	"""

	CONFIGURATION = {}

	def initialize(self, **config):
		self.addComponent(GlowingCircle(
			radius=_getFromConfig('radius', self.CONFIGURATION, config),
			colour=_getFromConfig('colour', self.CONFIGURATION, config)
			))
		self.addComponent(DieIfOffscreen(leeway=10))

	def update(self):
		"""Update the bullet."""
		self.render()


class DirectionalShot(Bullet):
	"""
	A bullet with a required ``direction`` parameter.
	"""

	CONFIGURATION = {}

	def initialize(self, **config):
		self.direction = _getDirectionOrAngle(config, self.CONFIGURATION)


class DirectionalCircleShot(CircleShot):

	"""
	A circle shot with a direction.
	"""

	def initialize(self, **config):
		super().initialize(**config)
		self.direction = getDirectionOrAngle(config)

	def getDirection(self):
		"""Retrieve this bullet's direction."""
		return self.direction

	def rotate(self, amount, radians=True):
		"""Rotate this bullet's direction by the given amount."""
		self.direction = self.direction.rotate(amount, radians=radians)


class VelocityShot(DirectionalShot):
	"""
	A bullet with a required ``direction`` and ``speed`` parameter.
	"""

	CONFIGURATION = {}

	def initialize(self, **config):
		super().initialize(**config)
		self.speed = _getFromConfig('speed', config, self.CONFIGURATION)

	def getSpeed(self):
		"""Retrieve this bullet's speed."""
		return self.speed

	def getVelocity(self):
		"""Retrieve this bullet's velocity."""
		return self.speed * self.direction


class GatlingShot(VelocityShot):
	"""
	A VelocityShot variant with specific rendering capabilities.

	GatlingShots can be rendered in three different ways:

		Normal: Ordinary rendering using a GlowingCircle component.

		Stroboscopic: Ordinary rendering, but the bullet is rendered
			as if it were being captured by a stroboscopic flash camera.
			This gives it the effect of moving very fast.

		Diminishing Stroboscopic: Same as stroboscopic, but the radius
			of stroboscopic flashes diminishes over time.

	These correspond to the Enum values RenderType.NORMAL,
	RenderType.STROBOSCOPIC and RenderType.DIMINISHING_STROBOSCOPIC
	respectively.
	"""

	class RenderType(enum.Enum):
		"""
		An option determining how the gatling shot is to be rendered.
		"""

		NORMAL = 1
		STROBOSCOPIC = 2
		DIMINISHING_STROBOSCOPIC = 3

	CONFIGURATION = {}

	def initialize(self, **config):
		super().initialize(**config)

		self.addComponent(GlowingCircle(
			radius=_getFromConfig('radius', self.CONFIGURATION, config),
			colour=_getFromConfig('colour', self.CONFIGURATION, config)
			))

		self.addComponent(DieIfOffscreen(leeway=30))
		self.addComponent(LinearAccelerator(initialSpeed=self.speed, direction=self.direction))

		# Having references to components eliminates the time spent retrieving them
		# in the update method.
		self._drawer = self.getComponent(GlowingCircle)

		render_type = self.CONFIGURATION.get("renderType", GatlingShot.RenderType.NORMAL)

		if render_type is GatlingShot.RenderType.STROBOSCOPIC or \
		   render_type is GatlingShot.RenderType.DIMINISHING_STROBOSCOPIC:

			# GatlingShot bullets are rendered as if they were captured by a stroboscopic flash,
			# which gives it the effect of looking like its moving really fast when it really isn't.
			# The strobeInterval parameter determines how far apart individual strobe flashes are.
			# The higher this value is, the farther apart the strobe flashes are.
			self._strobe_interval = self.CONFIGURATION.get('strobeInterval', 15)

			# The number of strobe flashes.
			self._strobe_count = self.CONFIGURATION.get('strobeCount', 3)

			# The amount by which to darken the colour of the bullet per each strobe flash.
			self._darken = self.CONFIGURATION.get('darken', True)

			if self._darken:
				self._darken_amount = self.CONFIGURATION.get('darkenAmount', .5)
			else:
				self._lighten_amount = self.CONFIGURATION.get('lightenAmount', .5)

		if render_type is GatlingShot.RenderType.DIMINISHING_STROBOSCOPIC:

			# The amount by which to multiply the radius of strobe flashes by.
			self._retrograde_radius_multiplier = self.CONFIGURATION.get("radiusMultiplier", .5)
		else:
			self._retrograde_radius_multiplier = 1

		self._strobe_render = render_type is GatlingShot.RenderType.STROBOSCOPIC or \
							  render_type is GatlingShot.RenderType.DIMINISHING_STROBOSCOPIC

	def update(self):
		self.move()

		self._drawer.render()

		if self._strobe_render:
			# Render the stroboscopic effects.
			
			# Scale the radius of prior bullets.
			self._drawer.scale(self._retrograde_radius_multiplier)

			for i in range(1, self._strobe_count):
				# This check to see if the time is after 0.05 * i makes sure we
				# don't immediately render all the stroboscopic flashes. Trust me,
				# it would look stupid if we didn't do this.
				if self.After(0.05*i):
					if self._darken:
						self._drawer.darken(self._darken_amount)
					else:
						self._drawer.lighten(self._lighten_amount)
					# Render with an offset to create the trailing effect.
					self._drawer.render(self.direction * 2 * self._strobe_interval * i)
			# Reset the renderer's attributes.
			self._drawer.reset()

class Gatling(Bullet):

	"""
	A rapidly firing spawner that fires bullets randomly in a
	given range determined by a given probability distribution
	function.
	"""

	CONFIGURATION = {}

	def initialize(self, **config):
		# The type of bullet to spawn.
		self._bullet_type = _getFromConfig('bulletType', self.CONFIGURATION, config)

		# The angle at which to fire bullets
		direction = _getDirectionOrAngle(self.CONFIGURATION, config)
		self.angle = direction.angle()

		# The minimum angle of spread.
		self.min_angle = _getFromConfig('minAngle', self.CONFIGURATION, config)

		# The maximum angle of spread.
		self.max_angle = _getFromConfig('maxAngle', self.CONFIGURATION, config)

		# The density of bullets.
		self.density = _getFromConfig('bulletDensity', self.CONFIGURATION, config, default=1, strict=False)

		# The interval between spawning of each bullet.
		self.interval = _getFromConfig('spawnInterval', self.CONFIGURATION, config, default=0.01, strict=False)

		# The random distribution function.
		self._distribution = self.CONFIGURATION.get('distribution', random.uniform)

	def rotate(self, amount, radians=True):
		"""
		Rotate the angle by the given amount.
		"""
		if not radians:
			amount = math.radians(amount)
		self.angle += amount

	def rotateTo(self, angle, radians=True):
		"""
		Rotate to the new angle.
		"""
		if not radians:
			angle = math.radians(angle)
		self.angle = angle

	def update(self):
		if self.AtIntervals(self.interval):

			for i in range(self.density):

				direction = Vector2D.fromAngle(self.angle + \
					self._distribution(self.min_angle, self.max_angle) +\
					math.pi/2)
				self._bullet_type(self.position, direction=direction)


class AimedGatling(Gatling):

	"""
	A gatling that constantly rotates to aim at the player.
	"""

	def update(self):

		# Rotate to aim at the mouse.
		mx, my = pygame.mouse.get_pos()

		player_angle = math.atan2(
			my - self.position.y,
			mx - self.position.x) - math.pi/2

		self.rotateTo(player_angle)

		super().update()
