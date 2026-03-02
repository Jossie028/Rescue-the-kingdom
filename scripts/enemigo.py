import pygame
from scripts.Mapas import *
from scripts.navegacion import astar

# Clase del enemigo
class Enemigo:
    def __init__(self, x, y):
        # Rectángulo del enemigo (posición y tamaño)
        self.rect = pygame.Rect(x, y, 32, 32)
        self.color = (0, 0, 255)

        # Posición del enemigo en la grilla del mapa
        self.posicion_grid = [x // 32, y // 32]

        # Velocidad de movimiento
        self.velocidad = 2

        # Camino que calculará el A*
        self.camino = []

        # Estado del enemigo
        self.estado = "Reposo"

        # Distancia a la que puede ver al jugador
        self.radio_vision = 5

        # Daño que hace al jugador
        self.daño = 10

        # Control del tiempo entre ataques
        self.ultimo_ataque = 0
        self.tiempo_entre_ataques = 2000

    # Dibuja el enemigo en pantalla
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)

        # Dibuja el camino que calcula el A* (solo para visualizar)
        if self.camino:
            puntos_pixeles = []
            for punto in self.camino:
                px = (punto[0] * TILE_SIZE) + 16
                py = (punto[1] * TILE_SIZE) + 16
                puntos_pixeles.append((px, py))
            
            if len(puntos_pixeles) > 1:
                pygame.draw.lines(superficie, (255, 255, 255), False, puntos_pixeles, 2)

    # Actualiza el comportamiento del enemigo
    def actualizar(self, jugador_rect, mapa_actual):
        # Posición del enemigo en la grilla
        grid_x_yo = self.rect.x // TILE_SIZE
        grid_y_yo = self.rect.y // TILE_SIZE
        inicio = (grid_x_yo, grid_y_yo)

        # Posición del jugador en la grilla
        grid_x_jugador = jugador_rect.x // TILE_SIZE
        grid_y_jugador = jugador_rect.y // TILE_SIZE
        fin = (grid_x_jugador, grid_y_jugador)

        # Distancia entre enemigo y jugador
        distancia = abs(grid_x_yo - grid_x_jugador) + abs(grid_y_yo - grid_y_jugador)

        # Si el jugador está cerca, lo persigue
        if distancia <= self.radio_vision:
            self.estado = "Persecucion"
            self.color = (255, 0, 0)

            # Calcula el camino usando A*
            self.camino = astar(mapa_actual, inicio, fin)
        else:
            # Si está lejos, no hace nada
            self.estado = "Reposo"
            self.color = (0, 0, 255)
            self.camino = []

        # Movimiento siguiendo el camino
        if len(self.camino) > 1:
            siguiente_paso = self.camino[1]

            destino_x = siguiente_paso[0] * TILE_SIZE
            destino_y = siguiente_paso[1] * TILE_SIZE

            # Movimiento en X
            if self.rect.x < destino_x:
                self.rect.x += self.velocidad
            elif self.rect.x > destino_x:
                self.rect.x -= self.velocidad

            # Movimiento en Y
            if self.rect.y < destino_y:
                self.rect.y += self.velocidad
            elif self.rect.y > destino_y:
                self.rect.y -= self.velocidad
            
        elif self.estado == "Reposo":
            pass

    # Ataque del enemigo
    def atacar(self, jugador):
        # Verifica si está tocando al jugador
        if self.rect.colliderect(jugador.rect):
            tiempo_actual = pygame.time.get_ticks()

            # Solo ataca si pasó suficiente tiempo desde el último ataque
            if tiempo_actual - self.ultimo_ataque >= self.tiempo_entre_ataques:
                jugador.vida -= self.daño
                self.ultimo_ataque = tiempo_actual
                print(f"Jugador atacado! Vida restante: {jugador.vida}")