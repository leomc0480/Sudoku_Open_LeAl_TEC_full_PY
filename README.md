# Sudoku - Juego Cognitivo

**Proyecto integrador: Sudoku Juegos Cognitivos**
Por: Alonso Osuna Maruri - A01613556
Leonardo Montoya Chavarría - A01613677

## Descripción

El Sudoku es un juego que estimula la mente al combinar memoria de trabajo, razonamiento lógico, atención sostenida y toma de decisiones. Este programa permite resolver tableros de Sudoku de diferentes dificultades con una interfaz gráfica moderna desarrollada 100% en Python.

## Características

- **3 Niveles de Dificultad**: Fácil, Medio y Difícil
- **Interfaz Gráfica Moderna**: Diseño atractivo con Tkinter
- **Temporizador**: Seguimiento del tiempo de juego
- **Sistema de Ayudas**: Opción para revelar valores correctos
- **Verificación en Tiempo Real**: Comprueba tu progreso
- **Sistema de Puntuación**: Basado en precisión, tiempo y ayudas
- **Retroalimentación Visual**: Colores para celdas correctas/incorrectas

## Reglas del Juego

1. Completar la matriz 9x9 con dígitos del 1 al 9
2. Sin repetir números en:
   - Ninguna fila
   - Ninguna columna
   - Ningún subcuadro 3x3

## Cómo Ejecutar

### Requisitos
- Python 3.7 o superior
- Tkinter (incluido con Python estándar)

### Ejecución
```bash
python main.py
```

## Estructura del Proyecto

```
Proyect_Sudoku_py/
│
├── main.py                 # Punto de entrada de la aplicación
├── sudoku_generator.py     # Generación de tableros
├── sudoku_game.py         # Lógica del juego
├── sudoku_gui.py          # Interfaz gráfica
└── README.md              # Este archivo
```

## Cómo Jugar

1. **Seleccionar Dificultad**: Al iniciar, elige entre Fácil, Medio o Difícil
2. **Ingresar Números**:
   - Haz clic en una celda vacía
   - Usa el teclado numérico o los botones en pantalla
   - Escribe un número del 1 al 9
3. **Ayuda (Opcional)**:
   - Activa el modo ayuda
   - Haz clic en una celda para ver el valor correcto
   - Penalización: -10 puntos por ayuda
4. **Verificar**: Comprueba tu progreso en cualquier momento
5. **Finalizar**: Cuando termines, presiona "Finalizar" para ver tu puntuación

## Sistema de Puntuación

- **Base**: 1000 puntos
- **Bonificación por tiempo**: +1 punto cada 5 segundos restantes
- **Penalizaciones**:
  - -5 puntos por celda incorrecta
  - -10 puntos por cada ayuda usada
  - -3 puntos por celda vacía

## Características Visuales

- **Colores**:
  - Verde: Celdas correctas
  - Rojo: Celdas incorrectas
  - Gris oscuro: Celdas fijas
  - Gris claro: Celdas editables

## Tecnologías Utilizadas

- **Python 3**: Lenguaje de programación principal
- **Tkinter**: Biblioteca estándar de Python para interfaz gráfica
- **Algoritmo de Backtracking**: Generación de tableros válidos
- **Validación en Tiempo Real**: Verificación de reglas de Sudoku

## Arquitectura del Código

El proyecto está desarrollado 100% en Python puro, sin dependencias externas más allá de la biblioteca estándar.

### `sudoku_generator.py`
**Clase SudokuGenerator**: Responsable de crear tableros válidos de Sudoku.

- `generate_complete_board()`: Genera un tablero 9x9 completamente resuelto
- `_fill_board()`: Usa algoritmo de backtracking recursivo para llenar el tablero
- `_is_valid()`: Valida si un número cumple las reglas de Sudoku (fila, columna, subcuadro 3x3)
- `create_puzzle()`: Crea un puzzle eliminando celdas según dificultad:
  - Fácil: 35 celdas vacías (~43%)
  - Medio: 45 celdas vacías (~56%)
  - Difícil: 55 celdas vacías (~68%)

**Algoritmo de Backtracking**:
```
Para cada celda vacía:
  1. Probar números del 1-9 en orden aleatorio
  2. Si el número es válido, colocarlo y continuar
  3. Si se llena todo el tablero, éxito
  4. Si no hay solución, retroceder y probar otro número
```

### `sudoku_game.py`
**Clase SudokuGame**: Maneja la lógica del juego y las reglas.

**Atributos principales**:
- `puzzle`: Tablero inicial con celdas vacías
- `solution`: Solución completa del tablero
- `current_board`: Estado actual del juego
- `fixed_cells`: Set de posiciones no editables
- `start_time`: Tiempo de inicio para el temporizador

**Métodos clave**:
- `is_valid_move()`: Verifica si un número es válido según reglas de Sudoku
  - Comprueba fila: no repetir número
  - Comprueba columna: no repetir número
  - Comprueba subcuadro 3x3: no repetir número
- `set_value()`: Coloca un número en una celda si es editable
- `use_help()`: Muestra el valor correcto (con penalización)
- `check_cell()`: Retorna el estado de una celda (correct/incorrect/empty/fixed)
- `finish_game()`: Calcula puntuación final con bonificaciones y penalizaciones
- `is_complete()`: Verifica si el tablero está lleno
- `is_correct()`: Verifica si el tablero es correcto

**Sistema de puntuación implementado**:
```
puntuación_final = 1000 (base)
                 + (tiempo_restante / 5) (bonificación)
                 - (errores * 5) (penalización)
                 - (ayudas * 10) (penalización)
                 - (vacías * 3) (penalización)
```

