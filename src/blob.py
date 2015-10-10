import random



class Blob:

	def __init__(self, xy=[400,200], radius = 20):

		self.xy  = xy
		self.radius = radius
		self.xAccel = 0
		self.yAccel = 0

	def accelerateX(self, num):
		if -5 < self.xAccel < 5:
			self.xAccel += num
		else:
			print "Error with x accel"

	def accelerateY(self, num):
		if -5 < self.xAccel < 5:
			self.yAccel += num
		else:
			print "Error with y accel"

	def deccelX(self):
		if self.xAccel > 0: self.xAccel -= 1
		elif self.xAccel < 0: self.xAccel += 1

	def deccelY(self):
		if self.yAccel > 0: self.yAccel -= 1
		elif self.yAccel < 0: self.yAccel += 1


	def updatePos(self):
		xy = self.xy
		xy[0] += self.xAccel
		xy[1] += self.yAccel
		return xy