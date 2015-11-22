import socket
import math, time
import select
from blob import Blob
import game
import sys, traceback
import pygame

class BlobberClient:

	def __init__(self, addr, port):
		self.addr    = addr
		self.port    = port
		self.timeout = 1
		self.sock    = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((addr, port))
		self.sock.setblocking(1)
		self.id      = 0
		self.init_done = False

		#game stuff
		self.myBlob = None
		self.blobs  = {}
		self.resources = []
		self.screen = None
		self.MU     = 100.0
		self.viewPortSize = (800,600)

	def send(self, msg):
		messageSize = len(msg)
		self.sock.send("%d|%s" % (messageSize,msg))

	def receive(self):
		data = ''
		nextByte = ''
		while nextByte != '|':
			nextByte = self.sock.recv(1)
			data += nextByte
		messageSize = int(data[:-1])
		message = self.sock.recv(messageSize)
		return message

	def interp_blobs(self):
		for b in self.blobs:
			self.blobs[b].update()

	def sync_blobs(self, blobs):
		self.blobs = blobs

	def parseMessage(self, message):
		msg = message.split('|')

		#if msg[0] == 'syncBlobs':
		#	self.sync_blobs(game.blobsFromString(msg[1]))

		if msg[0] == 'init':
			print '!!!', msg[1]
			initMsg = msg[1].split('#')
			print '###', initMsg

			# init my blob
			self.myBlob = game.blobFromString(initMsg[0])
			self.id = self.myBlob.game_id
			self.blobs[self.id] = self.myBlob

			# init resources
			resourcesStrings = initMsg[1]
			for r in resourcesStrings.split(' '):
				print '\t', r
				tmp = game.resourceFromString(r)
				if tmp is not None:
					self.resources.append(tmp)


			self.init_done = True
			print "our blob is %s" % self.myBlob
			#print self.resources

		elif msg[0] == "updateBlobs":
			self.blobs = game.blobsFromString(msg[1])

		else:
			print 'undefined message %s' % msg[0]

	def draw_all(self):

		for blob in self.blobs:
			b = self.blobs[blob]
			pygame.draw.circle(self.screen, b.color, (int(b.x), int(b.y)), int(b.radius), 0)

		for res in self.resources:
			pygame.draw.circle(self.screen, res.color, (res.x, res.y), res.radius, 0)


	def run(self):
		done = False
		time.sleep(.1)
		print "sending init"
		self.send('init')
		msg = self.receive()
		self.parseMessage(msg)
		#self.sock.close()
		#return
		try:
			#initialize game-window stuff
			pygame.init()

			self.screen = pygame.display.set_mode(self.viewPortSize)

			while not done and self.init_done:
				#drawing the game
				for e in pygame.event.get():
					if e.type == pygame.QUIT:
						done = True

					#self.interp_blobs()
				msg = self.receive()
				self.parseMessage(msg)
				self.screen.fill((255,255,255))
				self.draw_all()
				mouse_pos = pygame.mouse.get_pos()
				self.send("updateBlob|%d|%s" % (self.id, mouse_pos))

				pygame.display.update()

				#server message checks
				#readReady, writeReady, exception = select.select([self.sock], [self.sock], [], self.timeout)
				#if len(readReady) != 0:
				#	print "received a message"
				#	msg = self.receive()
				#	print msg
				#	self.parseMessage(msg)

				#elif (len(writeReady) != 0) and self.init_done and (time.time()-sync_time) >= .1:
				#	msg = "updateBlob|%s" % (game.blobToString(self.myBlob))
				#	self.send(msg)


		except:
			print '\nUnhandled exception. Terminating.', sys.exc_info()[1]
			print traceback.format_exc()



if __name__ == "__main__":
	client = BlobberClient("localhost", 17098)
	print "running client"
	client.run()