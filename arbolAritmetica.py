#este codigo es para las gramaticas de aritmetica o expresiones regulares
import networkx as nx  # Importa la biblioteca NetworkX para crear y manipular grafos
import matplotlib.pyplot as plt  # Importa Matplotlib para graficar

class Nodo:
    _id_counter = 0  # Contador para asignar IDs únicos a los nodos

    def __init__(self, valor):
        self.valor = valor  # Valor del nodo
        self.izquierda = None  # Hijo izquierdo
        self.derecha = None  # Hijo derecho
        self.id = Nodo._id_counter  # Asigna un ID único al nodo
        Nodo._id_counter += 1  # Incrementa el contador de ID para el siguiente nodo

def leerGramatica(archivoGramatica):
    # Función para leer la gramática desde un archivo
    with open(archivoGramatica, 'r') as archivo:
        Vt = set()  # Conjunto de terminales
        Vxt = set()  # Conjunto de no terminales
        P = []  # Lista de producciones
        S = None  # Símbolo inicial

        for linea in archivo:
            linea = linea.strip()  # Elimina espacios en blanco al inicio y al final
            if linea.startswith('Vt:'):
                Vt = set(linea.replace('Vt:', '').strip().split())  # Asigna los terminales
            elif linea.startswith('Vxt:'):
                Vxt = set(linea.replace('Vxt:', '').strip().split())  # Asigna los no terminales
            elif linea.startswith('S:'):
                S = linea.replace('S:', '').strip()  # Asigna el símbolo inicial
            elif linea.startswith('P:'):
                break  # Termina la lectura de la sección de gramática

        for linea in archivo:
            linea = linea.strip()  # Elimina espacios en blanco al inicio y al final
            if '->' in linea:  # Verifica si la línea contiene una producción
                izquierda, derecha = linea.split('->')  # Divide en lado izquierdo y derecho
                izquierda = izquierda.strip()  # Limpia el lado izquierdo
                derecha = derecha.strip().split()  # Limpia y divide el lado derecho
                P.append((izquierda, derecha))  # Agrega la producción a la lista

        # Verifica si la gramática está completa
        if not (Vt and Vxt and S and P):
            raise ValueError("La gramática no está completa o el formato es incorrecto.")
        return Vt, Vxt, S, P  # Retorna los componentes de la gramática

def validarGramatica(Vt, Vxt, S, P):
    # Función para validar los componentes de la gramática
    if S not in Vxt:
        raise ValueError("El símbolo inicial no está en el conjunto de no terminales.")  # Verifica símbolo inicial
    for izq, der in P:
        if izq not in Vxt:
            raise ValueError(f"El lado izquierdo de la producción '{izq} -> {' '.join(der)}' no es un no terminal.")  # Verifica lado izquierdo
        for simbolo in der:
            if simbolo != 'ε' and simbolo not in Vt and simbolo not in Vxt:
                raise ValueError(f"El símbolo '{simbolo}' en la producción '{izq} -> {' '.join(der)}' no es válido.")  # Verifica símbolos en producción

def validarCadena(cadena, Vt, Vxt, S, P):
    # Función para validar una cadena con la gramática
    def derivar(actual, resto, arbolNodo):
        if not actual:  # Si no hay más símbolos para derivar
            return not resto, arbolNodo  # Retorna si la cadena restante está vacía

        simboloActual = actual[0]  # Obtiene el símbolo actual

        if simboloActual in Vt:  # Si el símbolo es terminal
            if resto and simboloActual == resto[0]:  # Verifica si coincide con el primer símbolo de la cadena restante
                hoja = Nodo(simboloActual)  # Crea un nodo hoja
                arbolNodo.izquierda = hoja  # Asigna la hoja como hijo izquierdo
                return derivar(actual[1:], resto[1:], arbolNodo)  # Continúa con los siguientes símbolos
            return False, None  # Si no coincide, retorna falso

        if simboloActual in Vxt:  # Si el símbolo es no terminal
            for izq, der in P:  # Revisa las producciones
                if izq == simboloActual:  # Si el lado izquierdo de la producción coincide
                    subarbol = Nodo(izq)  # Crea un subárbol para el símbolo
                    if arbolNodo.izquierda is None:  # Si no hay hijo izquierdo
                        arbolNodo.izquierda = subarbol  # Asigna el subárbol
                    else:
                        arbolNodo.derecha = subarbol  # Asigna el subárbol como hijo derecho

                    if der == ['ε']:  # Si la producción es epsilon
                        valido, _ = derivar(actual[1:], resto, subarbol)  # Deriva el siguiente símbolo
                        if valido:
                            return True, arbolNodo  # Si es válido, retorna verdadero
                    else:
                        nuevoActual = der + actual[1:]  # Combina la producción con los símbolos restantes
                        valido, nuevoArbol = derivar(nuevoActual, resto, subarbol)  # Deriva con la nueva cadena
                        if valido:
                            return True, arbolNodo  # Si es válido, retorna verdadero
            return False, None  # Si no hay producciones válidas, retorna falso

        return False, None  # Si no es ni terminal ni no terminal, retorna falso

    tokens = list(cadena.replace(" ", ""))  # Convierte la cadena a una lista de tokens
    valido, arbol = derivar([S], tokens, Nodo(S))  # Comienza la derivación desde el símbolo inicial
    return valido, arbol  # Retorna si es válida y el árbol de derivación

