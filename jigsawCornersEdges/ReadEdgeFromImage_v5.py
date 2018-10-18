'''
Missouri State University, Fall 2018
Ken Vollmar

Find a sequence of (x, y) points that form the boundary of a jigsaw puzzle piece.
Difficulty: The boundary is determined from a photo image, and the boundary line is a few
pixels wide. After the edge-detection of the photo, there will be several "light"-colored
pixels at each X value. At each X value, view several pixels up and down (+Y and -Y from 
the predicted Y value) to find the median light-colored pixel. Use that median as the Y value
for current X and as the predictor of the next X.


Resource: https://www.sitepoint.com/manipulating-images-with-the-python-imaging-library/

Pillow documentation: https://pillow.readthedocs.io/en/5.2.x/
https://stackoverflow.com/questions/11064786/get-pixels-rgb-using-pil

tkinter documentation:
http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html
https://www.c-sharpcorner.com/blogs/basics-for-displaying-image-in-tkinter-python
https://tkdocs.com/

'''
import time  # for pause during graphic display
import math 
import sys




# return true if three-component pixel indicated by tuple p is "white"
def isWhite(p):
	if p[0] > 200 and p[1] > 200 and p[2] > 200:
		return True
	
	return False

# return true if three-component pixel indicated by tuple p is "white"
def isWhiteDEBUG(p):
	print("isWhiteDEBUG:  ", p[0], " ", p[1], " ",p[2])
	if p[0] > 200 and p[1] > 200 and p[2] > 200:
		return True
	
	return False


# Return the distance from the point (xsource, ysource) to the point (xdest, ydest).
def distance(xsource, ysource, xdest, ydest):

	#print("distance(", xsource, " ", ysource, " ", xdest, " ", ydest, 
	#	" is ", math.hypot(xsource - xdest, ysource - ydest))
	return math.hypot(xsource - xdest, ysource - ydest)

	
# Return the angle (radians) from the point (xsource, ysource) to the 
# point (xdest, ydest).
# Range of return value is 0...2*PI.
def angle(xsource, ysource, xdest, ydest):
	h = distance(xsource, ysource, xdest, ydest)
	theta_cos = math.acos((xsource - xdest)/h)
	theta_sin = math.asin((ysource - ydest)/h)
	
	#print("theta_cos is ", theta_cos, ", theta_sin is ", theta_sin)
	
	# Test: abs(theta_cos) ~= abs(theta_sin)
	'''
	if abs(theta_cos - theta_sin) > EPSILON: 
		print("\n\n\tERROR! ERROR! angle() -- two thetas do not agree\n");
		return 0
	'''
		
	if theta_sin >= 0 and theta_cos >= 0:  # Quadrant 1
		print("Q1   angle(", xsource, " ", ysource, " ", xdest, " ", ydest, 
			" is ", theta_sin)
		return theta_sin
	elif theta_sin >= 0 and theta_cos <= 0:  # Quadrant 2
		print("Q2   angle(", xsource, " ", ysource, " ", xdest, " ", ydest, 
			" is ", theta_cos)
		return theta_cos
	elif theta_sin <= 0 and theta_cos <= 0:  # Quadrant 3
		print("Q3   angle(", xsource, " ", ysource, " ", xdest, " ", ydest, 
			" is ", theta_sin)
		return theta_sin
	else:  # Quadrant 4
		print("Q4   angle(", xsource, " ", ysource, " ", xdest, " ", ydest, 
			" is ", 4 * math.pi - theta_cos)
		return 4 * math.pi - theta_cos
		




# Return the point at distance h and angle a (radians) from point (x, y)
def pointAt(h, a, x, y):
	xNew = (h * math.cos(a)) + x
	yNew = (h * math.sin(a)) + y
	
	#print("the point at distance ", h, " and angle ", a, " from point (", x, ", ", y, " is ", xNew, ", ", yNew)
	return (xNew, yNew)



# Use PILLOW to read data from within image, but not to display image or graphically show path.
# This is because PILLOW displays the image using the "operating-system default application," such
# as MS Paint, IrfanView, etc., and it's not possible to annotate that graphic by displaying
# graphics primitives within that graphic default application.
from PIL import Image


# Open the file and read it into content
if (len(sys.argv) > 1): # A command-line argument exists; assume it is an input filename
	BASENAME = sys.argv[1]
else: # Prompt for input filename
	BASENAME = input("\n\n\tPlease type a BASE name:  (e.g., P1) ")
