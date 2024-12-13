import tkinter as tk
from tkinter import filedialog, messagebox
from enum import Enum
import networkx as nx
import matplotlib.pyplot as plt
from itertools import product

# Leer proposiciones desde un archivo
def leer_proposiciones_desde_archivo(archivo):
    proposiciones = []
    try:
        with open(archivo, "r") as file:
            for linea in file:
                linea = linea.strip()
                if ":" in linea:
                    descripcion, proposicion = linea.split(":", 1)
                    proposiciones.append((descripcion.strip(), proposicion.strip()))
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
    return proposiciones

# Extraer variables de una proposición
def extraer_variables(proposicion):
    tokens = set(proposicion.split())
    variables = [token for token in tokens if len(token) == 1 and token.isalpha()]
    return sorted(variables)

# Dibujar un árbol genérico
def dibujar_arbol(grafo, titulo):
    pos = nx.spring_layout(grafo)
    plt.figure(figsize=(12, 8))
    nx.draw(grafo, pos, with_labels=True, node_color="lightblue", font_size=10, node_size=3000)
    plt.title(titulo)
    plt.show()

# Generar Árbol AST
def generar_arbol_ast(proposicion):
    grafo = nx.DiGraph()
    tokens = proposicion.split()
    anterior = None

    for i, token in enumerate(tokens):
        nodo_actual = f"Nodo-{i+1} ({token})"
        grafo.add_node(nodo_actual)
        if anterior:
            grafo.add_edge(anterior, nodo_actual)
        anterior = nodo_actual

    return grafo

# Generar Árbol Semántico
def generar_arbol_semantico(variables):
    grafo = nx.DiGraph()
    grafo.add_node("Raíz: Variables")

    for var in variables:
        grafo.add_node(f"Variable: {var}")
        grafo.add_edge("Raíz: Variables", f"Variable: {var}")

    return grafo

# Generar Árbol de Decisiones
def generar_arbol_decisiones(variables, proposicion):
    grafo = nx.DiGraph()
    grafo.add_node("Raíz: Decisión")

    combinaciones = list(product([True, False], repeat=len(variables)))

    for i, combinacion in enumerate(combinaciones):
        decision = f"Decisión-{i+1}: {dict(zip(variables, combinacion))}"
        grafo.add_node(decision)
        grafo.add_edge("Raíz: Decisión", decision)

    return grafo

# Interfaz gráfica
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto - Árboles Visuales")
        self.proposiciones = []

        # Botón para cargar proposiciones desde archivo
        tk.Button(root, text="Cargar Proposiciones desde Archivo", command=self.cargar_proposiciones).pack(pady=10)

        # Lista de reglas cargadas
        self.reglas_label = tk.Label(root, text="Reglas cargadas:", font=("Arial", 12))
        self.reglas_label.pack(pady=10)

        self.reglas_listbox = tk.Listbox(root, height=10, selectmode=tk.SINGLE)
        self.reglas_listbox.pack(pady=10)

        # Botones para los diferentes árboles
        tk.Button(root, text="Generar Árbol AST", command=self.mostrar_arbol_ast).pack(pady=5)
        tk.Button(root, text="Generar Árbol Semántico", command=self.mostrar_arbol_semantico).pack(pady=5)
        tk.Button(root, text="Generar Árbol de Decisiones", command=self.mostrar_arbol_decisiones).pack(pady=5)

        # Resultado
        self.resultado = tk.Label(root, text="", font=("Arial", 14), fg="blue")
        self.resultado.pack(pady=10)

    def cargar_proposiciones(self):
        archivo = filedialog.askopenfilename(title="Seleccionar Archivo de Proposiciones", filetypes=[("Archivos de Texto", "*.txt")])
        if archivo:
            self.proposiciones = leer_proposiciones_desde_archivo(archivo)
            self.reglas_listbox.delete(0, tk.END)
            for descripcion, _ in self.proposiciones:
                self.reglas_listbox.insert(tk.END, descripcion)
            messagebox.showinfo("Cargar Proposiciones", f"Se cargaron {len(self.proposiciones)} proposiciones.")

    def mostrar_arbol_ast(self):
        seleccion = self.reglas_listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una regla para generar su Árbol AST.")
            return

        descripcion, proposicion = self.proposiciones[seleccion[0]]

        # Generar y mostrar el Árbol AST
        grafo_ast = generar_arbol_ast(proposicion)
        dibujar_arbol(grafo_ast, f"Árbol AST para: {descripcion}")

    def mostrar_arbol_semantico(self):
        seleccion = self.reglas_listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una regla para generar su Árbol Semántico.")
            return

        descripcion, proposicion = self.proposiciones[seleccion[0]]

        # Extraer variables únicas de la proposición
        variables = extraer_variables(proposicion)

        # Generar y mostrar el Árbol Semántico
        grafo_semantico = generar_arbol_semantico(variables)
        dibujar_arbol(grafo_semantico, f"Árbol Semántico para: {descripcion}")

    def mostrar_arbol_decisiones(self):
        seleccion = self.reglas_listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una regla para generar su Árbol de Decisiones.")
            return

        descripcion, proposicion = self.proposiciones[seleccion[0]]

        # Extraer variables únicas de la proposición
        variables = extraer_variables(proposicion)

        # Generar y mostrar el Árbol de Decisiones
        grafo_decisiones = generar_arbol_decisiones(variables, proposicion)
        dibujar_arbol(grafo_decisiones, f"Árbol de Decisiones para: {descripcion}")

# Inicializar aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
