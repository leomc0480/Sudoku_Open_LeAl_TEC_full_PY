"""
Proyecto integrador: Sudoku Juegos Cognitivos
Por: Alonso Osuna Maruri - A01613556
     Leonardo Montoya Chavarría - A01613677

Punto de entrada principal del juego Sudoku
"""

from sudoku_gui import SudokuGUI
import tkinter as tk


def main():
    """
    Inicializa y ejecuta la aplicación de Sudoku

    Crea la ventana principal de Tkinter, instancia la interfaz gráfica
    y ejecuta el bucle principal de eventos de la aplicación.

    Args:
        Ninguno

    Returns:
        None
    """
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
