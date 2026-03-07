import pygame
from scripts.Mapas import *
from scripts.navegacion import astar

# Clase del enemigo
class Enemigo:
    def __init__(self, x, y, tipo="comun"):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.tipo = tipo
        self.direccion = "ABAJO" 

        if self.tipo == "jefe":
            self.ancho = 44
            self.alto = 44
        else:
            self.ancho= 32
            self.alto= 32

        self.rect= pygame.Rect(x,y, self.ancho, self.alto)

        def cargar_escalar(ruta):
            img = pygame.image.load(ruta).convert_alpha()
            return pygame.transform.smoothscale(img,(self.ancho, self.alto)) 
        
        # Tipos de enemigos

        #Enemigo comun
        if tipo == "comun":
            self.vida = 30
            self.daño = 10
            self.velocidad = 1
            self.color = (0, 0, 255)      
            self.radio_vision = 5

            self.animaciones = {
                "ABAJO": [cargar_escalar("assets/imagenes/soldado/abajo.png"), cargar_escalar("assets/imagenes/soldado/frame_002_ab.png")],
                "ARRIBA": [cargar_escalar("assets/imagenes/soldado/arriba.png"), cargar_escalar("assets/imagenes/soldado/frame_002_arr.png")],
                "DERECHA": [cargar_escalar("assets/imagenes/soldado/derecha.png"), cargar_escalar("assets/imagenes/soldado/frame_002_der.png")],
                "IZQUIERDA":[cargar_escalar("assets/imagenes/soldado/izquierda.png"), cargar_escalar("assets/imagenes/soldado/frame_002_izq.png")]
            }

            self.sprites_ataque = {
                "ABAJO": cargar_escalar("assets/imagenes/soldado/ataque_ab_sol.png"), 
                "ARRIBA": cargar_escalar("assets/imagenes/soldado/ataque_arrib_sol.png"),
                "IZQUIERDA": cargar_escalar("assets/imagenes/soldado/ataque_izq_sol.png"),
                "DERECHA": cargar_escalar("assets/imagenes/soldado/ataque_der_sol.png")
            }

        #Enemigo fuerte
        elif tipo == "fuerte":
            self.vida = 60                
            self.daño = 15                
            self.velocidad = 1.75            
            self.radio_vision = 6

            self.animaciones = {
                "ABAJO": [cargar_escalar("assets/imagenes/marcial/south.png"), cargar_escalar("assets/imagenes/marcial/frame_abj.png")],
                "ARRIBA": [cargar_escalar("assets/imagenes/marcial/north.png"), cargar_escalar("assets/imagenes/marcial/frame_arrib.png")],
                "IZQUIERDA": [cargar_escalar("assets/imagenes/marcial/west.png"), cargar_escalar("assets/imagenes/marcial/frame_izqui.png")],
                "DERECHA": [cargar_escalar("assets/imagenes/marcial/east.png"), cargar_escalar("assets/imagenes/marcial/frame_dere.png")]
            }
            self.sprites_ataque = {
                "ABAJO": cargar_escalar("assets/imagenes/marcial/ataque_aba_mar.png"),
                "ARRIBA": cargar_escalar("assets/imagenes/marcial/ataque_arr_mar.png"),
                "IZQUIERDA": cargar_escalar("assets/imagenes/marcial/ataque_izq_mar.png"),
                "DERECHA": cargar_escalar("assets/imagenes/marcial/ataque_der_mar.png"),
            }

        #Jefe
        elif tipo == "jefe":
            self.vida = 150               
            self.daño = 25                
            self.velocidad = 2.5         
            self.radio_vision = 9     

            self.animaciones = {
                "ABAJO": [cargar_escalar("assets/imagenes/jefe/abajo.png"), cargar_escalar("assets/imagenes/jefe/frame_abaj.png")],
                "ARRIBA": [cargar_escalar("assets/imagenes/jefe/arriba.png"), cargar_escalar("assets/imagenes/jefe/frame_arriba.png")],
                "IZQUIERDA": [cargar_escalar("assets/imagenes/jefe/izquierda.png"), cargar_escalar("assets/imagenes/jefe/frame_izqu.png")],
                "DERECHA": [cargar_escalar("assets/imagenes/jefe/derecha.png"), cargar_escalar("assets/imagenes/jefe/frame_derecha.png")]
            }  
            self.sprites_ataque = {
                "ABAJO": cargar_escalar("assets/imagenes/jefe/ataque_ab.png"),
                "ARRIBA": cargar_escalar("assets/imagenes/jefe/ataque_arr.png"),
                "IZQUIERDA": cargar_escalar("assets/imagenes/jefe/ataque_izq.png"),
                "DERECHA": cargar_escalar("assets/imagenes/jefe/ataque_der.png")
            }

        self.posicion_grid = [x // 32, y // 32]
        self.camino = []
        self.estado = "Reposo"

        self.ultimo_ataque = 0
        self.tiempo_entre_ataques = 2000

        self.atacando= False
        self.tiempo_animacion_ataques= 0 
        self.duracion_ataque= 500 

        self.indice_animacion= 0
        self.velocidad_animacion = 0.2
        self.imagen_actual= self.animaciones[self.direccion][0]

    # Dibuja el enemigo en pantalla
    def dibujar(self, superficie):
        if self.atacando:
            tiempo_actual= pygame.time.get_ticks() 
            if tiempo_actual - self.tiempo_animacion_ataques > self.duracion_ataque:
                self.atacando=False
            
        if self.atacando:
            imagen_a_dibujar= self.sprites_ataque[self.direccion] 
        else:
            imagen_a_dibujar= self.imagen_actual

        superficie.blit(imagen_a_dibujar, self.rect)

        

    # Actualiza el comportamiento del enemigo
    def actualizar(self, jugador_rect, mapa_actual):

        if self.atacando:
            return
        
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
        
        # Variable para saber si movemos las piernas o no
        en_movimiento = False

        # Si el jugador está cerca, lo persigue
        if distancia <= self.radio_vision:
            self.estado = "Persecucion"
            # Calcula el camino usando A*
            self.camino = astar(mapa_actual, inicio, fin)
        else:
            # Si está lejos, no hace nada
            self.estado = "Reposo"
            self.camino = []

        # Movimiento siguiendo el camino
        if len(self.camino) > 1:
            siguiente_paso = self.camino[1]

            destino_x = siguiente_paso[0] * TILE_SIZE
            destino_y = siguiente_paso[1] * TILE_SIZE

            # Movimiento en X
            if self.rect.x < destino_x:
                self.rect.x += self.velocidad
                self.direccion = "DERECHA"
                en_movimiento = True
            elif self.rect.x > destino_x:
                self.rect.x -= self.velocidad
                self.direccion = "IZQUIERDA"
                en_movimiento = True

            # Movimiento en Y
            if self.rect.y < destino_y:
                self.rect.y += self.velocidad
                self.direccion = "ABAJO"
                en_movimiento = True
            elif self.rect.y > destino_y:
                self.rect.y -= self.velocidad
                self.direccion = "ARRIBA"
                en_movimiento = True
        
        #Reproductor de animacion
        lista_actual = self.animaciones[self.direccion]

        if en_movimiento:
            self.indice_animacion += self.velocidad_animacion
            if self.indice_animacion >= len(lista_actual):
                self.indice_animacion = 0
            self.imagen_actual = lista_actual[int(self.indice_animacion)]
        else:
            self.indice_animacion = 0
            self.imagen_actual = lista_actual[0]

    # Ataque del enemigo
    def atacar(self, jugador):
        # Verifica si está tocando al jugador
        if self.rect.colliderect(jugador.rect):
            tiempo_actual = pygame.time.get_ticks()

            # cooldown
            if tiempo_actual - self.ultimo_ataque >= self.tiempo_entre_ataques:
                
                self.atacando = True
                self.tiempo_animacion_ataques = pygame.time.get_ticks()
                
                if jugador.defendiendo:
                    print("Ataque bloqueado")
                else :
                    jugador.vida -= self.daño
                    print(f"Jugador atacado! Vida restante: {jugador.vida}")

                self.ultimo_ataque = tiempo_actual