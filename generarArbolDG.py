import networkx as nx  # Importar la biblioteca NetworkX para la creación de grafos
import matplotlib.pyplot as plt  # Importar Matplotlib para la visualización de gráficos
from networkx.drawing.nx_agraph import graphviz_layout  # Importar la función para el diseño de gráficos con Graphviz

# Función para leer las reglas gramaticales del archivo
def interpretarGramatica(archivo):
    reglasGramaticales = {}  # Diccionario para almacenar las reglas de la gramática
    with open(archivo, 'r') as f:  # Abrir el archivo de la gramática en modo lectura
        for linea in f:  # Iterar sobre cada línea del archivo
            linea = linea.strip()  # Eliminar espacios en blanco al inicio y al final de la línea
            if '->' in linea:  # Verificar si la línea contiene una producción
                parteIzquierda, parteDerecha = linea.split('->')  # Separar la parte izquierda y derecha de la producción
                parteIzquierda = parteIzquierda.strip()  # Eliminar espacios de la parte izquierda
                parteDerecha = [token.strip() for token in parteDerecha.split('|')]  # Separar y limpiar las producciones de la parte derecha
                
                # Agregar la producción al diccionario de reglas
                if parteIzquierda in reglasGramaticales:
                    reglasGramaticales[parteIzquierda].extend(parteDerecha)  # Extender la lista de producciones
                else:
                    reglasGramaticales[parteIzquierda] = parteDerecha  # Crear una nueva entrada en el diccionario
    return reglasGramaticales  # Retornar el diccionario con las reglas gramaticales

# Función para generar el árbol basado en las reglas y la cadena ingresada
def construirArbol(reglas, nodoInicial, tokens):
    arbol = nx.DiGraph()  # Crear un grafo dirigido para el árbol
    derivacion = []  # Lista para guardar la derivación y validar la entrada
    indiceToken = 0  # Índice para recorrer los tokens ingresados por el usuario
    
    def expandirNodo(nodo, profundidad):
        nonlocal indiceToken  # Permitir que la función interna acceda a la variable externa
        if nodo in reglas and indiceToken <= len(tokens):  # Aceptar incluso si llegamos al final de los tokens
            for produccion in reglas[nodo]:  # Iterar sobre las producciones de la regla actual
                simbolos = produccion.split()  # Separar los símbolos en la producción
                subArbolValido = True  # Bandera para verificar la validez del subárbol
                for simbolo in simbolos:  # Iterar sobre los símbolos en la producción
                    if simbolo == 'ε':  # Manejo del vacío
                        arbol.add_node('ε', layer=profundidad)  # Agregar nodo vacío al árbol
                        arbol.add_edge(nodo, 'ε')  # Crear un borde desde el nodo padre al símbolo vacío
                        derivacion.append('ε')  # Agregar el vacío a la derivación
                        continue  # Continuar con el siguiente símbolo de la producción

                    if indiceToken >= len(tokens):  # Salir si ya no hay más tokens por procesar
                        break

                    if simbolo == tokens[indiceToken]:  # Verificar si el símbolo coincide con el token actual
                        arbol.add_node(simbolo, layer=profundidad)  # Agregar el símbolo como nodo en el árbol
                        arbol.add_edge(nodo, simbolo)  # Crear un borde desde el nodo padre al símbolo
                        derivacion.append(simbolo)  # Agregar el símbolo a la lista de derivación
                        indiceToken += 1  # Avanzar al siguiente token
                    elif simbolo in reglas:  # Si el símbolo es un no terminal
                        arbol.add_node(simbolo, layer=profundidad)  # Agregar el símbolo como nodo en el árbol
                        arbol.add_edge(nodo, simbolo)  # Crear un borde desde el nodo padre al símbolo
                        derivacion.append(simbolo)  # Agregar el símbolo a la lista de derivación
                        expandirNodo(simbolo, profundidad + 1)  # Expandir el nodo no terminal
                    else:
                        subArbolValido = False  # Marcar el subárbol como no válido
                        break  # Romper el bucle si no se puede expandir
                    
                # Si generamos un subárbol válido que cubre la parte de la cadena, dejar de expandir
                if subArbolValido and indiceToken == len(tokens):
                    break

    arbol.add_node(nodoInicial, layer=0)  # Agregar el nodo inicial al árbol
    derivacion.append(nodoInicial)  # Agregar el nodo inicial a la lista de derivación
    expandirNodo(nodoInicial, 1)  # Llamar a la función para expandir el nodo inicial
    return arbol, derivacion  # Retornar el árbol y la lista de derivación

# Función para visualizar el árbol
def visualizarArbol(arbol):
    pos = graphviz_layout(arbol, prog='dot')  # Obtener posiciones de los nodos usando Graphviz
    plt.figure(figsize=(8, 6))  # Configurar el tamaño de la figura
    nx.draw(arbol, pos, with_labels=True, node_color='lightblue', font_size=10, node_size=3000, font_weight='bold')  # Dibujar el árbol
    plt.title("Árbol de derivación gramatical")  # Título del gráfico
    plt.show()  # Mostrar el gráfico

# Función para validar si la cadena ingresada corresponde a la derivación
def esCadenaValida(tokens, derivacion, reglas):
    # Filtrar los tokens que no son no terminales de la derivación
    derivacionSinTerminales = [token for token in derivacion if token not in reglas and token != 'ε']
    return tokens == derivacionSinTerminales[:len(tokens)]  # Comparar los tokens con la derivación filtrada

# Función principal
def main():
    archivoGramatica = 'pruebas.txt'  # Nombre y ruta del archivo de gramática
    reglasGramaticales = interpretarGramatica(archivoGramatica)  # Leer las reglas gramaticales del archivo
    
    # Definir el nodo de inicio (variable inicial de la gramática)
    nodoInicial = 'S'  # Esto puede cambiar dependiendo de tu gramática
    
    while True:  # Bucle para permitir múltiples entradas
        entradaUsuario = input("Ingrese una cadena para analizar (o 'salir' para terminar): ")  # Solicitar entrada al usuario
        if entradaUsuario.lower() == 'salir':  # Verificar si el usuario quiere salir
            break  # Romper el bucle si el usuario escribe 'salir'
        
        tokens = entradaUsuario.split()  # Dividir la cadena en tokens
        
        # Generar el árbol sintáctico
        arbol, derivacion = construirArbol(reglasGramaticales, nodoInicial, tokens)  # Llamar a la función para construir el árbol
        
        # Validar la cadena ingresada
        if esCadenaValida(tokens, derivacion, reglasGramaticales):  # Verificar la validez de la cadena
            print("La cadena es válida según la gramática.")  # Mensaje si la cadena es válida
        else:
            print("La cadena no es válida según la gramática.")  # Mensaje si la cadena no es válida
        
        visualizarArbol(arbol)  # Mostrar siempre el árbol

if __name__ == "__main__":
    main()  # Ejecutar la función principal si este archivo es el programa principal
