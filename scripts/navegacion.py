# Importamos el heapq para implementar A* 
import heapq

#Creacion de la clase Nodo para A*
class Nodo:

    #Construimos el nodo
    def __init__(self,  padre=None, posicion=None):
        self.padre=padre
        self.posicion=posicion

    #Valores para A*
        self.g=0
        self.h=0
        self.f=0

    #Comparacion de nodos
    def __eq__(self, otro):
        return self.posicion == otro.posicion

    #Ordenamos los nodos en la cola
    def __lt__(self, otro):
        return self.f < otro.f
    
#Funcion A*
def astar(mapa, inicio, fin):
    nodo_inicio=Nodo(None, inicio)
    nodo_fin=Nodo(None, fin)

#Lista de nodos abiertos y cerrados
    abiertos=[]
    cerrados=[]

#Nodo inicial
    heapq.heappush(abiertos, nodo_inicio)

#Control de itineraciones
    iteraciones=0
    max_iteraciones=1000

#Bucle principal de A*
    while len(abiertos)> 0:
        iteraciones+=1
        if iteraciones > max_iteraciones:
            return[]
        
        nodo_actual=heapq.heappop(abiertos)
        cerrados.append(nodo_actual)

        if nodo_actual == nodo_fin:
            camino=[]
            actual=nodo_actual
            while actual is not None:
                camino.append(actual.posicion)
                actual=actual.padre
            return camino[::-1]
        
        #Movimientos posibles
        movimientos=[(0, -1), (0, 1), (-1, 0), (1, 0)]
        for movimiento in movimientos:
            pos_nodo=(nodo_actual.posicion[0] + movimiento[0], nodo_actual.posicion[1] + movimiento[1]  )

            #Verificacion de que estemos dentro del mapa
            if (pos_nodo[0] > (len(mapa[0]) - 1) or 
                pos_nodo[0] < 0 or 
                pos_nodo[1] > (len(mapa) - 1) or 
                pos_nodo[1] < 0):
                continue

            #Obstaculos
            if mapa[pos_nodo[1]][pos_nodo[0]] == '1':
                continue

            #Nuevo Nodo
            nuevo_nodo=Nodo(nodo_actual, pos_nodo)

            #Verificacion de nodos cerrados
            if nuevo_nodo in cerrados:
                continue

            #Calculamos costos
            nuevo_nodo.g=nodo_actual.g + 1
            nuevo_nodo.h= ((nuevo_nodo.posicion[0] - nodo_fin.posicion[0]) ** 2) + ((nuevo_nodo.posicion[1] - nodo_fin.posicion[1]) ** 2)
            nuevo_nodo.f=nuevo_nodo.g + nuevo_nodo.h

            #Revisamos si hay algun nodo mejor en abiertos
            if any(hijo for hijo in abiertos if hijo == nuevo_nodo and hijo.g < nuevo_nodo.g):
                continue
            #Lo agregamos a abiertos
            heapq.heappush(abiertos, nuevo_nodo)

    return []