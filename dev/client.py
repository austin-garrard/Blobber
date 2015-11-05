import pygame
import blob
import traceback

viewportSize = (800, 600)

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
      		print "Error connecting.\n"
      		print e
      		#self.sock.close()
      		self.connected = False
      		return

	    #game data
	    self.MU = 100.0
	    self.viewportSize = viewportSize
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


def draw_all(blobs, screen):

	for b in blobs:
		pygame.draw.circle(screen, b.color, (int(b.x), int(b.y)), int(b.radius), 0)

#filler function for now, needs to connect to the server
def get_blobs(blobs):
	return [blobs]

#should also initiate our blob to the server
def start_blob():
	new_blob = blob.Blob("DEV", 3.0, 3.0, 100, (125,0,125))
	return new_blob

def update_blobs(blobs):
	for b in blobs:
		b.update()

def main():
	#initiate pygame
	pygame.init()

	MU           = 100.0
	screen       = pygame.display.set_mode(viewportSize)

	#TODO: INITIATE OUR BLOB TO THE SERVER
	ourBlob = start_blob()
	#TODO: GET THE POSITION OF OTHER BLOBS FROM THE SERVER, blobs will be my filler variable.
	blobs = get_blobs(ourBlob)

	try:
		done = False
		while not done:
			#Event checking
			for e in pygame.event.get():
				if e.type == pygame.QUIT:
					done = True


		ourBlob.updateDirection(pygame.mouse.get_pos())

		update_blobs(blobs)
		screen.fill((255,255,255))
		draw_all(blobs, screen)

		pygame.display.update()

	except Exception, err:
		print(traceback.format_exc())


if __name__ == "__main__":
	main()






