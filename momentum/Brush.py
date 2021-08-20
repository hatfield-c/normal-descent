import random
import math
import momentum.Vec2

class Brush:
	def __init__(self, mass):
		self.mass = mass

		self.position = momentum.Vec2.Vec2()
		self.velocity = momentum.Vec2.Vec2()
		self.active = True

	def Update(self, surface):
		gravity = surface.GetForce(self)
		gForce = gravity.Magnitude()

		if gForce > 0:
			acceleration = gForce / self.mass
			
			acceleration = gravity.WithMagnitude(acceleration)
			
			self.velocity = self.velocity.Add(acceleration)
			
			self.velocity = momentum.Vec2.Vec2(
				max(
					-momentum.CONSTANTS.MAX_VELOCITY, 
					min(self.velocity.y * momentum.CONSTANTS.DRAG, momentum.CONSTANTS.MAX_VELOCITY)
				),
				max(
					-momentum.CONSTANTS.MAX_VELOCITY, 
					min(self.velocity.x * momentum.CONSTANTS.DRAG, momentum.CONSTANTS.MAX_VELOCITY)
				)
			)

		moveDir = surface.PixelDirection(self.velocity)

		self.position.y += moveDir.y
		self.position.x += moveDir.x

		if self.position.y < 0:
			self.position.y = 0
			self.velocity.y = -self.velocity.y

		if self.position.y >= momentum.CONSTANTS.IMG_SIZE[0]:
			self.position.y = momentum.CONSTANTS.IMG_SIZE[0] - 1
			self.velocity.y = -self.velocity.y

		if self.position.x < 0:
			self.position.x = 0
			self.velocity.x = -self.velocity.x

		if self.position.x >= momentum.CONSTANTS.IMG_SIZE[1]:
			self.position.x = momentum.CONSTANTS.IMG_SIZE[1] - 1
			self.velocity.x = -self.velocity.x

	def ApplyDot(self, canvas, surface):
		if random.random() < surface.Get(self.position.y, self.position.x) * 0.1:
			return

		canvas[int(self.position.y), int(self.position.x)] = 0

	def ApplyCircle(self, canvas, radius):
		for j in range(-radius, radius, 1):
			for i in range(-radius, radius, 1):

				yPos = self.position.y + j
				xPos = self.position.x + i

				if yPos < 0 or yPos >= momentum.CONSTANTS.IMG_SIZE[0] or xPos < 0 or xPos >= momentum.CONSTANTS.IMG_SIZE[1]:
					continue

				canvas[int(yPos), int(xPos)] = 0

	def Die(self):
		self.active = False

	def IsActive(self):
		return self.active