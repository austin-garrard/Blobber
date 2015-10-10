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
done     = False
MU       = 10.0

try:
    while not done:
        for e in event.get():
            if e.type == QUIT:
               done = True

        keys_pressed = key.get_pressed()
        if keys_pressed[K_s]: myBlob.accelerateY(0.1)
        if keys_pressed[K_w]: myBlob.accelerateY(-0.1)
        if not (keys_pressed[K_w] or keys_pressed[K_s]): myBlob.deccelY()
        if keys_pressed[K_d]: myBlob.accelerateX(0.1)
        if keys_pressed[K_a]: myBlob.accelerateX(-0.1)
    	if not (keys_pressed[K_a] or keys_pressed[K_d]): myBlob.deccelX()



        screen.fill((255,255,255))
        xy = myBlob.updatePos()
        print int(xy[0]*MU),int(xy[1]*MU)
        myBlob.xy = xy    
        draw.circle(screen, myBlob.color, (int(myBlob.xy[0]*MU), int(myBlob.xy[1]*MU)), int(myBlob.radius*MU), 0)
        display.flip()
        display.update()

except Exception, err:
    print(traceback.format_exc())





