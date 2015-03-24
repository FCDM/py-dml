import warnings
import math

from ...maths import *
from ..core import *
from .core import *
from .common import AcceleratableElement


class _BezierBasePathElement(AcceleratableElement):

	"""
	An internal base class for BezierPathElements and ReparametrizableBezierPathElements.
	"""

	def initialize(self, **config):
		control_polygon = list(map(Vector2D, config["controlPolygon"]))
		if len(control_polygon) < 2:
			raise ConfigurationError(
				"Must have at least 2 points in controlPolygon.")

		# We need to store a separate time parameter because a bezier
		# curve ranges from t = 0 to 1.
		initial_time = config.get("initialTime", 0)
		duration = config.get("duration")

		# The number of times to repeat traversal of the path.
		repeats = config.get("repeatCount", 1)

		self.control_polygon = control_polygon
		self.duration = duration
		self._time = initial_time

		self._transition_time = 0
		self._transition_amount = 0

		self.repeats = repeats
		self._current_iteration = 0

class BezierPathElement(_BezierBasePathElement):

	"""
	A PathElement that represents motion in a bezier curve of variable degree.
	"""

	def initialize(self, **config):
		super().initialize(**config)
		duration = self.duration
		if duration is not None:
			# If a duration was set, define the speed.
			speed = (1 - self._time)/duration * globalSystem._timestep
		else:
			# Else, find the speed in the config.
			if "speed" in config:
				speed = config["speed"]
			else:
				speed = config["initialSpeed"]
		self.speed = speed

	def updateDisplacement(self):
		"""
		Update this PathElement's displacement.
		"""
		self.displacement = bezier(self.control_polygon, self._time)

		self._time += self.speed

		# Transition the speed (if necessary)
		self._transition()

		if self.duration is not None:
			# If we have completed a single iteration.
			if self._time >= 1 or self._time <= 0 and self._current_iteration < self.repeats:
				self._current_iteration += 1
				# Reversing the control polygon reverses the direction of traversal of
				# the bezier curve.
				self.control_polygon = self.control_polygon[::-1]
				self._time = 0

			# If we have completed all iterations.
			if self._current_iteration == self.repeats:
				self.done = True


# class ReparametrizableBezierPathElement(_BezierBasePathElement):

# 	def initialize(self, **config):
# 		super().initialize(**config)

# 		if self.duration is None:
# 			# This is really arbitrary. Figure out what you want to do here.
# 			self.duration = 1
# 		duration = self.duration

# 		arclength = bezierArclength(self.control_polygon)
# 		self.arclength = arclength

# 		reparametrization = config.get("reparametrization")

# 		if reparametrization == "fixed":
# 			# reparametrization = lambda t : 10*math.sin(t/10)
# 			reparametrization = lambda t : 1
		
# 		print("Here's some shit.")
# 		print()
# 		for i in range(100):
# 			print(bezierDerivative(self.control_polygon, i/100).magnitude())
# 		print()

# 		# Normalize the reparametrzation so that its integral is equal to the
# 		# arclength of the bezier curve.
# 		# 
# 		# Here's a piece of confusing math. In ``normalizeParametrization`` the second
# 		# parameter is the arclength. So why wouldn't we want to send the arclength of
# 		# the bezier curve in as that parameter? Well, I'm not entirely sure.
# 		reparametrization = normalizeParametrization(reparametrization, 0, 1)

# 		step_size = arclength / duration * globalSystem._timestep

# 		self.reparametrization = BezierReparametrizer(
# 			self.control_polygon, reparametrization, step_size, 
# 			initial=bezierArclength(self.control_polygon, self._time)
# 			)

# 	def stop(self):
# 		"""Completely hault all motion."""
# 		self.reparametrization.step_size = 0
# 		self._transition_time = 0

# 	def setSpeed(self, speed):
# 		"""Set a new speed."""
# 		self.reparametrization.step_size = speed * self.arclength / self.duration \
# 												 * globalSystem._timestep
# 		self._transition_time = 0

# 	def transitionToSpeed(self, new_speed, time):
# 		"""Smoothly transition to a new speed over a given period of time."""
# 		new_speed = new_speed * self.arclength / self.duration * globalSystem._timestep
# 		self._transition_amount = (
# 			new_speed - self.speed) / time * globalSystem._timestep
# 		self._transition_time = time

