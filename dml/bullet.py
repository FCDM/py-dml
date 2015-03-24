import pygame
import random

from .components import *

from .utils    import getBasesLinear
from .core     import globalSystem
from .maths    import Vector2D


class Bullet(object):
	"""
	The most basic bullet object representable in DML. Every
	projectile, weapon, generator, or particle effect is a
	child class of Bullet.

	The Bullet class provides methods of attaching components
	to an object such that the functionality of the component
	can be used to describe the behaviour of the bullet.
	"""

	# The size of a random name.
	_RAND_NAME_SIZE = 16**10

	def __init__(self, origin, name=None, **config):
		super().__init__()
		if name is None:
			# Generate a random name if none is given.
			name = "%010x" % random.randrange(Bullet._RAND_NAME_SIZE)
		self.name = name

		# The origin is the origin of this bullet's local coordinate space
		# relative to the world coordinate space. A bullet's position in the
		# its local coordinate space is its 'position' attribute, but its
		# position in the world coordinate space is the sum of its origin
		# and its position.
		self.origin = Vector2D(origin)
		self.position = self.origin

		# The current displacement is what motion components affect. It represents
		# the next position the bullet will move to, relative to its local coordinate
		# space.
		self._current_displacement = Vector2D.origin

		self.local_time = 0

		self._dead = False

		# Components are stored in a dictionary where the keys are the classes of the
		# components and the values are a list of all components of that type attached
		# to this bullet. This is so that we can say self.getComponent(Parent) and get
		# all components whose parent class Parent, rather than just all components of
		# type Parent.
		self._components = {}

		# Auto components are components that update themselves regardless of a 
		# bullet's ``update`` method.
		self._auto_components = []

		self.initialize(**config)

		globalSystem.addBullet(self)

	def initialize(self, **config):
		"""Extra initialization. Use this to add components to a bullet."""
		pass

	def addComponent(self, component):
		"""Add a component to this bullet."""
		component = component.withBullet(self)
		for base in getBasesLinear(type(component), Component):
			self._components.setdefault(base, []) \
						    .append(component)

		if component.AUTOMATIC:
			self._auto_components.append(component)

	def getComponent(self, componentType):
		"""
		Get a single component.

		If multiple of the same component exist, the one that was
		first created is returned.

		If the component does not exist, None will be returned.
		"""
		components = self._components.get(componentType)
		if components is None:
			return components
		return components[0]

	def getComponents(self, componentType):
		"""Get a list of components."""
		return self._components.get(componentType, [])

	def forEach(self, componentType):
		"""
		Return a list of components for which to call a method on each.

		The use case for this method is as follows:

		====

		self.forEach(ComponentType).methodName(*args, **kwargs)

		====

		The above code is functionally equivalent to the following code:

		====

		for component in self.getComponents(ComponentType):
			component.methodName(*args, **kwargs)

		====
		"""
		return ComponentListCaller(self._components[componentType])

	def getFromEach(self, componentType):
		"""
		Return a list of components for which to obtain a common attribute from each.

		The use case for this method is as follows:

		====
		```

		attributes = self.getFromEach(ComponentType).attributeName

		```
		====

		The above code is functionally equivalent to the following code:

		====

		attributes = []
		for component in self.getComponents(ComponentType):
			attributes.append(component.attributeName)

		====
		"""
		return ComponentListGetter(self._components[componentType])

	def After(self, time):
		"""
		Return True if the local time is after the given time.
		"""
		return self.local_time > time

	def Before(self, time):
		"""
		Return True if the local time is before the given time.
		"""
		return self.local_time < time

	def From(self, start, end):
		"""
		Return True if the local time is between the given start and end times.
		"""
		return start <= self.local_time < end

	def At(self, time):
		"""
		Return True once at the given time.
		"""
		return self.From(time, time + globalSystem._timestep)

	def AtIntervals(self, interval, start=0, end=float('inf')):
		"""
		Return True at given intervals.
		"""
		return 0 <= self.local_time % interval < globalSystem._timestep \
			   and self.local_time >= start \
			   and self.local_time <= end

	def isDead(self):
		"""Check if this bullet is dead or not."""
		return self._dead

	def kill(self):
		"""Set this bullet as dead."""
		self._dead = True

	def _update(self):
		"""Internal update."""
		self.update()
		for component in self._auto_components:
			component._auto()
		self.local_time += globalSystem._timestep

	def update(self):
		"""External update. Describe your bullet's functionality here."""
		pass

	def render(self):
		"""Activate all Render components."""
		for component in self.getComponents(Render):
			component.render()

	def move(self):
		"""Activate all Motion components."""
		for component in self.getComponents(Motion):
			component.moveBullet()
		self.position = self.origin + self._current_displacement
		self._current_displacement = Vector2D.origin