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

	2
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
		#print("Q1   angle(", xsource, " ", ysource, " ", xdest, " ", ydest,
			#" is ", theta_sin)
		return theta_sin
	elif theta_sin >= 0 and theta_cos <= 0:  # Quadrant 2
		#print("Q2   angle(", xsource, " ", ysource, " ", xdest, " ", ydest,
			#" is ", theta_cos)
		return theta_cos
	elif theta_sin <= 0 and theta_cos <= 0:  # Quadrant 3
		#print("Q3   angle(", xsource, " ", ysource, " ", xdest, " ", ydest,
			#" is ", theta_sin)
		return theta_sin
	else:  # Quadrant 4
		#print("Q4   angle(", xsource, " ", ysource, " ", xdest, " ", ydest,
			#" is ", 4 * math.pi - theta_cos)
		return 4 * math.pi - theta_cos





# Return the point at distance h and angle a (radians) from point (x, y)
def pointAt(h, a, x, y):
	xNew = (h * math.cos(a)) + x
	yNew = (h * math.sin(a)) + y

	print("the point at distance ", h, " and angle ", a, " from point (",
		x, ", ", y, " is ", xNew, ", ", yNew)
	return (xNew, yNew)



#rotating a piece
def rotate(a):

    #clear canvas
    canvas.delete("all")

    
    #specify the degrees that the piece should be rotated
    rotation_deg = input("How many degrees would you like to rotate? \n")

    #convert to rads
    rotation_rad = math.radians(int(rotation_deg))

    #finding origin for rotation, this uses the center of the canvas
    origin_x = int(PILimg.width/2)
    origin_y = int(PILimg.height/2)
    for point in a:
        x = point[0]
        y = point[1]
        # rotating the points around the origin by the specified angle
        adjusted_x = (x - origin_x)
        adjusted_y = (y - origin_y)

        rotated_x = origin_x + math.cos(rotation_rad) * adjusted_x + math.sin(rotation_rad) * adjusted_y
        rotated_y = origin_y + -math.sin(rotation_rad) * adjusted_x + math.cos(rotation_rad) * adjusted_y


        canvas.create_oval(rotated_x-5, rotated_y-5, rotated_x+5, rotated_y+5, fill='blue', outline='black')


def edgeFind(a):

        #count of current potentail edge
        pot_edge = 0

        #current point being checked
        curr_point = 0

        #this tracks points that fail to meet the edge criteria
        #if more than 2 in a row fail, a new potentail edge is created
        fail_points = 0
        #hash that list points for potential edges
        pot_edge_hash = {}

        #create list of possible edges
        while curr_point < len(a)-1:
                print(abs(a[curr_point] - a[curr_point+1]))
                if curr_point == 0:
                        pot_edge_hash.update({pot_edge: []})
                        curr_point += 1
                elif curr_point > 0 and abs(a[curr_point] - a[curr_point+1] ) <= 10:
                        pot_edge_hash[pot_edge].append(curr_point)
                        curr_point += 1
                elif abs(a[curr_point] - a[curr_point+1]) > 10:
                        fail_points += 1
                        pot_edge_hash[pot_edge].append(curr_point)
                        curr_point += 1
                        if fail_points > 3:
                                pot_edge += 1
                                pot_edge_hash.update({pot_edge: []})
                                fail_points = 0
       # for pot_edge in pot_edge_hash:
               # print(pot_edge_hash[pot_edge])





# Use PILLOW to read data from within image, but not to display image or graphically show path.
# This is because PILLOW displays the image using the "operating-system default application," such
# as MS Paint, IrfanView, etc., and it's not possible to annotate that graphic by displaying
# graphics primitives within that graphic default application.
from PIL import Image


# Open the file and read it into content
if (len(sys.argv) > 1): # A command-line argument exists; assume it is an input filename
	filename = sys.argv[1]
else: # Prompt for input filename
	filename = input("\n\n\tPlease type a BearPlot graphics data file name: ")
try:
	PILimg = Image.open(filename) # Valid file types: bmp, ppm, jpg, png, gif
	#PILimg.show()  # Uses the selected image application (MS Paint, IrfanView, etc.)
except FileNotFoundError:
	sys.exit('\n\n\tCould not find or open file ' + filename)


