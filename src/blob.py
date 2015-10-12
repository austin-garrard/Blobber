import random
import math


class Blob(object):

	def __init__(self, xy=[40.0,20.0], radius = .2, color = (255,255,0)):

		self.id 			= -1 # assigned when added to map
		self.xy       = xy
		self.radius   = radius
		self.xAccel   = 0.0
		self.yAccel   = 0.0
		self.color    = color
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

	def getDistBetween(self, blob):
		return math.sqrt((self.xy[0] - blob.xy[0])**2 + (self.xy[1] - blob.xy[1])**2)

	def canEat(self, blob):
		if self.radius*(0.9) > blob.radius:
			ratio    = (1-(blob.radius**2)/(self.radius**2))
			dist     = self.getDistBetween(blob)
			if dist < ratio*self.radius:
				return True
			else:
				return False
		return False

	def eat(self, blob):
		self.radius = math.sqrt(self.radius**2 + blob.radius**2)

			