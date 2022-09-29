import itertools
import json

def abrirJSON(fileName):
    f = open(str(fileName))
    return json.load(f)

def escribirJSON(diccionario, fileName):
    with open(str(fileName), 'w') as file:
        json.dump(diccionario, file, indent=4)

def printMatrix(newMatrix, newStates):
    # imprimir matrix
    general = []
    laTempo = []
    for i in range(len(newMatrix)):
        elemen = newMatrix[i]
        laTempo.append(elemen[2])
        if (i+1)%len(newStates)==0:
            general.append(laTempo)
            laTempo = []

    for i in general:
        print(i)

def transitions(estado, alcanzables, recorridos, transition_function):
    '''
        Función para saber a qué estados pueden llegar desde un estado dado.
    '''
    for i in transition_function:
        if sorted(estado) == sorted(i[0]):
            if sorted(i[2]) not in alcanzables:
                alcanzables.append(sorted(i[2]))

    recorridos.append(sorted(estado))

def induccion(parejaObjetivo, parejasMarcadas, porMarcar, transitionInput):
    '''
        Función para paso recursivo de minimización.
        donde:
            parejaObjetivo es la pareja que se va a buscar en las transiciones
            parejasMarcadas son las parejas que en la matriz tienen un 1 en el paso base.
            porMarcar son las parejas a las cuales se les debe asignar el numero 1 en la matriz
    '''

    if len(parejasMarcadas) > 1:
        # Recorrer la lista asignada a los valores
        for i in transitionInput.items():
            primero = [] # Origenes del primer valor de la pareja
            segundo = [] # Orígenes del segundo valor de la pareja
            for j in i[1]:
                if (parejaObjetivo[0]) == sorted(j[2]):
                    primero.append((j[0]))
                if (parejaObjetivo[1]) == sorted(j[2]):
                    segundo.append((j[0]))
            if len(primero) and len(segundo) > 0:
                # Calcular todas las posibles combinaciones
                all_combinations = []
                for a in primero:
                    for b in segundo:
                        if a != b:
                            all_combinations.append((sorted(a),sorted(b)))
                # Agregar a listas
                for k in all_combinations:
                    if k not in parejasMarcadas:
                        porMarcar.append(k)
                        parejasMarcadas.append(k)

        parejasMarcadas.remove(parejasMarcadas[0]) # Eliminar pareja que se calculó
        induccion(parejasMarcadas[0], parejasMarcadas, porMarcar, transitionInput) # Recursividad

