"""
Lógica del juego Sudoku: validación, puntuación y control de estado
"""

import time
from typing import List, Tuple, Optional
from datetime import datetime
import os


class SudokuGame:
    """
    Clase que maneja la lógica del juego Sudoku

    Controla el estado del juego, validaciones, sistema de ayuda,
    temporizador y cálculo de puntuación.

    Atributos:
        size (int): Tamaño del tablero (9x9)
        box_size (int): Tamaño de subcuadro (3x3)
        puzzle (List[List[int]]): Tablero inicial con celdas vacías
        solution (List[List[int]]): Solución correcta del tablero
        current_board (List[List[int]]): Estado actual del tablero
        difficulty (str): Nivel de dificultad seleccionado
        fixed_cells (set): Conjunto de posiciones de celdas fijas (no editables)
        start_time (float): Timestamp del inicio del juego
        errors_count (int): Contador de errores cometidos
        helps_used (int): Contador de ayudas utilizadas
        is_finished (bool): Indica si el juego ha terminado
        time_limits (dict): Límites de tiempo por dificultad en segundos
    """

    def __init__(self, puzzle: List[List[int]], solution: List[List[int]], difficulty: str):
        """
        Inicializa el juego

        Args:
            puzzle (List[List[int]]): Tablero inicial con celdas vacías (0)
            solution (List[List[int]]): Tablero completo correcto
            difficulty (str): Nivel de dificultad ('Fácil', 'Medio', 'Difícil')

        Returns:
            None
        """
        self.size = 9
        self.box_size = 3
        self.puzzle = [row[:] for row in puzzle]
        self.solution = [row[:] for row in solution]
        self.current_board = [row[:] for row in puzzle]
        self.difficulty = difficulty
        self.fixed_cells = self._get_fixed_cells()
        self.start_time = time.time()
        self.errors_count = 0
        self.helps_used = 0
        self.is_finished = False

        # Límites de tiempo por dificultad (en segundos)
        self.time_limits = {
            'Fácil': 1800,    # 30 minutos
            'Medio': 2400,    # 40 minutos
            'Difícil': 3000   # 50 minutos
        }

    def _get_fixed_cells(self) -> set:
        """
        Obtiene las posiciones de las celdas fijas (no editables)

        Recorre el tablero inicial y marca todas las celdas que
        ya tienen un valor como fijas (no editables por el jugador).

        Args:
            Ninguno

        Returns:
            set: Conjunto de tuplas (row, col) con las posiciones fijas
        """
        fixed = set()
        for row in range(self.size):
            for col in range(self.size):
                if self.puzzle[row][col] != 0:
                    fixed.add((row, col))
        return fixed

    def is_cell_fixed(self, row: int, col: int) -> bool:
        """
        Verifica si una celda es fija (no editable)

        Args:
            row (int): Fila de la celda (0-8)
            col (int): Columna de la celda (0-8)

        Returns:
            bool: True si la celda es fija, False si es editable
        """
        return (row, col) in self.fixed_cells

    def set_value(self, row: int, col: int, value: int) -> bool:
        """
        Establece un valor en una celda si es válida

        Intenta colocar un número en la celda especificada. Solo funciona
        si la celda no es fija. El valor 0 borra la celda.

        Args:
            row (int): Fila (0-8)
            col (int): Columna (0-8)
            value (int): Valor a colocar (0-9, donde 0 borra la celda)

        Returns:
            bool: True si se pudo establecer el valor, False si la celda es fija
        """
        if self.is_cell_fixed(row, col):
            return False

        self.current_board[row][col] = value
        return True

    def get_value(self, row: int, col: int) -> int:
        """
        Obtiene el valor actual de una celda

        Args:
            row (int): Fila (0-8)
            col (int): Columna (0-8)

        Returns:
            int: Valor actual en la celda (0-9, donde 0 es vacío)
        """
        return self.current_board[row][col]

    def is_valid_move(self, row: int, col: int, num: int) -> bool:
        """
        Verifica si un número es válido en una posición según las reglas

        Valida que el número no se repita en la fila, columna ni
        en el subcuadro 3x3 correspondiente.

        Args:
            row (int): Fila (0-8)
            col (int): Columna (0-8)
            num (int): Número a validar (1-9)

        Returns:
            bool: True si el movimiento es válido según las reglas de Sudoku,
                  False en caso contrario
        """
        if num < 1 or num > 9:
            return False

        # Crear tablero temporal con el número
        temp_board = [row[:] for row in self.current_board]
        temp_board[row][col] = num

        # Verificar fila
        if temp_board[row].count(num) > 1:
            return False

        # Verificar columna
        col_values = [temp_board[r][col] for r in range(self.size) if temp_board[r][col] != 0]
        if col_values.count(num) > 1:
            return False

        # Verificar subcuadro 3x3
        start_row = (row // self.box_size) * self.box_size
        start_col = (col // self.box_size) * self.box_size

        box_values = []
        for r in range(start_row, start_row + self.box_size):
            for c in range(start_col, start_col + self.box_size):
                if temp_board[r][c] != 0:
                    box_values.append(temp_board[r][c])

        if box_values.count(num) > 1:
            return False

        return True

    def use_help(self, row: int, col: int) -> Optional[int]:
        """
        Proporciona ayuda mostrando el valor correcto de una celda

        Revela el valor correcto de la celda especificada y lo coloca
        automáticamente en el tablero. Incrementa el contador de ayudas
        usadas (con penalización de -10 puntos).

        Args:
            row (int): Fila (0-8)
            col (int): Columna (0-8)

        Returns:
            Optional[int]: El valor correcto (1-9) o None si la celda es fija
        """
        if self.is_cell_fixed(row, col):
            return None

        self.helps_used += 1
        correct_value = self.solution[row][col]
        self.current_board[row][col] = correct_value
        return correct_value

    def check_cell(self, row: int, col: int) -> str:
        """
        Verifica si el valor en una celda es correcto

        Compara el valor actual de la celda con la solución
        y determina su estado.

        Args:
            row (int): Fila (0-8)
            col (int): Columna (0-8)

        Returns:
            str: Estado de la celda - 'correct', 'incorrect', 'empty', o 'fixed'
        """
        if self.is_cell_fixed(row, col):
            return 'fixed'

        current = self.current_board[row][col]

        if current == 0:
            return 'empty'

        if current == self.solution[row][col]:
            return 'correct'
        else:
            return 'incorrect'

    def check_all_cells(self) -> dict:
        """
        Verifica todas las celdas del tablero

        Recorre el tablero completo y clasifica cada celda
        según su estado actual.

        Args:
            Ninguno

        Returns:
            dict: Diccionario con listas de posiciones clasificadas por estado:
                - 'correct': Lista de tuplas (row, col) con celdas correctas
                - 'incorrect': Lista de tuplas (row, col) con celdas incorrectas
                - 'empty': Lista de tuplas (row, col) con celdas vacías
                - 'fixed': Lista de tuplas (row, col) con celdas fijas
        """
        result = {
            'correct': [],
            'incorrect': [],
            'empty': [],
            'fixed': []
        }

        for row in range(self.size):
            for col in range(self.size):
                status = self.check_cell(row, col)
                result[status].append((row, col))

        return result

    def is_complete(self) -> bool:
        """
        Verifica si el tablero está completamente lleno

        Recorre todas las celdas para verificar que no haya
        ninguna vacía (valor 0).

        Args:
            Ninguno

        Returns:
            bool: True si todas las celdas están llenas, False si hay al menos una vacía
        """
        for row in range(self.size):
            for col in range(self.size):
                if self.current_board[row][col] == 0:
                    return False
        return True

    def is_correct(self) -> bool:
        """
        Verifica si el tablero está correcto y completo

        Comprueba que el tablero esté lleno y que todos los valores
        coincidan con la solución.

        Args:
            Ninguno

        Returns:
            bool: True si el tablero está completamente correcto, False en caso contrario
        """
        if not self.is_complete():
            return False

        for row in range(self.size):
            for col in range(self.size):
                if self.current_board[row][col] != self.solution[row][col]:
                    return False

        return True

    def finish_game(self) -> dict:
        """
        Finaliza el juego y calcula la puntuación

        Calcula la puntuación final basándose en:
        - Base: 1000 puntos
        - Bonificación por tiempo: +1 punto cada 5 segundos restantes
        - Penalizaciones: -5 por error, -10 por ayuda, -3 por celda vacía

        Args:
            Ninguno

        Returns:
            dict: Diccionario con información del resultado:
                - 'score' (int): Puntuación final
                - 'time' (float): Tiempo transcurrido en segundos
                - 'errors' (int): Cantidad de celdas incorrectas
                - 'empty' (int): Cantidad de celdas vacías
                - 'helps' (int): Cantidad de ayudas utilizadas
                - 'correct' (bool): True si el tablero está completamente correcto
                - 'time_bonus' (int): Bonificación por tiempo
                - 'error_penalty' (int): Penalización por errores
                - 'help_penalty' (int): Penalización por ayudas
                - 'cell_status' (dict): Estado de todas las celdas
        """
        self.is_finished = True
        elapsed_time = time.time() - self.start_time

        # Verificar estado del tablero
        cell_status = self.check_all_cells()
        incorrect_count = len(cell_status['incorrect'])
        empty_count = len(cell_status['empty'])

        # Calcular puntuación
        base_score = 1000
        time_limit = self.time_limits.get(self.difficulty, 2400)
        time_remaining = max(0, time_limit - elapsed_time)

        # Bonificación por tiempo: +1 punto por cada 5 segundos restantes
        time_bonus = int(time_remaining / 5)

        # Penalizaciones
        error_penalty = incorrect_count * 5
        help_penalty = self.helps_used * 10
        empty_penalty = empty_count * 3

        # Puntuación final
        final_score = base_score + time_bonus - error_penalty - help_penalty - empty_penalty
        final_score = max(0, final_score)  # No negativo

        return {
            'score': final_score,
            'time': elapsed_time,
            'errors': incorrect_count,
            'empty': empty_count,
            'helps': self.helps_used,
            'correct': self.is_correct(),
            'time_bonus': time_bonus,
            'error_penalty': error_penalty,
            'help_penalty': help_penalty,
            'cell_status': cell_status
        }

    def save_statistics_to_file(self, result: dict) -> str:
        """
        Guarda las estadísticas del juego en un archivo de texto

        Crea o actualiza un archivo 'estadisticas_sudoku.txt' con las
        estadísticas de la partida actual, incluyendo fecha, hora,
        dificultad, tiempo, puntuación y detalles del desempeño.

        Args:
            result (dict): Diccionario con estadísticas del juego
                          (resultado de finish_game())

        Returns:
            str: Ruta del archivo donde se guardaron las estadísticas
        """
        # Nombre del archivo de estadísticas
        filename = "estadisticas_sudoku.txt"

        # Obtener fecha y hora actual
        now = datetime.now()
        fecha = now.strftime("%d/%m/%Y")
        hora = now.strftime("%H:%M:%S")

        # Calcular tiempo en formato legible
        minutes = int(result['time'] // 60)
        seconds = int(result['time'] % 60)
        tiempo_formateado = f"{minutes:02d}:{seconds:02d}"

        # Determinar si ganó o no
        estado = "COMPLETADO ✓" if result['correct'] else "INCOMPLETO ✗"

        try:
            # Verificar si el archivo existe para agregar separador
            file_exists = os.path.exists(filename)

            # Abrir archivo en modo append (agregar al final)
            with open(filename, 'a', encoding='utf-8') as file:
                # Si el archivo ya existe, agregar separador
                if file_exists:
                    file.write("\n" + "="*70 + "\n\n")

                # Escribir encabezado de la partida
                file.write("╔════════════════════════════════════════════════════════════════════╗\n")
                file.write("║           ESTADÍSTICAS DE PARTIDA - SUDOKU COGNITIVO               ║\n")
                file.write("╚════════════════════════════════════════════════════════════════════╝\n\n")

                # Información general
                file.write(f"📅 Fecha: {fecha}\n")
                file.write(f"🕐 Hora: {hora}\n")
                file.write(f"📊 Dificultad: {self.difficulty}\n")
                file.write(f"🎮 Estado: {estado}\n")
                file.write(f"⏱️  Tiempo Total: {tiempo_formateado}\n\n")

                # Puntuación
                file.write("─" * 70 + "\n")
                file.write("🏆 PUNTUACIÓN\n")
                file.write("─" * 70 + "\n")
                file.write(f"   Puntuación Final: {result['score']} puntos\n")
                file.write(f"   Puntuación Base: 1000 puntos\n")
                file.write(f"   Bonificación por tiempo: +{result['time_bonus']} puntos\n")
                file.write(f"   Penalización por errores: -{result['error_penalty']} puntos\n")
                file.write(f"   Penalización por ayudas: -{result['help_penalty']} puntos\n\n")

                # Estadísticas detalladas
                file.write("─" * 70 + "\n")
                file.write("📈 ESTADÍSTICAS DETALLADAS\n")
                file.write("─" * 70 + "\n")
                file.write(f"   ✅ Celdas correctas: {len(result['cell_status']['correct'])}/81\n")
                file.write(f"   ❌ Celdas incorrectas: {result['errors']}\n")
                file.write(f"   ⬜ Celdas vacías: {result['empty']}\n")
                file.write(f"   💡 Ayudas utilizadas: {result['helps']}\n\n")

                # Cálculo de porcentaje de completitud
                total_celdas = 81
                celdas_llenas = total_celdas - result['empty']
                porcentaje_completitud = (celdas_llenas / total_celdas) * 100

                # Cálculo de precisión (de las celdas llenas, cuántas son correctas)
                if celdas_llenas > 0:
                    celdas_correctas = len(result['cell_status']['correct'])
                    porcentaje_precision = (celdas_correctas / celdas_llenas) * 100
                else:
                    porcentaje_precision = 0

                file.write("─" * 70 + "\n")
                file.write("📊 ANÁLISIS DE DESEMPEÑO\n")
                file.write("─" * 70 + "\n")
                file.write(f"   Completitud: {porcentaje_completitud:.1f}%\n")
                file.write(f"   Precisión: {porcentaje_precision:.1f}%\n")

                # Evaluación del desempeño
                if result['correct']:
                    desempeño = "¡EXCELENTE! ⭐⭐⭐"
                elif porcentaje_precision >= 90:
                    desempeño = "MUY BUENO ⭐⭐"
                elif porcentaje_precision >= 70:
                    desempeño = "BUENO ⭐"
                else:
                    desempeño = "NECESITA MEJORAR"

                file.write(f"   Evaluación: {desempeño}\n\n")

            return os.path.abspath(filename)

        except Exception as e:
            print(f"Error al guardar estadísticas: {e}")
            return ""

    def get_elapsed_time(self) -> float:
        """
        Obtiene el tiempo transcurrido desde el inicio

        Args:
            Ninguno

        Returns:
            float: Tiempo transcurrido en segundos desde el inicio del juego
        """
        return time.time() - self.start_time

    def reset_game(self):
        """
        Reinicia el juego al estado inicial

        Restaura el tablero al estado inicial, reinicia el temporizador
        y resetea todos los contadores.

        Args:
            Ninguno

        Returns:
            None
        """
        self.current_board = [row[:] for row in self.puzzle]
        self.start_time = time.time()
        self.errors_count = 0
        self.helps_used = 0
        self.is_finished = False
