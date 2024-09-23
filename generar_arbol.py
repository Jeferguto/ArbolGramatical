import networkx as nx
import matplotlib.pyplot as plt

class Nodo:
    _id_counter = 0

    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.id = Nodo._id_counter
        Nodo._id_counter += 1

def leer_gramatica(archivo_gramatica):
    with open(archivo_gramatica, 'r') as archivo:
        Vt = set()
        Vxt = set()
        P = []
        S = None

        for linea in archivo:
            linea = linea.strip()
            if linea.startswith('Vt:'):
                Vt = set(linea.replace('Vt:', '').strip().split())
            elif linea.startswith('Vxt:'):
                Vxt = set(linea.replace('Vxt:', '').strip().split())
            elif linea.startswith('S:'):
                S = linea.replace('S:', '').strip()
            elif linea.startswith('P:'):
                break

        for linea in archivo:
            linea = linea.strip()
            if '->' in linea:
                izquierda, derecha = linea.split('->')
                izquierda = izquierda.strip()
                derecha = derecha.strip().split()
                P.append((izquierda, derecha))

        if not (Vt and Vxt and S and P):
            raise ValueError("La gramática no está completa o el formato es incorrecto.")
        return Vt, Vxt, S, P

def validar_gramatica(Vt, Vxt, S, P):
    if S not in Vxt:
        raise ValueError("El símbolo inicial no está en el conjunto de no terminales.")
    for izq, der in P:
        if izq not in Vxt:
            raise ValueError(f"El lado izquierdo de la producción '{izq} -> {' '.join(der)}' no es un no terminal.")
        for simbolo in der:
            if simbolo != 'ε' and simbolo not in Vt and simbolo not in Vxt:
                raise ValueError(f"El símbolo '{simbolo}' en la producción '{izq} -> {' '.join(der)}' no es válido.")

def validar_cadena(cadena, Vt, Vxt, S, P):
    def derivar(actual, resto, arbol_nodo):
        if not actual:
            return not resto, arbol_nodo

        simbolo_actual = actual[0]

        if simbolo_actual in Vt:
            if resto and simbolo_actual == resto[0]:
                hoja = Nodo(simbolo_actual)
                arbol_nodo.izquierda = hoja
                return derivar(actual[1:], resto[1:], arbol_nodo)
            return False, None

        if simbolo_actual in Vxt:
            for izq, der in P:
                if izq == simbolo_actual:
                    subarbol = Nodo(izq)
                    if arbol_nodo.izquierda is None:
                        arbol_nodo.izquierda = subarbol
                    else:
                        arbol_nodo.derecha = subarbol

                    if der == ['ε']:
                        valido, _ = derivar(actual[1:], resto, subarbol)
                        if valido:
                            return True, arbol_nodo
                    else:
                        nuevo_actual = der + actual[1:]
                        valido, nuevo_arbol = derivar(nuevo_actual, resto, subarbol)
                        if valido:
                            return True, arbol_nodo
            return False, None

        return False, None

    tokens = list(cadena.replace(" ", ""))
    valido, arbol = derivar([S], tokens, Nodo(S))
    return valido, arbol

def agregar_nodos(grafo, nodo):
    if nodo:
        grafo.add_node(nodo.id, label=nodo.valor)
        if nodo.izquierda:
            grafo.add_edge(nodo.id, nodo.izquierda.id)
            agregar_nodos(grafo, nodo.izquierda)
        if nodo.derecha:
            grafo.add_edge(nodo.id, nodo.derecha.id)
            agregar_nodos(grafo, nodo.derecha)

def dibujar_arbol(raiz, expresion):
    grafo = nx.DiGraph()
    agregar_nodos(grafo, raiz)

    pos = nx.spring_layout(grafo)
    etiquetas = nx.get_node_attributes(grafo, 'label')

    nx.draw(grafo, pos, labels=etiquetas, with_labels=True, arrows=True, node_size=2000, node_color='lightblue')
    plt.title(f"Árbol de Derivación para la Expresión: {expresion}")
    plt.show()

def analizar_aritmetica(archivo_gramatica):
    try:
        Vt, Vxt, S, P = leer_gramatica(archivo_gramatica)

        print("\nComponentes de la Gramática Aritmética:")
        print(f"Terminales (Vt): {Vt}")
        print(f"No terminales (Vxt): {Vxt}")
        print(f"Símbolo inicial (S): {S}")
        print("Producciones (P):")
        for izquierda, derecha in P:
            print(f"  {izquierda} -> {' '.join(derecha)}")

        validar_gramatica(Vt, Vxt, S, P)

        while True:
            expresion = input("\nIngrese la expresión aritmética a validar (o 'salir' para terminar): ")
            if expresion.lower() == 'salir':
                break

            valido, arbol = validar_cadena(expresion, Vt, Vxt, S, P)
            if valido:
                print(f"La expresión aritmética '{expresion}' es válida según la gramática.")
                dibujar_arbol(arbol, expresion)
            else:
                print(f"La expresión aritmética '{expresion}' no es válida según la gramática.")

    except Exception as e:
        print(f"Error: {str(e)}")

# Punto de entrada del programa
if __name__ == "__main__":
    archivo_gramatica = input("Ingrese el nombre del archivo de gramática aritmética (con extensión .txt): ")
    analizar_aritmetica(archivo_gramatica)
