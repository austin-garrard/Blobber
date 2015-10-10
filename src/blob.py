import random
import math


class Blob:

	def __init__(self, xy=[40.0,20.0], radius = .2, color = (255,255,0)):

		self.xy  = xy
		self.radius = radius
		self.xAccel = 0.0
		self.yAccel = 0.0
		self.color  = color
		self.mass   = (self.radius**2)*math.pi

	def sign(self,number):return cmp(number,0)

	def accelerateX(self, num):
		if self.sign(num) != self.sign(self.xAccel):
			self.xAccel = 0.0 + num
		else:
			if -.05 < self.xAccel < .05:
				self.xAccel += num

	def accelerateY(self, num):
		if self.sign(num) != self.sign(self.yAccel):
			self.yAccel = 0.0 + num
		else:
			if -.05 < self.yAccel < .05:
				self.yAccel += num


	def deccelX(self):
		if int(self.xAccel*100) > 0.0: self.xAccel -= 0.001
		elif int(self.xAccel*100) < 0.0: self.xAccel += 0.001

	def deccelY(self):
		if int(self.yAccel*100) > 0.0: self.yAccel -= 0.001
		elif int(self.yAccel*100) < 0.0: self.yAccel += 0.001



	def updatePos(self):
		xy = self.xy
		xy[0] += self.xAccel
		xy[1] += self.yAccel
		return xy

	def update(self):
		self.mass = (self.radius**2)*math.pi