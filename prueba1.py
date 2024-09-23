import networkx as nx
import matplotlib.pyplot as plt

def leer_gramatica(archivo):
    with open(archivo, 'r') as f:
        reglas = f.readlines()
    return [regla.strip() for regla in reglas]

def es_aceptada(cadena, reglas):
    gramatica = {}
    for regla in reglas:
        izquierda, derecha = regla.split("->")
        izquierda = izquierda.strip()
        derecha = derecha.strip().split('|')
        gramatica[izquierda] = [opcion.strip().split() for opcion in derecha]

    def analizar(simbolo, cadena):
        if simbolo not in gramatica:  # Si el símbolo no está en la gramática
            return False
        
        for produccion in gramatica[simbolo]:
            if analizar_produccion(produccion, cadena):
                return True
        return False

    def analizar_produccion(produccion, cadena):
        if not produccion:  # Producción vacía
            return cadena == ""
        
        primer_simbolo = produccion[0]
        
        if primer_simbolo in cadena:  # Si es un terminal
            index = cadena.index(primer_simbolo)
            siguiente_cadena = cadena[index + 1:]
            return analizar_produccion(produccion[1:], siguiente_cadena)
        elif primer_simbolo in gramatica:  # Si es un no terminal
            if analizar(primer_simbolo, cadena):
                return analizar_produccion(produccion[1:], cadena)
        
        return False

    return analizar('S', cadena)

def generar_arbol(reglas):
    G = nx.DiGraph()
    for regla in reglas:
        izquierda, derecha = regla.split("->")
        izquierda = izquierda.strip()
        derecha = derecha.strip().split('|')
        for opcion in derecha:
            simbolos = opcion.strip().split()
            for simbolo in simbolos:
                G.add_edge(izquierda, simbolo)
    return G

def dibujar_arbol(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, arrows=True)
    plt.show()

if __name__ == "__main__":
    reglas = leer_gramatica('gramatica.txt')
    
    cadena = input("Ingrese una cadena: ")
    
    if es_aceptada(cadena, reglas):
        print("La cadena es aceptada.")
        arbol = generar_arbol(reglas)
        dibujar_arbol(arbol)  # Solo dibujar el árbol si es aceptada
    else:
        print("La cadena no fue aceptada por la gramática.")

