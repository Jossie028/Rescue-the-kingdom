import pygame
from scripts.Mundos import *
from scripts.navegacion import astar


class Enemigo:
    def __init__(self, x, y):
        self.rect=pygame.Rect(x, y, 32, 32)
        self.color=(0,0,255)

        self.posicion_grid=[x//32, y//32]
        self.velocidad=2

        self.camino=[]

        self.estado="Reposo"
        self.radio_vision=5

        self.daño=10
        self.ultimo_ataque = 0
        self.tiempo_entre_ataques = 2000

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)

        if self.camino:
            puntos_pixeles = []
            for punto in self.camino:
                # Convertimos grid a pixeles para dibujar (+16 para centrar la linea)
                px = (punto[0] * TILE_SIZE) + 16
                py = (punto[1] * TILE_SIZE) + 16
                puntos_pixeles.append((px, py))
            
            if len(puntos_pixeles) > 1:
                pygame.draw.lines(superficie, (255, 255, 255), False, puntos_pixeles, 2)
    


    def actualizar(self, jugador_rect):
        grid_x_yo = self.rect.x // TILE_SIZE
        grid_y_yo = self.rect.y // TILE_SIZE
        inicio = (grid_x_yo, grid_y_yo)

        grid_x_jugador = jugador_rect.x // TILE_SIZE
        grid_y_jugador = jugador_rect.y // TILE_SIZE
        fin = (grid_x_jugador, grid_y_jugador)

        self.camino = astar(MAPA, inicio, fin)

        distancia = abs((grid_x_yo - grid_x_jugador) + (grid_y_yo - grid_y_jugador))

        if distancia <= self.radio_vision:
            self.estado = "Persecucion"
            self.color = (255, 0, 0)
        else:
            self.estado = "Reposo"
            self.color = (0, 0, 255)
            self.camino = []



        if len(self.camino) > 1:
            siguiente_paso = self.camino[1]  # El siguiente punto en el camino

            destino_x = siguiente_paso[0] * TILE_SIZE
            destino_y = siguiente_paso[1] * TILE_SIZE

            if self.rect.x < destino_x:
                self.rect.x += self.velocidad
            elif self.rect.x > destino_x:
                self.rect.x -= self.velocidad

            if self.rect.y < destino_y:
                self.rect.y += self.velocidad
            elif self.rect.y > destino_y:
                self.rect.y -= self.velocidad
            
        elif self.estado == "Reposo":
            pass


    def atacar(self, jugador):
        if self.rect.colliderect(jugador.rect):
            tiempo_actual= pygame.time.get_ticks()

            if tiempo_actual - self.ultimo_ataque >= self.tiempo_entre_ataques:
                jugador.vida -= self.daño
                self.ultimo_ataque = tiempo_actual
                print(f"Jugador atacado! Vida restante: {jugador.vida}")
