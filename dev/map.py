



class Map:

	def __init__(self, width, height):

		self.width  = width
		self.height = height
		self.blobs  = []
		self.numPlayers = 0
		self.numResources = 0
		self.currentId = 1

	def addBlob(self, blob):
		blob.id = self.currentId;
		self.currentId += 1
		self.blobs.append(blob)

	def addPlayer(self, player):
		player.id = self.currentId
		self.currentId += 1
		self.blobs.append(player)
		self.numPlayers += 1

	def addResource(self, resource):
		resource.id = self.currentId
		self.currentId += 1
		self.blobs.append(resource)
		self.numResources += 1

	def validPosition(self, pos):
		if (0 < pos[0] < self.width) and (0 < pos[1] < self.height):
			return True
		return False

	def moveBlob(self, blob, new_pos):
		if (0 < new_pos[0] < self.width) and (0 < new_pos[1] < self.height):
			blob.xy = new_pos
			return True
		return False