### `sudoku_gui.py`
**Clase SudokuGUI**: Interfaz gráfica completa con Tkinter.

**Componentes principales**:

1. **Pantalla de inicio** (`_show_start_screen()`):
   - Título y autores
   - Botones de selección de dificultad
   - Diseño con colores modernos

2. **Tablero de juego** (`_create_board()`):
   - Matriz 9x9 de widgets Entry
   - Bordes gruesos cada 3 celdas (subcuadros)
   - Colores diferenciados para celdas fijas/editables
   - Sistema de eventos de teclado y mouse

3. **Panel superior** (`_create_top_panel()`):
   - Temporizador en tiempo real
   - Indicador de dificultad
   - Contador de ayudas usadas

4. **Teclado numérico** (`_create_number_pad()`):
   - Botones del 1 al 9
   - Botón de borrar
   - Inserción de valores en celda seleccionada

5. **Panel de control** (`_create_control_panel()`):
   - Botón de ayuda (modo toggle)
   - Botón de verificación
   - Botón de finalizar
   - Botón de nuevo juego

**Manejo de eventos**:
- `_on_cell_select()`: Selecciona celda y aplica ayuda si está activa
- `_on_key_press()`: Captura entrada de teclado (solo dígitos 1-9, borrar)
- `_insert_number()`: Inserta número desde teclado numérico visual
- `_update_cell_color()`: Actualiza color de celda según estado
- `_verify_board()`: Colorea todas las celdas según corrección
- `_finish_game()`: Muestra resultados detallados

**Sistema de colores**:
```python
colors = {
    'bg': '#1e1e2e',           # Fondo principal
    'fg': '#cdd6f4',           # Texto
    'fixed': '#45475a',        # Celdas fijas
    'editable': '#313244',     # Celdas editables
    'selected': '#f5c2e7',     # Selección
    'correct': '#a6e3a1',      # Correctas
    'incorrect': '#f38ba8',    # Incorrectas
    'button': '#89b4fa',       # Botones
}
```

**Temporizador**:
- Actualización cada 1000ms (1 segundo)
- Formato MM:SS
- Método recursivo con `after()`

### `main.py`
Punto de entrada simple que inicializa la aplicación:
```python
def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
```

## Flujo de Ejecución

1. **Inicio**: `main.py` crea ventana Tkinter e instancia `SudokuGUI`
2. **Selección**: Usuario elige dificultad en pantalla de inicio
3. **Generación**: `SudokuGenerator` crea puzzle y solución
4. **Juego**: `SudokuGame` inicializa lógica y temporizador
5. **Interfaz**: `SudokuGUI` renderiza tablero y controles
6. **Interacción**: Usuario ingresa números, usa ayudas, verifica
7. **Finalización**: Sistema calcula puntuación y muestra resultados
8. **Reinicio**: Opción de nuevo juego vuelve a pantalla de inicio

## Uso de Estructuras de Programación

### Decisiones (if/elif/else)
- Validación de números en reglas de Sudoku
- Verificación de celdas fijas vs editables
- Evaluación de estado del juego (correcto/incorrecto)
- Determinación de dificultad y celdas a eliminar

### Repeticiones (for/while)
- Recorrido de matriz 9x9 para validaciones
- Iteración de subcuadros 3x3
- Bucle de backtracking para generar tablero
- Actualización periódica del temporizador

### Funciones
- Modularización en múltiples archivos
- Funciones específicas para cada responsabilidad
- Reutilización de código de validación

### Matrices (Listas de listas)
- Representación del tablero: `List[List[int]]`
- Operaciones por índices `[row][col]`
- Copia profunda de tableros para evitar referencias

## Beneficios Cognitivos

- **Memoria de Trabajo**: Recordar números colocados
- **Razonamiento Lógico**: Deducir valores correctos
- **Atención Sostenida**: Concentración prolongada
- **Toma de Decisiones**: Elegir estrategias óptimas

## Referencias y Recursos

El código de este proyecto fue desarrollado desde cero específicamente para este proyecto académico. Sin embargo, se utilizaron conceptos y algoritmos estándar de la literatura de programación:

### Algoritmo de Backtracking
El algoritmo de backtracking para generar y resolver Sudoku es un método clásico en ciencias de la computación. Referencias útiles:

- **Backtracking Algorithm** - GeeksforGeeks: https://www.geeksforgeeks.org/backtracking-algorithms/
- **Sudoku Solver using Backtracking** - GeeksforGeeks: https://www.geeksforgeeks.org/sudoku-backtracking-7/
- **Backtracking** - Wikipedia: https://en.wikipedia.org/wiki/Backtracking
- **Backtracking Video** - YouTube: https://youtu.be/ip2jC_kXGtg?si=JzJV8Ftp98UbxbGn

### Tkinter (Interfaz Gráfica)
Documentación oficial de Python para Tkinter:

- **Tkinter Documentation** - Python Official Docs: https://docs.python.org/3/library/tkinter.html
- **Tkinter Tutorial** - Real Python: https://realpython.com/python-gui-tkinter/

### Conceptos de Sudoku
- **Sudoku** - Wikipedia: https://es.wikipedia.org/wiki/Sudoku
- Reglas y estrategias del juego Sudoku

## Licencia

Proyecto académico desarrollado para el curso de Pensamiento Computacional para Ingeniería.

---

by Leonado Montoya Chavarria - A01613677
& Alonso Osuna Maruri - A01613556

---

¡Disfruta del juego y ejercita tu mente!
