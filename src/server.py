import socket
import threading
import math
import time
import select
import Queue
from blob import Blob
import game
import sys, traceback
from ast import literal_eval as make_tuple

class BlobberServer:

	#opens the socket for the server
	def __init__(self, port=17098):
		self.connections = [] #all of our server threads
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(("192.168.1.103", self.port))
		self.id_iter = 1
		self.game_thread = GameThread(self.connections)

	#runs the thread
	def run(self):
		done = False
		self.game_thread.start()
		while not done:
			self.sock.listen(5)
			sock,addr = self.sock.accept()
			print "we got a connection"

			#spawn a thread to handle the connection
			th = ConnectionThread(sock, addr, self.id_iter, self.game_thread)
			print "started connection thread with id %d" % (th.id)
			self.game_thread.connections[self.id_iter] = th
			self.id_iter += 1
			self.connections.append(th)
			th.start()


class GameThread(threading.Thread):

	def __init__(self, connections):
		super(GameThread, self).__init__()
		#gets a dictionary of connections, easier.
		self.connections = {}
		for connection in connections: 
			self.connections[connection.id] = connection

		self.blobs       = {}

	def getReady(self):
		for con in self.connections:
			if not self.connections[con].ready:
				return False
		return True

	def newBlob(self, game_id):
		print "making new blob"
		newBlob = Blob("DEV",20.0*game_id,20.0*game_id,10,(56*game_id,0,126*game_id),game_id)
		self.blobs[game_id] = newBlob
		return newBlob

	def updateBlob(self, id, mouse_pos):
		self.blobs[id].updateDirection(mouse_pos)

	def parseMessage(self, message, id):
		msg = message.split('|')

		if msg[0] == 'init':
			print "init message received"
			newblob = self.newBlob(id)
			msg = game.blobToString(newblob)
			self.connections[id].send('init|%s' % game.blobToString(newblob))

		elif msg[0] == 'updateBlob':
			self.updateBlob(int(msg[1]), make_tuple(msg[2]))

		else:
			print "Error with parsing connection message"

	def checkBlob(self, blob):
		pass

	def run(self):
		done = False
		while not done:
			if self.getReady() and len(self.blobs) != 0:
				print "ready to start"
				for b in self.blobs:
					blob = self.blobs[b]
					blob.update()
					self.checkBlob(blob)
				updated_blobs = game.blobsToString(self.blobs)
				for connection in self.connections:
					print "trying to send to %s" % (connection)
					self.connections[connection].send("updateBlobs|%s" % (game.blobsToString(self.blobs)))



class ConnectionThread(threading.Thread):

	def __init__(self, sock, addr, id, game_thread):
		super(ConnectionThread, self).__init__()
		self.sock    = sock
		self.addr    = addr
		self.game_thread = game_thread
		self.id      = id
		self.timeout = 1
		self.queue   = Queue.Queue()
		self.ready   = True
		self.sock.setblocking(1)

	def send(self, msg):
		messageSize = len(msg)
		self.sock.send("%d|%s" % (messageSize,msg))
		self.ready = False

	def receive(self):
		data = ''
		nextByte = ''
		while nextByte != '|':
			nextByte = self.sock.recv(1)
			data += nextByte
		messageSize = int(data[:-1])
		message = self.sock.recv(messageSize)
		self.ready = True
		return message

	def run(self):
		done = False
		try:
			while not done:

				msg = self.receive()
				self.game_thread.parseMessage(msg, self.id)

				#readReady, writeReady, exception = select.select([self.sock], [self.sock], [], self.timeout)
				#if self.queue.empty():
				#	if len(readReady) != 0: 
				#		print "r"
				#		msg = self.receive()
				#		self.game_thread.parseMessage(msg,self.id)
				#else:
				#	if len(writeReady) != 0 and (time.time() - sync_time) >= 1:
				#		msg = self.queue.get()
				#		print "sending a message: %s" % msg
				#		self.send(msg)
				#		sync_time = time.time()
				
		except:
			print '\nUnhandled exception. Terminating.', sys.exc_info()[1]
			print traceback.format_exc()

if __name__ == "__main__":
	print "starting server..."
	server = BlobberServer(17098)
	server.run()