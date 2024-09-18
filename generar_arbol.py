import networkx as nx
import matplotlib.pyplot as plt
import re

def leer_gramatica(archivo):
    reglas = {}
    with open(archivo, 'r') as f:
        for linea in f:
            if '->' in linea:
                lhs, rhs = linea.strip().split('->')
                lhs = lhs.strip()
                rhs = [r.strip() for r in rhs.split('|')]
                reglas[lhs] = rhs
    return reglas

def generar_gramatica_regex(reglas):
    def to_regex(expresion):
        if expresion in reglas:
            # Convertir cada parte de la regla a regex
            partes = [to_regex(rhs) for rhs in reglas[expresion]]
            return f"({'|'.join(partes)})"
        else:
            # Convertir palabras terminales a regex
            return expresion
    
    # Generar la expresión regular para el símbolo inicial 'S'
    regex = to_regex('S')
    return f"^{regex}$"

def verificar_expresion(expresion, regex):
    return re.fullmatch(regex, expresion) is not None

def agregar_nodos_y_aristas(G, nodo, reglas, padre=None):
    if nodo in reglas:
        for rhs in reglas[nodo]:
            for componente in rhs.split():
                if padre:
                    G.add_edge(padre, componente)
                agregar_nodos_y_aristas(G, componente, reglas, padre=componente)

def dibujar_arbol(reglas):
    G = nx.DiGraph()
    agregar_nodos_y_aristas(G, 'S', reglas)
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, arrows=True, node_color='lightblue', node_size=500, font_size=10, font_color='black')
    plt.show()

def main():
    archivo = 'gramatica.txt'
    reglas = leer_gramatica(archivo)
    regex = generar_gramatica_regex(reglas)
    
    # Mostrar la expresión regular generada para depuración
    print(f"Expresión regular generada: {regex}")
    
    expresion = input("Ingrese una expresión para verificar: ")
    
    if verificar_expresion(expresion, regex):
        print("La expresión es aceptada según la gramática.")
        dibujar_arbol(reglas)
    else:
        print("La expresión no es aceptada según la gramática.")

if __name__ == "__main__":
    main()
