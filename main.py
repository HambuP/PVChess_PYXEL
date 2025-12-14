# Pyxel Studio
import pyxel
import math
import time
import random
import copy

# Mazo original, inmutable
ORIGINAL_MAZOS = [
    [1]*8 + [2]*2 + [3]*2 + [4]*2 + [5],
    [1]*8 + [2]*2 + [3]*2 + [4]*2 + [5],
]

def recto(board, color, posicion):
    damage = board[color][posicion]["D"]
    if board[(color+1)%2][posicion] != 0:
        board[(color+1)%2][posicion]["HP"] -= damage
    else:
        juego["king"][(color + 1)%2] -= damage
    return board

def ele(board, color, posicion):
    damage = board[color][posicion]["D"]
    if posicion == 1 or posicion == 2 or posicion == 3:
        if board[(color+1)%2][posicion + 1] != 0:
            board[(color+1)%2][posicion + 1]["HP"] -= damage//2
        else:
            juego["king"][(color + 1)%2] -= damage//2
        if board[(color+1)%2][posicion - 1] != 0:
            board[(color+1)%2][posicion - 1]["HP"] -= damage//2
        else:
            juego["king"][(color + 1)%2] -= damage//2
    elif posicion == 0:
        if board[(color+1)%2][posicion + 1] != 0:
            board[(color+1)%2][posicion + 1]["HP"] -= damage
        else:
            juego["king"][(color + 1)%2] -= damage
    else:
        if board[(color+1)%2][posicion - 1] != 0:
            board[(color+1)%2][posicion - 1]["HP"] -= damage
        else:
            juego["king"][(color + 1)%2] -= damage
    return board
    
def area(board, color, posicion):
    damage = board[color][posicion]["D"]
    if board[(color+1)%2][posicion] == 0:
        juego["king"][(color + 1)%2] -= damage
    else:
        board[(color+1)%2][posicion]["HP"] -= damage//3
        if posicion == 1 or posicion == 2 or posicion == 3:
            if board[(color+1)%2][posicion + 1] != 0:
                board[(color+1)%2][posicion + 1]["HP"] -= damage//3
            else:
                juego["king"][(color + 1)%2] -= damage//3
            if board[(color+1)%2][posicion - 1] != 0:
                board[(color+1)%2][posicion - 1]["HP"] -= damage//3
            else:
                juego["king"][(color + 1)%2] -= damage//3
        elif posicion == 0:
            if board[(color+1)%2][posicion + 1] != 0:
                board[(color+1)%2][posicion + 1]["HP"] -= damage//3
            else:
                juego["king"][(color + 1)%2] -= damage//3
        else:
            if board[(color+1)%2][posicion - 1] != 0:
                board[(color+1)%2][posicion - 1]["HP"] -= damage//3
            else:
                juego["king"][(color + 1)%2] -= damage//3
    return board

def retriger(board, color, posicion):
    # 1) Detectar vecinos válidos
    vecinos = []
    if posicion > 0:
        vecinos.append(posicion - 1)
    if posicion < 4:
        vecinos.append(posicion + 1)

    # 2) Para cada vecino, si hay carta (dict) y no es otro bishop (type==2),
    #    le aplicamos su DamageType **sobre board**, no sobre tablero.
    for p in vecinos:
        cel = board[color][p]
        if isinstance(cel, dict) and cel["type"] != 2:
            board = cel["DamageType"](board, color, p)

    # 3) Al final el bishop se hace 1 punto de daño a sí mismo
    board[color][posicion]["HP"] -= 1

    return board

    

cartas_totales = {
    1 : {"HP": 2, "D": 1, "DamageType": recto, "Cost": 1}, #pawn
    2 : {"HP": 3, "D": 0, "DamageType": retriger, "Cost": 3}, #bishop
    3 : {"HP": 3, "D": 4, "DamageType": ele, "Cost": 4}, #horsey
    4 : {"HP": 5, "D": 4, "DamageType": recto, "Cost": 4}, #rooooook
    5 : {"HP": 5, "D": 6, "DamageType": area, "Cost": 8} #queen
}

cartas_mazo = []
cartas_mano = []
selected_card = 0
gameState = 0  # 0 = poner cartas, 1 = batalla