# pixel access   https://pillow.readthedocs.io/en/5.2.x/reference/PixelAccess.html
px = PILimg.load()  # px is an object of class PixelAccess

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
#temp_height = PILimg.size()
#print("DEBUG --- image size is ", PILimg.size)
#print("DEBUG --- image height is ", PILimg.height)
#print("DEBUG --- image width is ", PILimg.width)
# PILimg.getheight()):
# PILimg.getwidth()):  #
#print("************** ", temp_height)
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
				canvas.create_oval(x, y, x+2, y+2,
					fill='black', outline='black')
				canvas.update()




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
#print("Coord sequence is ", currentX, " ", currentY) # Initial point
canvas.create_oval(currentX, currentY, currentX+10, currentY+10, fill='red', outline='black')  # DEBUG
canvas.update()

#time.sleep(0.50) # HARDCODED




# -------------------------------------------------------------------
# Main loop --- circumnavigate the jigsaw puzzle shape, finding points on the edge
PIXEL_STEP = 15  # HARDCODED Number of pixels between each sampled jigsaw puzzle piece edge data
x1 = currentX
y1 = currentY

sweep_angle_tracker = []
point_tracker = []

sweepAngleDeg = 240  # -120  # degrees  HARDCODED -- we know the initial positions
sampleCount = 0  # Number of sampled points found on puzzle piece edge
# for testRepeat in range(0,10):  # Number of points to trace along jigsaw piece


while True: # all the way around the jigsaw puzzle piece
	#print("x1 is ", x1)
	#print("y1 is ", y1)
	while (True):  # infinite loop while sweeping, looking for black pixel
		sweepAngleRad = sweepAngleDeg * math.pi / 180
		x2 = PIXEL_STEP * math.cos(sweepAngleRad) + x1
		y2 = PIXEL_STEP * math.sin(sweepAngleRad) + y1

		#canvas.create_line(x1, y1, x2, y2, fill='springgreen2')
		canvas.update()
		# time.sleep(0.2) # HARDCODED  Pause at each sweep line

		tempPixelC = PILimg.getpixel((x2, y2))  # three-component RGB tuple
		#print("tempPixelC is    ", tempPixelC)

		# The input image is a white jigsaw puzzle shape on a black background.
		# Continue sweep while the pixel is black.
		if not (isWhite(tempPixelC)):  # Have not yet found white pixel on sweep
			sweepAngleDeg = sweepAngleDeg + 10 #5  # degrees
		else:  # have found white pixel on sweep

			sweep_angle_tracker.append(sweepAngleDeg)

			canvas.create_oval(x2-5, y2-5, x2+5, y2+5, fill='red', outline='black')

			#print("Point on jigsaw piece boundary:  (", "%.4f" % x2, ", ", "%.4f" % y2, ")" )
			#print("Rotation on jigsaw piece boundary:  (", "%.4f" % rotated_x, ", ", "%.4f" % rotated_y, ")" )
			x1 = x2
			y1 = y2
			point_tracker.append([x1, y1])
			sweepAngleDeg = sweepAngleDeg - 90  # next sweep starts 90 deg from this
			sampleCount = sampleCount + 1
			break  # Update point on boundary of puzzle piece and repeat sweep

	# If we've returned to the origin on the boundary of this puzzle piece, halt.
	# print(x1, "  ", currentX, "     ", y1, "  ", currentY)
	if (abs(x1 - currentX) <= PIXEL_STEP) and (abs(y1 - currentY) <= PIXEL_STEP) and sampleCount > 5:
		break
def findStraightEdges(point_list):
    angles = []
    edge_point = []
    angle_variance = 0.6
    for i in range(0,len(point_list)-1):
        
        point_a_x = point_list[i][0]
        point_a_y = point_list[i][1]
        
        point_b_x = point_list[i+1][0]
        point_b_y = point_list[i+1][1]
        
        angles.append(angle(point_a_x,point_a_y,point_b_x,point_b_y))
    for j in range(len(angles)-1):
        if(angles[j] <= angles[j+1] + angle_variance and angles[j] >= angles[j+1] - angle_variance and angles[j] >= angles[j-1] - angle_variance and angles[j] <= angles[j-1] + angle_variance):
            #print(angles[j])
            edge_point.append(point_list[j])
            #print(edge_point) 
        else:
            edge_point.clear();
        
    for point in edge_point:
        canvas.create_oval(point[0]-5, point[1]-5, point[0]+5, point[1]+5, fill='blue', outline='black')
    #print(slope)
    return []
        
                   
edgeFind(sweep_angle_tracker)
#rotate(point_tracker)
findStraightEdges(point_tracker)







mainloop()   # Graphics loop -- This statement follows all other statements



