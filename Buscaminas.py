import sys
import random
import pygame

primera_celda_pulsada = True
calidades_casilla = {} # numero de casilla = [indice (x, y) posicion en el tablero, posicion (x,y) en la pantalla, valor, pulsada (true o false)]

bombas_restantes = 0
bombas_correctas = 0

def crear_cuadricula(numero, tamaño_cuadricua):
    global ventana, font, cuadricula, tamano_cuadricula
    cuadricula = []    

    for _ in range(numero):
        linea = [0] * numero
        cuadricula.append(linea)
    
    tamano_cuadricula = tamaño_cuadricua
    medidas = tamano_cuadricula * numero
    ventana = pygame.display.set_mode((medidas + 100,medidas))
    
    font = pygame.font.Font(None, tamano_cuadricula)

    i = 0
    for row in range(len(cuadricula)):
        for col in range(len(cuadricula[row])):
            square_rect = pygame.Rect(2 + (1 * row * tamano_cuadricula), 2 + (1 * col * tamano_cuadricula),tamano_cuadricula - 4,tamano_cuadricula - 4)
            pygame.draw.rect(ventana, 'black', square_rect.inflate(2,2))
            pygame.draw.rect(ventana, 'white', square_rect)
            pygame.display.update()
            calidades_casilla[i] = {'numero': i ,'indice' : (row, col), 'posicion_xy': square_rect, 'valor' : ' ', 'pulsada' : False, 'bandera' : False}
            i += 1

    return cuadricula

def crear_bombas_random(numero,primer_click,dificultad):
    global cuadricula, bombas_correctas
    bombas = int(numero * numero * dificultad)
    bombas_correctas = int(numero * numero * dificultad)
    rows = len(cuadricula)
    cols = len(cuadricula[0])

    while bombas > 0:
        random_row = random.randint(0, rows - 1)
        random_col = random.randint(0, cols - 1)

        # Verificar si la posición aleatoria está dentro de la región 3x3 alrededor del primer_click
        if (
            abs(random_row - primer_click[0]) <= 1
            and abs(random_col - primer_click[1]) <= 1
        ):
            continue  # Salta esta iteración y busca otra posición aleatoria

        # Si la posición no está en la región 3x3 alrededor de primer_click y está vacía (0)
        if cuadricula[random_row][random_col] == 0:
            cuadricula[random_row][random_col] = 'b'
            bombas -= 1


    donde_ahy_bomba()

def donde_ahy_bomba():
    numero_filas = len(cuadricula)
    numero_columnas = len(cuadricula[0])

    indice = 0
    for row in range(numero_filas):
        for col in range(numero_columnas):
            bombas_alrededor = 0


            # Verificar celdas adyacentes en forma de cuadrícula de 3x3
            for i in range(-1, 2): # -1 0 1
                for j in range(-1, 2): # -1 0 1
                    if i == 0 and j == 0:
                        continue  # Saltar la propia celda, cuando pase por la celda

                    try:
                        if row + i >= 0 and col + j >= 0:
                            if cuadricula[row + i][col + j] == 'b':
                                bombas_alrededor += 1
                    except IndexError:
                        pass  # Ignorar si se produce un IndexError

            # Actualizar la celda con el número de bombas adyacentes
            if cuadricula[row][col] != 'b':
                cuadricula[row][col] = bombas_alrededor
            
            calidades_casilla[indice]['valor'] = cuadricula[row][col]  
            indice += 1    

def color_numero(element,color):
    valor_casilla = font.render(str(calidades_casilla[element]['valor']),True,color)
    ventana.blit(valor_casilla,(calidades_casilla[element]['posicion_xy'].x + (tamano_cuadricula / 4),calidades_casilla[element]['posicion_xy'].y + (tamano_cuadricula / 8)))
    pygame.display.update()

