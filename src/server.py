

import jsonpickle
import socket, time, threading
from blob import Blob
from map import Map
from resource import Resource, ResourceFactory



class StoppableThread(threading.Thread):
    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()
    def stop(self):
        self._stop.set()
    def stopped(self):
        return self._stop.isSet()



class BlobberServerThread(StoppableThread):
  def __init__(self, sock, lock, server):
    super(BlobberServerThread, self).__init__()
    self.sock = sock
    self.lock = lock
    self.server = server

  def run(self):
    #init
    data = self.sock.recv(4)
    if not data == "init":
      self.sock.close()
      return
    
    #serialize state
    state = [self.server.MU, self.server.viewportSize, self.server.myBlob, self.server.myMap]
    stateSerial = jsonpickle.encode(state)
    #send to client
    self.sock.sendall(stateSerial)
    
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
    self.threadPool = []
    self.mutex = threading.Lock()

    #display
    self.MU            = 100.0
    self.viewportSize  = (800, 600)

    #blobs
    self.myBlob   = Blob([3.0,3.0])
    self.blobs = [];
    self.blobs.append(Blob([4.0,3.0], 0.1))
    self.blobs.append(Blob([5.0,3.0], 0.1))
    self.blobs.append(Blob([6.0,3.0], 0.1))
    self.blobs.append(Blob([7.0,3.0], 0.1))

    #map
    self.myMap = Map(100.0,100.0)
    self.myMap.addBlob(self.myBlob)
    self.myMap.addBlobs(self.blobs)

    #resources
    self.rf = ResourceFactory(self.myMap, 200)
    self.rf.createInitialResources()
    
  def run(self):
    self.sock.bind(("",self.port)) 
    self.sock.settimeout(5)
    while not self.stopped():
      try:
        self.sock.listen(1) 
        sock = self.sock.accept()[0]
        print sock
        th = BlobberServerThread(sock, self.mutex, self)
        self.threadPool.append(th)
        th.start()
      except socket.error, v:
        print v[0]
        time.sleep(1)
        break


    for th in self.threadPool:
      th.stop()
      th.join()
    self.sock.close()




server = BlobberServer(17098)
try:
  server.start()
  server.join()
except:
  server.stop()
  server.join()
  

# Tcp_server_wait ( 5, 17098 )
# Tcp_server_next()
# print Tcp_Read()
# Tcp_Write('hi')
# print Tcp_Read()
# Tcp_Write('hi')
# Tcp_Close()