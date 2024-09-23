import networkx as nx  # Importa la biblioteca NetworkX para crear y manipular grafos.
import matplotlib.pyplot as plt  # Importa matplotlib para graficar los árboles sintácticos.

def mostrarArbol(grafo):
    # Función para mostrar el árbol sintáctico.
    plt.figure(figsize=(12, 8))  # Establece el tamaño de la figura.
    posicion = nx.spring_layout(grafo)  # Calcula las posiciones de los nodos en el grafo.
    nx.draw(grafo, posicion, with_labels=True, node_color='red', 
            node_size=3000, font_size=15, font_weight='bold', edge_color='black')  # Dibuja el grafo.
    etiquetas = {nodo: nodo for nodo in grafo.nodes()}  # Crea un diccionario de etiquetas para los nodos.
    nx.draw_networkx_labels(grafo, posicion, etiquetas, font_size=8)  # Dibuja las etiquetas en el grafo.
    plt.title("Árbol Sintáctico")  # Establece el título de la figura.
    plt.axis('off')  # Desactiva los ejes.
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  # Ajusta los márgenes de la figura.
    plt.show()  # Muestra la figura.

def leerGramatica(nombreArchivo):
    # Función para leer la gramática desde un archivo.
    with open(nombreArchivo, 'r') as archivo:  # Abre el archivo en modo lectura.
        V = set()  # Conjunto de símbolos terminales.
        Vxt = set()  # Conjunto de símbolos no terminales.
        P = []  # Lista de producciones.
        S = None  # Símbolo inicial.
        
        for linea in archivo:  # Itera sobre cada línea del archivo.
            linea = linea.strip()  # Elimina espacios en blanco al inicio y al final.
            if linea.startswith('Vt:'):  # Si la línea indica los terminales.
                V = set(linea.replace('Vt:', '').strip().split())  # Extrae los terminales.
            elif linea.startswith('Vxt:'):  # Si la línea indica los no terminales.
                Vxt = set(linea.replace('Vxt:', '').strip().split())  # Extrae los no terminales.
            elif linea.startswith('S:'):  # Si la línea indica el símbolo inicial.
                S = linea.replace('S:', '').strip()  # Extrae el símbolo inicial.
            elif linea.startswith('P:'):  # Si la línea indica el inicio de las producciones.
                break  # Salir del bucle para empezar a leer las producciones.
        
        for linea in archivo:  # Lee las producciones del archivo.
            linea = linea.strip()  # Elimina espacios en blanco.
            if '->' in linea:  # Si la línea contiene una producción.
                izquierda, derecha = linea.split('->')  # Separa la producción en izquierda y derecha.
                izquierda = izquierda.strip()  # Elimina espacios en blanco de la izquierda.
                derecha = derecha.strip().split()  # Separa los símbolos de la derecha.
                P.append((izquierda, derecha))  # Agrega la producción a la lista.
        
        if not (V and Vxt and S and P):  # Verifica si todos los componentes de la gramática están presentes.
            raise ValueError("La gramática no está completa o el formato es incorrecto.")  # Lanza un error si falta algo.
        
        return V, Vxt, S, P  # Devuelve los componentes de la gramática.

def validarGramatica(V, Vxt, S, P):
    # Función para validar la gramática leída.
    if S not in Vxt:  # Verifica si el símbolo inicial está en los no terminales.
        raise ValueError("El símbolo inicial no está en el conjunto de no terminales.")  # Lanza un error si no está.
    
    for izq, der in P:  # Itera sobre cada producción.
        if izq not in Vxt:  # Verifica si el lado izquierdo de la producción es un no terminal.
            raise ValueError(f"El lado izquierdo de la producción '{izq} -> {' '.join(der)}' no es un no terminal.")  # Lanza un error si no lo es.
        for simbolo in der:  # Itera sobre los símbolos del lado derecho.
            if simbolo not in V and simbolo not in Vxt:  # Verifica si cada símbolo es válido.
                raise ValueError(f"El símbolo '{simbolo}' en la producción '{izq} -> {' '.join(der)}' no es válido.")  # Lanza un error si no lo es.

def validarCadena(cadena, V, Vxt, S, P):
    # Función para validar una cadena según la gramática.
    def derivar(actual, resto):
        # Función interna recursiva para derivar símbolos.
        if not actual and not resto:  # Si no hay símbolos por derivar y no queda resto.
            return True  # La cadena es válida.
        if not actual or not resto:  # Si hay símbolos por derivar pero no queda resto o viceversa.
            return False  # La cadena no es válida.
        
        if actual[0] in V:  # Si el primer símbolo es un terminal.
            if actual[0] == resto[0]:  # Si coincide con el primer símbolo del resto.
                return derivar(actual[1:], resto[1:])  # Deriva el siguiente símbolo.
            return False  # Si no coincide, la cadena no es válida.
        
        for izq, der in P:  # Itera sobre las producciones.
            if izq == actual[0]:  # Si el símbolo actual es igual al lado izquierdo de una producción.
                if derivar(der + actual[1:], resto):  # Intenta derivar la producción.
                    return True  # Si se puede derivar, la cadena es válida.
        return False  # Si no se puede derivar, la cadena no es válida.
        
    return derivar([S], list(cadena))  # Inicia la derivación desde el símbolo inicial.

