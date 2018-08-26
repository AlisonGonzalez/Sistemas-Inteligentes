import pygame
from random import choice


class Celda(pygame.sprite.Sprite):
	ancho = 5
	alto = 5
	def __init__(self, x,y,laberinto):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface([self.ancho, self.alto])
		self.image.fill((5, 144, 255))
		self.rect = self.image.get_rect()
		self.rect.x = x * self.ancho
		self.rect.y = y * self.alto

		self.x = x
		self.y = y
		self.laberinto = laberinto

		self.nbs = [(x+na, y +  nb) for na,nb in ((-2,0),(0,-2),(2,0),(0,2))
					if 0 <= x + na < laberinto.ancho and 0 <= y + nb < laberinto.alto]

	def pinta(self, pantalla):
		pantalla.blit(self.image, self.rect)

	def cambiaColor(self, r, g, b):
		self.image.fill((r,g,b))


class Pared(Celda):
	def __init__(self, x, y, laberinto):
		super(Pared, self).__init__(x,y,laberinto)
		self.image.fill((255,255,40))
		self.type = 0

class Laberinto:
		def __init__(self, tamanio):
			self.ancho, self.alto = tamanio[0] // Celda.ancho, tamanio[1] // Celda.alto
			self.tablero = [[Pared(x,y, self) for y in range(self.alto)] for x in range(self.ancho) ]
			self.nodos = []


		def getCelda(self, x, y):
			return self.tablero[x][y]


		def agregaPared(self, x, y):
			self.tablero[x][y] = Pared(x,y,self)

		def inicio(self, r,g,b, pantalla):
			celda = choice(self.nodos)
			celda.cambiaColor(r,g,b)
			celda.pinta(pantalla)
			return celda

		def meta(self, r,g,b, pantalla):
			celda = choice(self.nodos)
			celda.cambiaColor(r,g,b)
			celda.pinta(pantalla)
			return celda

		def pintaLaberinto(self, pantalla):
			for renglon in self.tablero:
				for celda in renglon:					
					celda.pinta(pantalla)


		def creaLaberinto(self, pantalla = None, animado = False):
			sinVisitar = [columna for renglon in self.tablero for columna in renglon if columna.x % 2 and columna.y % 2]
			actual = sinVisitar.pop()
			pila = []
			self.nodos = []

			while sinVisitar:
				try:
					nuevo = choice([ c for c in map(lambda x: self.getCelda(*x), actual.nbs ) if c in sinVisitar ])
					pila.append(actual)
					na, nb = actual.x - (actual.x -nuevo.x) // 2, actual.y - (actual.y -nuevo.y) // 2 
					self.tablero[na][nb] = Celda(na, nb, self)
					self.tablero[actual.x][actual.y] =  Celda(actual.x, actual.y, self)
					
					self.nodos.append(self.tablero[na][nb])
					self.nodos.append(self.tablero[actual.x][actual.y])

					actual = nuevo
					sinVisitar.remove(nuevo)

					self.pintaLaberinto(pantalla)
					pygame.display.update()
					pygame.time.wait(10)
				except IndexError:
					if pila:
						actual = pila.pop()