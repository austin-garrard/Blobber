from pygame import *
import blob
import os
import traceback
import sys
init()

# root_dir = os.getcwd()
# sprite_dir = root_dir[:root_dir.rfind("\\")] + "\\sprites"


screen   = display.set_mode((800, 600))
myBlob   = blob.Blob()
done = False


try:
    while not done:
        for e in event.get():
            if e.type == QUIT:
               done = True

        keys_pressed = key.get_pressed()
        if keys_pressed[K_s]: myBlob.accelerateY(1)
        if keys_pressed[K_w]: myBlob.accelerateY(-1)
        if not (keys_pressed[K_w] or keys_pressed[K_s]): myBlob.deccelY()
        if keys_pressed[K_d]: myBlob.accelerateX(1)
        if keys_pressed[K_a]: myBlob.accelerateX(-1)
    	if not (keys_pressed[K_a] or keys_pressed[K_d]): myBlob.deccelX()



        screen.fill((255,255,255))
        print myBlob.xAccel,myBlob.yAccel
        xy = myBlob.updatePos()
        myBlob.xy = xy    
        draw.circle(screen, (126,126,126), (myBlob.xy[0], myBlob.xy[1]), myBlob.radius, 0)
        display.flip()
        display.update()

except Exception, err:
    print(traceback.format_exc())





