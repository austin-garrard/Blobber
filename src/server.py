

import jsonpickle
import socket, time, threading, select
from blob import Blob
from map import Map
from resource import Resource, ResourceFactory
from util import StoppableThread, BBuffer, SocketWrapper



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
    msg = self.sock.recvMessage()
    if not msg == "init":
      self.sock.close()
      return
    
    #init client
    self.sock.sendData("MU", server.MU)
    self.sock.sendData("viewportSize", server.viewportSize)
    blobs = ("blobs", server.myMap.blobs)
    for blob in server.myMap.blobs : 
      self.sock.sendData("newBlob", blob)
    self.myBlob = server.myMap.blobs[0]

    #end client init
    self.sock.sendMessage("initdone")

    

    #init timing
    startTime = time.time()
    endTime = time.time()
    
    #main loop
    while not self.stopped():
      newBlobs = []
      updatedBlobs = []

      readReady, writeReady, exception = select.select([self.sock.sock], [], [], self.timeout)
      
      if len(readReady) == 0:
        continue

      #read client message
      msg = self.sock.recvMessage()
      if not msg:
        continue
      if msg == "disconnect":
        break
      
      clientState = jsonpickle.decode(msg)[1]
      #init key state
      K_s = False
      K_w = False
      K_d = False
      K_a = False
      for key in clientState:
        if key == "K_s":
          K_s = True
        if key == "K_w":
          K_w = True
        if key == "K_d":
          K_d = True
        if key == "K_a":
          K_a = True
      
      #act on key presses
      if K_s and not K_w:
        self.myBlob.accelerateY(1)
      if K_w and not K_s:
        self.myBlob.accelerateY(-1)
      if not (K_s or K_w):
        self.myBlob.deccelY()
      
      if K_d and not K_a:
        self.myBlob.accelerateX(1)
      if K_a and not K_d:
        self.myBlob.accelerateX(-1)
      if not (K_a or K_d):
        self.myBlob.deccelX()

      xy = self.myBlob.updatePos()
      self.server.myMap.moveBlob(self.myBlob, xy)
      updatedBlobs.append(self.myBlob)

      #generate resources
      if endTime - startTime > 1.0:
        created = self.server.rf.createResource(5)
        updatedBlobs.extend(created)
        startTime = time.time()
      
      #send update
      if len(newBlobs) > 0:
        self.sock.sendData("newBlobs", newBlobs)
      if len(updatedBlobs) > 0:
        self.sock.sendData("updatedBlobs", updatedBlobs)

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
    #self.sock.setblocking(1)
    
    #self.timeout = 1

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
        # readReady, writeReady, exception = select.select([self.sock], [], [], self.timeout)
        # if len(readReady) < 0:
        #   continue
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
  

if __name__ == '__main__':
  server = BlobberServer(17098)
  try:
    server.start()
    while True:
      pass
  except:
    server.stop()
    server.join()
  