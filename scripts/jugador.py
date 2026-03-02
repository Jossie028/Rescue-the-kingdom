import pygame

#Clase del jugador
class Caballero:
    def __init__(self, x, y):

        #Representacion del jugador
        self.rect = pygame.Rect(x, y, 32, 32)
        self.color = (255, 0, 0)

        self.direccion = "ABAJO"

        #vida del jugadoe
        self.vida = 100

    #funcion para dibujarlo 
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)

    #funcion para moverlo
    def mover(self, muros):
        print(f"Cantidad de muros: {len(muros)}")
        teclas = pygame.key.get_pressed()
        velocidad = 5

        # eje x 
        if teclas[pygame.K_LEFT]:
            self.rect.x -= velocidad
            self.direccion = "IZQUIERDA"
        if teclas[pygame.K_RIGHT]:
            self.rect.x += velocidad
            self.direccion = "DERECHA"

        # Verificamos colisión horizontal
        for muro in muros:
            if self.rect.colliderect(muro):
                if teclas[pygame.K_RIGHT]:
                    self.rect.right = muro.left
                    self.direccion = "DERECHA"
                if teclas[pygame.K_LEFT]:
                    self.rect.left = muro.right
                    self.direccion = "IZQUIERDA"

        # eje y
        if teclas[pygame.K_UP]:
            self.rect.y -= velocidad
        if teclas[pygame.K_DOWN]:
            self.rect.y += velocidad

        # Verificamos colisión vertical
        for muro in muros:
            if self.rect.colliderect(muro):
                if teclas[pygame.K_DOWN]:
                    self.rect.bottom = muro.top
                if teclas[pygame.K_UP]:
                    self.rect.top = muro.bottom


#funcion para atacar a los enemigos
    def atacar(self, lista_enemigos):
        rango = 32

    #area de ataque
        if self.direccion == "ARRIBA":
            area_ataque = pygame.rect(self.rect.x, self.rect.y - rango, 32, 32)

        elif self.direccion == "ABAJO":
            area_ataque = self.rect.x, self.rect.y + rango, 32, 32

        elif self.direccion == "IZQUIERDA": 
            area_ataque = pygame.Rect(self.rect.x - rango, self.rect.y, 32, 32)

        elif self.direccion == "DERECHA":
            area_ataque = pygame.Rect(self.rect.x + rango, self.rect.y, 32, 32)


# Verificamos colision con enemigos
        for enemigo in lista_enemigos[:]:
            if area_ataque.colliderect(enemigo.rect):
                lista_enemigos.remove(enemigo)
                print("Enemigo eliminado")