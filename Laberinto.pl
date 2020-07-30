#Posiciones de Conecta
'''conecta(inicio,7).
conecta(1,2).
conecta(2,3).
conecta(3,4).
conecta(5,6).
conecta(2,8).
conecta(4,10).
conecta(5,11).
conecta(6,12).
conecta(7,8).
conecta(8,9).
conecta(10,11).
conecta(11,12).
conecta(7,13).
conecta(8,14).
conecta(9,15).
conecta(10,16).
conecta(11,17).
conecta(17,18).
conecta(19,20).
conecta(22,23).
conecta(23,24).
conecta(19,25).
conecta(21,27).
conecta(22,28).
conecta(23,29).
conecta(24,30).
conecta(26,27).
conecta(27,28).
conecta(29,30).
conecta(30,fin).
conecta(26,32).
conecta(28,34).
conecta(31,32).
conecta(33,34).
conecta(34,35).
conecta(35,36).
'''

conectado(Pos1,Pos2) :- conecta(Pos1,Pos2).
conectado(Pos1,Pos2) :- conecta(Pos2,Pos1).

miembro(X,[X|_]).
miembro(X,[_|Y]) :- miembro(X,Y) .
sol :- camino([inicio],Sol),write(Sol) .
camino([fin|RestoDelCamino],[fin|RestoDelCamino]).
camino([PosActual|RestoDelCamino],Sol) :- conectado(PosActual,PosSiguiente),\+ miembro(PosSiguiente,RestoDelCamino),
					   camino([PosSiguiente,PosActual|RestoDelCamino],Sol).