def construirArbol(cadena, S, P, V):
    # Función para construir el árbol sintáctico.
    def derivacion(simbolo, cadenaRestante, grafo=None, padre=None):
        # Función interna recursiva para construir el árbol.
        if grafo is None:  # Si no se ha creado un grafo.
            grafo = nx.DiGraph()  # Crea un nuevo grafo dirigido.
            grafo.add_node(simbolo)  # Agrega el símbolo como nodo inicial.
        
        if not cadenaRestante and simbolo in V:  # Si no queda resto y el símbolo es un terminal.
            return grafo, ''  # Devuelve el grafo y un resto vacío.
        
        if simbolo in V:  # Si el símbolo actual es un terminal.
            if cadenaRestante and simbolo == cadenaRestante[0]:  # Si coincide con el primer símbolo del resto.
                if padre:  # Si hay un padre.
                    grafo.add_edge(padre, simbolo)  # Agrega una arista del padre al símbolo.
                return grafo, cadenaRestante[1:]  # Devuelve el grafo y el resto restante.
            return None, cadenaRestante  # Si no coincide, devuelve None y el resto.
        
        for izq, der in P:  # Itera sobre las producciones.
            if izq == simbolo:  # Si el símbolo actual es el lado izquierdo de una producción.
                subgrafo = grafo.copy()  # Crea una copia del grafo.
                restoTemp = cadenaRestante  # Guarda el resto de la cadena.
                todosDerivan = True  # Bandera para verificar si todos los símbolos derivan.
                for s in der:  # Itera sobre los símbolos del lado derecho.
                    resultado, restoTemp = derivacion(s, restoTemp, subgrafo, simbolo)  # Intenta derivar cada símbolo.
                    if resultado is None:  # Si no se puede derivar.
                        todosDerivan = False  # Cambia la bandera.
                        break  # Sale del bucle.
                    subgrafo = resultado  # Actualiza el subgrafo.
                if todosDerivan:  # Si todos los símbolos derivaron correctamente.
                    if padre:  # Si hay un padre.
                        subgrafo.add_edge(padre, simbolo)  # Agrega una arista del padre al símbolo.
                    return subgrafo, restoTemp  # Devuelve el subgrafo y el resto restante.
        
        return None, cadenaRestante  # Si no se pudo derivar, devuelve None y el resto.

    arbol, _ = derivacion(S, cadena)  # Inicia la derivación desde el símbolo inicial.
    return arbol  # Devuelve el árbol construido.

def main():
    nombreArchivo = input("Ingrese el nombre del archivo de gramática: ")  # Solicita el nombre del archivo de gramática.
    
    try:
        V, Vxt, S, P = leerGramatica(nombreArchivo)  # Lee la gramática del archivo.
        
        print("\nGramatica en Formato BNF:")  # Imprime un encabezado para la gramática.
        print(f"(Vt): {V}")  # Imprime los símbolos terminales.
        print(f"(Vxt): {Vxt}")  # Imprime los símbolos no terminales.
        print(f"(S): {S}")  # Imprime el símbolo inicial.
        print("(P):")  # Imprime un encabezado para las producciones.
        for izquierda, derecha in P:  # Itera sobre las producciones.
            print(f"  {izquierda} -> {' '.join(derecha)}")  # Imprime cada producción.
        
        validarGramatica(V, Vxt, S, P)  # Valida la gramática leída.
        
        while True:  # Bucle para ingresar cadenas de prueba.
            cadena = input("\nIngresar cadena de prueba gramatical (o 'salir' para terminar): ")  # Solicita una cadena.
            if cadena.lower() == 'salir':  # Si el usuario quiere salir.
                break  # Sale del bucle.
            
            if validarCadena(cadena, V, Vxt, S, P):  # Valida la cadena ingresada.
                print(f"La cadena '{cadena}' fue aceptada por la gramática.")  # Imprime que la cadena fue aceptada.
                arbol = construirArbol(cadena, S, P, V)  # Construye el árbol sintáctico para la cadena.
                if arbol and len(arbol.nodes()) > 0:  # Si se generó un árbol válido.
                    mostrarArbol(arbol)  # Muestra el árbol.
                else:
                    print("Error al generar arbol")  # Imprime error si no se generó un árbol.
            else:
                print(f"La cadena '{cadena}' no es aceptada por la gramática.")  # Imprime que la cadena no fue aceptada.
    
    except Exception as e:  # Captura cualquier excepción que ocurra.
        print(f"Error: {str(e)}")  # Imprime el mensaje de error.

if __name__ == "__main__":
    main()  # Ejecuta la función principal al iniciar el programa.
