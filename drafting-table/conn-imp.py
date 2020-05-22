import numpy as np
import math
import cv2 as cv

COLOR_THRESH = 20

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

def getAngle(coord1, coord2):
	return math.atan2(coord1[0] - coord2[0], coord1[1] - coord2[1])

def getDist(coord1, coord2):
	return math.sqrt(pow(coord1[0] - coord2[0], 2) + pow(coord1[1] - coord2[1], 2))

def isInBounds(y, x, upper_bound, lower_bound, left_bound, right_bound):
	return y > upper_bound and y < lower_bound and x > left_bound and x < right_bound

def interpImg():
	img = cv.imread('../example-images/irl1.bmp')
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	
	dimensions = img.shape

	height = dimensions[0]
	width = dimensions[1]

	#Get the cornered image
	edge_gray = gray.copy()
	edge_img = cv.cornerHarris(edge_gray, 2, 3, 0.04)
	
	#Getting image dimensions
	dimensions = img.shape
	height = dimensions[0]
	width = dimensions[1]

	corners = []
	bounds = [[0, 0], [0, 0], [0, 0], [0, 0]]
	max_sz = 0

	for y in range(height):
		for x in range(width):
			if edge_img[y][x] > 0.005:
				corners.append([y, x])
	
	for top_left in corners:
		for top_right in corners:
			for bot_left in corners:
				for bot_right in corners:
					#If they're oriented properly
					if top_left[1] < top_right[1] and top_left[1] < bot_right[1] and bot_left[1] < bot_right[1] and bot_left[1] < bot_right[1] and top_left[0] < bot_left[0] and top_left[0] < bot_right[0] and top_right[0] < bot_right[0] and top_right[0] < bot_left[0]:
						#If they're parallel on opposite sides
						if abs(getAngle(top_left, top_right) - getAngle(bot_left, bot_right)) < 0.01 and abs(getAngle(top_left, bot_left) - getAngle(top_right, bot_right)) < 0.01:
							size = getDist(top_left, top_right) * getDist(top_left, bot_right)
							#If they're the max area
							if size > max_sz:
								bounds[0] = top_left
								bounds[1] = top_right
								bounds[2] = bot_left
								bounds[3] = bot_right
								max_sz = size

	print(bounds[0])
	print(bounds[1])
	print(bounds[2])
	print(bounds[3])

	dot_img = img.copy()
	for y in range(height):
		for x in range(width):
			if int(img[y][x][0]) - ((int(img[y][x][1]) + img[y][x][2]) / 2) > COLOR_THRESH or int(img[y][x][1]) - ((int(img[y][x][0]) + img[y][x][2]) / 2) > COLOR_THRESH or int(img[y][x][2]) - ((int(img[y][x][0]) + img[y][x][1]) / 2) > COLOR_THRESH:
				for i in range(3):
					dot_img[y][x][i] = 255
			else:
				for i in range(3):
					dot_img[y][x][i] = 0
				
	bw_dot_img = cv.cvtColor(dot_img, cv.COLOR_BGR2GRAY)

	cv.imwrite('bwdot.bmp', bw_dot_img)

	#Set the bounds based upon image dimensions
	#Using top left as a starting point, go a quarter of the way to bot left.
	strike_upper_bound = bounds[0][0] + ((bounds[0][0] - bounds[2][0]) / 4)

	#Using top left as a starting point, go three quarters of the way to bot left.
	strike_lower_bound = bounds[0][0] + ((bounds[0][0] - bounds[2][0]) * 3 / 4)

	#Using top left as a starting point, go a quarter of the way to top right.
	strike_left_bound = bounds[0][1] + ((bounds[0][1] - bounds[1][1]) / 4)

	#Using top left as a starting point, go three quarters of the way to top right.
	strike_right_bound = bounds[0][1] + ((bounds[0][1] - bounds[1][1]) * 3 / 4)

	num_comp, conn_img = cv.connectedComponents(bw_dot_img, 4)
	used_val = np.zeros(num_comp)
	used_val[0] = 1

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
			if used_val[bwval] == 0:
				#We should have hit the peak of the circle due to our search ordering, so x == x_center
				#Calculating the Y center
				y_val = y
				while y_val < height and conn_img[y_val][x] == bwval:
					y_val += 1
				y_center = (y_val + y) / 2

				#If the dot is red
				color = getColor(img, y, x)
				if color == 0:
					if isInBounds(y_center, x, strike_upper_bound, strike_lower_bound, strike_left_bound, strike_right_bound):
						red_strike += 1
					else:
						red_ball += 1
				#Else if green
				elif color == 1:
					if isInBounds(y_center, x, strike_upper_bound, strike_lower_bound, strike_left_bound, strike_right_bound):
						green_strike += 1
					else:
						green_ball += 1
				#Else if blue
				elif color == 2:
					if isInBounds(y_center, x, strike_upper_bound, strike_lower_bound, strike_left_bound, strike_right_bound):
						blue_strike += 1
					else:
						blue_ball += 1

				#Set the checked flag
				used_val[bwval] = 1
		
	#Output
	print("Red strikes:", red_strike)
	print("Red balls:", red_ball)
	print("Blue strikes:", blue_strike)
	print("Blue balls:", blue_ball)
	print("Green strikes:", green_strike)
	print("Green balls:", green_ball)

interpImg()