try:
	PILimg = Image.open(BASENAME + "edges.png") # Valid file types: bmp, ppm, jpg, png, gif
	#PILimg.show()  # Uses the selected image application (MS Paint, IrfanView, etc.)
except FileNotFoundError:
	sys.exit('\n\n\tCould not find or open file ' + filename)


# pixel access   https://pillow.readthedocs.io/en/5.2.x/reference/PixelAccess.html
px = PILimg.load()  # px is an object of class PixelAccess


# Test ---- file of jigsaw puzzle piece image pixels
PILimg2 = Image.open(BASENAME + "cropped.png") # Valid file types: bmp, ppm, jpg, png, gif
px2 = PILimg2.load()  # px is an object of class PixelAccess







'''
# Demo of two ways of obtaining RGB at a selected point as a three-component tuple
print (px[4,4])
myPixel = PILimg.getpixel((4, 4))   
print (myPixel)
'''

# Use tkinter to display image and graphically show path, but not read data from within image
# This version is GIF or PPM file
from tkinter import *      
root = Tk()      
canvas = Canvas(root, width = PILimg.width, height = PILimg.height, bg="white")   # HARDCODED
canvas.pack()  
# Don't need to display the edge-detection of original image from which these (x,y) points are read    
#TKimg = PhotoImage(file="P1edges.png")  # Valid file types: ppm, png file, NOT GIF, BMP, JPG
#canvas.create_image(0,0, anchor=NW, image=TKimg)
# canvas.create_line(10, 10, 100, 100)

'''
# DEBUG TEST Read many pixels and display their values. Find out what's really in the image.
for y in range(336, 340):
	for x in range(86, 800):
		tempPixel = PILimg.getpixel((x, y))[0]  # Only the first of the three-component RGB tuple
		print("(", x, ",", y, ") => ", tempPixel)
		if tempPixel > 100:
			print("HEY -- larger than 100")
'''		

# Find and display black/white boundary of the jigsaw puzzle piece
for y in range(0, PILimg.height-1):  # height
	for x in range(0, PILimg.width-1):   # width
		tempPixelA = PILimg.getpixel((x, y))  # three-component RGB tuple
		tempPixelB = PILimg.getpixel((x+1, y))  # three-component RGB tuple
		if (tempPixelA[0] > 128 and tempPixelA[1] > 128 and tempPixelA[2] > 128 and    #  White pixel then black . . .
			tempPixelB[0] < 128 and tempPixelB[1] < 128 and tempPixelB[2] < 128) or  ( 
			tempPixelA[0] < 128 and tempPixelA[1] < 128 and tempPixelA[2] < 128 and   # or black pixel then white
			tempPixelB[0] > 128 and tempPixelB[1] > 128 and tempPixelB[2] > 128):    
			
				# This is presumably a boundary
				'''
				print("(", x, ",", y, ") => ", tempPixel)
				if tempPixel > 100:
				print("HEY -- larger than 100")
				'''
				
				# Draw a two-pixel circle that is part of the shape
				canvas.create_oval(x, y, x+2, y+2,  
					fill='black', outline='black')


		canvas.update() # After all boundary and interior pixels drawn

				
			
				
# Determine (x,y) sequence based on black/white boundaries
# HARDCODED
currentY = 375  # PILimg.height()/2  # at vertical center of image  
currentX = 0
while True: # Find a white pixel on this row, which is the edge of the jigsaw puzzle piece
	tempPixelA = PILimg.getpixel((currentX, currentY))  # three-component RGB tuple
	if (tempPixelA[0] > 128 and tempPixelA[1] > 128 and tempPixelA[2] > 128):
		break
	else:
		currentX = currentX + 1  # Move to the right; continue looking for white pixel
print("Coord sequence is ", currentX, " ", currentY) # Initial point
canvas.create_oval(currentX, currentY, currentX+10, currentY+10, fill='red', outline='black')  # DEBUG
canvas.update()
	
time.sleep(0.50) # HARDCODED



