import dml
from dml.components import *

import random

dml.globalSystem.setFPS(30)
dml.globalSystem.setDimensions((600, 800))


class Bullet1(dml.extras.DirectionalCircleShot):

	CONFIGURATION = {
		'colour' : (0x00, 0x00, 0x84),
		'radius' : 5
	}

	def initialize(self, **config):
		super().initialize(**config)
		self.accelerator = LinearAccelerator(initialSpeed=8, direction=self.direction)
		self.addComponent(self.accelerator)
		self.final_speed = (random.random() + 1)*4

	def update(self):
		self.render()
		self.move()

		if self.At(0.25):
			self.accelerator.transitionToSpeed(0, 0.5)

		if self.At(1.5):
			self.accelerator.transitionToSpeed(self.final_speed, 0.5)
			self.accelerator.rotate(random.random()*0.3)

class Generator1(dml.Bullet):

	def initialize(self, **config):
		self.shooter = LinearShooter(direction=config["direction"], bulletType=Bullet1)
		self.addComponent(self.shooter)

	def update(self):
		if self.AtIntervals(0.02):
			for i in range(3):
				self.shooter.fire()
			self.shooter.rotate(0.1*math.sin(self.local_time/2))

Generator1((300, 400), direction=(0, 1))
Generator1((300, 400), direction=(1, 0))
Generator1((300, 400), direction=(0,-1))
Generator1((300, 400), direction=(-1,0))

dml.globalSystem.run()

# import cProfile
# cProfile.run("dml.globalSystem.run()")