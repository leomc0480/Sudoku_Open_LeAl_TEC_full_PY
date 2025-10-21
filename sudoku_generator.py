"""
Generador de tableros de Sudoku con diferentes niveles de dificultad
"""

import random
from typing import List, Tuple


class SudokuGenerator:
    """
    Clase para generar tableros de Sudoku válidos

    Utiliza el algoritmo de backtracking para crear tableros completos
    y luego elimina celdas según el nivel de dificultad deseado.

    Atributos:
        size (int): Tamaño del tablero (9x9)
        box_size (int): Tamaño de cada subcuadro (3x3)
    """

    def __init__(self):
        """
        Inicializa el generador de Sudoku

        Args:
            Ninguno

        Returns:
            None
        """
        self.size = 9
        self.box_size = 3

    def generate_complete_board(self) -> List[List[int]]:
        """
        Genera un tablero de Sudoku completamente resuelto

        Crea una matriz 9x9 inicializada en ceros y la llena usando
        el algoritmo de backtracking para garantizar una solución válida.

        Args:
            Ninguno

        Returns:
            List[List[int]]: Tablero 9x9 completamente resuelto con números del 1 al 9
        """
        board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self._fill_board(board)
        return board

    def _fill_board(self, board: List[List[int]]) -> bool:
        """
        Llena el tablero usando backtracking

        Método recursivo que prueba números del 1 al 9 en orden aleatorio
        para cada celda vacía. Si encuentra una celda donde ningún número
        es válido, retrocede (backtrack) y prueba otra opción.

        Args:
            board (List[List[int]]): Tablero 9x9 a llenar (modificado in-place)

        Returns:
            bool: True si se logró llenar todo el tablero, False si no hay solución
        """
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
        """
        Verifica si un número es válido en una posición dada

        Comprueba las tres reglas fundamentales del Sudoku:
        1. No repetir en la fila
        2. No repetir en la columna
        3. No repetir en el subcuadro 3x3

        Args:
            board (List[List[int]]): Tablero actual a validar
            row (int): Fila donde se quiere colocar el número (0-8)
            col (int): Columna donde se quiere colocar el número (0-8)
            num (int): Número a validar (1-9)

        Returns:
            bool: True si el número es válido en esa posición, False en caso contrario
        """
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

        Genera primero un tablero completo válido y luego elimina celdas
        aleatoriamente según el nivel de dificultad seleccionado.

        Args:
            difficulty (str): Nivel de dificultad - 'Fácil', 'Medio', o 'Difícil'
                - Fácil: elimina 35 celdas (~43% vacías)
                - Medio: elimina 45 celdas (~56% vacías)
                - Difícil: elimina 55 celdas (~68% vacías)

        Returns:
            Tuple[List[List[int]], List[List[int]]]: Tupla con dos matrices 9x9:
                - Primera: Tablero del juego con celdas vacías (marcadas con 0)
                - Segunda: Solución completa del tablero
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
        """
        Crea una copia profunda del tablero

        Genera una copia independiente del tablero para evitar modificar
        el original por referencia.

        Args:
            board (List[List[int]]): Tablero original a copiar

        Returns:
            List[List[int]]: Nueva matriz 9x9 con los mismos valores que el original
        """
        return [row[:] for row in board]
