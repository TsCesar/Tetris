import pygame

# Inicializar Pygame
pygame.init()

# Obtener el tamaño de la pantalla
info_pantalla = pygame.display.Info()
ANCHO_PANTALLA = info_pantalla.current_w
ALTO_PANTALLA = info_pantalla.current_h

# Tamaño de la cuadrícula (Tetris clásico: 10 columnas x 20 filas)
COLUMNAS = 10
FILAS = 20

# Espacio extra para la interfaz (siguiente pieza, puntuación, etc.)
MARGEN_X = 150  # Espacio lateral
MARGEN_Y = 50   # Espacio superior e inferior

# Tamaño inicial de la ventana (puede cambiar)
ANCHO_VENTANA = min(600 + MARGEN_X * 2, ANCHO_PANTALLA)
ALTO_VENTANA = min(800 + MARGEN_Y * 2, ALTO_PANTALLA)

# Colores
NEGRO = (0, 0, 0)
GRIS = (50, 50, 50)

# Crear la ventana redimensionable
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.RESIZABLE)
pygame.display.set_caption("Tetris")

def calcular_tamano_celda(ancho, alto):
    """Calcula el tamaño de cada celda según el tamaño actual de la ventana."""
    tamano_celda_ancho = (ancho - MARGEN_X * 2) // COLUMNAS
    tamano_celda_alto = (alto - MARGEN_Y * 2) // FILAS
    return min(tamano_celda_ancho, tamano_celda_alto)

def dibujar_cuadricula():
    """Dibuja la cuadrícula del Tetris centrada en la ventana."""
    ancho, alto = ventana.get_size()  # Obtener tamaño actual de la ventana
    TAMANO_CELDA = calcular_tamano_celda(ancho, alto)

    # Calcular dimensiones reales del tablero
    ANCHO_TABLERO = COLUMNAS * TAMANO_CELDA
    ALTO_TABLERO = FILAS * TAMANO_CELDA

    # Posición centrada
    x_inicio = (ancho - ANCHO_TABLERO) // 2
    y_inicio = (alto - ALTO_TABLERO) // 2

    for x in range(COLUMNAS + 1):
        pygame.draw.line(ventana, GRIS, 
                         (x_inicio + x * TAMANO_CELDA, y_inicio),
                         (x_inicio + x * TAMANO_CELDA, y_inicio + ALTO_TABLERO))

    for y in range(FILAS + 1):
        pygame.draw.line(ventana, GRIS, 
                         (x_inicio, y_inicio + y * TAMANO_CELDA),
                         (x_inicio + ANCHO_TABLERO, y_inicio + y * TAMANO_CELDA))

def main():
    reloj = pygame.time.Clock()
    corriendo = True

    while corriendo:
        ventana.fill(NEGRO)
        dibujar_cuadricula()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