def agregarNodos(grafo, nodo):
    # Función para agregar nodos al grafo
    if nodo:  # Si el nodo no es None
        grafo.add_node(nodo.id, label=nodo.valor)  # Agrega el nodo al grafo
        if nodo.izquierda:  # Si hay un hijo izquierdo
            grafo.add_edge(nodo.id, nodo.izquierda.id)  # Conecta el nodo con su hijo izquierdo
            agregarNodos(grafo, nodo.izquierda)  # Llama recursivamente para el hijo izquierdo
        if nodo.derecha:  # Si hay un hijo derecho
            grafo.add_edge(nodo.id, nodo.derecha.id)  # Conecta el nodo con su hijo derecho
            agregarNodos(grafo, nodo.derecha)  # Llama recursivamente para el hijo derecho

def dibujarArbol(raiz, expresion):
    # Función para dibujar el árbol de derivación
    grafo = nx.DiGraph()  # Crea un grafo dirigido
    agregarNodos(grafo, raiz)  # Agrega los nodos del árbol al grafo

    pos = nx.spring_layout(grafo)  # Define la disposición de los nodos en el grafo
    etiquetas = nx.get_node_attributes(grafo, 'label')  # Obtiene las etiquetas de los nodos

    nx.draw(grafo, pos, labels=etiquetas, with_labels=True, arrows=True, node_size=2000, node_color='lightblue')  # Dibuja el grafo
    plt.title(f"Árbol de Derivación para la Expresión: {expresion}")  # Título del gráfico
    plt.show()  # Muestra el gráfico

def analizarAritmetica(archivoGramatica):
    # Función principal para analizar la gramática aritmética
    try:
        Vt, Vxt, S, P = leerGramatica(archivoGramatica)  # Lee la gramática

        print("\nComponentes de la Gramática Aritmética:")
        print(f"Terminales (Vt): {Vt}")  # Muestra los terminales
        print(f"No terminales (Vxt): {Vxt}")  # Muestra los no terminales
        print(f"Símbolo inicial (S): {S}")  # Muestra el símbolo inicial
        print("Producciones (P):")
        for izquierda, derecha in P:
            print(f"  {izquierda} -> {' '.join(derecha)}")  # Muestra las producciones

        validarGramatica(Vt, Vxt, S, P)  # Valida los componentes de la gramática

        while True:
            expresion = input("\nIngrese la expresión aritmética a validar (o 'salir' para terminar): ")  # Solicita una expresión
            if expresion.lower() == 'salir':
                break  # Termina si el usuario escribe 'salir'

            valido, arbol = validarCadena(expresion, Vt, Vxt, S, P)  # Valida la expresión
            if valido:
                print(f"La expresión '{expresion}' es válida.")  # Si es válida, lo indica
                dibujarArbol(arbol, expresion)  # Dibuja el árbol de derivación
            else:
                print(f"La expresión '{expresion}' no es válida.")  # Si no es válida, lo indica

    except Exception as e:
        print(f"Error: {str(e)}")  # Maneja errores durante la ejecución

# Ejemplo de uso:
analizarAritmetica('aritmetica.txt')  # Llama a la función principal con el archivo de gramática
