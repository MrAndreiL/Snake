import pygame
class Tail():
	def __init__(self, x, y, color, width, height, speed):
		self.x = x
		self.y = y
		self.color = color
		self.width = width
		self.height = height
		self.speed = speed

	def draw(self, surface):
		#print(self.x, self.y)
		pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

	def move(self, direction):
		self.direction = direction
		if direction == 1:
			self.x += self.speed
		elif direction == 2:
			self.y -= self.speed
		elif direction == 3:
			self.x -= self.speed
		else:
			self.y += self.speed

	def get_tail_pos(self):
		return self.x,self.y

	def get_tail_relative_pos(self):
		return [self.x, self.y]

	def return_direction(self):
		return self.direction
