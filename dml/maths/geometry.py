import math

class Vector2D(object):
	"""
	A vector in 2-dimensional space.
	"""

	def __init__(self, x, y=None):
		if y is None:
			x, y = x
		self.x = x
		self.y = y

	@classmethod
	def fromAngle(cls, angle, radians=True):
		"""Return the unit vector in the given direction."""
		if not radians:
			angle = math.radians(angle)
		return cls(math.cos(angle), math.sin(angle))


	def __repr__(self):
		return "Vector2D(%g, %g)" % (self.x, self.y)

	def __hash__(self):
		return hash((self.x, self.y))

	def __getitem__(self, key):
		if key == 0:
			return self.x
		return self.y

	def __iter__(self):
		return iter((self.x, self.y))

	def __pos__(self):
		return Vector2D(self.x, self.y)

	def __neg__(self):
		return Vector2D(-self.x, -self.y)

	def __add__(self, other):
		return Vector2D(self.x + other.x, self.y + other.y)

	__radd__ = __add__

	def __sub__(self, other):
		return Vector2D(self.x - other.x, self.y - other.y)

	def __rsub__(self, other):
		return Vector2D(other.x - self.x, other.y - self.y)

	def __mul__(self, other):
		return Vector2D(self.x*other, self.y*other)

	__rmul__ = __mul__

	def __div__(self, other):
		return Vector2D(self.x/other, self.y/other)

	__truediv__ = __div__

	def floor(self):
		"""Floor the components of this vector."""
		return Vector2D(int(self.x), int(self.y))

	def magnitude(self):
		"""Calculate the magnitude of this vector."""
		return math.sqrt(self.x*self.x + self.y*self.y)

	def magnitudeSquared(self):
		"""Calculate the squared magnitude of this vector."""
		return self.dot(self)

	def dot(self, other):
		"""Calculate the dot product of this vector and another."""
		return self.x*other.x + self.y*other.y

	def normalize(self):
		"""Return the normalization of this vector."""
		return self/self.magnitude()

	def lnormal(self):
		"""Return the left normal of this vector."""
		return Vector2D(self.y, -self.x)

	def rnormal(self):
		"""Return the right normal of this vector."""
		return vector2D(-self.y, self.x)

	def projectOnto(self, other):
		"""Return the projection of this vector onto another."""
		scalar = self.dot(other)/other.magnitudeSquared()
		return other*scalar

	def rotateRelative(self, angle, origin, radians=True):
		"""Rotate this vector relative to another by the given amount."""
		if not radians:
			angle = math.radians(angle)
		x, y = self

		x -= origin.x
		y -= origin.y

		cos_theta = math.cos(angle)
		sin_theta = math.sin(angle)

		nx = x*cos_theta - y*sin_theta
		ny = x*sin_theta + y*cos_theta

		return Vector2D(nx + origin.x, ny + origin.y)

	def rotate(self, angle, radians=True):
		"""Rotate this vector by the given amount."""
		if not radians:
			angle = math.radians(angle)
		x, y = self

		cos_theta = math.cos(angle)
		sin_theta = math.sin(angle)

		return Vector2D(x*cos_theta - y*sin_theta, x*sin_theta + y*cos_theta)

	def lerp(self, other, amount):
		"""Linearly interpolate between this vector and another."""
		return self + amount*(other - self)

	def angle(self, radians=True):
		"""
		Return the angle at which this vector points relative to the 
		positive x-axis.
		"""
		angle = math.atan2(self.y, self.x)
		if not radians:
			angle = math.degrees(angle)
		return angle


Vector2D.origin = Vector2D(0, 0)