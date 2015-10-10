from pygame import *
from resource import Resource, ResourceFactory
import blob, map
import os
import traceback
import sys

#init pygame, view constants
init()
MU            = 100.0
viewportSize  = (800, 600)
screen        = display.set_mode((viewportSize[0], viewportSize[1]))

#init map
myMap = map.Map(100.0,100.0)

#init myBlob
myBlob   = blob.Blob([3.0,3.0])
myMap.addBlob(myBlob)
#init other blobs
blobs = [];
blobs.append(blob.Blob([1.0,1.0]))
blobs.append(blob.Blob([5.0,5.0]))
blobs.append(blob.Blob([7.0,5.0]))
blobs.append(blob.Blob([7.0,7.0]))
myMap.addBlobs(blobs)

#init default resources
rf = ResourceFactory(myMap)
resources = []
for i in range(1000):
  myMap.addResource(rf.createResource())




try:
    done = False
    while not done:
        #handle events
        for e in event.get():
            if e.type == QUIT:
               done = True

        #update position of myBlob
        xy = myBlob.updatePos()
        #print int(xy[0]*MU),int(xy[1]*MU)
        myMap.moveBlob(myBlob, xy)
        #draw.circle(screen, myBlob.color, (int(myBlob.xy[0]*MU), int(myBlob.xy[1]*MU)), int(myBlob.radius*MU), 0)

        keys_pressed = key.get_pressed()
        if keys_pressed[K_s]: myBlob.accelerateY(.001)
        if keys_pressed[K_w]: myBlob.accelerateY(-.001)
        if not (keys_pressed[K_w] or keys_pressed[K_s]): myBlob.deccelY()
        if keys_pressed[K_d]: myBlob.accelerateX(.001)
        if keys_pressed[K_a]: myBlob.accelerateX(-.001)
        if not (keys_pressed[K_a] or keys_pressed[K_d]): myBlob.deccelX()

        #draw background
        screen.fill((255,255,255))

        #calculate viewport
        currentX = int(myBlob.xy[0]*MU)
        currentY = int(myBlob.xy[1]*MU)
        vpXmin = currentX - viewportSize[0]/2
        vpXmax = currentX + viewportSize[0]/2
        vpYmin = currentY - viewportSize[1]/2
        vpYmax = currentY + viewportSize[1]/2
        #print vpXmin,vpXmax,vpYmin,vpYmax

        #draw myBlob at the center of the viewport
        draw.circle(screen, (255,0,0), (viewportSize[0]/2, viewportSize[1]/2), int(myBlob.radius*MU), 0)

        #draw all the blobs at their respective positions
        for blob in blobs:
          if (vpXmin < int(blob.xy[0]*MU) < vpXmax) and (vpYmin < int(blob.xy[1]*MU) < vpYmax):
            draw.circle(screen, (126,126,126), (int(blob.xy[0]*MU)-vpXmin, int(blob.xy[1]*MU)-vpYmin), int(blob.radius*MU), 0)
        
        #draw resources
        for r in myMap.resources:
          draw.circle(screen, (0,255,0), (int(r.xy[0]*MU)-vpXmin, int(r.xy[1]*MU)-vpYmin), int(r.radius*MU), 0)

        

        display.flip()
        display.update()

except Exception, err:
    print(traceback.format_exc())





