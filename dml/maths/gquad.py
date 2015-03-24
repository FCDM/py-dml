def gaussianQuadrature(function, a, b):
	"""
	Perform a Gaussian quadrature approximation of the integral of a function
	from a to b.
	"""
	# Coefficient values can be found at pomax.github.io/bezierinfo/legendre-gauss.html
	A = (b - a)/2
	B = (b + a)/2
	return A * (
		0.2955242247147529*function(-A*0.1488743389816312 + B) + \
		0.2955242247147529*function(+A*0.1488743389816312 + B) + \
		0.2692667193099963*function(-A*0.4333953941292472 + B) + \
		0.2692667193099963*function(+A*0.4333953941292472 + B) + \
		0.2190863625159820*function(-A*0.6794095682990244 + B) + \
		0.2190863625159820*function(+A*0.6794095682990244 + B) + \
		0.1494513491505806*function(-A*0.8650633666889845 + B) + \
		0.1494513491505806*function(+A*0.8650633666889845 + B) + \
		0.0666713443086881*function(-A*0.9739065285171717 + B) + \
		0.0666713443086881*function(+A*0.9739065285171717 + B)
		)