import math
import time



class Blob:

	def __init__(self, name, x, y, radius, color, game_id, direction=[1.0,1.0], velocity=1.0, timestamp=time.time()):

		self.name      = name
		self.game_id   = game_id
		self.x         = x
		self.y         = y
		self.radius    = radius
		self.color     = color
		self.direction = direction
		self.velocity  = velocity
		self.maxV      = math.log(self.radius ** 2)*100
		self.accel     = self.maxV*0.1 * 10
		self.timestamp = timestamp

	def update(self):

		t      = time.time() - self.timestamp
		self.x += self.velocity*self.direction[0]*t + ((self.direction[0] * self.accel * (t ** 2)) / 2)
		self.y += self.velocity*self.direction[1]*t + ((self.direction[1] * self.accel * (t ** 2)) / 2)
		self.velocity  = min(self.velocity + self.accel*t, self.maxV)
		self.timestamp = time.time()
		#print self.x,self.y,self.velocity

	def updateDirection(self, mouse_pos):
		magnitude = math.sqrt((mouse_pos[0]-self.x) ** 2 + (mouse_pos[1] - self.y) ** 2)
		self.direction = [(mouse_pos[0] - self.x)/(magnitude), (mouse_pos[1] - self.y)/(magnitude)]
