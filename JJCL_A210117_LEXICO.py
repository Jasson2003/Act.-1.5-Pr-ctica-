import tkinter as tk
from tkinter import ttk
import ply.lex as lex

def analizar(event=None):
    datos = entry1.get("1.0", tk.END)
    lineas = datos.split('\n')  # Dividir los datos en líneas
    resultado_texto.config(state=tk.NORMAL)
    palabras_mostradas = set()  # Conjunto para almacenar las palabras ya mostradas
    for num_linea, linea in enumerate(lineas, start=1):  # Iterar sobre cada línea con su número correspondiente
        ci = ingreso(linea)  # Analizar la línea actual
        for estado in ci:  # Mostrar cada estado analizado de la línea
            palabra = estado.split()[3]  # Extraer la palabra (cuarta palabra en cada estado)
            if palabra == "lenght":
                continue
            if palabra in ["arreglo", ";", "int", "i"] and palabra in palabras_mostradas:
                continue  # Si ya se mostró esta palabra, omítela
            palabras_mostradas.add(palabra)  # Agrega la palabra al conjunto de palabras mostradas
            resultado_texto.insert(tk.END, f"Línea--> {num_linea}, {estado}\n")
    resultado_texto.config(state=tk.DISABLED)

def eliminar():
    resultado_texto.config(state=tk.NORMAL)
    resultado_texto.delete('1.0', tk.END)
    resultado_texto.config(state=tk.DISABLED)

tokens = ['ID', 'STATIC', 'VOID', 'BURBUJA', 'ARREGLO', 'ITERADOR', 'IZQPARENT', 'DERPARENT', 'IZQCORCHET', 'DERCORCHET', 'LLAVEIZQ', 'LLAVEDER', 'INCREMENT', 'INT', 'IGUAL', 'PUNTOCOMA', 'FOR', 'MENORQUE', 'MAYORQUE', 'MAS', 'MENOS', 'UNION', 'DIGIT']

palabras_reservadas = {
    'static': 'STATIC',
    'void': 'VOID',
    'burbuja': 'BURBUJA',
    'arreglo':'ARREGLO',
    'i': 'ITERADOR',
    'for':'FOR',
    '(': 'IZQPARENT',
    ')': 'DERPARENT',
    '{': 'IZQCORCHET',
    '}': 'DERCORCHET',
    '[': 'LLAVEIZQ',
    ']':'LLAVEDER',
    '++':'INCREMENT',
    'int': 'INT',
    '=': 'IGUAL',
    ';': 'PUNTOCOMA',
    '.':'UNION'
}

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = palabras_reservadas.get(t.value, 'ID')
    return t

#regex tokens
t_INT = r'int'
t_IGUAL = r'='
t_MAS= r'\+'
t_MENOS = r'\-'
t_PUNTOCOMA = r';'
t_INCREMENT = r'\++'
t_MENORQUE = r'\<'
t_MAYORQUE = r'\>'
t_DIGIT = r'\d+'
t_UNION = r'\.'
#paréntesis
t_IZQPARENT = r'\('
t_DERPARENT = r'\)'
#corchete
t_IZQCORCHET = r'\{'
t_DERCORCHET = r'\}'
#llaves
t_LLAVEIZQ = r'\['
t_LLAVEDER = r'\]'
#ignore espacios en blanco
def t_WHITESPACE(t):
    r'[\t]+'
    pass
t_ignore = ' \t'

def t_error(t):
    #print(f"Carácter ilegal: {t.value[0]} en la línea {t.lineno}")
    t.lexer.skip(1)

def error(datos):
    return [f'no definido: {datos}']

def ingreso(datos):

    if len(datos) < 1:
        return ['Cadena inválida: La cadena está vacía.']

    token = lex.lex()  # Definir el objeto token aquí
    token.input(datos)
    lexer = []
    es_valido = True

    for toke in token:
        if toke.type == 'ID':
            es_valido = es_valido and (toke.value in palabras_reservadas or toke.value.isdigit())
            categoria = 'Identificador'
        elif toke.type in ['STATIC', 'VOID', 'BURBUJA', 'ARREGLO', 'ITERADOR']:
            categoria = 'Identificador'
        elif toke.type in ['MENORQUE', 'MAYORQUE', 'MAS', 'MENOS', 'UNION']:
            categoria = 'Operadores'
        elif toke.type == 'IZQPARENT':
            categoria = 'Paréntesis de apertura'
        elif toke.type == 'DERPARENT':
            categoria = 'Paréntesis de cierre'
        elif toke.type == 'IZQCORCHET':
            categoria = 'Corchete de apertura'
        elif toke.type == 'DERCORCHET':
            categoria = 'Corchete de cierre'
        elif toke.type == 'LLAVEIZQ':
            categoria = 'Llave de apertura'
        elif toke.type == 'LLAVEDER':
            categoria = 'Llave de cierre'
        elif toke.type == 'DIGIT':
            categoria = 'Integrador'
        else:
            es_valido = es_valido and toke.type in palabras_reservadas.values()
            if toke.type == 'FOR':
                categoria = 'Reservada while'
            elif toke.type == 'INT':
                categoria = 'Tipo de dato'
            elif toke.type == 'IGUAL':
                categoria = 'Operador'
            elif toke.type == 'PUNTOCOMA':
                categoria = 'Punto y coma'
            elif toke.type == 'INCREMENT':
                categoria = 'Operador Incremento'
            else:
                categoria = 'No clasificado'

        estado = "Valor: {:16} Categoría: {:16}".format(
            str(toke.value), categoria)
        lexer.append(estado)

    return lexer

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Analizador léxico")
ventana.geometry("1000x800")  

# Estilos para los widgets
ventana.style = ttk.Style()
ventana.style.configure('Green.TButton', background='green')
ventana.style.configure('Red.TButton', background='red')
ventana.style.configure('Frame.TFrame', background='white')  # Establecer color de fondo para el marco

frame = ttk.Frame(ventana, padding=(50, 50, 50, 50), style='Frame.TFrame')  
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

entry1 = tk.Text(frame, height=5, width=100)
entry1.grid(column=0, row=0, padx=30, pady=30)
entry1.configure(bg='orange')  
resultado_texto = tk.Text(frame, height=25, width=100, state=tk.DISABLED) 
resultado_texto.grid(column=0, row=1, padx=10, pady=10)
resultado_texto.configure(bg='orange')  

boton_analizar = ttk.Button(frame, text="Analizar", command=analizar, style='Green.TButton')  
boton_analizar.grid(column=0, row=2, pady=20, sticky=tk.N+tk.S+tk.W+tk.E)

boton_limpiar = ttk.Button(frame, text="Limpiar", command=eliminar, style='Red.TButton')  
boton_limpiar.grid(column=0, row=3, pady=20, sticky=tk.N+tk.S+tk.W+tk.E)

ventana.mainloop()