juego = {
    "listo": [False,False],
    "king": [20,20],
	"turno": 0,
	"money": [8,8],
	"tablero": [[0,0,0,0,0], [0,0,0,0,0]], #fila blanca y negro
	"cartas": [[],[]], #cartas blancas y negras
	"batallaResuelta": False,
	"batallaDelay":0,
	"roundStarted": False,
	"cartasSuccess" : False,
	"gameOver": False,
	"winner": None,
	"cartasMazos" : [
    	[
        	1,1,1,1,1,1,1,1,
        	2,2,
        	3,3,
        	4,4,
        	5
    	],
    	[
        	1,1,1,1,1,1,1,1,
        	2,2,
        	3,3,
        	4,4,
        	5
    	]
    	]
}


tablero = [[(x+y)%2 for x in range(7)] for y in range(5)]

pyxel.init(144, 112)
pyxel.load("res1.pyxres")
tilemap = pyxel.tilemap(0)
tilemap1 = pyxel.tilemap(1)
pyxel.mouse(True)
pyxel.playm(0, 20, True)

def cartasX():
    cards = juego["cartas"][juego["turno"]%2]
    mitad = 144 / 2 - 6
    posiciones = {
        1: [mitad],
        2: [mitad - 13, mitad + 13],
        3: [mitad - 20, mitad, mitad + 20],
        4: [mitad - 37, mitad - 12, mitad + 12, mitad + 37],
        5: [mitad - 48, mitad - 24, mitad, mitad + 24, mitad + 48],
    }
    return posiciones.get(len(cards), [])
'''
def selectCard(card):
    global selected_card
    turno = juego["turno"] % 2
    selected_card = juego["cartas"][turno][card]
    juego["cartas"][turno][card] = 0
'''
def pintar_Tablero():
    global juego
    for i in range(len(juego["tablero"][0])):
        if juego["tablero"][0][i] != 0:
            pyxel.bltm(16,14+16*i,tilemap,0,(juego["tablero"][0][i]["type"]-1)*16,16,16,11)
    for i in range(len(juego["tablero"][1])):
        if juego["tablero"][1][i] != 0:
            pyxel.bltm(112,14+16*i,tilemap,16,(juego["tablero"][1][i]["type"]-1)*16,16,16,7)
    
def placeCardToTablero():
    global selected_card, juego
    turno = juego["turno"]%2
    slc = juego["cartas"][turno][selected_card]

        
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        x = (mx - 16) // 16
        y = (my - 16) // 16
        if 0 <= x < 1 and 0 <= y < 5 and juego["tablero"][0][y] == 0 and juego["turno"] % 2 == 0:
            if cartas_totales[slc]["Cost"] > juego["money"][turno]:
                return
            else:
                juego["money"][turno] -= cartas_totales[slc]["Cost"]
            juego["tablero"][0][y] = { "type": slc, "HP" : cartas_totales[slc]["HP"],"D" : cartas_totales[slc]["D"], "DamageType" : cartas_totales[slc]["DamageType"] }
            print(juego["cartas"][turno])
            juego["roundStarted"] = True
            juego["cartas"][turno].pop(selected_card)
            selected_card = 0
            juego["turno"] += 1
        if 6 <= x < 7 and 0 <= y < 5 and juego["tablero"][1][y] == 0 and juego["turno"] % 2 == 1:
            if cartas_totales[slc]["Cost"] > juego["money"][turno]:
                return
            else:
                juego["money"][turno] -= cartas_totales[slc]["Cost"]
            juego["tablero"][1][y] = { "type": slc, "HP" : cartas_totales[slc]["HP"],"D" : cartas_totales[slc]["D"], "DamageType" : cartas_totales[slc]["DamageType"] }
            print(juego["cartas"][turno])
            juego["roundStarted"] = True
            juego["cartas"][turno].pop(selected_card)
            selected_card = 0
            juego["turno"] += 1
        print(juego["tablero"])

def player_can_play(player):
    """
    True si el jugador `player` (0 o 1) tiene
    - al menos un hueco libre en su fila, y
    - al menos una carta cuyo coste pueda pagar.
    """
    # 1) ¿Hueco libre?
    if all(cell != 0 for cell in juego["tablero"][player]):
        return False

    # 2) ¿Carta jugable?
    for carta in juego["cartas"][player]:
        if juego["money"][player] >= cartas_totales[carta]["Cost"]:
            return True

    return False



