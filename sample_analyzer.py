from util import *
from components import *
from logicanalyzer import *

# esta primeira parte simula a interação com a interface gráfica

# primeiro caso : Check Conectado a nada
"""
Neste caso, deverá constar None em seu valor
"""
checker_1 = Checker(coords=Coords(0*POINT_SPACE, 0*POINT_SPACE))

# segundo caso : Check Conectado diretamente a um Entry Válido
"""
Neste caso, deverá constar o valor do Entry em seu valor
"""
checker_2 = Checker(coords=Coords(1*POINT_SPACE, 0*POINT_SPACE))
Entry_2 = Entry(coords=Coords(1*POINT_SPACE, 0*POINT_SPACE))
Entry_2.setValue(True)

# terceiro caso : Check conectado a uma porta lógica conectada diretamente a entries válidos
"""
Neste caso, deverá constar o valor da saída da porta em seu valor,
issó após a verificação das entradas da porta
"""
checker_3 = Checker(coords=Coords(7*POINT_SPACE, 0*POINT_SPACE))
Gate_3 = AndGate(coords=Coords(5*POINT_SPACE, 0*POINT_SPACE))
Entry_3_1 = Entry(coords=Coords(2*POINT_SPACE, -1*POINT_SPACE))
Entry_3_2 = Entry(coords=Coords(2*POINT_SPACE, 1*POINT_SPACE))
Entry_3_1.setValue(True)
Entry_3_2.setValue(True)

# quarto caso : Check conectado a uma porta lógica com entradas conectadas a outras portas lógicas
"""
Neste caso, o checker deverá constar o valor da saída da porta em seu valor
isso após a verificação das entradas que receberão a saida das outras duas portas
isso após a verificação das entradas
"""
checker_4 = Checker(coords=Coords(18*POINT_SPACE, 0*POINT_SPACE))
Gate_4_1 = AndGate(coords=Coords(16*POINT_SPACE, 0*POINT_SPACE))
Gate_4_2 = AndGate(coords=Coords(11*POINT_SPACE, -1*POINT_SPACE))
Gate_4_3 = OrGate(coords=Coords(11*POINT_SPACE, 1*POINT_SPACE))
Entry_4_1 = Entry(coords=Coords(8*POINT_SPACE, -2*POINT_SPACE))
Entry_4_2 = Entry(coords=Coords(8*POINT_SPACE, 0*POINT_SPACE))
Entry_4_3 = Entry(coords=Coords(8*POINT_SPACE, 2*POINT_SPACE))
Entry_4_1.setValue(True)
Entry_4_2.setValue(True)
Entry_4_3.setValue(False)

"""
Para não bagunçar a leitura, não foram feitas operações de rotações, nem incluida a utilização dos wires
Para conseguir exeplificar este ultimo caso, dentro dessas condições, a Entry_4_2 é utilizada nas 2 portas Gate_4_2 e Gate_4_3
"""

# Concatenação
"""
Esta parte simulará o algoritmo de zequinha, que concatenará todos os componentes nas 3 listas
neste caso, serão apenas 2 listas, e a terceira(de wires) estará vazia, pelo motivo já explicado
"""
checkers = []
checkers.append(checker_1)
checkers.append(checker_2)
checkers.append(checker_3)
checkers.append(checker_4)
checkers.extend(Gate_3.getChecks())
checkers.extend(Gate_4_1.getChecks())
checkers.extend(Gate_4_2.getChecks())
checkers.extend(Gate_4_3.getChecks())

entries = []
entries.append(Entry_2)
entries.append(Entry_3_1)
entries.append(Entry_3_2)
entries.append(Entry_4_1)
entries.append(Entry_4_2)
entries.append(Entry_4_3)
entries.append(Gate_3.gateOut())
entries.append(Gate_4_1.gateOut())
entries.append(Gate_4_2.gateOut())
entries.append(Gate_4_3.gateOut())

wires = []

# valores ainda não atualizados
for i in checkers:
    print(str(i))
for i in entries:
    print(str(i))

print()
print(len(entries[7].getGate().getChecks()))
a=entries[7].getGate().getChecks()
print(a[0].getChecked())

logicAnalyzer = LogicAnalyzer(entries, wires, checkers)
logicAnalyzer.analyze()

#simulando o analyzer
"""
#primeiro caso
for i in entries:
    if i.getCoords().equals(checker_1.getCoords()):
        checker_1.setValue(i.getValue())
# segundo caso
for i in entries:
    if i.getCoords().equals(checker_2.getCoords()):
        checker_2.setValue(i.getValue())
# terceiro caso
for i in entries:
    if i.getCoords().equals(checker_3.getCoords()):
        if(i.getValue() == None and i.getGate()!= None):
            gate = i.getGate()
            for j in entries:
                if j.getCoords().equals(gate.getIn(0).getCoords()):
                    gate.getIn(0).setValue(j.getValue())
            for j in entries:
                if j.getCoords().equals(gate.getIn(1).getCoords()):
                    gate.getIn(1).setValue(j.getValue())
            checker_3.setValue(gate.gateOut().getValue())

#o quarto caso exige 2 iterações (é o caso que representa 2 ou mais iterações)
# a implementação do mesmo estaticamente não ajuda em nada o entendimento
# e a implementação iterativa deixaria de ser o exemplo de funcionamento 
#   se tornando quase a própria implementação
"""

# valores atualizados
"""
Após a chamada do analizador, ao chamar o draw do componente, 
ele se comportará com o valor calculado pelo analisador
"""
for i in checkers:
    print(str(i))
for i in entries:
    print(str(i))
