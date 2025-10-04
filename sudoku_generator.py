"""
Generador de tableros de Sudoku con diferentes niveles de dificultad
"""

import random
from typing import List, Tuple


class SudokuGenerator:
    """Clase para generar tableros de Sudoku válidos"""

    def __init__(self):
        self.size = 9
        self.box_size = 3

    def generate_complete_board(self) -> List[List[int]]:
        """Genera un tablero de Sudoku completamente resuelto"""
        board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self._fill_board(board)
        return board

    def _fill_board(self, board: List[List[int]]) -> bool:
        """Llena el tablero usando backtracking"""
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)

                    for num in numbers:
                        if self._is_valid(board, row, col, num):
                            board[row][col] = num

                            if self._fill_board(board):
                                return True

                            board[row][col] = 0

                    return False
        return True

    def _is_valid(self, board: List[List[int]], row: int, col: int, num: int) -> bool:
        """Verifica si un número es válido en una posición dada"""
        # Verificar fila
        if num in board[row]:
            return False

        # Verificar columna
        for r in range(self.size):
            if board[r][col] == num:
                return False

        # Verificar subcuadro 3x3
        start_row = (row // self.box_size) * self.box_size
        start_col = (col // self.box_size) * self.box_size

        for r in range(start_row, start_row + self.box_size):
            for c in range(start_col, start_col + self.box_size):
                if board[r][c] == num:
                    return False

        return True

    def create_puzzle(self, difficulty: str) -> Tuple[List[List[int]], List[List[int]]]:
        """
        Crea un tablero de Sudoku con celdas vacías según la dificultad

        Args:
            difficulty: 'Fácil', 'Medio', o 'Difícil'

        Returns:
            Tupla (tablero_juego, solución_completa)
        """
        # Generar tablero completo (solución)
        solution = self.generate_complete_board()

        # Crear copia para el tablero de juego
        puzzle = [row[:] for row in solution]

        # Determinar número de celdas a eliminar según dificultad
        cells_to_remove = {
            'Fácil': 35,      # ~43% vacías
            'Medio': 45,      # ~56% vacías
            'Difícil': 55     # ~68% vacías
        }

        remove_count = cells_to_remove.get(difficulty, 40)

        # Eliminar celdas aleatoriamente
        positions = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(positions)

        for i in range(remove_count):
            row, col = positions[i]
            puzzle[row][col] = 0

        return puzzle, solution

    def copy_board(self, board: List[List[int]]) -> List[List[int]]:
        """Crea una copia profunda del tablero"""
        return [row[:] for row in board]
