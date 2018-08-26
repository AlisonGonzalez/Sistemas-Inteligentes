import os
from laberinto import *
import pygame
from pygame.locals import *

T = (Celda.ancho * 50, Celda.alto * 50)


def main():
		pygame.init()
		pantalla_info = pygame.display.Info()
		os.environ['SDL_VIDEO_WINDOWS_POS'] = '{},{}'.format(pantalla_info.current_w // 2 - T[0] // 2,
												pantalla_info.current_h // 2 - T[1] // 2)
		pantalla = pygame.display.set_mode(T)

		pygame.display.set_caption('Laberinto')
		r = pygame.time.Clock()
		laberinto = Laberinto(T)
		laberinto.creaLaberinto(pantalla, True)
		laberinto.inicio(80, 255,120, pantalla)
		laberinto.meta(200, 5,210, pantalla)

		fin = False
		while not fin:
			for e in pygame.event.get():
				if e.type == QUIT:
					fin = True
			pygame.display.update()
			r.tick()

if __name__ == '__main__':
	main()