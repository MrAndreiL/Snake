import pygame
class Food():
	def __init__(self, x, y, tileWidth, tileHeight, surface, color):
		self.x = x
		self.y = y
		self.tileWidth = tileWidth
		self.tileHeight = tileHeight
		self.surface = surface
		self.color = color
		self.pos = []

	def draw(self):
		self.x = self.pos[0][0]
		self.y = self.pos[0][1]
		centerx = self.x + (self.tileWidth // 2)
		centery = self.y + (self.tileHeight // 2)
		pygame.draw.circle(self.surface, self.color, (centerx, centery), 15)

	def add_pos(self, x, y):
		if len(self.pos) != 0:
			self.pos.pop()
		self.pos.append([x, y])

	def get_pos(self):
		return self.pos[0][0], self.pos[0][1]

