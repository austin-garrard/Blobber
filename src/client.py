import socket
import math, time
import select
from blob import Blob
import game
import sys, traceback

class BlobberClient:

	def __init__(self, addr, port):
		self.addr    = addr
		self.port    = port
		self.timeout = 1
		self.sock    = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((addr, port))
		self.sock.setblocking(0)

		#game stuff
		self.myBlob = Blob("DEV", 5.0, 5.0, 10.0, (255,0,126), 0, [1.0,1.0],1)
		self.blobs  = [self.myBlob]

	def send(self, msg):
		messageSize = len(msg)
		self.sock.send("%d %s" % (messageSize,msg))

	def receive(self):
		data = ''
		nextByte = ''
		while nextByte != ' ':
			nextByte = self.sock.recv(1)
			data += nextByte
		messageSize = int(data)
		message = self.sock.recv(messageSize)
		return message

	def interp_blobs(self):
		for b in self.blobs:
			b.update()

	def sync_blobs(self):
		self.blobs = blobs

	def parseMessage(self, message):
		msg = message.split(' ')

		if msg[0] == 'syncBlobs':
			self.sync_blobs(game.blobsFromString(msg[1]))

		else:
			print 'undefined message %s' % msg[0]

	def draw(self):
		for blob in self.blobs:
			if blob.game_id == 0:
				print blob.x

	def run(self):
		done = False
		time.sleep(.1)
		self.send('newBlob %d %s' % (0, game.blobToString(self.myBlob)))
		try:
			while not done:
				readReady, writeReady, exception = select.select([self.sock], [self.sock], [], self.timeout)
				if len(readReady) != 0:
					print "received a message"
					msg = self.receive()
					self.parseMessage(msg)

				elif len(writeReady) != 0:
					msg = "updateBlob 0 %s" % (game.blobToString(self.myBlob))
					self.send(msg)

				self.interp_blobs()
				self.draw()
		except:
			print '\nUnhandled exception. Terminating.', sys.exc_info()[1]
			print traceback.format_exc()



if __name__ == "__main__":
	client = BlobberClient("localhost", 17098)
	print "running client"
	client.run()