import scipy.integrate
import scipy.special
import math

from ..newton import newtonRaphson
from .basic import clampf

def linearTransition(x1=0, x2=1, y1=0, y2=1):
	slope = (y2 - y1)/(x2 - x1)
	return clampf(lambda t : (t - x1)*slope + y1, x1, x2)

def sineSquaredTransition(x1=0, x2=1, y1=0, y2=1):
	dx = math.pi/(2*(x2 - x1))
	dy = y2 - y1
	return clampf(lambda t : dy * math.sin((t - x1)*dx)**2 + y1)

def betaDistributionTransition(alpha, x1=0, x2=1, y1=0, y2=1):
	c = math.sqrt(math.pi)*2**(1 - 2*alpha)*math.gamma(alpha)/math.gamma(alpha + .5)
	dx = x2 - x1
	dy = y2 - y1
	alpha -= 1
	integrand = lambda t: (t*(1 - t))**alpha
	return clampf(lambda t: dy/c*scipy.integrate.quad(integrand, 0, (t - x1)/dx)[0] + y1, x1, x2)

# mutagrade - muta ('changeable') + grade ('slope')
def mutagradeTransition(slope, x1=0, x2=1, y1=0, y2=1):
	"""
	Return a beta distribution transition with an appropriate alpha value such
	that its slope at t = (x2 - x1)/2 is equal to the given slope.
	"""
	alpha = newtonRaphson(
		lambda t: 2*math.gamma(t + .5)/math.sqrt(math.pi)/math.gamma(t) - slope,
		lambda t: math.sqrt(math.pi)*math.gamma(t)/(2*math.gamma(t + .5) \
			* (scipy.special.digamma(t + .5) - scipy.special.digamma(t))),
		initial_guess=slope,
		error=1e-7)
	return betaDistributionTransition(alpha, x1, x2, y1, y2)