def stateMachine():
    global gameState
    global juego
    global cartas_totales
    global selected_card
    if not juego["cartasSuccess"]:
        for i in (0,1):
            if len(juego["cartasMazos"][i]) < 5:
                juego["cartasMazos"][i] = ORIGINAL_MAZOS[i].copy()    
        
        for i in range(2):
            juego["cartas"][i] = []
            for j in range(5):
                carta = juego["cartasMazos"][i].pop(random.randint(0, len(juego["cartasMazos"][i]) - 1))
                print("carta carta", carta)
                juego["cartas"][i] += [carta]
        juego["cartasSuccess"] = True
        print(juego["cartasSuccess"], "cartas", juego["cartas"], juego["cartasMazos"])
        
    
    if gameState == 0:
        # 1) Si ninguno puede jugar, arrancamos batalla:
        if  juego["roundStarted"] and not player_can_play(0) and not player_can_play(1):
            gameState = 1
            juego["batallaResuelta"] = False
            return
    
        # 2) Al hacer click, primero probamos si seleccionas carta:
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            msx, msy = pyxel.mouse_x, pyxel.mouse_y
            posiciones = cartasX()
            # recorre las posiciones visibles de las cartas en mano
            for idx, x in enumerate(posiciones):
                if x < msx < x + 24 and msy > 90:
                    selected_card = idx
                    return
    
            # 3) Si no clicaste sobre mano, intentamos colocar la carta seleccionada:
            turno = juego["turno"] % 2
            if not player_can_play(turno):
                # si no puedes jugar, pasas turno
                juego["listo"][turno] = True
                juego["turno"] += 1
                return
    
            # si había carta seleccionada, la colocas; si no, placeCardToTablero simplemente no hace nada
            placeCardToTablero()
            return
    
        # 4) Si ambos ya pasaron (lo dejaste para compatibilidad):
        if juego["listo"][0] and juego["listo"][1]:
            gameState = 1
            juego["batallaResuelta"] = False
            return

    if gameState == 1:
        if not juego["batallaResuelta"]:
            recorrer()
            juego["batallaResuelta"] = True
            juego["batallaDelay"]   = 0
            if juego["king"][0] <= 0:
                juego["winner"]   = 1    # blancas perdieron → gana negro
                juego["gameOver"] = True
                gameState         = 2
                return
            if juego["king"][1] <= 0:
                juego["winner"]   = 0    # negras perdieron → gana blanco
                juego["gameOver"] = True
                gameState         = 2
                return
            return
    

        if juego["batallaDelay"] < 60:
            juego["batallaDelay"] += 1
            return
    
        # 3) Tras el delay, reiniciamos para la siguiente ronda
        juego["money"]         = [8, 8]
        juego["listo"]         = [False, False]
        juego["cartasSuccess"] = False
        juego["roundStarted"]  = False
        juego["turno"]         = 0        # blancas empiezan siempre
        selected_card          = 0
    
        # limpiamos los flags de batalla
        juego["batallaResuelta"] = False
        juego["batallaDelay"]    = 0
    
        gameState = 0
        return



def draw_tablero():
    for y in range(len(tablero)):
        for x in range(len(tablero[y])):
            dx, dy = 16 + 16*x, 16 + 16*y
            tile_y = 16 if tablero[y][x] == 1 else 0
            pyxel.bltm(dx, dy, tilemap, 64, tile_y, 16, 16)

def draw_decoracion():
    pyxel.rect(12,12,120,88,9)
    pyxel.rect(14,14,116,84,4)
    pyxel.rect(32,100,80,12,13)
    pyxel.bltm(12,100,tilemap1,0,0,20,12,6)
    pyxel.bltm(112,100,tilemap1,0,0,-20,12,6)
    pyxel.bltm(32,100,tilemap1,0,16,16,16,7)
    pyxel.bltm(64,100,tilemap1,0,32,16,16,7)
    pyxel.bltm(96,100,tilemap1,0,16,-16,16,7)

def pintar_cartas():
    t = cartasX()
    global selected_card, juego
    turno = juego["turno"] % 2
    card = 0
    ard = -1
    msx, msy = pyxel.mouse_x, pyxel.mouse_y
    for c in t:
        if c < msx and msx < c+24 and msy > 90:
            ard = card
            break
        card += 1
    for i in range(len(t)):
        slc = juego["cartas"][juego["turno"]%2][i]
        f = math.sin(time.time()*0.7+i - turno*math.pi)
        if msy > 95:
            pyxel.bltm(t[i] ,85 if i == selected_card else 95,tilemap,2+16*2 + turno*16,(slc-1)*16,12,16,0,f*10, 1.7 if ard == i else 1.3)
        else:
            pyxel.bltm(t[i] ,91 if i == selected_card else 101,tilemap,2+16*2 + turno*16,(slc-1)*16,12,16,0,f*10, 1.7 if ard == i else 1.3)
        
        
        
        

    
