from ...timeline import *
from ...maths    import Vector2D
from ...core     import globalSystem

from ..motion import Motion

class Path(Motion):

	"""
	A component describing the motion of a bullet as a piecewise
	path of vector-valued functions called PathElements.
	"""

	def initialize(self, **config):
		super().initialize(**config)
		self._elements = []
		self._current_element = 0

	def addPathElement(self, path_element):
		"""
		Add a PathElement to this path.
		"""
		self._elements.append(path_element)
		path_element.setParent(self)

	def getCurrentElement(self):
		"""
		Return the current PathElement.
		"""
		return self._elements[self._current_element]

	def forceNext(self):
		"""
		Force the path to move to the next PathElement, regardless of whether
		or not the current one is done.
		"""
		self._current_element += 1

	def _move(self):
		# Do nothing if there are no PathElements left to perform.
		if self._current_element >= len(self._elements):
			return

		current_element = self._elements[self._current_element]
		current_element.updateTimeline()
		self.displacement = current_element.getDisplacement()

		if current_element.done:
			# Move to the next PathElement if the current one is done and
			# there are PathElements left in the list.
			self._current_element += 1
			if self._current_element < len(self._elements):
				self._elements[self._current_element].setOrigin(
					self.displacement)
				self._elements[self._current_element].timeline.begin()

	def isFinished(self):
		"""
		Check if this path is finished (i.e. there are no more PathElements
		left to perform).
		"""
		return self.current_element > len(self._elements)

class PathElement(object):

	"""
	Base class for all PathElements used by the Path component.
	"""

	def __init__(self, **config):
		# The ``done`` flag tells the Path component that this
		# PathElement is complete, and it can move on to the next
		# one.
		self.done = False

		# The origin is the origin of this PathElement's local coordinate
		# space.
		self.origin = Vector2D.origin

		# The displacement is this PathElement's displacement relative to
		# its local coordinate space.
		self.displacement = Vector2D.origin
		self.initialize(**config)

		self.timeline = Timeline()

		self.local_time = 0

		self.parent = None

	def initialize(self, **config):
		"""
		Initialize this PathElement.
		"""
		pass

	def withTimeline(self, *events):
		"""
		Add a timeline of events to this PathElement.
		"""
		for event in events:
			self.timeline.addTimestamp(event)

	def setParent(self, path):
		"""
		Set this PathElement's parent Path component.
		"""
		self.parent = path

	def setOrigin(self, origin):
		"""
		Set the origin for this PathElement.
		"""
		self.origin = origin

	def getDisplacement(self):
		"""
		Return this PathElement's displacement.
		"""
		if not self.done:
			self.updateDisplacement()
		self.local_time += globalSystem._timestep
		return self.displacement + self.origin

	def updateTimeline(self):
		"""
		Perform the next event in this PathElement's timeline.
		"""
		self.timeline.doNext(self.local_time, self)

	def updateDisplacement(self):
		"""
		Update this PathElement's displacement.
		"""
		raise NotImplementedError

	def forceEnd(self):
		"""
		Force this element to end.
		"""
		self.done = True


class CompoundElement(PathElement):
	
	"""
	A PathElement that compounds multiple PathElements of different types
	into a single PathElement.
	"""

	def __init__(self, *elements):
		super().__init__()
		self.elements = elements

	def updateDisplacement(self):
		"""
		Update this PathElement's displacement.
		"""
		sum = Vector2D.origin
		self.done = True
		for element in self.elements:
			if not element.done:
				self.done = False
			sum += element.getDisplacement()
		self.displacement = sum


class StaticPathElement(PathElement):

	"""
	A PathElement that represents a single point in space. It tells the
	Path component to stay still and do nothing for the given duration.
	"""

	def initialize(self, **config):
		self.duration = config["duration"]
		self._current_time = 0

	def updateDisplacement(self):
		"""
		Update this PathElement's displacement.
		"""
		self._current_time += globalSystem._timestep
		if self._current_time >= self.duration:
			self.done = True