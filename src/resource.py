from random import randint, uniform

class Resource:
  def __init__(self, xy, radius, value):
    self.xy = xy
    self.color = (0,255,0)
    self.radius = radius
    self.value = value
    self.name  = 'res'

  def change_pos(self, new_x, new_y):
    self.xy = (new_x, new_y)

  def updatePos(self):
    pass

class CenaBoost:
  def __init__(self, xy, radius):
    self.xy = xy
    self.color = (0, 0, 255)
    self.radius = radius
    self.name = "CENA"
    self.songfile = "songs\\CENA.mp3"

  def change_pos(self, new_x, new_y):
    self.xy = (new_x, new_y)

class ResourceFactory:
  def __init__(self, map, maxResources=2000):
    self.map = map
    self.minValue = .05
    self.maxValue = .11
    self.maxResources = maxResources

  #initially populate the map with resources
  def createInitialResources(self):
    self.createResource(self.maxResources/2)

  #generate a number of resources
  def generateResources(self, numResources):
    numNeedResources = self.maxResources - numResources;
    for i in range(numNeedResources/self.maxResources):
      self.map.addResource(self.createResource())

  #randomly create a default resource
  def createResource(self, N=1):
    n = min(N, self.maxResources - len(self.map.resources))
    for i in range(n):
      while True:
        x = uniform(0, self.map.width)
        y = uniform(0, self.map.height)
        if self.map.validPosition((x,y)):
          value = uniform(self.minValue, self.maxValue)
          self.map.addResource(Resource((x,y), value, value))
          break

  #create a default resource in a given area
  def createResourceInArea(self, pos, dim, N=1):
    n = min(N, self.maxResources - len(self.map.resources))
    for i in range(n):
      while True:
        x = uniform(int(pos[0]), int(pos[0] + dim[0]))
        y = uniform(int(pos[1]), int(pos[1] + dim[1]))
        if self.map.validPosition((x,y)):
          value = uniform(self.minValue, self.maxValue)
          self.map.addResource(Resource((x,y), value, value))
          break

  #create a randomly placed, specifically valued resource
  def createResourceWithValue(self, value):
    while True:
      x = randint(0, self.map.width)
      y = randint(0, self.map.width)
      if self.map.validPosition((x,y)):
        return Resource((x,y), value, value)

  def createResourceInAreaWithValue(self, pos, dim, value):
    while True:
      x = randint(pos[0], pos[0] + dim[0])
      y = randint(pos[1], pos[1] + dim[1])
      if self.map.validPosition((x,y)):
        return Resource((x,y), value, value)