# 	def _transition(self):
# 		"""
# 		Update the speed if we are in the middle of transitioning.
# 		"""
# 		if self._transition_time > 1e-9:  # Accounts for floating point errors
# 			self.reparametrization.step_size += self._transition_amount
# 			self._transition_time -= globalSystem._timestep

# 	def updateDisplacement(self):
# 		"""
# 		Update this PathElement's displacement.
# 		"""
# 		self.displacement = self.reparametrization.getNext()

# 		# self._time += self.reparametrization._yn

# 		# Transition the speed (if necessary)
# 		self._transition()

# 		# If we have completed a single iteration.
# 		if self._time >= 1 or self._time < 0:
# 			self._current_iteration += 1
# 			# Reversing the control polygon reverses the direction of traversal of
# 			# the bezier curve.
# 			# self.reparametrization.reverse()
# 			# self._time = 0

# 		# If we have completed all iterations.
# 		if self._current_iteration == self.repeats:
# 			self.done = True



class CompositeBezierPathElement(PathElement):
	
	def initialize(self, **config):
		self.control_polygon = list(map(Vector2D, config["controlPolygon"]))

		if len(self.control_polygon) < 2:
			raise ConfigurationError(
				"Must have at least 2 points in controlPolygon.")

		self.weight_polygon  = list(map(Vector2D, config["weightPolygon"]))

		if len(self.weight_polygon) != len(self.control_polygon):
			raise ConfigurationError(
				"weightPolygon and controlPolygon must have the same number of points.")

		self.duration = config["duration"]

		self._max_time = len(self.control_polygon) - 1
		self._speed = self._max_time/self.duration * globalSystem._timestep
		self._time = 0

		self._origin = Vector2D.origin

		self._current_bezier_num = 1
		self._current_bezier = current_bezier = [
			self.control_polygon[0],
			self.control_polygon[0] + self.weight_polygon[0],
			self.control_polygon[1] - self.weight_polygon[1],
			self.control_polygon[1]
			]

		fixed_speed = config.get("fixedSpeed", False)
		if fixed_speed:
			warnings.warn(
				"Fixed speed traversal of bezier curves is " \
				"an expensive operation. Do not use in excess.")
			self._distance_increment = compositeBezierArclength(
				self.control_polygon, self.weight_polygon) \
				/ self.duration * globalSystem._timestep
			# Runge-Kutta ODE solver.
			self._rkode = inverseBezier(self._current_bezier, step_size=self._distance_increment)
		self.fixed_speed = fixed_speed

		self.repeats = config.get("repeatCount", 1)
		self._current_iteration = 0
		self._reverse = False

	def setOrigin(self, origin):
		self._origin = origin

	def getDisplacement(self):
		if self.done:
			return self._displacement + self._origin

		self._displacement = bezier(self._current_bezier, self._time)

		if self.fixed_speed:
			self._time = self._rkode.getNext()
		else:
			if self._reverse:
				self._time -= self._speed
			else:
				self._time += self._speed

		# UGHH comment this trash later please
		if (self._time < 0 and self._reverse) or (self._time > 1 and not self._reverse):
			if self._reverse:
				self._current_bezier_num -= 1
			else:
				self._current_bezier_num += 1
			if self._current_bezier_num == len(self.control_polygon) or self._current_bezier_num == 0:
				self._current_iteration += 1
				self._reverse = not self._reverse
				if self._current_iteration == self.repeats:
					self.done = True
				if self._reverse:
				 	self._current_bezier_num -= 1
				else:
				 	self._current_bezier_num += 1
				if self.fixed_speed:
					self._rkode.reverse()
			else:
				n = self._current_bezier_num - 1
				self._current_bezier = current_bezier = [
					self.control_polygon[n],
					self.control_polygon[n] + self.weight_polygon[n],
					self.control_polygon[n + 1] - self.weight_polygon[n + 1],
					self.control_polygon[n + 1]
					]
				if self.fixed_speed:
					if self._reverse:
						self._rkode = inverseBezier(
							self._current_bezier, step_size=-self._distance_increment, initial=1)
					else:
						self._rkode = inverseBezier(
							self._current_bezier, step_size=self._distance_increment)
			if self._reverse:
				self._time = 1
			else:
				self._time = 0
		return self._displacement + self._origin