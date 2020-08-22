import pygame
pygame.init()
class Button:
	def __init__(self, x, y, width, height, color, surface, text = None):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color
		self.text = text
		self.font = font = pygame.font.SysFont("comicsans", 40)
		self.surface = surface

	def draw_button(self):
		pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))

		if self.text is not None:
			text = self.font.render(self.text, 1, (0, 0, 0))
			textwidth = text.get_width()
			textheight = text.get_height()
			self.surface.blit(text, ((self.x + self.width / 2) - (textwidth / 2), (self.y + self.height / 2) - (textheight / 2)))


