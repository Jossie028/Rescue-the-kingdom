#Importamos las librerias y archivos
import pygame
import sys

from scripts.jugador import Caballero
from scripts.Mundos import *
from scripts.enemigo import Enemigo


# Hacemos la pantalla y le damos nombre
size = (ANCHO_PANTALLA, ALTO_PANTALLA)
screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.FULLSCREEN)
pygame.display.set_caption("Rescue The Kingdom")

# Creamos el jugador y los enemigos
jugador=Caballero(400,300)
enemigos =[]
enemigo_prueba=Enemigo(200,200)
enemigos.append(enemigo_prueba)
print(f"Enemigos creados: {len(enemigos)}")

# Reloj del juego
clock = pygame.time.Clock()

#Creamos los muros
muros = []
for fila_index, fila in enumerate(MAPA):
    for col_index, piso in enumerate(fila):
        x =col_index * TILE_SIZE
        y = fila_index * TILE_SIZE
        if piso == '1':
            muros.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

# Inicializacion del bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jugador.atacar(enemigos)
            

#Dibujamos el fondo y los muros
    screen.fill((0, 0, 0))
    for muro in muros:
        pygame.draw.rect(screen, (100, 100, 100), muro)
    

#Dibujamos al jugador y enemigos
    jugador.mover(muros)
    jugador.dibujar(screen)


    for enemigo in enemigos:
            enemigo.actualizar(jugador.rect)
            enemigo.atacar(jugador)
            enemigo.dibujar(screen)


#ibujamos y configuramos la barra de vida del jugador
    pygame.draw.rect(screen, (50,50,50), (20, 20, 200, 20))

    if jugador.vida >0:
        pygame.draw.rect(screen, (0, 255, 0), (20, 20, jugador.vida * 2, 20))
    if jugador.vida <= 0:
        print("game over")
        pygame.quit()
        sys.exit()

    pygame.display.flip()

# Establecemos el tiempo del juego a 30 FPS
    clock.tick(30)

pygame.quit()
sys.exit()