def click_casilla(numero,event,dificultad):
    global primera_celda_pulsada, bombas_restantes, bombas_correctas
    for element in calidades_casilla:
        if calidades_casilla[element]['posicion_xy'].collidepoint(event.pos):
            if primera_celda_pulsada:
                print(calidades_casilla[element]['indice'])
                crear_bombas_random(numero,calidades_casilla[element]['indice'],dificultad)
                primera_celda_pulsada = False
            if not primera_celda_pulsada:
                keys = pygame.mouse.get_pressed()
                if keys[0] and not calidades_casilla[element]['bandera'] == True:
                    match calidades_casilla[element]['valor']:
                        case 0:
                            color_numero(element,(0,0,255)) 
                        case 1:
                            color_numero(element,(0,255,0)) 
                        case 2:
                            color_numero(element,(255,255,0)) 
                        case 3:
                            color_numero(element,(255,100,0)) 
                        case 4:
                            color_numero(element,(200,0,0)) 
                        case 5:
                            color_numero(element,(255,0,0))
                        case 6:
                            color_numero(element,(255,0,0))
                        case 7:
                            color_numero(element,(255,0,0))
                        case 8:
                            color_numero(element,(255,0,0))
                        case 9:
                            color_numero(element,(255,0,0))
                        case 'b':
                            return False, True
                            
                    calidades_casilla[element]['pulsada'] = True

                if keys[2]:
                    if not calidades_casilla[element]['pulsada'] == True and not calidades_casilla[element]['bandera'] == True and not bombas_restantes == 0:
                        valor_casilla = font.render('?',True,(0,0,0))
                        ventana.blit(valor_casilla,(calidades_casilla[element]['posicion_xy'].x + 10,calidades_casilla[element]['posicion_xy'].y + 5))
                        pygame.display.update()
                        calidades_casilla[element]['bandera'] = True
                        bombas_restantes -= 1

                    elif not calidades_casilla[element]['pulsada'] == True and not calidades_casilla[element]['bandera'] == False: 
                        square_rect = pygame.Rect(calidades_casilla[element]['posicion_xy'].x,calidades_casilla[element]['posicion_xy'].y,tamano_cuadricula - 4,tamano_cuadricula - 4)
                        pygame.draw.rect(ventana, 'white', square_rect)          
                        pygame.display.update()
                        calidades_casilla[element]['bandera'] = False
                        bombas_restantes += 1
                
            if calidades_casilla[element]['valor'] == 'b' and calidades_casilla[element]['bandera'] == True:
                bombas_correctas -= 1
                if bombas_correctas == 0:
                    return True, False

    return False, False

def menu():
    pygame.init()

    menu_active = True
    font = pygame.font.Font(None, 50)

    screen = pygame.display.set_mode((400,300))

    easy_button = pygame.Rect(100, 0, 200, 80)
    normal_button = pygame.Rect(100, 100, 200, 80)
    hard_button = pygame.Rect(100, 200, 200, 80)

    BLACK_COLOR = (0,0,0)
    WHITE_COLOR = (255,255,255)
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    numero = 7
                    dificultad = .3
                    casillas = 40
                    return numero, dificultad, casillas
                elif normal_button.collidepoint(event.pos):
                    numero = 10
                    dificultad = .5
                    casillas = 40
                    return numero, dificultad, casillas
                elif hard_button.collidepoint(event.pos):
                    numero = 15
                    dificultad = .7
                    casillas = 40
                    return numero, dificultad, casillas
			
            pygame.draw.rect(screen, BLACK_COLOR, easy_button)
            pygame.draw.rect(screen, BLACK_COLOR, normal_button) 
            pygame.draw.rect(screen, BLACK_COLOR, hard_button)   
			
            start_text = font.render("FACIL", True, WHITE_COLOR)			
            screen.blit(start_text, (easy_button.x + 40, easy_button.y + 20))

            start_text = font.render("NORMAL", True, WHITE_COLOR)			
            screen.blit(start_text, (normal_button.x + 40, normal_button.y + 20))

            start_text = font.render("DIFICIL", True, WHITE_COLOR)			
            screen.blit(start_text, (hard_button.x + 40, hard_button.y + 20))
                	

            pygame.display.update()

def mostrar_bombas(numero,casillas):
    global bombas_restantes
    x = numero * casillas + 50
    y = 0
    pygame.draw.rect(ventana, (0,0,0), (x,y,100,100))
    font = pygame.font.Font(None,60)
    start_text = font.render(str(bombas_restantes), True, (255,255,255))			
    ventana.blit(start_text, (x,y))
    pygame.display.update()

def game(numero,dificultad,casillas):
    global primera_celda_pulsada, calidades_casilla, bombas_restantes
    ganar, perder = False, False
    while not ganar and not perder:
        for event in pygame.event.get():
            mostrar_bombas(numero,casillas)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ganar, perder =  click_casilla(numero,event,dificultad)
    primera_celda_pulsada = True
    calidades_casilla = {}
    bombas_restantes = 0
    run()
    
def run():
    global bombas_restantes
    numero,dificultad,casillas = menu()
    crear_cuadricula(numero,casillas)
    bombas_iniciales = int(numero * numero * dificultad)
    bombas_restantes = bombas_iniciales
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game(numero,dificultad,casillas)

if __name__ == '__main__':
   run()