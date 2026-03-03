import pygame

class Caballero:
    def __init__(self, x, y):
        # Representación del jugador
        self.rect = pygame.Rect(x, y, 32, 32)
        self.direccion = "ABAJO"
        
        # Vida del jugador
        self.vida = 100

        # Defensa
        self.defendiendo = False

        #estado de ataque
        self.atacando= False
        self.tiempo_ataque = 0
        self.duracion_ataque= 1000

        # --- ANIMACIONES ---
        # Función interna para cargar y escalar fácilmente
        def cargar_escalar(ruta):
            img_gigante = pygame.image.load(ruta).convert_alpha()
            # 2. Usamos 'smoothscale' para alta calidad al encoger
            return pygame.transform.smoothscale(img_gigante, (32, 32))
        
        # imagenes direccionales
        self.animaciones = {
            "ABAJO": [cargar_escalar("assets/imagenes/caballero/abajo.png"), cargar_escalar("assets/imagenes/caballero/abajo.2.png")],
            "ARRIBA": [cargar_escalar("assets/imagenes/caballero/arriba.png"), cargar_escalar("assets/imagenes/caballero/arriba.2.png")],
            "IZQUIERDA": [cargar_escalar("assets/imagenes/caballero/izquierda.png"), cargar_escalar("assets/imagenes/caballero/izquierda.2.png")],
            "DERECHA": [cargar_escalar("assets/imagenes/caballero/derecha.png"), cargar_escalar("assets/imagenes/caballero/derecha.2.png")]
        }
        
        #sprites de ataque
        self.sprites_ataque = {
            "ABAJO": cargar_escalar("assets/imagenes/caballero/ataque.abajo.png"),
            "ARRIBA": cargar_escalar("assets/imagenes/caballero/ataque.arriba.png"),
            "IZQUIERDA": cargar_escalar("assets/imagenes/caballero/ataque.izquierda.png"),
            "DERECHA": cargar_escalar("assets/imagenes/caballero/ataque.derecha.png")
        }

        # Control de animaciones
        self.indice_animacion = 0
        self.velocidad_animacion = 0.2
        self.imagen_actual = self.animaciones[self.direccion][0]
        self.en_movimiento = False

    # Función para dibujarlo (¡Habías olvidado esta!)
    def dibujar(self, superficie):

        # Dibujamos el sprite
        if self.atacando:
            tiempo_actual =  pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_ataque > self.duracion_ataque:
                self.atacando=False

        if self.atacando:
            imagen_a_dibujar = self.sprites_ataque[self.direccion]
        else:
            imagen_a_dibujar = self.imagen_actual

        # CAMBIO AQUÍ: Usamos la variable 'imagen_a_dibujar' que calculamos arriba
        superficie.blit(imagen_a_dibujar, self.rect)

        
        # Si está usando la tecla X (defensa), le ponemos un aura celeste
        if self.defendiendo:
            pygame.draw.rect(superficie, (0, 255, 255), self.rect, 3)

    # Función unificada para moverlo
    def mover(self, muros):
        if self.atacando:
            return
        teclas = pygame.key.get_pressed()
        
        # Detectamos la tecla X para defender
        self.defendiendo = teclas[pygame.K_x]
        
        # Si defiende va lento (2), si no, normal (5)
        velocidad = 2 if self.defendiendo else 5

        self.en_movimiento = False

        # --- EJE X ---
        if teclas[pygame.K_LEFT]:
            self.rect.x -= velocidad
            self.direccion = "IZQUIERDA"
            self.en_movimiento = True
        if teclas[pygame.K_RIGHT]:
            self.rect.x += velocidad
            self.direccion = "DERECHA"
            self.en_movimiento = True

        for muro in muros:
            if self.rect.colliderect(muro):
                if teclas[pygame.K_RIGHT]:
                    self.rect.right = muro.left
                if teclas[pygame.K_LEFT]:
                    self.rect.left = muro.right

        # --- EJE Y ---
        if teclas[pygame.K_UP]:
            self.rect.y -= velocidad
            self.direccion = "ARRIBA"
            self.en_movimiento = True
        if teclas[pygame.K_DOWN]:
            self.rect.y += velocidad
            self.direccion = "ABAJO"
            self.en_movimiento = True

        for muro in muros:
            if self.rect.colliderect(muro):
                if teclas[pygame.K_DOWN]:
                    self.rect.bottom = muro.top
                if teclas[pygame.K_UP]:
                    self.rect.top = muro.bottom

        # --- REPRODUCTOR DE ANIMACIONES ---
        lista_actual = self.animaciones[self.direccion]

        if self.en_movimiento:
            self.indice_animacion += self.velocidad_animacion
            if self.indice_animacion >= len(lista_actual):
                self.indice_animacion = 0
            self.imagen_actual = lista_actual[int(self.indice_animacion)]
        else:
            self.indice_animacion = 0
            self.imagen_actual = lista_actual[0]

    # Función para atacar
    def atacar(self, lista_enemigos):
        if self.defendiendo:
            print("¡No puedes atacar mientras te defiendes!")
            return
        
        #activar animacion de ataque
        self.atacando= True
        self.tiempo_ataque= pygame.time.get_ticks()

        rango = 32

        # Área de ataque (Ya corregidos los pygame.Rect)
        if self.direccion == "ARRIBA":
            area_ataque = pygame.Rect(self.rect.x, self.rect.y - rango, 32, 32)
        elif self.direccion == "ABAJO":
            area_ataque = pygame.Rect(self.rect.x, self.rect.y + rango, 32, 32)
        elif self.direccion == "IZQUIERDA": 
            area_ataque = pygame.Rect(self.rect.x - rango, self.rect.y, 32, 32)
        elif self.direccion == "DERECHA":
            area_ataque = pygame.Rect(self.rect.x + rango, self.rect.y, 32, 32)

        # Verificamos colision con enemigos
        for enemigo in lista_enemigos[:]:
            if area_ataque.colliderect(enemigo.rect):
                lista_enemigos.remove(enemigo)
                print("Enemigo eliminado")