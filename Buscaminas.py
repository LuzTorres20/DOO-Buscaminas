from bot import bot_jugar
import sys
import random
import pygame


primera_celda_pulsada = True
cantidad_casilla = (
    {}
)  # numero de casilla = [indice (x, y) posicion en el tablero, posicion (x,y) en la pantalla, valor, pulsada (true o false)]

bombas_activas = 0
bombas_inactivas = 0


def crear_cuadricula(numero, tamaño_cuadricua):
    global ventana, font, cuadricula, tamano_cuadricula
    cuadricula = []

    for _ in range(numero):
        linea = [0] * numero
        cuadricula.append(linea)

    tamano_cuadricula = tamaño_cuadricua
    medidas = tamano_cuadricula * numero
    ventana = pygame.display.set_mode((medidas + 115, medidas))

    font = pygame.font.Font(None, tamano_cuadricula)

    i = 0
    for row in range(len(cuadricula)):
        for col in range(len(cuadricula[row])):
            square_rect = pygame.Rect(
                2 + (1 * row * tamano_cuadricula),
                2 + (1 * col * tamano_cuadricula),
                tamano_cuadricula - 4,
                tamano_cuadricula - 4,
            )
            pygame.draw.rect(ventana, "black", square_rect.inflate(2, 2))
            pygame.draw.rect(ventana, "white", square_rect)
            pygame.display.update()
            cantidad_casilla[i] = {
                "numero": i,
                "indice": (row, col),
                "posicionXY": square_rect,
                "valor": " ",
                "pulsada": False,
                "bandera": False,
            }
            i += 1

    return cuadricula


def crear_bombas_random(numero, primer_click, dificultad):
    global cuadricula, bombas_inactivas
    bombas = int(numero * numero * dificultad)
    bombas_inactivas = int(numero * numero * dificultad)
    rows = len(cuadricula)
    cols = len(cuadricula[0])

    while bombas > 0:
        random_row = random.randint(0, rows - 1)
        random_col = random.randint(0, cols - 1)

        # Verificar si la posición aleatoria está dentro de la región 3x3 alrededor del primer_click
        if abs(random_row - primer_click[0]) <= 1 and abs(random_col - primer_click[1]) <= 1:
            continue  # Salta esta iteración y busca otra posición aleatoria

        # Si la posición no está en la región 3x3 alrededor de primer_click y está vacía (0)
        if cuadricula[random_row][random_col] == 0:
            cuadricula[random_row][random_col] = "b"
            bombas -= 1

    donde_hay_bomba()


def donde_hay_bomba():
    numero_filas = len(cuadricula)
    numero_columnas = len(cuadricula[0])

    indice = 0
    for row in range(numero_filas):
        for col in range(numero_columnas):
            bombas_alrededor = 0

            # Verificar celdas adyacentes en forma de cuadrícula de 3x3
            for i in range(-1, 2):  # -1 0 1
                for j in range(-1, 2):  # -1 0 1
                    if i == 0 and j == 0:
                        continue  # Saltar la propia celda, cuando pase por la celda

                    try:
                        if row + i >= 0 and col + j >= 0:
                            if cuadricula[row + i][col + j] == "b":
                                bombas_alrededor += 1
                    except IndexError:
                        pass  # Ignorar si se produce un IndexError

            # Actualizar la celda con el número de bombas adyacentes
            if cuadricula[row][col] != "b":
                cuadricula[row][col] = bombas_alrededor

            cantidad_casilla[indice]["valor"] = cuadricula[row][col]
            indice += 1


def color_numero(element, color):
    valor_casilla = font.render(str(cantidad_casilla[element]["valor"]), True, color)
    ventana.blit(
        valor_casilla,
        (
            cantidad_casilla[element]["posicionXY"].x + (tamano_cuadricula / 4),
            cantidad_casilla[element]["posicionXY"].y + (tamano_cuadricula / 8),
        ),
    )
    pygame.display.update()


def click_casilla(numero, event, dificultad):
    global primera_celda_pulsada, bombas_activas, bombas_inactivas
    for element in cantidad_casilla:
        if cantidad_casilla[element]["posicionXY"].collidepoint(event.pos):
            if primera_celda_pulsada:
                print(cantidad_casilla[element]["indice"])
                crear_bombas_random(numero, cantidad_casilla[element]["indice"], dificultad)
                primera_celda_pulsada = False
            if not primera_celda_pulsada:
                keys = pygame.mouse.get_pressed()
                if keys[0] and not cantidad_casilla[element]["bandera"] == True:
                    match cantidad_casilla[element]["valor"]:
                        case 0:
                            color_numero(element, (0, 0, 255))
                        case 1:
                            color_numero(element, (0, 255, 0))
                        case 2:
                            color_numero(element, (255, 255, 0))
                        case 3:
                            color_numero(element, (255, 100, 0))
                        case 4:
                            color_numero(element, (200, 0, 0))
                        case 5:
                            color_numero(element, (255, 0, 0))
                        case 6:
                            color_numero(element, (255, 0, 0))
                        case 7:
                            color_numero(element, (255, 0, 0))
                        case 8:
                            color_numero(element, (255, 0, 0))
                        case 9:
                            color_numero(element, (255, 0, 0))
                        case "b":
                            return False, True

                    cantidad_casilla[element]["pulsada"] = True

                if keys[2]:
                    if (
                        not cantidad_casilla[element]["pulsada"] == True
                        and not cantidad_casilla[element]["bandera"] == True
                        and not bombas_activas == 0
                    ):
                        valor_casilla = font.render("?", True, (0, 0, 0))
                        ventana.blit(
                            valor_casilla,
                            (
                                cantidad_casilla[element]["posicionXY"].x + 10,
                                cantidad_casilla[element]["posicionXY"].y + 5,
                            ),
                        )
                        pygame.display.update()
                        cantidad_casilla[element]["bandera"] = True
                        bombas_activas -= 1

                    elif (
                        not cantidad_casilla[element]["pulsada"] == True
                        and not cantidad_casilla[element]["bandera"] == False
                    ):
                        square_rect = pygame.Rect(
                            cantidad_casilla[element]["posicionXY"].x,
                            cantidad_casilla[element]["posicionXY"].y,
                            tamano_cuadricula - 4,
                            tamano_cuadricula - 4,
                        )
                        pygame.draw.rect(ventana, "white", square_rect)
                        pygame.display.update()
                        cantidad_casilla[element]["bandera"] = False
                        bombas_activas += 1

            if cantidad_casilla[element]["valor"] == "b" and cantidad_casilla[element]["bandera"] == True:
                bombas_inactivas -= 1
                if bombas_inactivas == 0:
                    return True, False

    return False, False


