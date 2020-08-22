import pygame

class Snake():
	def __init__(self, color, startx, starty, width, height):
		self.color  = color
		self.width  = width
		self.height = height
		self.q  	= [[startx, starty]]
		self.length = 1

	def draw(self, surface, positions):
		for e in self.q:
			pygame.draw.rect(surface, self.color, (e[0], e[1], self.width, self.height))
	
	def add_head(self, newx, newy):
		# Adds the heads new position.
		#print(self.length)
		#self.q.pop()
		self.q.insert(0,[newx, newy])
		if (len(self.q) > self.length):
			self.q.pop(1)


	def delete_last_pos(self):
		self.q.pop(1)
		print(self.q)

	def get_headx(self):
		return self.q[0][0]

	def get_heady(self):
		return self.q[0][1]

	def get_body(self):
		return self.q

	def get_body_lenght(self):
		return self.length





	


