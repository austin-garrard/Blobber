from pygame import *
from resource import Resource, ResourceFactory
import blob, map
import os, time
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

blobs.append(blob.Blob([4.0,3.0], 0.1, (0,0,255)))
blobs.append(blob.Blob([5.0,3.0], 0.1, (0,0,255)))
blobs.append(blob.Blob([6.0,3.0], 0.1, (0,0,255)))
blobs.append(blob.Blob([7.0,3.0], 0.1, (0,0,255)))
myMap.addBlobs(blobs)

#init resources
rf = ResourceFactory(myMap, 2000)
rf.createInitialResources()

#init timing
startTime = time.time()
endTime = time.time()

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
        checkBlobs = []
        #empty list that is filled with blobs in our view to check hitboxes.
        #get keyboard input 
        keys_pressed = key.get_pressed()
        if (keys_pressed[K_s] and not keys_pressed[K_w]): myBlob.accelerateY(1)
        if (keys_pressed[K_w] and not keys_pressed[K_s]): myBlob.accelerateY(-1)
        if not (keys_pressed[K_w] or keys_pressed[K_s]): myBlob.deccelY()
        if (keys_pressed[K_d] and not keys_pressed[K_a]): myBlob.accelerateX(1)
        if (keys_pressed[K_a] and not keys_pressed[K_d]): myBlob.accelerateX(-1)
        if not (keys_pressed[K_a] or keys_pressed[K_d]): myBlob.deccelX()

        #update position of myBlob
        xy = myBlob.updatePos()
        #print int(xy[0]*MU),int(xy[1]*MU)
        myMap.moveBlob(myBlob, xy)

        #generate resources
        if endTime - startTime > 1.0:
          rf.createResource(5)
          startTime = time.time()

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
        for blob in myMap.blobs:
          if (vpXmin < int(blob.xy[0]*MU) < vpXmax) and (vpYmin < int(blob.xy[1]*MU) < vpYmax):
            draw.circle(screen, blob.color, (int(blob.xy[0]*MU)-vpXmin, int(blob.xy[1]*MU)-vpYmin), int(blob.radius*MU), 0)
            checkBlobs.append(blob)
        
        # #draw resources
        # for r in myMap.resources:
        #   if (vpXmin < int(r.xy[0]*MU) < vpXmax) and (vpYmin < int(r.xy[1]*MU) < vpYmax):
        #     draw.circle(screen, (0,255,0), (int(r.xy[0]*MU)-vpXmin, int(r.xy[1]*MU)-vpYmin), int(r.radius*MU), 0)
        #     checkBlobs.append(r)

        for check in checkBlobs:
          if myBlob.canEat(check):
            myBlob.eat(check)
            myMap.blobs.remove(check)
            if isinstance(check, Resource):
                myMap.numResources -= 1

        

        endTime = time.time()
        display.update()

except Exception, err:
    print(traceback.format_exc())





