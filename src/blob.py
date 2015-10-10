import random
import math


class Blob:

	def __init__(self, xy=[40.0,20.0], radius = .2, color = (255,255,0)):

		self.xy       = xy
		self.radius   = radius
		self.xAccel   = 0.0
		self.yAccel   = 0.0
		self.color    = color
		self.mass     = (self.radius**2)*math.pi
		self.aRate    = .001
		self.maxAccel = .1551


	def sign(self,number):return cmp(number,0)

	def accelerateX(self, s):
		if self.sign(s) != self.sign(self.xAccel):
			self.xAccel = 0.0 + s*self.aRate
		else:
			if -1.0*self.maxAccel < self.xAccel < self.maxAccel:
				self.xAccel += s*self.aRate

	def accelerateY(self, s):
		if self.sign(s) != self.sign(self.yAccel):
			self.yAccel = 0.0 + s*self.aRate
		else:
			if -1.0*self.maxAccel < self.yAccel < self.maxAccel:
				self.yAccel += s*self.aRate


	def deccelX(self):
		if int(self.xAccel*100) == 0: self.xAccel = 0.0
		elif int(self.xAccel*100) > 0.0: self.xAccel -= .001
		elif int(self.xAccel*100) < 0.0: self.xAccel += .001
	def deccelY(self):
		if int(self.yAccel*100) == 0: self.yAccel = 0.0
		elif int(self.yAccel*100) > 0.0: self.yAccel -= .001
		elif int(self.yAccel*100) < 0.0: self.yAccel += .001



	def updatePos(self):
		xy = list(self.xy)
		xy[0] += self.xAccel
		xy[1] += self.yAccel
		return xy

	def update(self):
		self.mass = (self.radius**2)*math.pi