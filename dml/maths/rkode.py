class RKODE(object):
	"""
	A Runge-Kutta Ordinary Differential Equation solver.
	"""

	def __init__(self, function, step_size, initial_t, initial_y):
		print("RKODE __init__ sent : ", function, step_size, initial_t, initial_y)
		self.step_size = step_size
		self._tn = initial_t
		self._yn = initial_y
		self._f = function

	def getCurrent(self):
		"""Return the current approximation."""
		return self._yn

	def getNext(self):
		"""Get the next approximation."""
		self._tn += self.step_size
		k1 = self._f(self._tn, self._yn)
		k2 = self._f(self._tn + self.step_size/2, self._yn + 1/2*k1*self.step_size)
		k3 = self._f(self._tn + self.step_size/2, self._yn + 1/2*k2*self.step_size)
		k4 = self._f(self._tn + self.step_size, self._yn + k3*self.step_size)

		self._yn += self.step_size/6*(k1 + 2*k2 + 2*k3 + k4)
		return self._yn

	def reverse(self):
		"""Reverse the step direction."""
		self.step_size *= -1