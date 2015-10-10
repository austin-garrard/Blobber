import random
import math


class Blob:

	def __init__(self, xy=[40.0,20.0], radius = .2, color = (255,255,0)):

		self.name         = 'blob'
		self.xy           = xy
		self.radius       = radius
		self.xAccel       = 0.0
		self.yAccel       = 0.0
		self.color        = color
		self.aRate        = .0001
		self.maxAccel     = .2
		self.maxDiagAccel = self.maxAccel/math.sqrt(2.0)
		self.movingDiag   = False

	def change_pos(self, x_new, y_new):
		self.xy[0] = x_new
		self.xy[1] = y_new

	def sign(self,number):return cmp(number,0)

	def accelerateX(self, s):
		if self.movingDiag: accel = self.maxDiagAccel
		else: accel = self.maxAccel
		if self.sign(s) != self.sign(self.xAccel):
			self.xAccel = 0.0 + s*self.aRate
		else:
			if -1.0*accel < self.xAccel < accel:
				self.xAccel += s*self.aRate

	def accelerateY(self, s):
		if self.movingDiag: accel = self.maxDiagAccel
		else: accel = self.maxAccel
		if self.sign(s) != self.sign(self.yAccel):
			self.yAccel = 0.0 + s*self.aRate
		else:
			if -1.0*accel < self.yAccel < accel:
				self.yAccel += s*self.aRate


	def deccelX(self):
		if int(self.xAccel*100) == 0: self.xAccel = 0.0
		elif int(self.xAccel*100) > 0.0: self.xAccel -= self.aRate
		elif int(self.xAccel*100) < 0.0: self.xAccel += self.aRate
	def deccelY(self):
		if int(self.yAccel*100) == 0: self.yAccel = 0.0
		elif int(self.yAccel*100) > 0.0: self.yAccel -= self.aRate
		elif int(self.yAccel*100) < 0.0: self.yAccel += self.aRate



	def updatePos(self):
		xy = list(self.xy)
		xy[0] += self.xAccel
		xy[1] += self.yAccel
		return xy

	def update(self):
		self.maxAccel = math.exp((-1*self.radius))*0.0183
		self.maxDiagAccel = self.maxAccel/(math.sqrt(2.0))

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
		#self.radius = math.sqrt(self.radius**2 + blob.radius**2)
		#self.update()
		pass

			