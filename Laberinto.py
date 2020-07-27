from pyswip import Prolog 
prolog = Prolog()
Prolog.consult('laberinto.pl')

import turtle
import time
wn= turtle.Screen()
wn.bgcolor("Black")
wn.title("Laberinto")
wn.setup(400,400)
def leerLaberinto():
  x=  [line.split() for line in open("mapa.txt" , "r").readlines()]
  return x
def buscarNumeros(matriz,caracter):
  for filas in range(len(matriz)):
    for columnas in range(len(matriz)[1]):
      if(matriz[filas][columnas]==caracter):
          pos=[filas,columnas]
  return pos

class Penwall(turtle.Turtle):
  def __init__(self):
    turtle.Turtle.__init__(self)
    self.shape("square")
    self.color("blue")
    self.penup()
    self.speed(10)
class Penfood(turtle.Turtle):
  def __init__(self):
    turtle.Turtle.__init__(self)
    self.shape("circle")
    self.pensize(1)
    self.color("gray")
    self.penup()
    self.speed(10)
class Penexplorer(turtle.Turtle):
  def __init__(self,color):
    turtle.Turtle.__init__(self)
    self.shape("circle")
    self.color(color)
    self.penup()
    self.speed(10)

def iniciarlab(lab,penwall,penfood):
  for fila in range(len(lab)):
    for column in range (len(lab[fila])):
      muro=lab[fila][column]
      screen_x=-130+(column*22)
      screen_y=140-(fila*22)
      if (muro=="X"):
        penwall.goto(screen_x,screen_y)
        penwall.stamp()
      else:  
        if(muro!="0"):
          penfood.goto(screen_x,screen_y)
          penfood.stamp()
def pintar(num,lab,penexp):
  for fila in range(len(lab)):
    for column in range (len(lab[fila])):
      muro=lab[fila][column]
      screen_x=-130+(column*22)
      screen_y=140-(fila*22)
      if (muro==num):
          penexp.goto(screen_x,screen_y)
          penexp.stamp()

def explorar(camino,lab,p,p2):    
  for i in range(len(camino)):
    pintar(camino[i],lab,p)
    if i>0:
      pintar(camino[i-1],lab,p2)
    time.sleep(0.2)

p= Penwall()
p2= Penexplorer("Yellow")
p3=Penexplorer("Black")
p4= Penfood()
cam=["fin", "36", "35", "34", "28", "27", "21", "15", "9", "8", "2", "3", "4", "inicio"]
cam.reverse()
iniciarlab(leerLaberinto(),p,p4) 
explorar(cam,leerLaberinto(),p2,p3)

