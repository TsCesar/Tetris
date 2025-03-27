import pygame
import random
import json
import os
from piezas import Pieza

pygame.init()

# Pantalla
ANCHO_VENTANA = 600
ALTO_VENTANA = 800
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.RESIZABLE)
pygame.display.set_caption("Tetris")

# Colores
NEGRO = (0, 0, 0)
GRIS = (50, 50, 50)
ROJO = (200, 0, 0)
AZUL = (0, 150, 255)
BLANCO = (255, 255, 255)

# Parámetros del juego
COLUMNAS = 10
FILAS = 20
MARGEN_X = 150
MARGEN_Y = 50
TIEMPO_CAIDA = 0.5
ARCHIVO_PUNTUACIONES = "puntuaciones.json"

# Fuentes
fuente = pygame.font.Font("PressStart2P.ttf", 18)
fuente_grande = pygame.font.Font("PressStart2P.ttf", 24)
fuente_pequena = pygame.font.Font("PressStart2P.ttf", 14)

def calcular_tamano_celda(ancho, alto):
    return min((ancho - MARGEN_X * 2) // COLUMNAS, (alto - MARGEN_Y * 2) // FILAS)

def dibujar_cuadricula(TAMANO_CELDA):
    ancho, alto = ventana.get_size()
    x_inicio = (ancho - COLUMNAS * TAMANO_CELDA) // 2
    y_inicio = (alto - FILAS * TAMANO_CELDA) // 2
    for x in range(COLUMNAS + 1):
        pygame.draw.line(ventana, GRIS,
                         (x_inicio + x * TAMANO_CELDA, y_inicio),
                         (x_inicio + x * TAMANO_CELDA, y_inicio + FILAS * TAMANO_CELDA))
    for y in range(FILAS + 1):
        pygame.draw.line(ventana, GRIS,
                         (x_inicio, y_inicio + y * TAMANO_CELDA),
                         (x_inicio + COLUMNAS * TAMANO_CELDA, y_inicio + y * TAMANO_CELDA))

def fijar_pieza(tablero, pieza):
    for x, y in pieza.obtener_posiciones():
        if y >= 0:
            tablero[y][x] = pieza.color

def limpiar_filas(tablero):
    filas_completas = [i for i in range(FILAS) if all(tablero[i])]
    for fila in filas_completas:
        del tablero[fila]
        tablero.insert(0, [None] * COLUMNAS)
    return filas_completas

def verificar_game_over(tablero):
    return any(tablero[0])

def cargar_puntuaciones():
    if os.path.exists(ARCHIVO_PUNTUACIONES):
        with open(ARCHIVO_PUNTUACIONES, "r") as archivo:
            return json.load(archivo)
    return []

def eliminar_puntuacion(nombre):
    puntuaciones = cargar_puntuaciones()
    puntuaciones = [p for p in puntuaciones if p["nombre"] != nombre]
    with open(ARCHIVO_PUNTUACIONES, "w") as archivo:
        json.dump(puntuaciones, archivo, indent=4)

def guardar_puntuacion(nombre, puntuacion):
    puntuaciones = cargar_puntuaciones()

    # Buscar si el jugador ya existe
    jugador_existente = next((p for p in puntuaciones if p["nombre"] == nombre), None)

    if jugador_existente:
        if puntuacion > jugador_existente["puntuacion"]:
            jugador_existente["puntuacion"] = puntuacion  # Solo actualiza si mejora
    else:
        puntuaciones.append({"nombre": nombre, "puntuacion": puntuacion})

    puntuaciones = sorted(puntuaciones, key=lambda x: x["puntuacion"], reverse=True)[:10]

    with open(ARCHIVO_PUNTUACIONES, "w") as archivo:
        json.dump(puntuaciones, archivo, indent=4)

def introducir_nombre():
    nombre = ""
    escribiendo = True
    mensaje_error = False

    while escribiendo:
        ancho, alto = ventana.get_size()
        ventana.fill(NEGRO)

        texto = fuente_grande.render("Introduce tu nombre:", True, BLANCO)
        ventana.blit(texto, ((ancho - texto.get_width()) // 2, alto // 3))

        texto_nombre = fuente_grande.render(nombre + "_", True, AZUL)
        ventana.blit(texto_nombre, ((ancho - texto_nombre.get_width()) // 2, alto // 2))

        texto_instr = fuente_pequena.render("Pulsa Enter para empezar", True, BLANCO)
        ventana.blit(texto_instr, ((ancho - texto_instr.get_width()) // 2, alto - 100))

        if mensaje_error:
            texto_error = fuente_pequena.render("¡Introduce un nombre!", True, ROJO)
            ventana.blit(texto_error, ((ancho - texto_error.get_width()) // 2, alto // 2 + 50))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if nombre.strip():
                        escribiendo = False
                        mensaje_error = False
                    else:
                        mensaje_error = True
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif evento.unicode.isprintable() and len(nombre) < 10:
                    nombre += evento.unicode
                    mensaje_error = False

        pygame.display.flip()

    return nombre.strip()

def main(nombre_jugador):
    global tablero
    tablero = [[None for _ in range(COLUMNAS)] for _ in range(FILAS)]

    reloj = pygame.time.Clock()
    puntuacion = 0
    corriendo = True
    pieza = Pieza()
    tiempo_ultimo_mov = 0
    tiempo_ultimo_descenso = 0
    game_over = False
    puntuacion_guardada = False
    textos_flotantes = []

    while corriendo:
        dt = reloj.tick(60) / 1000
        ancho, alto = ventana.get_size()
        TAMANO_CELDA = calcular_tamano_celda(ancho, alto)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    pieza.rotar(tablero)

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and tiempo_ultimo_mov <= 0:
            pieza.mover(-1, tablero)
            tiempo_ultimo_mov = 0.08
        elif teclas[pygame.K_RIGHT] and tiempo_ultimo_mov <= 0:
            pieza.mover(1, tablero)
            tiempo_ultimo_mov = 0.08

        if teclas[pygame.K_DOWN]:
            tiempo_caida_actual = 0.05
        else:
            tiempo_caida_actual = TIEMPO_CAIDA

        tiempo_ultimo_descenso += dt
        if tiempo_ultimo_descenso >= tiempo_caida_actual:
            if not pieza.mover_abajo(tablero):
                fijar_pieza(tablero, pieza)
                filas = limpiar_filas(tablero)
                if filas:
                    puntos = len(filas) * 100
                    puntuacion += puntos

                    x_centro = (ancho // 2)
                    y_base = (alto - FILAS * TAMANO_CELDA) // 2 + min(filas) * TAMANO_CELDA
                    textos_flotantes.append({
                        "texto": f"+{puntos}",
                        "x": x_centro,
                        "y": y_base,
                        "color": (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                        "alpha": 255,
                        "size": 30,
                        "fade_speed": 2,
                        "rise_speed": 0.3
                    })

                if verificar_game_over(tablero):
                    if not puntuacion_guardada:
                        guardar_puntuacion(nombre_jugador, puntuacion)
                        puntuacion_guardada = True
                    game_over = True
                else:
                    pieza = Pieza()
            tiempo_ultimo_descenso = 0

        tiempo_ultimo_mov -= dt

        ventana.fill(NEGRO)
        dibujar_cuadricula(TAMANO_CELDA)

        for y, fila in enumerate(tablero):
            for x, color in enumerate(fila):
                if color:
                    pygame.draw.rect(ventana, color,
                                     ((ancho - COLUMNAS * TAMANO_CELDA) // 2 + x * TAMANO_CELDA,
                                      (alto - FILAS * TAMANO_CELDA) // 2 + y * TAMANO_CELDA,
                                      TAMANO_CELDA, TAMANO_CELDA))

        pieza.dibujar(ventana, TAMANO_CELDA)

        # Puntuación y nombre del jugador
        ventana.blit(fuente.render(f"Score: {puntuacion}", True, BLANCO), (30, 30))
        ventana.blit(fuente.render(f"Jugador: {nombre_jugador}", True, BLANCO), (30, 60))

        # Top 3
        top_puntuaciones = cargar_puntuaciones()[:3]
        y_offset = 100
        ventana.blit(fuente.render("Top 3:", True, BLANCO), (30, y_offset))
        for i, entrada in enumerate(top_puntuaciones):
            texto_top = fuente.render(f"{i+1}. {entrada['nombre']}: {entrada['puntuacion']}", True, BLANCO)
            ventana.blit(texto_top, (30, y_offset + 30 * (i + 1)))

        # Animar texto flotante
        for texto in textos_flotantes[:]:
            texto["y"] -= texto["rise_speed"]
            texto["alpha"] -= texto["fade_speed"]
            if texto["alpha"] <= 0:
                textos_flotantes.remove(texto)
            else:
                fuente_anim = pygame.font.Font("PressStart2P.ttf", texto["size"])
                surf = fuente_anim.render(texto["texto"], True, texto["color"])
                surf.set_alpha(max(0, texto["alpha"]))
                ventana.blit(surf, (texto["x"] - surf.get_width() // 2, texto["y"]))

        if game_over:
            pantalla_game_over(nombre_jugador)
            corriendo = False

        pygame.display.flip()
def pantalla_game_over(nombre_jugador):
    seleccionando = True
    opciones = ["Reintentar", "Cambiar jugador", "Salir del juego"]
    seleccion = 0
    reloj = pygame.time.Clock()

    while seleccionando:
        ancho, alto = ventana.get_size()
        ventana.fill(NEGRO)

        # Título
        titulo = fuente_grande.render("GAME OVER", True, ROJO)
        ventana.blit(titulo, ((ancho - titulo.get_width()) // 2, 100))

        # Mostrar top 3
        top = cargar_puntuaciones()[:3]
        ventana.blit(fuente.render("Top 3:", True, BLANCO), (30, 200))
        for i, entrada in enumerate(top):
            texto = fuente.render(f"{i+1}. {entrada['nombre']}: {entrada['puntuacion']}", True, BLANCO)
            ventana.blit(texto, (30, 230 + i * 30))

        # Opciones
        for i, opcion in enumerate(opciones):
            color = AZUL if i == seleccion else BLANCO
            texto = fuente_grande.render(opcion, True, color)
            ventana.blit(texto, ((ancho - texto.get_width()) // 2, 400 + i * 60))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        eliminar_puntuacion(nombre_jugador)
                        main(nombre_jugador)
                        return
                    elif seleccion == 1:
                        nombre = introducir_nombre()
                        main(nombre)
                        return
                    elif seleccion == 2:
                        pygame.quit()
                        exit()

        pygame.display.flip()
        reloj.tick(60)


if __name__ == "__main__":
    nombre = introducir_nombre()
    main(nombre)
