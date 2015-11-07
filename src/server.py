import socket
import threading
import math
import time
import select
import Queue
from blob import Blob
import game
import sys, traceback

class BlobberServer:

	#opens the socket for the server
	def __init__(self, port=17098):
		self.connections = [] #all of our server threads
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(("", self.port))
		self.id_iter = 0
		self.game_thread = GameThread(self.connections)

	#runs the thread
	def run(self):
		done = False

		while not done:
			self.sock.listen(5)
			sock,addr = self.sock.accept()
			print "we got a connection"

			#spawn a thread to handle the connection
			th = ConnectionThread(sock, addr, self.id_iter, self.game_thread)
			print "started connection thread"
			self.id_iter += 1
			self.connections.append(th)
			th.start()

class GameThread(threading.Thread):

	def __init__(self, connections):
		self.connections = connections
		self.blobs       = {}

	def newBlob(self, blob, id):
		self.blobs[id] = blob

	def updateBlob(self, blob, id):
		self.blobs[id] = blob

	def parseMessage(self, message):
		msg = message.split(' ')

		if msg[0] == 'newBlob':
			self.newBlob(game.blobFromString(msg[2]), msg[1])

		elif msg[0] == 'updateBlob':
			self.updateBlob(game.blobFromString(msg[2]), msg[1])

		else:
			print "Error with parsing connection message"

	def checkBlob(self, blob):
		if blob.x > 100:
			blob.x = 100

	def run(self):
		for blob in self.blobs:
			blob.update()
			checkBlob(blob)
		updated_blobs = game.blobsToString(self.blobs)
		for connection in self.connections:
			connection.queue.put("updateBlobs %s" % (game.blobsToString(blobs)))



class ConnectionThread(threading.Thread):

	def __init__(self, sock, addr, id, game_thread):
		super(ConnectionThread, self).__init__()
		self.sock    = sock
		self.addr    = addr
		self.game_thread = game_thread
		self.id      = id
		self.timeout = 1
		self.queue   = Queue.Queue()
		self.sock.setblocking(0)

	def send(self, msg):
		messageSize = len(msg)
		self.sock.send("%d %s" % (messageSize,msg))
		print msg

	def receive(self):
		data = ''
		nextByte = ''
		while nextByte != ' ':
			nextByte = self.sock.recv(1)
			data += nextByte
		messageSize = int(data)
		message = self.sock.recv(messageSize)
		return message

	def run(self):
		done = False
		try:
			while not done:
				print "starting select"
				readReady, writeReady, exception = select.select([self.sock], [self.sock], [], self.timeout)
				if len(readReady) != 0:
					print "received a message"
					msg = self.receive()
					game_thread.parseMessage(msg)
				

				elif len(writeReady) != 0:
					print "sending a message"
					while not self.queue.empty():
						msg = self.queue.get()
						self.send(msg)
						print msg
		except:
			print '\nUnhandled exception. Terminating.', sys.exc_info()[1]
			print traceback.format_exc()

if __name__ == "__main__":
	print "starting server..."
	server = BlobberServer(17098)
	server.run()