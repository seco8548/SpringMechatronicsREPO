# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# setup GPIO using Board numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.OUT) # make BCM pin 5 an output
GPIO.output(5,GPIO.LOW) # initialize the pin as low, or off

# define what color to look for (this is blue)
boundaries = [
	([86, 31, 4], [220, 88, 50])
]

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array

	# check for colors in the defined boundary
	for (lower, upper) in boundaries:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")

		# find the colors within the specified boundaries and apply
		# the mask
		mask = cv2.inRange(image, lower, upper)
		output = cv2.bitwise_and(image, image, mask = mask)
		# show the images
		#cv2.imshow("frame", np.hstack([image, output])) # shows feed and the filter side by side
		cv2.imshow("frame", output)

		# checks if output has values > 10, (if there's blue in the image)
		if np.count_nonzero(output)>10:
			GPIO.output(5,GPIO.HIGH) # sends pin 5 high (stops the cyclone game)
			#print("Oh Boy it's BLUE")
			GPIO.output(5,GPIO.LOW)
			#GPIO.cleanup()
			break

	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame. Important!!
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop, quit the program
	if key == ord("q"):
		break
