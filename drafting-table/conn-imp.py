import numpy as np
import cv2 as cv

def getColor(img, y, x):
	#Red
	if img[y][x][2] > img[y][x][1] and img[y][x][2] > img[y][x][0]:
		return 0
	#Green
	elif img[y][x][1] > img[y][x][2] and img[y][x][1] > img[y][x][0]:
		return 1
	#Blue
	elif img[y][x][0] > img[y][x][1] and img[y][x][0] > img[y][x][2]:
		return 2
	return -1

def isInBounds(y, x, upper_bound, lower_bound, left_bound, right_bound):
	return y > upper_bound and y < lower_bound and x > left_bound and x < right_bound

def interpImg():
	img = cv.imread('../example-images/colortestfile.bmp')
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	
	dimensions = img.shape

	height = dimensions[0]
	width = dimensions[1]

	dot_img = img.copy()
	for y in range(height):
		for x in range(width):
			if abs(img[y][x][0] - img[y][x][1]) < 40 and abs(img[y][x][1] - img[y][x][2]) < 40 and abs(img[y][x][2] - img[y][x][0]) < 40:
				for i in range(3):
					dot_img[y][x][i] = 0
			else:
				for i in range(3):
					dot_img[y][x][i] = 255
				
	bw_dot_img = cv.cvtColor(dot_img, cv.COLOR_BGR2GRAY)
	cv.imshow("img", bw_dot_img)

	#Set the bounds based upon image dimensions
	strike_upper_bound = height / 3
	strike_lower_bound = height * 2 / 3
	strike_left_bound = width / 3
	strike_right_bound = width * 2 / 3

	num_comp, conn_img = cv.connectedComponents(bw_dot_img, 4)
	used_val = np.zeros(num_comp)

	print(set(conn_img.reshape(-1).tolist()))

	#Initialize incrementors
	red_strike = 0
	red_ball = 0
	blue_strike = 0
	blue_ball = 0
	green_strike = 0
	green_ball = 0

	print(conn_img)

	for y in range(height):
		for x in range(width):
			bwval = conn_img[y][x]
			#print(img[y][x])
			if used_val[bwval] == 0:
				print(img[y][x])
				#If the dot is red
				color = getColor(img, y, x)
				if color == 0:
					if isInBounds(y, x, strike_upper_bound, strike_lower_bound, strike_left_bound, strike_right_bound):
						red_strike += 1
					else:
						red_ball += 1
				#Else if green
				elif color == 1:
					if isInBounds(y, x, strike_upper_bound, strike_lower_bound, strike_left_bound, strike_right_bound):
						green_strike += 1
					else:
						green_ball += 1
				#Else if blue
				elif color == 2:
					if isInBounds(y, x, strike_upper_bound, strike_lower_bound, strike_left_bound, strike_right_bound):
						blue_strike += 1
					else:
						blue_ball += 1

				#Set the checked flag
				used_val[bwval] = 1

	cv.waitKey(0)
		
	print("Red strikes:", red_strike)
	print("Red balls:", red_ball)
	print("Blue strikes:", blue_strike)
	print("Blue balls:", blue_ball)
	print("Green strikes:", green_strike)
	print("Green balls:", green_ball)
	cv.destroyAllWindows()

	cv.imwrite("bw_img.png", bw_dot_img)

interpImg()