def menu():
    pygame.init()
    font = pygame.font.Font(None, 50)
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Buscaminas - Menú")

    easy_button = pygame.Rect(100, 0, 200, 80)
    normal_button = pygame.Rect(100, 100, 200, 80)
    hard_button = pygame.Rect(100, 200, 200, 80)

    player_button = pygame.Rect(100, 300, 200, 40)
    bot_button = pygame.Rect(100, 350, 200, 40)

    BLACK_COLOR = (0, 0, 0)
    WHITE_COLOR = (255, 255, 255)

    dificultad = None
    numero = None
    casillas = None
    modo = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Selección de dificultad
                if easy_button.collidepoint(event.pos):
                    numero, dificultad, casillas = 7, 0.3, 40
                elif normal_button.collidepoint(event.pos):
                    numero, dificultad, casillas = 10, 0.5, 40
                elif hard_button.collidepoint(event.pos):
                    numero, dificultad, casillas = 15, 0.7, 40

                # Selección de modo (solo si ya hay dificultad)
                if numero is not None:
                    if player_button.collidepoint(event.pos):
                        modo = "player"
                    elif bot_button.collidepoint(event.pos):
                        modo = "bot"

                    # Solo retorna si se eligió modo
                    if modo is not None:
                        return numero, dificultad, casillas, modo

        # --- Dibujar pantalla ---
        screen.fill((50, 50, 50))

        # Botones de dificultad
        pygame.draw.rect(screen, BLACK_COLOR, easy_button)
        pygame.draw.rect(screen, BLACK_COLOR, normal_button)
        pygame.draw.rect(screen, BLACK_COLOR, hard_button)
        screen.blit(font.render("FACIL", True, WHITE_COLOR), (easy_button.x + 40, easy_button.y + 20))
        screen.blit(font.render("NORMAL", True, WHITE_COLOR), (normal_button.x + 40, normal_button.y + 20))
        screen.blit(font.render("DIFICIL", True, WHITE_COLOR), (hard_button.x + 40, hard_button.y + 20))

        # Botones de modo solo si hay dificultad elegida
        if numero is not None:
            pygame.draw.rect(screen, (0, 100, 0), player_button)
            pygame.draw.rect(screen, (100, 0, 0), bot_button)
            screen.blit(font.render("JUGAR TU", True, WHITE_COLOR), (player_button.x + 20, player_button.y + 5))
            screen.blit(font.render("BOT", True, WHITE_COLOR), (bot_button.x + 70, bot_button.y + 5))

            pygame.display.update()


def mostrar_bombas(numero, casillas):
    global bombas_activas
    x = numero * casillas + 50
    y = 0
    pygame.draw.rect(ventana, (0, 0, 0), (x, y, 100, 100))
    font = pygame.font.Font(None, 60)
    start_text = font.render(str(bombas_activas), True, (255, 255, 255))
    ventana.blit(start_text, (x, y))
    pygame.display.update()


def mostrar_resultado(ganaste):
    ventana.fill((0, 0, 0))  # Fondo negro

    mensaje = "¡HAS GANADO!" if ganaste else "HAS PERDIDO"
    color = (0, 255, 0) if ganaste else (255, 0, 0)

    font_grande = pygame.font.Font(None, 80)
    texto = font_grande.render(mensaje, True, color)

    # Centrar texto en la ventana
    rect_texto = texto.get_rect(center=(ventana.get_width() // 2, ventana.get_height() // 2))
    ventana.blit(texto, rect_texto)

    pygame.display.update()

    # Esperar que el jugador presione una tecla o click
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                esperando = False


def game(numero, dificultad, casillas):
    global primera_celda_pulsada, cantidad_casilla, bombas_activas
    ganar, perder = False, False
    while not ganar and not perder:
        for event in pygame.event.get():
            mostrar_bombas(numero, casillas)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ganar, perder = click_casilla(numero, event, dificultad)

    mostrar_resultado(ganar)
    primera_celda_pulsada = True
    cantidad_casilla = {}
    bombas_activas = 0
    run()


def run():
    global bombas_activas
    numero, dificultad, casillas, modo = menu()
    crear_cuadricula(numero, casillas)
    bombas_iniciales = int(numero * numero * dificultad)
    bombas_activas = bombas_iniciales

    if modo == "player":
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    game(numero, dificultad, casillas)
    else:
        bot_jugar(numero, dificultad, casillas, cantidad_casilla, click_casilla, mostrar_resultado, run)


if __name__ == "__main__":
    run()
