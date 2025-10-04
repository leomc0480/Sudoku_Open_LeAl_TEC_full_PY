"""
Proyecto integrador: Sudoku Juegos Cognitivos
Por: Alonso Osuna Maruri - A01613556
     Leonardo Montoya Chavarría - A01613677

Punto de entrada principal del juego Sudoku
"""

from sudoku_gui import SudokuGUI
import tkinter as tk


def main():
    """Inicializa y ejecuta la aplicación de Sudoku"""
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
