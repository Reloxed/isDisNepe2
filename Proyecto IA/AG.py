import random
import networkx as nx
from MetodosAuxiliares import *
#from Main import *

g = nx.Graph();

g.add_edge(1, 2);
g.add_edge(2, 3);
g.add_edge(1, 3);
g.add_edge(2, 4);
g.add_edge(1, 4);
g.add_edge(4, 5);
g.add_edge(1, 6);

tam = 2 # Número de individuos por población
largo = nx.number_of_nodes(g) # Longitud de la lista
gc_modelo = nx.greedy_color(g) # Coloreado óptimo del grafo
presion = 3 # Número de individuos que se seleccionan para la evolución
posibilidad_mutacion = 0.2 # Probabilidad de que un individuo mute

"""
Crea un individuo
"""
def crea_individuo(min, max):
    return[random.randint(min, max) for i in range(largo)]

"""
Crea una población
"""

def crea_poblacion():
    return [crea_individuo(1, colores(g)) for i in range(tam)]

poblacion_inicial = crea_poblacion();

"""
Calcula el fitness para un individuo
"""
def calcula_fitness(individuo):
    fitness = 0
    for i in range(len(gc_modelo)):
        if crea_individuo[i] != gc_modelo[i]:
            fitness += 1
    return fitness

'''
1. Se puntúan todos los elementos de la población y nos quedamos con los mejores (se guardan en 'seleccionados').
2. Se mezclan los elegidos para crear nuevos individuos
'''
def seleccion(poblacion):
    puntuados = [(calcula_fitness(i), i) for i in poblacion]
    puntuados = [i[1] for i in sorted(puntuados)]

    seleccionados = puntuados[(len(puntuados) - presion)]

    return seleccionados

def genera_sucesor():
    #poblacion = poblacion_inicial;
    individuo = random.choice(poblacion_inicial)
    elegido = random.choice(individuo)
    numero = random.randint(0, len(individuo))
    individuo_cambiado = individuo
    individuo_cambiado[elegido] = numero;
    #return ', '.join(str(e) for e in individuo) + " de los cuales la posicion " + str(elegido) + " cambia a " + str(numero) + " que pasa a ser " + str(individuo_cambiado)
    return individuo_cambiado;


def enfriamiento_simulado(t_inicial, factor_descenso, n_enfriamientos, n_iteraciones):
    temperatura = t_inicial;
    actual = poblacion_inicial;
    valor_actual = seleccion(actual);
    mejor = actual;
    valor_mejor = valor_actual;

    for i in range (0, n_enfriamientos):
        for j in range (0, n_iteraciones):
            candidata = genera_sucesor()
            valor_candidata = calcula_fitness(candidata)
            incremento = valor_candidata - valor_actual
            if(incremento < 0):
                actual = candidata
                valor_actual = valor_candidata
            if(valor_actual < valor_mejor):
                mejor = actual
                valor_mejor = valor_actual
        temperatura -= factor_descenso

    return mejor & valor_mejor

