import math

from ..maths import Vector2D
from .core import ConfigurationError

def getDirectionOrAngle(config, direction_name='direction', angle_name='angle', return_none=False):
	direction = config.get(direction_name)
	angle     = config.get(angle_name)

	if return_none and direction == angle == None:
		return None

	if (direction is None) == (angle is None):
		raise ConfigurationError(
			"Either only ``direction`` or ``angle`` must be defined.")

	if direction is None:
		direction = Vector2D.fromAngle(angle, radians=config.get("radians", True))
	else:
		direction = Vector2D(*direction).normalize()
	return direction
