import math

class Vec2:
	def __init__(self, y = 0, x = 0):
		self.y = y
		self.x = x

	def Tuple(self):
		return (self.y, self.x)

	def Magnitude(self):
		return math.sqrt( ( self.y ** 2) + ( self.x ** 2) )

	def WithMagnitude(self, magnitude):
		unit = self.Unit()

		return Vec2(
			unit.y * magnitude,
			unit.x * magnitude
		)

	def Distance(self, y, x):
		return math.sqrt(
			( (self.y - y) ** 2 ) + ( (self.x - x) ** 2 )
		)

	def Add(self, amount):
		return Vec2(
			self.y + amount.y,
			self.x + amount.x
		)

	def Subtract(self, amount):
		return Vec2(
			self.y - amount.y,
			self.x - amount.x
		)

	def Unit(self):
		if self.y == 0 and self.x == 0:
			return Vec2(0, 0)

		return Vec2(
			self.y / self.Magnitude(),
			self.x / self.Magnitude()
		)

	def ToList(self, reverse = False):
		if not reverse:
			return [ self.y, self.x ]
		else:
			return [ self.x, self.y ]

	def __str__(self):
		return "(y:" + str(self.y) + ", x:" + str(self.x) + ")"