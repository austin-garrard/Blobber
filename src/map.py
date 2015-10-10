



class Map:

	def __init__(self, width, height):

		self.width  = width
		self.height = height
		self.blobs  = []
		self.resources = []

	def addBlob(self, blob):
		self.blobs.append(blob)
	def addBlobs(self, blobs):
		self.blobs.extend(blobs)
	def addResource(self, resource):
		self.resources.append(resource)

	def validPosition(self, pos):
		if (0 < pos[0] < self.width) and (0 < pos[1] < self.height):
			return True
		return False

	def moveBlob(self, blob, new_pos):
		if (0 < new_pos[0] < self.width) and (0 < new_pos[1] < self.height):
			blob.xy = new_pos
			return True
		return False

