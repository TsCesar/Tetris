import pygame
import random

# Tamaño de la cuadrícula
COLUMNAS = 10
FILAS = 20

# Colores de las piezas
COLORES = {
    "I": (0, 255, 255),
    "J": (0, 0, 255),
    "L": (255, 165, 0),
    "O": (255, 255, 0),
    "S": (0, 255, 0),
    "T": (128, 0, 128),
    "Z": (255, 0, 0)
}

# Definir las formas de las piezas
PIEZAS = {
    "I": [[1, 1, 1, 1]],
    "J": [[1, 0, 0], [1, 1, 1]],
    "L": [[0, 0, 1], [1, 1, 1]],
    "O": [[1, 1], [1, 1]],
    "S": [[0, 1, 1], [1, 1, 0]],
    "T": [[0, 1, 0], [1, 1, 1]],
    "Z": [[1, 1, 0], [0, 1, 1]]
}


class Pieza:
    def __init__(self):
        """Inicializa una nueva pieza aleatoria en el centro de la cuadrícula."""
        self.tipo = random.choice(list(PIEZAS.keys()))
        self.forma = PIEZAS[self.tipo]
        self.color = COLORES[self.tipo]
        self.x = COLUMNAS // 2 - len(self.forma[0]) // 2  # Centrada horizontalmente
        self.y = 0  # Aparece arriba
        self.velocidad_caida = 0.5
        self.tiempo_acumulado = 0

    def mover(self, dx):
        """Mueve la pieza horizontalmente sin salirse del tablero."""
        nueva_x = self.x + dx
        if 0 <= nueva_x <= COLUMNAS - len(self.forma[0]):
            self.x = nueva_x

    def rotar(self):
        """Rota la pieza en sentido horario sin salirse del tablero."""
        nueva_forma = list(zip(*self.forma[::-1]))  # Rotación 90° (transpuesta + invertir filas)
        nueva_forma = [list(row) for row in nueva_forma]  # Convertir de nuevo a lista de listas
        ancho_pieza = len(nueva_forma[0])

        # Ajustar si se sale del tablero
        if self.x + ancho_pieza > COLUMNAS:
            self.x = COLUMNAS - ancho_pieza

        self.forma = nueva_forma

    def mover_abajo(self, tablero):
        """Mueve la pieza hacia abajo si es posible. 
        Si no puede moverse más, devuelve False para indicar que debe fijarse.
        """
        for i, fila in enumerate(self.forma):
            for j, celda in enumerate(fila):
                if celda:
                    nueva_y = self.y + i + 1
                    if nueva_y >= FILAS or tablero[nueva_y][self.x + j] is not None:
                        return False  # Ha llegado al final o choca con otra pieza

        self.y += 1  # Mueve la pieza una fila abajo
        return True

    def actualizar(self, dt, tablero):
        """Mueve la pieza hacia abajo de forma automática."""
        self.tiempo_acumulado += dt
        if self.tiempo_acumulado >= self.velocidad_caida:
            if not self.mover_abajo(tablero):  # Si no puede moverse más, se debe fijar
                return False
            self.tiempo_acumulado = 0
        return True

    def obtener_posiciones(self):
        """Devuelve las coordenadas ocupadas por la pieza en la cuadrícula."""
        posiciones = []
        for i, fila in enumerate(self.forma):
            for j, celda in enumerate(fila):
                if celda:
                    posiciones.append((self.x + j, self.y + i))
        return posiciones

    def dibujar(self, pantalla, TAMANO_CELDA):
        """Dibuja la pieza en su posición dentro del tablero."""
        ancho, alto = pantalla.get_size()
        x_inicio = (ancho - COLUMNAS * TAMANO_CELDA) // 2
        y_inicio = (alto - FILAS * TAMANO_CELDA) // 2

        for i, fila in enumerate(self.forma):
            for j, celda in enumerate(fila):
                if celda:
                    x_pix = x_inicio + (self.x + j) * TAMANO_CELDA
                    y_pix = y_inicio + (self.y + i) * TAMANO_CELDA
                    pygame.draw.rect(pantalla, self.color, (x_pix, y_pix, TAMANO_CELDA, TAMANO_CELDA))
                    pygame.draw.rect(pantalla, (0, 0, 0), (x_pix, y_pix, TAMANO_CELDA, TAMANO_CELDA), 2)  # Contorno
