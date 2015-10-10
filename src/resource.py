from random import randint

class Resource:
  def __init__(self, xy, radius, value):
    self.xy = xy
    self.radius = radius
    self.value = value





class ResourceFactory:
  def __init__(self, map, maxResources=2000):
    self.map = map
    self.minValue = .05
    self.maxValue = .11
    self.maxResources = maxResources

  #initially populate the map with resources
  def createInitialResources(self):
    for i in range(self.maxResources/2):
      self.map.addResource(self.createResource())

  #generate a number of resources
  def generateResources(self, numResources):
    numNeedResources = self.maxResources - numResources;
    for i in range(numNeedResources/self.maxResources):
      self.map.addResource(self.createResource())

  #randomly create a default resource
  def createResource(self):
    while True:
      x = randint(0, int(self.map.width))
      y = randint(0, int(self.map.width))
      if self.map.validPosition((x,y)):
        value = randint(int(self.minValue*100), int(self.maxValue*100))/100.0
        return Resource((x,y), value, value)

  #create a default resource in a given area
  def createResourceInArea(self, pos, dim, n=1):
    for i in range(n):
      while True:
        x = randint(int(pos[0]), int(pos[0] + dim[0]))
        y = randint(int(pos[1]), int(pos[1] + dim[1]))
        if self.map.validPosition((x,y)):
          value = randint(int(self.minValue*100), int(self.maxValue*100))/100.0
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