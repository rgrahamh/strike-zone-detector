import numpy as np
import cv2 as cv

def interpImg():
	img = cv.imread('../example-images/colortestfile.bmp')
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	
	dimensions = img.shape

	height = dimensions[0]
	width = dimensions[1]

	#Set the bounds based upon image dimensions
	strike_upper_bound = height / 3
	strike_lower_bound = height * 2 / 3
	strike_left_bound = width / 3
	strike_right_bound = width * 2 / 3

	num_comp, conn_img = cv.connectedComponents(gray, 8)
	used_val = np.zeros(num_comp)

	#Initialize incrementors
	red_strike = 0
	red_ball = 0
	blue_strike = 0
	blue_ball = 0
	green_strike = 0
	green_ball = 0

	for y in range(height):
		for x in range(width):
			bwval = conn_img[y][x]
			#print(img[y][x])
			if used_val[bwval] == 0:
				print(img[y][x])
				#If the dot is red
				if img[y][x][0] == 255 and img[y][x][1] == 0 and img[y][x][2] == 0:
					if y < strike_upper_bound and y > strike_lower_bound and x > strike_left_bound and x < strike_right_bound:
						red_strike += 1
					else:
						red_ball += 1
				#Else if green
				elif img[y][x][0] == 0 and img[y][x][1] == 255 and img[y][x][2] == 0:
					if y < strike_upper_bound and y > strike_lower_bound and x > strike_left_bound and x < strike_right_bound:
						green_strike += 1
					else:
						green_ball += 1
				#Else if blue
				elif img[y][x][0] == 64 and img[y][x][1] == 64 and img[y][x][2] == 192:
					if y < strike_upper_bound and y > strike_lower_bound and x > strike_left_bound and x < strike_right_bound:
						blue_strike += 1
					else:
						blue_ball += 1

				#Set the checked flag
				used_val[bwval] = 1
		
	print("Red strikes:", red_strike)
	print("Red balls:", red_ball)
	print("Blue strikes:", blue_strike)
	print("Blue balls:", blue_ball)
	print("Green strikes:", green_strike)
	print("Green balls:", green_ball)

interpImg()
