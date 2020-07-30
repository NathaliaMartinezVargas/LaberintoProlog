from pyswip import Prolog
import turtle

prolog = Prolog()
infile = open('Laberinto.txt', 'r')
lista = []
for line in infile:
    lista = lista+[line]

for i in range(0,len(lista)-1):
    for j in range(0,len(lista[i])-1):
        if(lista[i][j]==lista[i][j+1]=="0"):
            print ("conecta("+str(i)+str(j)+","+str(i)+str(j+1)+").")
        if(lista[i][j]=="0" and lista[i][j+1]=="X"):
            print ("conecta("+str(i)+str(j)+",x).")
        if(lista[i][j]=="X" and lista[i][j+1]=="0"):
            print ("conecta(x,"+str(i)+str(j+1)+").")
        if(lista[i][j]=="0" and lista[i][j+1]=="Y"):
            print ("conecta("+str(i)+str(j)+",y).")
        if(lista[i][j]=="Y" and lista[i][j+1]=="0"):
            print ("conecta(y,"+str(i)+str(j+1)+").")

for i in range(0,len(lista[0])-1):
    for j in range(0,len(lista)-1):
        if(lista[j][i]==lista[j+1][i]=="0"):
            print ("conecta("+str(j)+str(i)+","+str(j+1)+str(i)+").")
        if(lista[j][i]=="0" and lista[j+1][i]=="X"):
            print ("conecta("+str(j)+str(i)+",x).")
        if(lista[j][i]=="X" and lista[j+1][i]=="0"):
            print ("conecta(x,"+str(j+1)+str(i)+").")
        if(lista[j][i]=="0" and lista[j+1][i]=="Y"):
            print ("conecta("+str(j)+str(i)+",y).")
        if(lista[j][i]=="Y" and lista[j+1][i]=="0"):
            print ("conecta(y,"+str(j+1)+str(i)+").")

recorrido = 'O'
visto = '.'
pared = '+'
callejon = '-'            

class Laberinto:
    def __init__(self,ArchivoLaberinto):
        filasEnLaberinto = 0
        columnasEnLaberinto = 0
        self.listaLaberinto = []
        archivoLaberinto = open("map2.txt",'r')
        #filasEnLaberinto = 0
        for linea in archivoLaberinto:
            listaFila = []
            columna = 0
            for caracter in linea[:-1]:
                listaFila.append(caracter)
                if caracter == 'S':
                    self.filaInicio = filasEnLaberinto
                    self.columnaInicio = columna
                columna = columna + 1
            filasEnLaberinto = filasEnLaberinto + 1
            self.listaLaberinto.append(listaFila)
            columnasEnLaberinto = len(listaFila)

        self.filasEnLaberinto = filasEnLaberinto
        self.columnasEnLaberinto = columnasEnLaberinto
        self.xTranslate = -columnasEnLaberinto/2
        self.yTranslate = filasEnLaberinto/2
        self.t = turtle.Turtle()
        self.t.shape('turtle')
        self.wn = turtle.Screen()
        self.wn.setworldcoordinates(-(columnasEnLaberinto-1)/2-.5,-(filasEnLaberinto-1)/2-.5,(columnasEnLaberinto-1)/2+.5,(filasEnLaberinto-1)/2+.5)
    
    #Laberinto dibujado con paredes y caminos libres  
    def dibujarLaberinto(self):
        self.t.speed(10)
        self.wn.tracer(0)
        for y in range(self.filasEnLaberinto):
            for x in range(self.columnasEnLaberinto):
                if self.listaLaberinto[y][x] == pared:
                    self.dibujarCajaCentrada(x+self.xTranslate,-y+self.yTranslate,'purple')
        self.t.color('black')
        self.t.fillcolor('blue')
        self.wn.update()
        self.wn.tracer(1)

    def dibujarCajaCentrada(self,x,y,color):
        self.t.up()
        self.t.goto(x-.5,y-.5)
        self.t.color(color)
        self.t.fillcolor(color)
        self.t.setheading(90)
        self.t.down()
        self.t.begin_fill()
        for i in range(4):
            self.t.forward(1)
            self.t.right(90)
        self.t.end_fill()

    # Movimiento tortuguita 
    def moverTortuga(self,x,y):
        self.t.up()
        self.t.setheading(self.t.towards(x+self.xTranslate,-y+self.yTranslate))
        self.t.goto(x+self.xTranslate,-y+self.yTranslate)

    #Camino de punticos o miga de pan
    def tirarMigaDePan(self,color):
        self.t.dot(10,color)

    def actualizarPosicion(self,fila,columna,val=None):
        if val:
            self.listaLaberinto[fila][columna] = val
        self.moverTortuga(columna,fila)

        if val == recorrido:
            color = 'green'
        elif val == pared:
            color = 'red'
        elif val == visto:
            color = 'black'
        elif val == callejon:
            color = 'red'
        else:
            color = None

        if color:
            self.tirarMigaDePan(color)

    def esSalida(self,fila,columna):
        return (fila == 0 or
                fila == self.filasEnLaberinto-1 or
                columna == 0 or
                columna == self.columnasEnLaberinto-1 )

    def __getitem__(self,indice):
        return self.listaLaberinto[indice]

prolog.assertz('conectado(X,Y):-conecta(X,Y)')
prolog.assertz('conectado(X,Y):-conecta(Y,X)')
prolog.assertz('miembro(X,[X|_])')
prolog.assertz('miembro(X,[_|Y]) :- miembro(X,Y)')
prolog.assertz('tiene_solucion():-hay_camino([x],_)')
prolog.assertz('hay_camino([y|L],[y|L])')
prolog.assertz('hay_camino([X|L],Y):-conectado(X,S),\+miembro(S,L),hay_camino([S,X|L],Y)')

def buscarDesde(laberinto, filaInicio, columnaInicio):
    laberinto.actualizarPosicion(filaInicio, columnaInicio)
    #  Hay una pared, devolver False
    if laberinto[filaInicio][columnaInicio] == pared :
        return False
    #  ya hemos pasado por aqui (mision secreta en espacio explorado vamos)
    if laberinto[filaInicio][columnaInicio] == visto:
        return False
    # 3. parte del camino libre, no hay obstrucción
    if laberinto.esSalida(filaInicio,columnaInicio):
        laberinto.actualizarPosicion(filaInicio, columnaInicio, recorrido)
        return True
    laberinto.actualizarPosicion(filaInicio, columnaInicio, visto)

    # Girar tortuga como cieguito 
    camino = buscarDesde(laberinto, filaInicio-1, columnaInicio) or \
            buscarDesde(laberinto, filaInicio+1, columnaInicio) or \
            buscarDesde(laberinto, filaInicio, columnaInicio-1) or \
            buscarDesde(laberinto, filaInicio, columnaInicio+1)
    if camino:
        laberinto.actualizarPosicion(filaInicio, columnaInicio, recorrido)
    else:
        laberinto.actualizarPosicion(filaInicio, columnaInicio, callejon)
    return camino

miLaberinto = Laberinto('map2.txt')
miLaberinto.dibujarLaberinto()
miLaberinto.actualizarPosicion(miLaberinto.filaInicio,miLaberinto.columnaInicio)

buscarDesde(miLaberinto, miLaberinto.filaInicio, miLaberinto.columnaInicio)