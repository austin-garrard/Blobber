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

    #map
    self.myMap = Map(100.0,100.0)

    #blobs

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