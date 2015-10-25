import socket, time, sys, traceback, select
import pygame, jsonpickle
from blob import Blob
from resource import Resource 
from util import SocketWrapper


class BlobberClient:
  def __init__(self, serverAddr="localhost", port=17098):
    #network
    self.serverAddr = serverAddr
    self.port = port
    try:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.connect((serverAddr, port))
      self.connected = True
      self.sock = SocketWrapper(sock)
    except socket.error, e:
      print "Error connecting."
      print e
      #self.sock.close()
      self.connected = False
      return

    #game data
    self.MU = None
    self.viewportSize = None
    self.blobs = []

    #init phase
    self.sock.sock.setblocking(1)
    try: 
      self.sock.sendMessage("init")
      
      initdone = False
      while not initdone:
        msg = self.sock.recvMessage()

        if msg == "initdone":
          break

        obj = jsonpickle.decode(msg)

        if obj[0] == "MU":
          self.MU = obj[1]

        elif obj[0] == "viewportSize":
          self.viewportSize = obj[1]

        elif obj[0] == "newBlob":
          self.blobs.append(obj[1])

        #end init phase
        elif obj[0] == "initdone":
          initdone = True
      
    except Exception:
      print "Error initializing."
      print(traceback.format_exc())   
      self.sock.close()
      self.connected = False
      return
    self.sock.sock.setblocking(0)

    self.myBlob = self.blobs[0]
    print self.myBlob.xy
    self.sock.sock.setblocking(0)

    #pygame
    pygame.init()
    self.screen = pygame.display.set_mode((self.viewportSize[0], self.viewportSize[1]))

  def run(self):
    done = False
    while not done:
      #handle events
      for e in pygame.event.get():
          if e.type == pygame.QUIT:
             done = True

      #get client state 
      clientState = [] 
      keysPressed = pygame.key.get_pressed()
      if     (keysPressed[pygame.K_s] and not keysPressed[pygame.K_w]): clientState.append('K_s')
      if     (keysPressed[pygame.K_w] and not keysPressed[pygame.K_s]): clientState.append('K_w')
      if not (keysPressed[pygame.K_w] or      keysPressed[pygame.K_s]): pass
      if     (keysPressed[pygame.K_d] and not keysPressed[pygame.K_a]): clientState.append('K_d')
      if     (keysPressed[pygame.K_a] and not keysPressed[pygame.K_d]): clientState.append('K_a')
      if not (keysPressed[pygame.K_a] or      keysPressed[pygame.K_d]): pass

      #send client state
      self.sock.sendData("clientState", clientState)


      #calculate viewport
      currentX = int(self.myBlob.xy[0]*self.MU)
      currentY = int(self.myBlob.xy[1]*self.MU)
      vpXmin = currentX - self.viewportSize[0]/2
      vpXmax = currentX + self.viewportSize[0]/2
      vpYmin = currentY - self.viewportSize[1]/2
      vpYmax = currentY + self.viewportSize[1]/2

      #draw background
      self.screen.fill((255,255,255))

      #draw myBlob at the center of the viewport
      pygame.draw.circle(self.screen, (255,0,0), (self.viewportSize[0]/2, self.viewportSize[1]/2), int(self.myBlob.radius*self.MU), 0)

      #draw all the blobs at their respective positions
      for blob in self.blobs:
        if (vpXmin < int(blob.xy[0]*self.MU) < vpXmax) and (vpYmin < int(blob.xy[1]*self.MU) < vpYmax):
          pygame.draw.circle(self.screen, blob.color, (int(blob.xy[0]*self.MU)-vpXmin, int(blob.xy[1]*self.MU)-vpYmin), int(blob.radius*self.MU), 0)

      pygame.display.update()

      #get server updates
      readReady, writeRead, exception = select.select([self.sock.sock], [], [], 1)
      if len(readReady) == 0:
        continue

      msg = self.sock.recvMessage()
      if not msg:
        continue

      if msg == "done":
        done = True
        break

      obj = jsonpickle.decode(msg)

      if obj[0] == "newBlobs":
        self.blobs.extend(obj[1])

      if obj[0] == "updatedBlobs":
        self.myBlob = obj[1][0]

    self.sock.sendMessage("disconnect")
    self.sock.close()
    self.connected = False


if __name__ == '__main__':
  client = BlobberClient()
  if client.connected:
    client.run()