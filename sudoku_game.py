"""
Lógica del juego Sudoku: validación, puntuación y control de estado
"""

import time
from typing import List, Tuple, Optional


class SudokuGame:
    """Clase que maneja la lógica del juego Sudoku"""

    def __init__(self, puzzle: List[List[int]], solution: List[List[int]], difficulty: str):
        """
        Inicializa el juego

        Args:
            puzzle: Tablero inicial con celdas vacías (0)
            solution: Tablero completo correcto
            difficulty: Nivel de dificultad
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
        """Obtiene las posiciones de las celdas fijas (no editables)"""
        fixed = set()
        for row in range(self.size):
            for col in range(self.size):
                if self.puzzle[row][col] != 0:
                    fixed.add((row, col))
        return fixed

    def is_cell_fixed(self, row: int, col: int) -> bool:
        """Verifica si una celda es fija (no editable)"""
        return (row, col) in self.fixed_cells

    def set_value(self, row: int, col: int, value: int) -> bool:
        """
        Establece un valor en una celda si es válida

        Args:
            row: Fila (0-8)
            col: Columna (0-8)
            value: Valor a colocar (0-9, donde 0 borra la celda)

        Returns:
            True si se pudo establecer el valor, False si la celda es fija
        """
        if self.is_cell_fixed(row, col):
            return False

        self.current_board[row][col] = value
        return True

    def get_value(self, row: int, col: int) -> int:
        """Obtiene el valor actual de una celda"""
        return self.current_board[row][col]

    def is_valid_move(self, row: int, col: int, num: int) -> bool:
        """
        Verifica si un número es válido en una posición según las reglas

        Args:
            row: Fila (0-8)
            col: Columna (0-8)
            num: Número a validar (1-9)

        Returns:
            True si el movimiento es válido según las reglas de Sudoku
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

        Args:
            row: Fila (0-8)
            col: Columna (0-8)

        Returns:
            El valor correcto o None si la celda es fija
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

        Args:
            row: Fila (0-8)
            col: Columna (0-8)

        Returns:
            'correct', 'incorrect', 'empty', o 'fixed'
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

        Returns:
            Diccionario con posiciones clasificadas por estado
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
        """Verifica si el tablero está completamente lleno"""
        for row in range(self.size):
            for col in range(self.size):
                if self.current_board[row][col] == 0:
                    return False
        return True

    def is_correct(self) -> bool:
        """Verifica si el tablero está correcto y completo"""
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

        Returns:
            Diccionario con información del resultado
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

    def get_elapsed_time(self) -> float:
        """Obtiene el tiempo transcurrido desde el inicio"""
        return time.time() - self.start_time

    def reset_game(self):
        """Reinicia el juego al estado inicial"""
        self.current_board = [row[:] for row in self.puzzle]
        self.start_time = time.time()
        self.errors_count = 0
        self.helps_used = 0
        self.is_finished = False