'''
Bresenham's line algorithm -- to be used to interpolate the jigsaw puzzle piece
boundary between two known points. Each point on that interpolated segment will
be used as the starting point for a raster row of pixel data from the color image
of the jigsaw puzzle piece, so that we can "color" the jigsaw puzzle piece within
its boundary using the pixels of the photo image.
https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
'''
def plot(x, y):

	''' Here (x, y) is a point on the jigsaw puzzle piece boundary, one pixel away from 
	another point on the boundary. Draw the raster scan of pixels.
	TBD -- the "other end" of the raster scan is determined by a black pixel
	at least 10 pixels away from the start of that raster scan. That reduces 
	incorrectly short raster rows due to "noise" at the start of the raster row.
	'''
	
	'''
	# TBD --- This is a hack. Only do these raster scans for even values of y coordinate.
	# By observation, the smallest tKinter oval is 2 pixels, so we must draw an oval of that size.
	# Since we can't really achieve a single-pixel oval, we may as well only draw every other data
	# point rather than EACH data point. 
	if y % 2 == 0:
		return
	'''
	
	# print("Point at (", x, ", ", y, ")")
	
	# DEBUG DEBUG DEBUG
	#return
	
	# (x,y) is a point on the "left" boundary of the jigsaw puzzle piece (that is,
	# there exist pixel points on the puzzle piece to the "right" of x at the same y).
	# (tempX, tempY) is a point on the raster scan line between (x,y) and some (END_X, y).
	tempX = x; 
	tempY = y;
	
	while True:  # For each pixel on this raster-scan row of the image of the jigsaw puzzle piece...
		tempPixelA = PILimg.getpixel((tempX, tempY))  # three-component RGB tuple, 0 => black, 255 => white
		if (tempPixelA[0] < 128 and tempPixelA[1] < 128 and tempPixelA[2] < 128 and tempX > x + 10):
			# Have reached a black pixel at least 10 pixels away from the start of that raster scan. 
			# Assume this is the end of the raster scan of pixels within this piece.
			#print("end of raster scan is   ", tempX, ", ", tempY)
			break
			
		# This pixel is from the photo image of the jigsaw puzzle piece
		tempPixelB = PILimg2.getpixel((tempX, tempY))  # three-component RGB tuple
		
		#canvas.create_oval(tempX, tempY, tempX+2, tempY+2, fill='red', outline='red')  # DEBUG red 
		#canvas.update()
		#print("tempX is  ", tempX)
		#time.sleep(0.1) # HARDCODED
		
		
		
		''' Draw an image pixel on this row.
		# Draw a two-pixel circle that is the color of the image.
		# Color needs to be a string of hex digits, without the usual
		# "0x" preceding the digits. First create the hex string INCLUDING
		# the "0x", then strip the "0x" from the string.
		Sequence of data:
		1. tuple of integers, RGB where 0 is black, 255 is white.
		2. use hex() function to convert to a string with leading "0x", 
		so an int value of 0 becomes "0". (TBD -- this may need to be a
		fixed width so that an int value of 0 becomes "00".) The string
		has internal "0x" substrings, e.g. (0, 0, 0) becomes "0x00x00x0"
		3. Strip out occurrences of the substring "0x", and prepend "#".
		The result is "#000", the correct form for tKinter color specification,
		http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/colors.html
		'''
		
		# TBD This is a hack --- If pixel component value is a single hex digit, then
		# the use of that digit as a string may not have consistent number of digits 
		# among R, G, B. Force a "low" component to have two hex digits. This will not affect
		# visual appearance.
		tempPixelC = [0 for i in range(3)] # tempPixelC = [3]  # tempPixelC is a list so we can modify the elements of the tuple tempPixelB
		for ttt in range(0,3):
			if tempPixelB[ttt] < 0x10:
				tempPixelC[ttt] = tempPixelB[ttt] + 0x10  # Force value to be of two hex digits
			else:
				tempPixelC[ttt] = tempPixelB[ttt]

		# Change integer values to string
		tempColorString = hex(tempPixelC[0]) + hex(tempPixelC[1]) + hex(tempPixelC[2])
		#print("tempColorString A is ", tempColorString)
							
		tempColorString = tempColorString[ 2: ]  # Remove "0x" at index 0
		tempColorString = ( tempColorString[ : tempColorString.find("0x", 1)] +
			tempColorString[tempColorString.find("0x", 1) + 2 :] )
		tempColorString = ( tempColorString[ : tempColorString.find("0x", 1)] +
			tempColorString[tempColorString.find("0x", 1) + 2 :] )
		tempColorString = "#" + tempColorString
		#print("tempColorString B is ", tempColorString)
			
		canvas.create_oval(tempX, tempY, tempX+2, tempY+2, fill=tempColorString, outline=tempColorString)  # Don't outline with black
					
		
		# By observation, the smallest tKinter oval is 2 pixels, so we must draw an oval of that size.
		# Since we can't really achieve a single-pixel oval, we may as well only draw every other data
		# point rather than EACH data point. Increase X by 2. (Y stays the same.)
		tempX = tempX + 2

	canvas.update()


