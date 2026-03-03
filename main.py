import pygame
import sys

from scripts.jugador import Caballero
from scripts.Mapas import *
from scripts.enemigo import Enemigo

pygame.init()
pygame.font.init()

# Hacemos la pantalla del juego

size= (ANCHO_PANTALLA, ALTO_PANTALLA)
screen= pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Rescue The Kingdom")

# Fuentes para los textos del juego
fuente_titulo = pygame.font.SysFont("Arial", 32, bold=True)
fuente_texto = pygame.font.SysFont("Arial", 24)

# Funcion para dibujar texto centrado en pantalla
def dibujar_texto(texto, fuente, color, x, y):
    imagen_texto = fuente.render(texto, True, color)
    rectangulo_texto = imagen_texto.get_rect(center=(x, y))
    screen.blit(imagen_texto, rectangulo_texto)

#Texturas del mapa

img_muro = pygame.image.load("assets/imagenes/escenario/descarga.WEBP") .convert_alpha()
img_muro = pygame.transform.scale (img_muro, (TILE_SIZE, TILE_SIZE))

img_suelo = pygame.image.load("assets/imagenes/escenario/piso.jpg")

# Indice del mapa actual
indice_mapa = 0  

# Funcion que convierte el mapa en muros y puerta
def cargar_mapa(mapa_array):
    muros_nuevos = []
    puerta_nueva = None
    suelos_nuevos = []

    # Recorremos el mapa
    for fila_index, fila in enumerate(mapa_array):
        for col_index, piso in enumerate(fila):
            x = col_index * TILE_SIZE
            y = fila_index * TILE_SIZE

            suelos_nuevos.append((x, y))

            # Si es 1 es muro
            if piso == '1':
                muros_nuevos.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

            # Si es 2 es la puerta
            elif piso == '2':
                puerta_nueva = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                
    return muros_nuevos, suelos_nuevos, puerta_nueva

# Cargamos el primer mapa
muros,suelos, puerta = cargar_mapa(MAPAS[indice_mapa])

# Creamos jugador y enemigos
jugador = Caballero(400, 300)
enemigos = [Enemigo(200, 200)]

# Reinicia el juego
def reiniciar_juego():
    global indice_mapa, muros, puerta, jugador, enemigos, suelos

    indice_mapa = 0
    muros,suelos, puerta = cargar_mapa(MAPAS[indice_mapa])

    jugador = Caballero(400, 300)
    enemigos = [Enemigo(200, 200)]

# Estado inicial del juego
estado_juego = "MENU"

clock = pygame.time.Clock()

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # Salir del juego
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            # Control de ENTER para cambiar estados
            if event.key == pygame.K_RETURN: 
                if estado_juego == "MENU":
                    estado_juego = "INTRO"

                elif estado_juego == "INTRO":
                    reiniciar_juego() 
                    estado_juego = "JUGANDO"

                elif estado_juego == "GAME_OVER" or estado_juego == "VICTORIA":
                    estado_juego = "MENU" 

            # Ataque del jugador
            if event.key == pygame.K_SPACE and estado_juego == "JUGANDO":
                jugador.atacar(enemigos)

    # Limpiamos la pantalla
    screen.fill((0, 0, 0))
    
    centro_x = ANCHO_PANTALLA // 2
    centro_y = ALTO_PANTALLA // 2

    # Menu principal
    if estado_juego == "MENU":
        dibujar_texto("RESCUE THE KINGDOM", fuente_titulo, (255, 215, 0), centro_x, centro_y - 50)
        dibujar_texto("Presiona ENTER para empezar", fuente_texto, (255, 255, 255), centro_x, centro_y + 50)

    # Historia del juego
    elif estado_juego == "INTRO":
        dibujar_texto("El Rey ha sido capturado en las mazmorras oscuras.", fuente_texto, (200, 200, 200), centro_x, centro_y - 80)
        dibujar_texto("Eres el último caballero en pie.", fuente_texto, (200, 200, 200), centro_x, centro_y - 30)
        dibujar_texto("Tu misión: Sobrevivir y encontrar la salida.", fuente_texto, (200, 200, 200), centro_x, centro_y + 20)
        dibujar_texto("[Presiona ENTER para entrar a la mazmorra]", fuente_texto, (255, 215, 0), centro_x, centro_y + 120)

    # Estado donde se juega
    elif estado_juego == "JUGANDO":

        for sx, sy in suelos:
            screen.blit((img_suelo),(sx, sy))

        # Dibujamos los muros
        for muro in muros:
            screen.blit(img_muro, muro)
        
        # Dibujamos la puerta
        if puerta is not None:
            pygame.draw.rect(screen, (255, 255, 0), puerta)

        # Si el jugador toca la puerta pasa de nivel
        if puerta is not None and jugador.rect.colliderect(puerta):
            indice_mapa += 1

            if indice_mapa < len(MAPAS):
                muros,suelos, puerta = cargar_mapa(MAPAS[indice_mapa])

                # Reposicionamos jugador
                jugador.rect.x = 400
                jugador.rect.y = 300

                # Reiniciamos enemigos
                enemigos = [Enemigo(200, 200)]
            else:
                estado_juego = "VICTORIA"

        # Movimiento del jugador
        jugador.mover(muros)
        jugador.dibujar(screen)

        # Actualizamos enemigos
        for enemigo in enemigos:
            enemigo.actualizar(jugador.rect, MAPAS[indice_mapa])
            enemigo.atacar(jugador)
            enemigo.dibujar(screen)

        # Barra de vida del jugador
        pygame.draw.rect(screen, (50, 50, 50), (20, 20, 200, 20))

        if jugador.vida > 0:
            pygame.draw.rect(screen, (0, 255, 0), (20, 20, jugador.vida * 2, 20))

        # Si el jugador muere
        if jugador.vida <= 0:
            estado_juego = "GAME_OVER"

    # Pantalla de derrota
    elif estado_juego == "GAME_OVER":
        dibujar_texto("¡GAME OVER!", fuente_titulo, (255, 0, 0), centro_x, centro_y - 50)
        dibujar_texto("Has caído en combate...", fuente_texto, (255, 255, 255), centro_x, centro_y + 20)
        dibujar_texto("Presiona ENTER para volver al menú", fuente_texto, (150, 150, 150), centro_x, centro_y + 80)

    # Pantalla de victoria
    elif estado_juego == "VICTORIA":
        dibujar_texto("¡VICTORIA!", fuente_titulo, (0, 255, 0), centro_x, centro_y - 50)
        dibujar_texto("¡Has escapado de la mazmorra y salvado al reino!", fuente_texto, (255, 255, 255), centro_x, centro_y + 20)
        dibujar_texto("Presiona ENTER para volver al menú", fuente_texto, (150, 150, 150), centro_x, centro_y + 80)

    pygame.display.flip()
    clock.tick(30)