# Reversi IA

Implementación de una heurística empleando el algoritmo Minimax Alpha Beta Prune.

## Descripción

El proyecto consistía en implementar el algoritmo [Minimax Alpha Beta Prunning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
y una heurística para dicho algoritmo que se aplica en los estados
intermedios para determinar cual es el mejor movimiento.

Nuestra heurística se basa en 4 estrategias que por separado no son muy efectivas
pero que juntas y con las respectivas ponderaciones a las mismas se vuelven
bastante fuertes. En concreto son: movilidad, fichas, estabilidad y corners.

Además, nuestra heurística se basó principalmente en la implementación de las ideas
recogidas en el paper [An Analysis of Heuristics in Othello](https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf).

## Requerimientos

Para poder ejecutar el juego necesitaras tener instalado:

- numpy
- tkinter
- python 3.7 o mayor.

## Juega!

Puedes jugar de dos formas:

1. Tu mismo contra la IA:
```sh
cd src
python simulation_manual_vs_IA.py
```
Tu serás las negras y la IA serán las blancas.

2. Tu IA contra nuestra IA:
```sh
cd src
python simulation_IA_vs_IA.py
```
No obstante, antes de ejecutar el juego recuerda importar tu 
función heurística dentro del archivo [simulation_IA_vs_IA.py](./src/simulation_IA_vs_IA.py), tal y como se indica en el mismo.