def plotLineLow(x0,y0, x1,y1):

	# Force all data to integer values
	x0 = int(x0) 
	y0 = int(y0) 
	x1 = int(x1) 
	y1 = int(y1) 
	
	dx = x1 - x0
	dy = y1 - y0
	yi = 1
	if dy < 0:
		yi = -1
		dy = -dy

	D = 2*dy - dx
	y = y0

	for x in range(x0, x1+1):  # x from x0 to x1
		plot(x,y)
		if D > 0:
			 y = y + yi
			 D = D - 2*dx

		D = D + 2*dy

	
''' By switching the x and y axis 
an implementation for positive or 
negative steep gradients can be written as:
'''
def plotLineHigh(x0,y0, x1,y1):

	# Force all data to integer values
	x0 = int(x0) 
	y0 = int(y0) 
	x1 = int(x1) 
	y1 = int(y1) 

	dx = x1 - x0
	dy = y1 - y0
	xi = 1
	if dx < 0:
		xi = -1
		dx = -dx

	D = 2*dx - dy
	x = x0

	for y in range(y0, y1+1):  # y from y0 to y1
		plot(x,y)
		if D > 0:
			 x = x + xi
			 D = D - 2*dy

		D = D + 2*dx

	
'''A complete solution would need to detect whether 
x1 > x0 or y1 > y0 and reverse the input coordinates before drawing, thus:
'''
def plotLine(x0,y0, x1,y1):

	# Force all data to integer values
	x0 = int(x0) 
	y0 = int(y0) 
	x1 = int(x1) 
	y1 = int(y1) 

	if abs(y1 - y0) < abs(x1 - x0):
		if x0 > x1:
			plotLineLow(x1, y1, x0, y0)
		else:
			plotLineLow(x0, y0, x1, y1)

	else:
		if y0 > y1:
			plotLineHigh(x1, y1, x0, y0)
		else:
			plotLineHigh(x0, y0, x1, y1)



# -------------------------------------------------------------------
# Main loop --- circumnavigate the jigsaw puzzle shape, finding points on the edge
PIXEL_STEP = 15  # Number of pixels between each sampled jigsaw puzzle piece edge data
x1 = currentX
y1 = currentY
sweepAngleDeg = 240  # -120  # degrees  HARDCODED -- we know the initial positions
sampleCount = 0  # Number of sampled points found on puzzle piece edge
#for testRepeat in range(0,10):  # Number of points to trace along jigsaw piece
while True: # all the way around the jigsaw puzzle piece
	#print("x1 is ", x1)
	#print("y1 is ", y1)
	while (True):  # infinite loop while sweeping, looking for black pixel
		sweepAngleRad = sweepAngleDeg * math.pi / 180
		x2 = PIXEL_STEP * math.cos(sweepAngleRad) + x1
		y2 = PIXEL_STEP * math.sin(sweepAngleRad) + y1
		#print("x2 is ", x2)
		#print("y2 is ", y2)
		#time.sleep(0.2) # HARDCODED
		#canvas.create_line(x1, y1, x2, y2, fill='springgreen2')  # DEBUG
		#canvas.update()
		#time.sleep(0.2) # HARDCODED
		
		tempPixelC = PILimg.getpixel((x2, y2))  # three-component RGB tuple
		#print("tempPixelC is    ", tempPixelC)

		# The input image is a white jigsaw puzzle shape on a black background.
		# Continue sweep while the pixel is black.
		if not (isWhite(tempPixelC)):  # Have not yet found white pixel on sweep
			sweepAngleDeg = sweepAngleDeg + 10 #5  # degrees
		else:  # have found white pixel on sweep
			canvas.create_oval(x2-5, y2-5, x2+5, y2+5, fill='red', outline='black')
			canvas.update()
			#print("Point on jigsaw piece boundary:  (", "%.4f" % x2, ", ", "%.4f" % y2, ")" )
			
			# DEBUG TEST -- Show all points on an extrapolated line between 
			# two known points on the jigsaw puzzle boundary
			plotLine(x1,y1, x2, y2)
			
			x1 = x2
			y1 = y2
			sweepAngleDeg = sweepAngleDeg - 90  # next sweep starts 90 deg from this
			sampleCount = sampleCount + 1
			break  # Update point on boundary of puzzle piece and repeat sweep
			
	# If we've returned to the origin on the boundary of this puzzle piece, halt.
	# print(x1, "  ", currentX, "     ", y1, "  ", currentY)
	if (abs(x1 - currentX) <= PIXEL_STEP) and (abs(y1 - currentY) <= PIXEL_STEP) and sampleCount > 5:
		break
		


			





mainloop()   # Graphics loop -- This statement follows all other statements



