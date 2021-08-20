import numpy as np
import math
import random
import cv2

import momentum.Surface
import momentum.Brush

class Artist:
	def __init__(
		self, 
    	imgPath
	):
		self.img = momentum.Surface.Surface(imgPath)

	def paint(self, steps):
		canvas = np.ones(momentum.CONSTANTS.IMG_SIZE)
		#canvas = np.copy(self.surface.img)

		brushes = []

		b1 = self.CirlceRandom(
			num = 900, 
			yCenter = 1270,
			xCenter = 670,
			radius = 400
		)

		b2 = self.CirlceRandom(
			num = 1600, 
			yCenter = 830,
			xCenter = 670,
			radius = 400
		)

		b3 = self.CirlceRandom(
			num = 500, 
			yCenter = 520,
			xCenter = 670,
			radius = 150
		)

		b4 = self.CirlceRandom(
			num = 500, 
			yCenter = 260,
			xCenter = 670,
			radius = 120
		)

		b5 = self.CirlceRandom(
			num = 100, 
			yCenter = 75,
			xCenter = 688,
			radius = 40
		)

		brushes.extend(b1)
		brushes.extend(b2)
		brushes.extend(b3)
		brushes.extend(b4)
		brushes.extend(b5)

		print("    Brushes     :", len(brushes), "\n")

		for step in range(steps):

			if step % math.ceil(steps / 10) == 0:
				print("[ Step", step, "]")

			for brush in brushes:
				brush.ApplyDot(
					canvas, 
					self.img
				)

			for brush in brushes:
				if not brush.IsActive():
					brushes.remove(brush)
					continue

				brush.Update(self.img)

			if len(brushes) < 1:
				print("No active brushes remaining! Terminating.")
				break

		canvas = canvas * 255
		canvas = canvas.astype("uint8")

		return canvas

	def Vertical(self, num, x, direction, strength):
		brushes = []

		spacing = int(momentum.CONSTANTS.IMG_SIZE[0] / num)

		for i in range(num):
			brush = momentum.Brush.Brush(momentum.CONSTANTS.BRUSH_MASS)

			brush.position.y = i * spacing
			brush.position.x = x

			brush.velocity.y = 0
			brush.velocity.x = direction * strength

			brushes.append(brush)		

		return brushes

	def Horizontal(self, num, y, direction, strength):
		brushes = []

		spacing = int(momentum.CONSTANTS.IMG_SIZE[1] / num)

		for i in range(num):
			brush = momentum.Brush.Brush(momentum.CONSTANTS.BRUSH_MASS)

			brush.position.y = y
			brush.position.x = i * spacing

			brush.velocity.y = direction * strength
			brush.velocity.x = 0

			brushes.append(brush)		

		return brushes

	def RandomBrushes(self, num):
		brushes = []
		velocity = 1.5

		for i in range(num):
			brush = momentum.Brush.Brush(momentum.CONSTANTS.BRUSH_MASS)

			brush.position.y = random.randrange(0, momentum.CONSTANTS.IMG_SIZE[0])
			brush.position.x = random.randrange(0, momentum.CONSTANTS.IMG_SIZE[1])

			brush.velocity.y = random.uniform(-velocity, velocity)
			brush.velocity.x = random.uniform(-velocity, velocity)

			brushes.append(brush)

		return brushes

	def CirlceRandom(self, num, yCenter, xCenter, radius):
		brushes = []
		velocity = 1.5
		modeMult = 0.6

		for i in range(num):
			r = random.triangular(0.0000001, radius, radius * modeMult)
			theta = random.uniform(-math.pi, math.pi)

			yPos = r * math.sin(theta) + yCenter
			xPos = r * math.cos(theta) + xCenter

			if yPos < 0 or yPos >= momentum.CONSTANTS.IMG_SIZE[0] or xPos < 0 or xPos >= momentum.CONSTANTS.IMG_SIZE[1]:
				continue

			brush = momentum.Brush.Brush(momentum.CONSTANTS.BRUSH_MASS)

			brush.position.y = yPos
			brush.position.x = xPos

			brush.velocity.y = random.uniform(-velocity, velocity)
			brush.velocity.x = random.uniform(-velocity, velocity)

			brushes.append(brush)

		return brushes