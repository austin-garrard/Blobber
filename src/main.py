from pygame import *
from resource import Resource, ResourceFactory, CenaBoost
import blob, map
import os, time
import traceback
import sys
import random

#init pygame, view constants
init()
mixer.init()
MU            = 100.0
viewportSize  = (800, 600)
screen        = display.set_mode((viewportSize[0], viewportSize[1]))
cenaBoost     = None
c             = False

#init map
myMap = map.Map(100.0,100.0)

#init myBlob
myBlob   = blob.Blob([3.0,3.0])
myMap.addBlob(myBlob)
#init other blobs
blobs = [];

blobs.append(myBlob)
blobs.append(blob.Blob([6.31,3.51], 0.1))
blobs.append(blob.Blob([5.26,3.41], 0.1))
blobs.append(blob.Blob([3.0,7.5], 0.1))
blobs.append(blob.Blob([2.0,3.5], 0.1))
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
        if ((keys_pressed[K_s] or keys_pressed[K_w]) and (keys_pressed[K_a] or keys_pressed[K_d])): myBlob.movingDiag = True
        else: myBlob.movingDiag = False

        #update position of myBlob
        xy = myBlob.updatePos()
        #print int(xy[0]*MU),int(xy[1]*MU)
        myMap.moveBlob(myBlob, xy)

        #generate resources
        if endTime - startTime > 1.0:
          rf.createResource(5)
          startTime = time.time()

        if not c:
          if random.randint(0,100) >= 5:
            x = random.uniform(0, myMap.width)
            y = random.uniform(0, myMap.height)
            radius = random.uniform(.05, .11)
            cenaBoost = CenaBoost((x,y), radius)
            myMap.addResource(cenaBoost)
            mixer.music.load("songs\\CENA.mp3")
            mixer.music.play()
            c = True


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

        #draw all the blobs at their respective positions
        if c:
          print myBlob.getDistBetween(cenaBoost)
          mixer.music.set_volume(1.0 - myBlob.getDistBetween(cenaBoost)/100.0)

        for blob in blobs:
          if (vpXmin - blob.radius*MU < int(blob.xy[0]*MU) < vpXmax + blob.radius*MU) and (vpYmin - blob.radius*MU < int(blob.xy[1]*MU) < vpYmax + blob.radius):
            draw.circle(screen, (126,126,126), (int(blob.xy[0]*MU)-vpXmin, int(blob.xy[1]*MU)-vpYmin), int(blob.radius*MU), 0)
            checkBlobs.append(blob)
        
        #draw resources
        for r in myMap.resources:
          if (vpXmin < int(r.xy[0]*MU) < vpXmax) and (vpYmin < int(r.xy[1]*MU) < vpYmax):
            draw.circle(screen, r.color, (int(r.xy[0]*MU)-vpXmin, int(r.xy[1]*MU)-vpYmin), int(r.radius*MU), 0)
            checkBlobs.append(r)
            if r.name == "CENA":
              b = sprite.Sprite()
              b.image = image.load("sprites\\CENA.png").convert() # load ball image
              b.rect = b.image.get_rect() # use image extent values
              b.rect.topleft = [int(r.xy[0]*MU) - vpXmin - 10, int(r.xy[1]*MU) - vpYmin - 10] # put the ball in the top left corner
              screen.blit(b.image, b.rect)
              display.flip()


        for this_blob in checkBlobs:
          for check in checkBlobs:
            if this_blob == check:
              pass
            else:
              if this_blob.name == 'res' or this_blob.name == "CENA":
                pass
              else:
                if this_blob.canEat(check):
                  if check.name == "CENA":
                    mixer.music.stop()
                    c = False
                  this_blob.eat(check)
                  if check in blobs:
                    blobs.remove(check)
                  else:
                    myMap.resources.remove(check)
                # elif (this_blob.radius > check.radius) and (True):
                #   if (this_blob.xy[0] - check.xy[0]) == 0:
                #     grav_x = 0.0
                #   else:
                #     grav_x = (this_blob.radius**2 * check.radius**2)/(this_blob.xy[0] - check.xy[0])
                #   if (this_blob.xy[1] - check.xy[1]) == 0:
                #     grav_y = 0.0
                #   else:
                #     grav_y = (this_blob.radius**2 * check.radius**2)/(this_blob.xy[1] - check.xy[1])
                #   check.change_pos(check.xy[0] + grav_x, check.xy[1] + grav_y)
                #   print grav_x,grav_y
        

        endTime = time.time()
        display.update()

except Exception, err:
    print(traceback.format_exc())





