from random import randint, uniform
from blob import Blob

class Resource(Blob):
  def __init__(self, value, xy=[40.0,20.0], radius = .2, color = (255,255,0)):
    super(Resource, self).__init__(xy, radius, color)
    self.value = value


class ResourceFactory:
  def __init__(self, map, maxResources=2000):
    self.map = map
    self.minValue = .05
    self.maxValue = .11
    self.maxResources = maxResources

  #initially populate the map with resources
  def createInitialResources(self):
    self.createResource(self.maxResources/2)

  #randomly create a default resource
  def createResource(self, N=1):
    n = min(N, self.maxResources - self.map.numResources)
    newBlobs = []
    for i in range(n):
      while True:
        x = uniform(0, self.map.width)
        y = uniform(0, self.map.width)
        if self.map.validPosition((x,y)):
          value = uniform(self.minValue, self.maxValue)
          r = Resource(value, [x,y], value, (0,255,0))
          newBlobs.append(r)
          self.map.addResource(r)
          break
    return newBlobs

