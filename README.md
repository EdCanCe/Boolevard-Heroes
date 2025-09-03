# Boolevard Heroes

Este proyecto reliza una simulación del juego de mesa **Flash Point: Fire Rescue** utilizando **Unity** y un sistema de **agentes**.  

El objetivo es recrear la dinámica juego original, pero envés de ser bomberos que apagarán fuego, serán héroes dispersando a fantasmas de una casa embrujada.

<center><img src="https://gifdb.com/images/high/backyardigans-tyrone-tasha-dancing-efggqyqs84kn6yfs.gif"></center>

La simulación incluye:
- Representación del tablero y propagación del fuego.
- Reglas inspiradas en la mecánica original del juego de mesa.

## Índice
 - [Paredes y puertas](#paredes-y-puertas)
 - [Fantasmas y niebla](#fantasmas-y-niebla)
 - [Puntos de interés](#puntos-de-interés)

## Paredes y puertas

Dentro de [walls.py](/backend/walls.py) se pasan las paredes y puertas a 2 matrices en python para poderlas manejar de manera correcta. La base para pasar éstos datos es el tablero original:

<center><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTH3LzP1H99HlgrHrFYmg0O0XdbWEf8MlqIyHMIvd7E9YWm1s4743mZpEW7CwcdcTqmdAc&usqp=CAU"></center>

Los datos estarán guardados de ésta manera:
 - La matriz de verticales guardará el dato del lado derecho de la casilla.
 - La matriz de horizontales guardará el dato del lado inferior de la casilla.

Ésto representan los datos en las matrices:
 - 0: no hay nada / pared destruida
 - 0.5 pared dañada
 - 1: pared completa
 - 2: puerta abierta
 - 3: puerta cerrada
 - 4: puerta destruida

## Fantasmas y niebla

Dentro de [ghosts.py](/backend/ghosts.py) se tiene la representación del turno del fuego, donde empieza colocandose niebla al azar, y si se encuentra con alguna de las siguientes consideraciones ocurren diversos eventos.

Los datos estarán guardados de ésta manera:
 - Se guardarán en una matriz de 8x10, para representar también los bordes de nuestro tablero.

Ésto representan los datos en las matrices:
 - 0: celda vacia.
 - 1: niebla.
 - 2: fuego.

### Niebla:
 - [x] Si donde se va a colocar niebla, ya hay niebla, se convierte en fantasma.
 - [x] Si donde se va a colocar niebla, hay adyacente fantasma, se convierte en fantasma.
 - [x] Si donde se va a colocar niebla, hay un fantasma, ocurre una explosión.
 - [x] Avanza en las 4 direcciónes.
 - [x] Si hay pared, se pone marcador de daño.
 - [x] Si hay una puerta, se destruye.
 - [x] Si hay una casilla vacía, se coloca un fantasma.
 - [x] Si hay niebla, se convierte a fantasma.
 - [x] Si hay una puerta abierta, el fantasma continua su recorrido y se destruye la puerta.
 - [x] Si hay fantasma en una dirección adyacente, continua su recorrido en la misma dirección hasta llegar con alguno de los elementos anteriores.

### Fantasmas:
 - [ ] Si hay un fantasma en un punto de interes se voltea este inmediatamente, si era persona se coloca en el area de personas no salvadas, sino no pasa nada.
 - [ ] Si hay fantasmas en un heroe, se va a la ambulancia más cercana.

## Puntos de interés:

Dentro de [poi.py](/backend/poi.py) se encuentran las funciones de los puntos de interés:
 - Si hay fuego en un punto de interés se voltea automaticamente, descrubriendose si era persona o punto vacío.
 - Si un bombero llega a un POI se voltea automáticamente, descubriendo si era persona o falsa alarma.
 - Se deben salvar a 7 victimas para ganar.
 - Si se pierden 4 victimas, es una derrota.

### Cantidades
 - 18 puntos de interés totales
 - 12 victimas reales
 - 6 falsas alarmas

### Layout
Para representar el escenario con los puntos de interés se usará una matriz de 8x10 (POI_dashboard), donde los valores representarán lo siguiente:
 - Punto de interes -> 3
 - Victima real -> 4
 - Falsa alarma -> 5

Se tienen al principio 3 puntos de interés en las siguientes casillas (x,y), cuando bajen de 3, se tendrán que reponer aleatoriamente en cualquier casilla, eliminando algun fantasma o niebla.