from pygame import *
import blob, map
import os
import traceback
import sys

init()
viewportSize = (800, 600)
viewportPos = x, y = 0, 0
screen   = display.set_mode((viewportSize))

myBlob   = blob.Blob([300,300])
blobs = [];
blobs.append(blob.Blob([100,100]))
blobs.append(blob.Blob([500,500]))
blobs.append(blob.Blob([700,500]))
blobs.append(blob.Blob([700,700]))

myMap = map.Map(10000,10000)
myMap.addBlob(myBlob)
myMap.addBlobs(blobs)

try:
    done = False
    while not done:
        for e in event.get():
            if e.type == QUIT:
               done = True
            if e.type == KEYDOWN:
              if e.key == K_w:
                myBlob.xy[1] -= 10
              if e.key == K_s:
                myBlob.xy[1] += 10
              if e.key == K_d:
                myBlob.xy[0] += 10
              if e.key == K_a:
                myBlob.xy[0] -= 10

     #    keys_pressed = key.get_pressed()
     #    if keys_pressed[K_s]: myBlob.accelerateY(1)
     #    if keys_pressed[K_w]: myBlob.accelerateY(-1)
     #    if not (keys_pressed[K_w] or keys_pressed[K_s]): myBlob.deccelY()
     #    if keys_pressed[K_d]: myBlob.accelerateX(1)
     #    if keys_pressed[K_a]: myBlob.accelerateX(-1)
    	# if not (keys_pressed[K_a] or keys_pressed[K_d]): myBlob.deccelX()

        screen.fill((255,255,255))
        currentX = myBlob.xy[0]
        currentY = myBlob.xy[1]
        vpXmin = currentX - viewportSize[0]/2
        vpXmax = currentX + viewportSize[0]/2
        vpYmin = currentY - viewportSize[1]/2
        vpYmax = currentY + viewportSize[1]/2
        #draw myBlob at the center of the viewport
        draw.circle(screen, (255,0,0), (viewportSize[0]/2, viewportSize[1]/2), myBlob.radius, 0)

        #draw all the blobs at their respective positions
        for blob in blobs:
          if (vpXmin < blob.xy[0] < vpXmax) and (vpYmin < blob.xy[1] < vpYmax):
            draw.circle(screen, (126,126,126), (blob.xy[0]-vpXmin, blob.xy[1]-vpYmin), blob.radius, 0)
        

        display.flip()
        display.update()

except Exception, err:
    print(traceback.format_exc())





