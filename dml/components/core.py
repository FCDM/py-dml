class ComponentError(Exception):
	"""
	An error thrown if a component's requirements aren't all met.
	"""
	pass

class ConfigurationError(Exception):
	"""
	An error thrown if the configuration of a component is incorrect.
	"""
	pass

class Component(object):

	"""
	Basic component object.

	Components describe functionality which can be applied to
	bullets to aid in describing their behaviour.
	"""

	REQUIREMENTS = []
	CONFLICTS = []

	SINGLETON = False
	AUTOMATIC = False

	def __init__(self, **config):
		self._config = config
		self.bullet = None

	def withBullet(self, bullet):
		"""Initialize this component with a bullet instance."""

		# Check if the requirements are met.
		for req in self.REQUIREMENTS:
			if bullet.getComponents(req) == []:
				raise ComponentError(
					"%s component requires %s." % (
						self.__class__.__name__,
						req.__class__.__name__
					)
				)

		# Check if any conflicting components exist.
		for con in self.CONFLICTS:
			if bullet.getComponents(con):
				raise ComponentError(
					"%s component conflicts with %s." % (
						self.__class__.__name__,
						con.__class__.__name__
						)
					)

		# Check if the bullet already has this component.
		if self.SINGLETON and bullet.getComponents(self.__class__):
			raise ComponentError(
				"%s component cannot be duplicated." % (
					self.__class__.__name__
					)
				)

		self.bullet = bullet
		self.initialize(**self._config)
		return self

	def initialize(self, **config):
		"""Extra initialization specific to the component class."""
		pass

	def _auto(self):
		"""Automatically update the component (Internal)."""
		pass


class _ComponentList(object):

	"""Maintains a list of components (Internal)."""
	
	def __init__(self, components):
		self._components = components

class ComponentListCaller(_ComponentList):

	"""
	Used by Bullet.forEach to call a method on a set of components (Internal).
	"""

	def __init__(self, components):
		super().__init__(components)
		self._attr = None
		self._callable = False

	def __getattr__(self, name):
		self._callable = True
		self._attr = name
		return self

	def __call__(self, *args, **kwargs):
		if self._callable:
			attrs = []
			for component in self._components:
				attrs.append(getattr(component, self._attr)(*args, **kwargs))
			self._callable = False
			return attrs
		else:
			raise ComponentError("No bound method to apply to components.")

class ComponentListGetter(_ComponentList):

	"""
	Used by Bullet.getFromEach to return a common 
	element from a list of components (Internal).
	"""

	def __getattr__(self, name):
		attrs = []
		for component in self._components:
			attrs.append(getattr(component, name))
		return attrs