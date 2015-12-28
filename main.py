import ucam
import time
import sys

cam = ucam.UCam()
synced = cam.sync()
print 'synced? ', synced
if synced:
	time.sleep(2)
	filename = 'me.jpg'
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	cam.take_picture(filename)
