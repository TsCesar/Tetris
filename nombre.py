import pygame

pygame.init()

ANCHO = 600
ALTO = 800
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tetris")

fuente = pygame.font.Font("PressStart2P.ttf", 24)
fuente_pequena = pygame.font.Font("PressStart2P.ttf", 14)

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 150, 255)

def introducir_nombre():
    nombre = ""
    escribiendo = True

    while escribiendo:
        ventana.fill(NEGRO)

        texto = fuente.render("Introduce tu nombre:", True, BLANCO)
        ventana.blit(texto, ((ANCHO - texto.get_width()) // 2, ALTO // 3))

        texto_nombre = fuente.render(nombre + "_", True, AZUL)
        ventana.blit(texto_nombre, ((ANCHO - texto_nombre.get_width()) // 2, ALTO // 2))

        texto_instr = fuente_pequena.render("Pulsa Enter para continuar", True, BLANCO)
        ventana.blit(texto_instr, ((ANCHO - texto_instr.get_width()) // 2, ALTO - 100))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre.strip():
                    escribiendo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif evento.unicode.isprintable() and len(nombre) < 10:
                    nombre += evento.unicode

        pygame.display.flip()

    return nombre.strip()

# Para probar:
if __name__ == "__main__":
    jugador = introducir_nombre()
    print("Nombre ingresado:", jugador)
    # Aquí llamarías a tu juego con main(jugador)