import socket, time
from pygame import *
from blob import Blob
from resource import Resource 
import jsonpickle
import traceback
import sys



host = 'localhost'
port = 17098
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

#init
init()


try: 
  #get server state
  sock.sendall('init')
  bigSerial = sock.recv(2048)
  server_state = jsonpickle.decode(bigSerial)
  #decode server state
  MU = server_state[0]
  viewportSize = server_state[1]
  myBlob = server_state[2]
  myMap = server_state[3]
  screen        = display.set_mode((viewportSize[0], viewportSize[1]))
  blobs = myMap.blobs
  done = False
  while not done:

    

    #handle events
    for e in event.get():
        if e.type == QUIT:
           done = True

    #get client state 
    client_state = [] 
    keys_pressed = key.get_pressed()
    if (keys_pressed[K_s] and not keys_pressed[K_w]): client_state.append(K_s)
    if (keys_pressed[K_w] and not keys_pressed[K_s]): client_state.append(K_w)
    if not (keys_pressed[K_w] or keys_pressed[K_s]): pass
    if (keys_pressed[K_d] and not keys_pressed[K_a]): client_state.append(K_d)
    if (keys_pressed[K_a] and not keys_pressed[K_d]): client_state.append(K_a)
    if not (keys_pressed[K_a] or keys_pressed[K_d]): pass

    #calculate viewport
    currentX = int(myBlob.xy[0]*MU)
    currentY = int(myBlob.xy[1]*MU)
    vpXmin = currentX - viewportSize[0]/2
    vpXmax = currentX + viewportSize[0]/2
    vpYmin = currentY - viewportSize[1]/2
    vpYmax = currentY + viewportSize[1]/2

    #draw background
    screen.fill((255,255,255))

    #draw myBlob at the center of the viewport
    draw.circle(screen, (255,0,0), (viewportSize[0]/2, viewportSize[1]/2), int(myBlob.radius*MU), 0)

    #draw all the blobs at their respective positions
    for blob in blobs:
      if (vpXmin < int(blob.xy[0]*MU) < vpXmax) and (vpYmin < int(blob.xy[1]*MU) < vpYmax):
        draw.circle(screen, (126,126,126), (int(blob.xy[0]*MU)-vpXmin, int(blob.xy[1]*MU)-vpYmin), int(blob.radius*MU), 0)
      
    
    #draw resources
    for r in myMap.resources:
      if (vpXmin < int(r.xy[0]*MU) < vpXmax) and (vpYmin < int(r.xy[1]*MU) < vpYmax):
        draw.circle(screen, (0,255,0), (int(r.xy[0]*MU)-vpXmin, int(r.xy[1]*MU)-vpYmin), int(r.radius*MU), 0)


    display.update()
    
except Exception, err:
    print(traceback.format_exc())          

sock.close()