def recorrer():
    print("=== Inicio recorrer, estado previo:", juego["tablero"])
    board_copy = copy.deepcopy(juego["tablero"])

    # 1) PASADA DE DAÑO: aplica todos los ataques de todas las cartas
    for posicion in range(5):
        for color in (0, 1):
            cell = board_copy[color][posicion]
            if isinstance(cell, dict):
                board_copy = cell["DamageType"](board_copy, color, posicion)

    # 2) PASADA DE LIMPIEZA: elimina **todas** las cartas con HP ≤ 0
    for posicion in range(5):
        for color in (0, 1):
            cell = board_copy[color][posicion]
            if isinstance(cell, dict) and cell["HP"] <= 0:
                board_copy[color][posicion] = 0

    juego["tablero"] = board_copy
    print("=== Fin recorrer, estado nuevo  :", juego["tablero"])
    print("===== ",juego["king"])

def info():
    global juego
    tablero = juego["tablero"]
    mx, my = pyxel.mouse_x, pyxel.mouse_y
    if 16 < mx < 32:
        for i, ficha in enumerate(tablero[0]):
            if ficha != 0:
                if 16*(i+1) < my < 16*(i+2):
                        HP, D = tablero[0][i]["HP"], tablero[0][i]["D"]
                        pyxel.text(16, 13 +(i+1)*16, str(HP), 8)
                        pyxel.text(29, 13 +(i+1)*16, str(D), 10)
    elif 112 < mx < 128 :
        for i, ficha in enumerate(tablero[1]):
            if ficha != 0:
                if 16*(i+1) < my < 16*(i+2):
                        HP, D = tablero[1][i]["HP"], tablero[1][i]["D"]
                        pyxel.text(112, 13 +(i+1)*16, str(HP), 8)
                        pyxel.text(125, 13 +(i+1)*16, str(D), 10)
                        


def update():
    if juego["gameOver"]:
        return
    stateMachine()

intro = 0

def draw():
    global rx,ry, rot,scl, selected_card, gameState, intro
    f = math.sin(time.time()*0.7)
    if intro == 0:
        pyxel.cls(0)
        pyxel.text(50,10,"BIENVENIDO A CHESS.EXE",10)
        pyxel.bltm(10,16+ f*3,tilemap,0,0,16,16,11)
        pyxel.bltm(10,32+ f*3,tilemap,16,16,16,16,7)
        pyxel.bltm(10,48+ f*3,tilemap,0,32,16,16,11)
        pyxel.bltm(10,64+ f*3,tilemap,16,48,16,16,7)
        pyxel.bltm(10,80+ f*3,tilemap,0,64,16,16,11)
        
        pyxel.text(26,16+ f*3 +5,"Recto, 1 D, 2 HP",7)
        pyxel.text(26,32+ f*3+5,"Retrigger, 3 HP -1p/r",7)
        pyxel.text(26,48+ f*3+5,"L, 2 o 4 D, 3 HP",7)
        pyxel.text(26,64+ f*3+5,"Recto, 4 D, 5 HP",7)
        pyxel.text(26,80+ f*3+5,"Area, 6 D, 5 HP",7)
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            intro = 1
        
    if intro != 0:
        turno = juego["turno"] % 2
        pyxel.cls(6 if juego["turno"] % 2 == 0 else 1)
        if gameState == 1:
            pyxel.cls(15)
            pyxel.text(56, 5, "BATTLE !" ,9)
        if gameState == 2:
            pyxel.cls(0)  # fondo negro
            msg = "WHITE WINS!" if juego["winner"] == 0 else "BLACK WINS!"
            pyxel.text( (144 - len(msg)*4)//2, 50, msg, pyxel.COLOR_WHITE )
            return
        
        if gameState == 0:
            pyxel.text(53, 5, "WHITE TURN" if juego["turno"] % 2 == 0 else "BLACK TURN", 1 if juego["turno"] % 2 == 0 else 6)
        
            pyxel.text(5 if juego["turno"] % 2 == 0 else 110 , 5, "MONEY: " + str(juego["money"][turno]), 1 if juego["turno"] % 2 == 0 else 6)
    
        pyxel.text(2, 16*3 + 4, str(juego["king"][0]), 8)
        pyxel.text(16*8 + 7, 16*3 + 4, str(juego["king"][1]), 8)
    
        draw_decoracion()
        draw_tablero()
        pintar_Tablero()
        if gameState == 0 :
            pintar_cartas()
        #pyxel.bltm(50,95,tilemap,2+16*2,0,12,16,0,f*10,1.5)
        #pyxel.bltm(16,0,tilemap,2,0,12,16)
        info()



print(selected_card)
pyxel.run(update, draw)