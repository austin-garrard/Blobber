import socket, time, sys, traceback
import pygame, jsonpickle
from blob import Blob
from resource import Resource 
from util import SocketWrapper


class BlobberClient:
  def __init__(self, serverAddr='localhost', port=17098):
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
      self.sock.close()
      self.connected = False
      return

    #game data
    self.MU = None
    self.viewportSize = None
    self.blobs = []

    #init phase
    try: 
      self.sock.sendMessage('init')
      
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

    self.myBlob = self.blobs[0]

    #pygame
    pygame.init()
    self.screen = pygame.display.set_mode((self.viewportSize[0], self.viewportSize[1]))

  def run(self):
    done = False
    while not done:

      #get server updates
      

      #handle events
      for e in pygame.event.get():
          if e.type == pygame.QUIT:
             done = True

      #get client state 
      client_state = [] 
      keys_pressed = pygame.key.get_pressed()
      if (keys_pressed[pygame.K_s] and not keys_pressed[pygame.K_w]): client_state.append('K_s')
      if (keys_pressed[pygame.K_w] and not keys_pressed[pygame.K_s]): client_state.append('K_w')
      if not (keys_pressed[pygame.K_w] or keys_pressed[pygame.K_s]): pass
      if (keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_a]): client_state.append('K_d')
      if (keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_d]): client_state.append('K_a')
      if not (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_d]): pass

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

    self.sock.close()
    self.connected = False


if __name__ == '__main__':
  client = BlobberClient()
  if client.connected:
    client.run()