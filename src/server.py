

import jsonpickle
import socket, time, threading
from blob import Blob
from map import Map
from resource import Resource, ResourceFactory
from util import StoppableThread, BBuffer, SocketWrapper



class BlobberServerThread(StoppableThread):
  def __init__(self, sock, clientAddr, lock, server):
    super(BlobberServerThread, self).__init__()
    self.sock = SocketWrapper(sock)
    self.clientAddr = clientAddr
    self.lock = lock
    self.server = server
    self.updateQueue = BBuffer(100)

  

  def run(self):
    #init
    data = self.sock.recv(4)
    if not data == "init":
      self.sock.close()
      return
    
    #serialize state
    self.sendData("MU", server.MU)

    self.sendData("viewportSize", server.viewportSize)

    blobs = ("blobs", server.myMap.blobs)
    for blob in server.myMap.blobs : 
      self.sendData("newBlob", blob)


    #send to client
    self.sendMessage("initdone")
    
    while not self.stopped():
      break
      
      #read keypresses from client
      
      #update server state
      
      #send response
    self.sock.close()
    print "server thread stopping"



class BlobberServer(StoppableThread):
  def __init__(self, port=17098):
    super(BlobberServer, self).__init__()
    #network
    self.port = port;
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind(("",self.port)) 
    self.sock.settimeout(2)

    #sync
    self.threadPool = []
    self.mutex = threading.Lock()

    #display
    self.MU            = 100.0
    self.viewportSize  = (800, 600)

    #map
    self.myMap = Map(100.0,100.0)

    #blobs
    self.myMap.addPlayer(Blob([3.0,3.0], .2, (255,0,0))) #myBlob
    self.myMap.addPlayer(Blob([4.0,3.0], 0.1, (0,0,255)))
    self.myMap.addPlayer(Blob([5.0,3.0], 0.1, (0,0,255)))
    self.myMap.addPlayer(Blob([6.0,3.0], 0.1, (0,0,255)))
    self.myMap.addPlayer(Blob([7.0,3.0], 0.1, (0,0,255)))

    #resources
    self.rf = ResourceFactory(self.myMap, 2000)
    self.rf.createInitialResources()
    
  #listen for new connections, spawn threads to handle them 
  def run(self):
    while not self.stopped():
      try:
        self.sock.listen(5) 
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
  

server = BlobberServer(17098)
try:
  server.start()
  while True:
    pass
except:
  server.stop()
  server.join()
  