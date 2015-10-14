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

MU = None
viewportSize = None
blobs = []


try: 
  #get server state
  sock.send('4 init')
  
  initdone = False
  while not initdone:

    data = ''
    nextByte = ''
    while nextByte != ' ':
      nextByte = sock.recv(1)
      data += nextByte
    messageSize = int(data)
    message = sock.recv(messageSize)

    if message == "initdone":
      break

    obj = jsonpickle.decode(message)

    if obj[0] == "MU":
      MU = obj[1]

    elif obj[0] == "viewportSize":
      viewportSize = obj[1]

    elif obj[0] == "newBlob":
      blobs.append(obj[1])

    elif obj[0] == "initdone":
      break




  screen        = display.set_mode((viewportSize[0], viewportSize[1]))
  myBlob = blobs[0]
  done = False
  while not done:

    #get server updates
    

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
        draw.circle(screen, blob.color, (int(blob.xy[0]*MU)-vpXmin, int(blob.xy[1]*MU)-vpYmin), int(blob.radius*MU), 0)
      


    display.update()

except Exception, err:
    print(traceback.format_exc())          

sock.close()