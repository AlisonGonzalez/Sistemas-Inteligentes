import pygame
from random import choice
from time import sleep


class Celda(pygame.sprite.Sprite):
	ancho = 10
	alto = 10
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
		self.heuristic = 0;

		self.nbs = [(x+na, y +  nb) for na,nb in ((-2,0),(0,-2),(2,0),(0,2))
					if 0 <= x + na < laberinto.ancho and 0 <= y + nb < laberinto.alto]

	def pinta(self, pantalla):
		self.pantalla = pantalla
		pantalla.blit(self.image, self.rect)

	def update(self):
		self.pantalla.blit(self.image, self.rect)

	def cambiaColor(self, r, g, b):
		self.image.fill((r,g,b))

	def __str__(self):
		return 'x: ' + str(self.x) + ' y: ' + str(self.y) + ' h:' + str(self.heuristic)


class Pared(Celda):
	def __init__(self, x, y, laberinto):
		super(Pared, self).__init__(x,y,laberinto)
		self.image.fill((255,255,40))
		self.type = 0

class Astar:
	def __init__(self, laberinto):
		self.laberinto = laberinto

	def calculateHeuristic(self):
		for cell in self.laberinto.nodos:
				x = abs(self.laberinto.meta.x - cell.x)
				y = abs(self.laberinto.meta.y - cell.y)
				cell.heuristic = x + y;

	def getPath(self):
		self.current = self.laberinto.inicio
		self.openList = {}
		self.closedList = {self.laberinto.inicio: None}
		flag = True

		while flag:

			if self.current.x > 1:
				left = self.laberinto.getCelda(self.current.x-1,self.current.y)
				leftClass = self.laberinto.getCelda(self.current.x-1,self.current.y).__class__.__name__
				if leftClass != 'Pared' and left not in self.closedList:
					self.openList[self.laberinto.getCelda(self.current.x-1,self.current.y)] = self.current
			if self.current.x < 49:
				right = self.laberinto.getCelda(self.current.x+1,self.current.y)
				rightClass = self.laberinto.getCelda(self.current.x+1,self.current.y).__class__.__name__
				if rightClass != 'Pared' and right not in self.closedList:
					self.openList[self.laberinto.getCelda(self.current.x+1,self.current.y)] = self.current
			if self.current.y > 1:
				down = self.laberinto.getCelda(self.current.x,self.current.y-1)
				downClass = self.laberinto.getCelda(self.current.x,self.current.y-1).__class__.__name__
				if downClass != 'Pared' and down not in self.closedList:
					self.openList[self.laberinto.getCelda(self.current.x,self.current.y-1)] = self.current
			if self.current.y < 49:
				up = self.laberinto.getCelda(self.current.x,self.current.y+1)
				upClass = self.laberinto.getCelda(self.current.x,self.current.y+1).__class__.__name__
				if upClass != 'Pared' and up not in self.closedList:
					self.openList[self.laberinto.getCelda(self.current.x,self.current.y+1)] = self.current

			smaller = 1000
			for neighbor in self.openList:
				if neighbor.heuristic < smaller:
					smaller = neighbor.heuristic
					self.current = neighbor

			self.closedList[self.current] = self.openList.get(self.current)
			if len(self.openList) == 0 or (self.current.x == self.laberinto.meta.x and self.current.y == self.laberinto.meta.y):
				self.current == self.laberinto.meta
				flag = False;
			else:
				del self.openList[self.current]

		stack = []
		prev = self.closedList.get(self.laberinto.meta)
		stack.append(prev)

		while self.closedList.get(prev)!=self.laberinto.inicio:
			prev = self.closedList.get(prev)
			stack.append(prev)

		while stack:
			val = stack.pop()
			val.cambiaColor(1,2,3)
			self.laberinto.updateLaberinto()
			print(val)

	def printer(self):
		for cell in self.laberinto.nodos:
			print('x: {0} y: {1} heuristic:{2}'.format(cell.x, cell.y, cell.heuristic))

	def __str__(self):
		return 'laberinto: ' + str(self.laberinto)


class Laberinto:
		def __init__(self, tamanio):
			self.ancho, self.alto = tamanio[0] // Celda.ancho, tamanio[1] // Celda.alto
			self.tablero = [[Pared(x,y, self) for y in range(self.alto)] for x in range(self.ancho) ]
			self.nodos = []

		def __str__(self):
			return 'Laberinto'


		def getCelda(self, x, y):
			return self.tablero[x][y]

		def getNodos(self):
			return self.nodos;

		def agregaPared(self, x, y):
			self.tablero[x][y] = Pared(x,y,self)

		def inicio(self, r,g,b, pantalla):
			self.pantalla = pantalla
			celda = choice(self.nodos)
			celda.cambiaColor(r,g,b)
			celda.pinta(pantalla)
			print(' ==== > inicio:', celda)
			self.inicio = celda
			return celda

		def meta(self, r,g,b, pantalla):
			celda = choice(self.nodos)
			print(' ==== > meta:', celda)
			#celda = self.getCelda(2,2)
			celda.cambiaColor(r,g,b)
			celda.pinta(pantalla)
			self.meta = celda
			return celda

		def pintaLaberinto(self, pantalla):
			self.pantalla = pantalla
			for renglon in self.tablero:
				for celda in renglon:					
					celda.pinta(pantalla)

		def updateLaberinto(self):
			for renglon in self.tablero:
				for celda in renglon:					
					celda.pinta(self.pantalla)


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