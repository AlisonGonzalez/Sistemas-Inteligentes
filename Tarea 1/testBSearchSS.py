from estructuras import *

def bsV03(g, s, m):
	frontera = ColaPriorizada()
	frontera.put(0, s)
	anteriores = {}
	anteriores[s] = None
	while not frontera.esVacia():
		actual = frontera.get()
		if actual == m:
			break
		for n in g.vecinos(actual):
			if n not in anteriores:
				frontera.put(g.costo(actual, n), n)
				anteriores[n] = actual

	return anteriores
	
def main():
	g = Grafo()
	with open("espana.txt") as f:
		for l in f:
			(c1, c2, c) = l.split(',')
			g.agregarAristaPeso(c1, c2, c)
	
	print(bsV03(g,'Coruna','Sevilla'))

if __name__ == '__main__':
	main()