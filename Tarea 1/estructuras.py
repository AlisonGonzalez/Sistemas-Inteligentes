import collections
import heapq

class Nodo:
	def __init__(self, n, c = 0):
		self.nombre = n
		self.costo = c
		self.vecinos = {}
	def agregarVecino(self, v, c = 0):
		self.vecinos[v] = c
	def getVecinos(self):
		return self.vecinos.keys()
	def getId(self):
		return self.nombre
	def getCosto(self,v):
		return self.vecinos[v]
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

class ColaPriorizada:
	def __init__(self):
		self.elementos = []

	def esVacia(self):
		return len(self.elementos) == 0

	def put(self, prioridad , d):
		heapq.heappush(self.elementos, (prioridad, d))

	def get(self):
		return heapq.heappop(self.elementos)[1]

class Cola:
	def __init__(self):
		self.elementos = collections.deque()
	def esVacia(self):
		return len(self.elementos) == 0

	def put(self, d):
		self.elementos.append(d)

	def get(self):
		return self.elementos.popleft()

class Grafo:
	def __init__(self):
		self.aristas = {}

	def agregarNodo(self, v):
		nuevoNodo = Nodo(v)
		self.aristas[v] = nuevoNodo
	
	def agregarAristaPeso(self, f, to, c = 0):
		if f not in self.aristas:
			self.agregarNodo(f)
		if to not in self.aristas:
			self.agregarNodo(to)
		self.aristas[f].agregarVecino(to, c)
		self.aristas[to].agregarVecino(f, c)

	def vecinos(self, id):
		return self.aristas[id].getVecinos()

	def costo(self, id, id2):
		return self.aristas[id].getCosto(id2)

	def __str__(self):
		return str(self.aristas)

