



class Map:

	def __init__(self, width=10000, height=10000):

		self.width  = width
		self.height = height
		self.blobs  = []

	def addBlob(self, blob):
		self.blobs.append(blob)
	def addBlobs(self, blobs):
		self.blobs.extend(blobs)

	def moveBlob(self, blob, new_pos):
		if (0 < new_pos[0] < self.width) and (0 < new_pos[1] < self.height):
			blob.xy = new_pos
			return True
		return False

