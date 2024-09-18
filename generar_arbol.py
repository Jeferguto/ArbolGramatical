import networkx as nx
import matplotlib.pyplot as plt

# Leer la gramática desde un archivo
def leer_gramatica(archivo_gramatica):
    # Abrir el archivo de gramática en modo lectura
    with open(archivo_gramatica, 'r') as archivo:
        Vt = set()  # Conjunto de símbolos terminales
        Vxt = set()  # Conjunto de símbolos no terminales
        P = []  # Lista de producciones
        S = None  # Símbolo inicial
        
        # Leer cada línea del archivo
        for linea in archivo:
            linea = linea.strip()  # Eliminar espacios en blanco al inicio y al final
            # Procesar líneas que definen terminales
            if linea.startswith('Vt:'):
                Vt = set(linea.replace('Vt:', '').strip().split())
            # Procesar líneas que definen no terminales
            elif linea.startswith('Vxt:'):
                Vxt = set(linea.replace('Vxt:', '').strip().split())
            # Procesar la línea que define el símbolo inicial
            elif linea.startswith('S:'):
                S = linea.replace('S:', '').strip()
            # Procesar líneas que definen producciones
            elif linea.startswith('P:'):
                break
        
        # Leer las producciones desde el archivo
        for linea in archivo:
            linea = linea.strip()
            if '->' in linea:
                izquierda, derecha = linea.split('->')  # Dividir en parte izquierda y derecha
                izquierda = izquierda.strip()
                derecha = derecha.strip().split()  # Dividir la parte derecha en símbolos
                P.append((izquierda, derecha))  # Añadir la producción a la lista
        
        # Devolver los componentes de la gramática
        return Vt, Vxt, S, P

# Construir un grafo a partir de la gramática
def construir_grafo(S, P):
    G = nx.DiGraph()  # Crear un grafo dirigido
    # Función auxiliar para agregar nodos y arcos al grafo
    def agregar_nodo(izq, der):
        for simbolo in der:
            G.add_edge(izq, simbolo)  # Añadir un arco del símbolo izquierdo al derecho
    
    # Iterar sobre las producciones y agregar nodos y arcos al grafo
    for izq, der in P:
        agregar_nodo(izq, der)
    
    # Devolver el grafo construido
    return G

# Función para mostrar el grafo
def mostrar_grafo(G):
    plt.figure(figsize=(10, 6))  # Establecer el tamaño de la figura
    pos = nx.spring_layout(G, k=0.5, iterations=50)  # Posiciones de los nodos usando el diseño de primavera
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_weight='bold')  # Dibujar el grafo
    plt.title("Grafo Sintáctico de la Gramática")  # Título del gráfico
    plt.show()  # Mostrar el gráfico

# Función para verificar si una cadena es aceptada por la gramática
def es_aceptada(cadena, S, P, Vt):
    # Crear una lista de estados iniciales con el símbolo inicial
    estados = [S]
    # Iterar sobre cada símbolo en la cadena
    for simbolo in cadena:
        nuevos_estados = []
        for estado in estados:
            for izq, der in P:
                if estado == izq:
                    if der[0] == simbolo or der[0] == '*':  # '*' representa un símbolo de terminal
                        nuevos_estados.append(der[1])  # Añadir el nuevo estado si el símbolo coincide
        estados = nuevos_estados  # Actualizar la lista de estados con los nuevos estados
    # Verificar si algún estado final es una cadena vacía
    return any(estado == '' for estado in estados)

# Función principal
def main(archivo_gramatica):
    # Leer la gramática desde el archivo
    Vt, Vxt, S, P = leer_gramatica(archivo_gramatica)
    
    # Imprimir los componentes de la gramática para verificar
    print(f"Terminales (Vt): {Vt}")
    print(f"No terminales (Vxt): {Vxt}")
    print(f"Símbolo inicial (S): {S}")
    print("Producciones (P):")
    for izquierda, derecha in P:
        print(f"  {izquierda} -> {' '.join(derecha)}")
    
    # Construir el grafo sintáctico
    G = construir_grafo(S, P)
    # Mostrar el grafo
    mostrar_grafo(G)
    
    # Leer una cadena del usuario
    cadena = input("Ingrese una cadena para verificar si es aceptada por la gramática: ")
    
    # Verificar si la cadena es aceptada por la gramática
    if es_aceptada(cadena, S, P, Vt):
        print(f"La cadena '{cadena}' es aceptada por la gramática.")
    else:
        print(f"La cadena '{cadena}' no es aceptada por la gramática.")

# Ejecutar el programa si este archivo es el principal
if __name__ == "__main__":
    archivo_gramatica = "gramatica.txt"  # Nombre del archivo de gramática
    main(archivo_gramatica)
