class SingletonError(Exception):
	"""
	An error thrown upon trying to instantiate another instance of a Singleton
	class. For more information, see SingletonMeta.
	"""
	pass

class SingletonMeta(type):
	"""
	A class for which only one instance can be created.

	If the class' has a static __strict__ attribute whose value is True,
	then a SingletonError will be thrown upon trying to instantiate a
	second instance. By default __strict__ is True. If it is False, then
	the original instance is returned upon intantiation.
	"""

	def __new__(metacls, name, bases, kwargs):
		kwargs["__instance__"] = None
		kwargs.setdefault("__strict__", True)
		return super().__new__(metacls, name, bases, kwargs)

	def __call__(cls, *args, **kwargs):
		if cls.__instance__ is None:
			cls.__instance__ = cls.__new__(cls, *args, **kwargs)
			cls.__instance__.__init__(*args, **kwargs)
		elif cls.__strict__:
			raise SingletonError(
				"Singleton class %s already instantiated." % cls.__name__)
		return cls.__instance__