import jsonpickle
import socket, time, threading, select
from blob_ import Blob
from map import Map
from util import StoppableThread, BBuffer, SocketWrapper
import game

class BlobberServerThread(StoppableThread):
	def __init__(self, sock, clientAddr, lock, server, timeout=1):
		super(BlobberServerThread, self).__init__()
		self.sock = SocketWrapper(sock)
		self.clientAddr = clientAddr
		self.lock = lock
		self.server = server
		self.updateQueue = BBuffer(100)
		self.timeout = 1


	def run(self):
		#begin init phase
		msg = self.sock.recvMessage().split(" ")
	
		if msg[0] == "newblob":
	  		print "holy fuckin shit\n"
	  	else:
	  		print msg[0]

		self.sock.close()
		print "server thread stopping"
	



class BlobberServer(StoppableThread):
	def __init__(self, port=17098):
		super(BlobberServer, self).__init__()
		#network
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		#self.sock.settimeout(2)
		#self.sock.setblocking(1)

		#self.timeout = 1

		#sync
		self.threadPool = []
		self.mutex = threading.Lock()

		#map
		self.myMap = Map(100.0,100.0)

		print "Starting server..."

		#listen for new connections, spawn threads to handle them 
		def run(self):
			try:
				self.sock.bind(("127.0.0.1",self.port))
			except Exception, err:
				print error
			while not self.stopped():
				try:
					# readReady, writeReady, exception = select.select([self.sock], [], [], self.timeout)
					# if len(readReady) < 0:
					#   continue
					self.sock.listen(10) 
					sock, addr = self.sock.accept()

					th = BlobberServerThread(sock, addr, self.mutex, self)
					self.threadPool.append(th)
					th.start()

				#for now, ignore errors
				except socket.error, v:
						pass

			#cleanup
			for th in self.threadPool:
					th.stop()
					th.join()
			self.sock.close()

if __name__ == "__main__":
	server = BlobberServer()
	try:
		server.start()
		while True:
		  	pass
	except Exception, error:
		print error
		server.stop()
		server.join()
		raw_input()