def minimizacion(data):
    # Variables para el AFD minimizado
    newStates = []
    newMatrix = []
    minAFD_estados = []
    minAFD_final_states = []

    # Leer archivo JSON y crear variables con su respectivo valor

    states = data['states']
    letters = data['alphabet']
    transition_function = data['transition']
    start_states = data['start_state']
    final_states = data['final_states']

    # Eliminación de estados inalcanzables desde estado inicial.
    startList = [] # Lista con estado inicial
    recorridos = [] # Para saber qué estados ya los busqué en las transiciones
    alcanzables = [] # Lista con los primeros estados
    recorridos.append(sorted(start_states))

    for i in transition_function:
        startState = [i[0]]
        if startState == start_states or i[0] == start_states:
            startList = i[2]
            alcanzables.append(sorted(startList))

    for i in alcanzables:
        if sorted(i) not in recorridos:
            transitions(i, alcanzables, recorridos, transition_function)

    newStates = alcanzables

    # Reviso que todos sean listas
    for i in newStates:
        if isinstance(i, str):
            i = [i]
    # Reviso si el estado inicial es una lista
    if isinstance(start_states, str):
        start_states = [start_states]
    newStates.append(start_states)

    # Producto cartesiano
    matrix = list(itertools.product(newStates, newStates))

    # Sort de cada elemento
    sorted_final_states = []
    for i in final_states:
        sorted_final_states.append(sorted(i))

    final_states = sorted_final_states
    parejasMarcadas = [] # Lista con las parejas de los estados que tienen 1 

    # Verificar que parejas de la matriz (producto cartesiano) tienen solo 1 estado de aceptación
    for i in matrix:
        first = sorted(i[0])
        second = sorted(i[1])
        if (first in final_states and second not in final_states) or (second in final_states and first not in final_states):
            newMatrix.append((first, second, 1))
            # Añadir a lista de parejas
            parejasMarcadas.append((first, second))
        else:
            newMatrix.append((first, second, 0))

    copyParejas = parejasMarcadas
    # Sacar todas las transiciones según input
    transitionInput = {} # Diccionario con transiciones según input

    # Definir llaves
    for i in letters:
        transitionInput[i] = []

    for i in transition_function:
        tempInput = i[1]
        if isinstance(i[0], str):
            i[0] = [i[0]]
        transitionInput[tempInput].append(i)

    porMarcar = []
    induccion(parejasMarcadas[0], parejasMarcadas, porMarcar, transitionInput)

    for i in copyParejas:
        if i not in porMarcar:
            porMarcar.append(i)

    # Marcar otra vez
    newMatrix2 = []
    for i in newMatrix:
        if (i[0], i[1]) in porMarcar:
            newMatrix2.append((i[0], i[1], 1))
        else:
            newMatrix2.append(i)

    newMatrix = newMatrix2

    # Categorizar según 0 o 1
    ceros = []
    for i in newMatrix:
        if i[2] == 0:
            # No jalar (q,q)
            if i[0] != i[1]:
                if (i[1], i[0]) not in ceros:
                    ceros.append((i[0],i[1]))

    # Eliminar repetidos en ceros
    cerosTemp = []
    for i in ceros:
        if i[0] not in cerosTemp:
            cerosTemp.append(sorted(i[0]))
        if i[1] not in cerosTemp:
            cerosTemp.append(sorted(i[1]))

    ceros = cerosTemp

    # Fusionar todos los estado de cero
    cerosFusion = []
    for i in ceros:
        cerosFusion.extend(i)

    cerosFusion = list(dict.fromkeys(cerosFusion)) # Eliminar repetidos

    # Cambiar transiciones
    for i in ceros:
        for j in transition_function:
            # Sustituir valor por nuevo conjunto
            # Si es el origen lo puedo borrar, pero tengo que dejar  las transiciones con las letters para el estado cerosFusion
            if sorted(j[0]) in i:
                j[0] = cerosFusion
            if sorted(j[2]) in i:
                j[2] = cerosFusion
            j[0] = sorted(j[0])
            j[2] = sorted(j[2])

    # Eliminar los que no son el inicio de otra tranformación.
    for i in transition_function:
        starting = 0
        for j in transition_function:
            if i[2] == j[0]:
                starting += 1
        if starting == 0:
            transition_function.remove(i)

    newTransition = []
    lettersTemp = []
    for i in transition_function:
        if sorted(i[0]) == sorted(cerosFusion):
            # Ver si es estado final
            if sorted(i[0]) in final_states:
                if cerosFusion not in minAFD_final_states:
                    minAFD_final_states.append(sorted(cerosFusion))
                # Añadir las cantidad de transiciones = a len(letter)
                for j in letters:
                    if i[1] == j and j not in lettersTemp:
                        newTransition.append(i)
                        lettersTemp.append(i[1])
                final_states.remove(sorted(i[0]))
        else:
            newTransition.append(i)

    transition_function = newTransition

    transition_functionTemp = []
    for i in transition_function:
        if i not in transition_functionTemp:
            transition_functionTemp.append(i)

    transition_function = transition_functionTemp
    transition_function = [x for x in transition_function if x] #Eliminar objetos incompletos

    # Tomar los estados nuevos
    for i in transition_function:
        if sorted(i[0]) not in minAFD_estados:
            minAFD_estados.append(sorted(i[0]))

    # Eliminar duplicados
    tempDuplicates = []
    for i in final_states:
        if sorted(i) not in tempDuplicates:
            tempDuplicates.append(sorted(i))

    final_states = tempDuplicates
    if sorted(cerosFusion) not in final_states:
        final_states.append(sorted(cerosFusion)) 

    # Escribir en JSON
    minAfd = {}
    minAfd['letters'] = letters
    minAfd['start_state'] = start_states
    minAfd['states'] = minAFD_estados
    minAfd['final_states'] = final_states
    minAfd['transition'] = transition_function

    return minAfd

# Llamar
def minimise():
    data = abrirJSON('AFD.json')
    minAfd = minimizacion(data)
    escribirJSON(minAfd, 'minAFD.json')
    return minAfd

def acceptance(estadoActual, cadena, transition, final_states):
    if len(cadena) > 1:
        for i in transition:
            if i[0] == estadoActual and i[1] == cadena[0]:
                cadena = cadena[1:]
                acceptance(i[2], cadena, transition, final_states)
    else:
        if estadoActual in final_states:
            return True
        return False
