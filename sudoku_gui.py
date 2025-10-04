"""
Interfaz gráfica de usuario para el juego Sudoku usando Tkinter
"""

import tkinter as tk
from tkinter import messagebox, ttk
from sudoku_generator import SudokuGenerator
from sudoku_game import SudokuGame
from typing import List, Optional
import time


class SudokuGUI:
    """Interfaz gráfica principal del juego Sudoku"""

    def __init__(self, master):
        self.master = master
        self.master.title("🎮 Sudoku - Juego Cognitivo")
        self.master.resizable(False, False)

        # Colores modernos
        self.colors = {
            'bg': '#1e1e2e',
            'fg': '#cdd6f4',
            'fixed': '#45475a',
            'editable': '#313244',
            'selected': '#f5c2e7',
            'correct': '#a6e3a1',
            'incorrect': '#f38ba8',
            'empty': '#313244',
            'grid_line': '#585b70',
            'button': '#89b4fa',
            'button_hover': '#74c7ec',
            'panel': '#181825'
        }

        # Variables del juego
        self.generator = SudokuGenerator()
        self.game: Optional[SudokuGame] = None
        self.cells: List[List[tk.Entry]] = []
        self.selected_cell: Optional[tuple] = None
        self.help_mode = False
        self.timer_running = False

        # Configurar estilo
        self._configure_styles()

        # Mostrar pantalla de inicio
        self._show_start_screen()

    def _configure_styles(self):
        """Configura los estilos de la aplicación"""
        self.master.configure(bg=self.colors['bg'])

        style = ttk.Style()
        style.theme_use('clam')

        # Estilo de botones
        style.configure('Game.TButton',
                        background=self.colors['button'],
                        foreground='#1e1e2e',
                        borderwidth=0,
                        focuscolor='none',
                        font=('Segoe UI', 10, 'bold'),
                        padding=10)

        style.map('Game.TButton',
                  background=[('active', self.colors['button_hover'])])

    def _show_start_screen(self):
        """Muestra la pantalla de inicio con selección de dificultad"""
        self.start_frame = tk.Frame(self.master, bg=self.colors['bg'])
        self.start_frame.pack(padx=40, pady=40)

        # Título
        title = tk.Label(self.start_frame,
                         text="🎮 SUDOKU",
                         font=('Segoe UI', 36, 'bold'),
                         bg=self.colors['bg'],
                         fg=self.colors['button'])
        title.pack(pady=(0, 10))

        subtitle = tk.Label(self.start_frame,
                            text="Juego Cognitivo",
                            font=('Segoe UI', 14),
                            bg=self.colors['bg'],
                            fg=self.colors['fg'])
        subtitle.pack(pady=(0, 30))

        # Autores
        authors = tk.Label(self.start_frame,
                          text="Por: Alonso Osuna Maruri - A01613556\nLeonardo Montoya Chavarría - A01613677",
                          font=('Segoe UI', 9),
                          bg=self.colors['bg'],
                          fg=self.colors['fixed'],
                          justify='center')
        authors.pack(pady=(0, 30))

        # Instrucciones
        instructions = tk.Label(self.start_frame,
                                text="Selecciona el nivel de dificultad:",
                                font=('Segoe UI', 12),
                                bg=self.colors['bg'],
                                fg=self.colors['fg'])
        instructions.pack(pady=(0, 20))

        # Botones de dificultad
        difficulties = [
            ('🟢 Fácil', 'Fácil', '#a6e3a1'),
            ('🟡 Medio', 'Medio', '#f9e2af'),
            ('🔴 Difícil', 'Difícil', '#f38ba8')
        ]

        for label, diff, color in difficulties:
            btn = tk.Button(self.start_frame,
                           text=label,
                           font=('Segoe UI', 14, 'bold'),
                           bg=color,
                           fg='#1e1e2e',
                           activebackground=color,
                           activeforeground='#1e1e2e',
                           bd=0,
                           padx=40,
                           pady=15,
                           cursor='hand2',
                           command=lambda d=diff: self._start_game(d))
            btn.pack(pady=8, fill='x')

    def _start_game(self, difficulty: str):
        """Inicia un nuevo juego con la dificultad seleccionada"""
        # Destruir pantalla de inicio
        self.start_frame.destroy()

        # Generar tablero
        puzzle, solution = self.generator.create_puzzle(difficulty)
        self.game = SudokuGame(puzzle, solution, difficulty)

        # Crear interfaz de juego
        self._create_game_interface()

        # Iniciar temporizador
        self._start_timer()

    def _create_game_interface(self):
        """Crea la interfaz principal del juego"""
        # Frame principal
        main_frame = tk.Frame(self.master, bg=self.colors['bg'])
        main_frame.pack(padx=20, pady=20)

        # Panel superior (info y controles)
        self._create_top_panel(main_frame)

        # Tablero de Sudoku
        self._create_board(main_frame)

        # Panel inferior (teclado numérico)
        self._create_number_pad(main_frame)

        # Panel de control
        self._create_control_panel(main_frame)

    def _create_top_panel(self, parent):
        """Crea el panel superior con información del juego"""
        top_panel = tk.Frame(parent, bg=self.colors['panel'], bd=2, relief='flat')
        top_panel.pack(fill='x', pady=(0, 15))

        # Temporizador
        timer_frame = tk.Frame(top_panel, bg=self.colors['panel'])
        timer_frame.pack(side='left', padx=15, pady=10)

        tk.Label(timer_frame,
                 text="⏱️ Tiempo:",
                 font=('Segoe UI', 10),
                 bg=self.colors['panel'],
                 fg=self.colors['fg']).pack(side='left')

        self.timer_label = tk.Label(timer_frame,
                                     text="00:00",
                                     font=('Segoe UI', 12, 'bold'),
                                     bg=self.colors['panel'],
                                     fg=self.colors['button'])
        self.timer_label.pack(side='left', padx=5)

        # Dificultad
        diff_frame = tk.Frame(top_panel, bg=self.colors['panel'])
        diff_frame.pack(side='left', padx=15, pady=10)

        tk.Label(diff_frame,
                 text="📊 Nivel:",
                 font=('Segoe UI', 10),
                 bg=self.colors['panel'],
                 fg=self.colors['fg']).pack(side='left')

        self.diff_label = tk.Label(diff_frame,
                                    text=self.game.difficulty,
                                    font=('Segoe UI', 12, 'bold'),
                                    bg=self.colors['panel'],
                                    fg=self.colors['selected'])
        self.diff_label.pack(side='left', padx=5)

        # Ayudas usadas
        help_frame = tk.Frame(top_panel, bg=self.colors['panel'])
        help_frame.pack(side='right', padx=15, pady=10)

        tk.Label(help_frame,
                 text="💡 Ayudas:",
                 font=('Segoe UI', 10),
                 bg=self.colors['panel'],
                 fg=self.colors['fg']).pack(side='left')

        self.help_label = tk.Label(help_frame,
                                    text="0",
                                    font=('Segoe UI', 12, 'bold'),
                                    bg=self.colors['panel'],
                                    fg=self.colors['incorrect'])
        self.help_label.pack(side='left', padx=5)

    def _create_board(self, parent):
        """Crea el tablero de Sudoku 9x9"""
        board_frame = tk.Frame(parent, bg=self.colors['grid_line'], bd=3)
        board_frame.pack(pady=10)

        self.cells = []

        for row in range(9):
            row_cells = []
            for col in range(9):
                # Frame de celda con borde para las subcuadrículas
                cell_frame = tk.Frame(board_frame,
                                      bg=self.colors['grid_line'],
                                      highlightthickness=0)

                # Añadir bordes más gruesos cada 3 celdas
                padx = (3 if col % 3 == 0 else 1, 3 if col % 3 == 2 else 1)
                pady = (3 if row % 3 == 0 else 1, 3 if row % 3 == 2 else 1)

                cell_frame.grid(row=row, column=col, padx=padx, pady=pady)

                # Determinar si es celda fija
                is_fixed = self.game.is_cell_fixed(row, col)
                value = self.game.get_value(row, col)

                # Crear Entry
                cell = tk.Entry(cell_frame,
                               width=2,
                               font=('Segoe UI', 20, 'bold'),
                               justify='center',
                               bg=self.colors['fixed'] if is_fixed else self.colors['editable'],
                               fg=self.colors['fg'],
                               disabledbackground=self.colors['fixed'],
                               disabledforeground=self.colors['fg'],
                               bd=0,
                               highlightthickness=2,
                               highlightcolor=self.colors['selected'],
                               highlightbackground=self.colors['grid_line'])

                # Si es celda fija, mostrar valor y deshabilitar
                if is_fixed:
                    cell.insert(0, str(value))
                    cell.config(state='disabled')

                # Eventos
                cell.bind('<FocusIn>', lambda e, r=row, c=col: self._on_cell_select(r, c))
                cell.bind('<Key>', lambda e, r=row, c=col: self._on_key_press(e, r, c))

                cell.pack(padx=2, pady=2)
                row_cells.append(cell)

            self.cells.append(row_cells)

    def _create_number_pad(self, parent):
        """Crea el teclado numérico"""
        pad_frame = tk.Frame(parent, bg=self.colors['bg'])
        pad_frame.pack(pady=15)

        tk.Label(pad_frame,
                 text="Teclado Numérico:",
                 font=('Segoe UI', 10),
                 bg=self.colors['bg'],
                 fg=self.colors['fg']).pack()

        numbers_frame = tk.Frame(pad_frame, bg=self.colors['bg'])
        numbers_frame.pack(pady=10)

        # Botones del 1 al 9
        for i in range(1, 10):
            btn = tk.Button(numbers_frame,
                           text=str(i),
                           font=('Segoe UI', 14, 'bold'),
                           width=3,
                           bg=self.colors['button'],
                           fg='#1e1e2e',
                           activebackground=self.colors['button_hover'],
                           bd=0,
                           cursor='hand2',
                           command=lambda n=i: self._insert_number(n))

            row = (i - 1) // 3
            col = (i - 1) % 3
            btn.grid(row=row, column=col, padx=3, pady=3)

        # Botón borrar
        clear_btn = tk.Button(numbers_frame,
                             text="🗑️ Borrar",
                             font=('Segoe UI', 12, 'bold'),
                             bg=self.colors['incorrect'],
                             fg='#1e1e2e',
                             activebackground='#eba0ac',
                             bd=0,
                             cursor='hand2',
                             command=self._clear_cell)
        clear_btn.grid(row=3, column=0, columnspan=3, padx=3, pady=3, sticky='ew')

    def _create_control_panel(self, parent):
        """Crea el panel de control con botones de acción"""
        control_frame = tk.Frame(parent, bg=self.colors['bg'])
        control_frame.pack(pady=15, fill='x')

        # Botón de ayuda
        self.help_btn = tk.Button(control_frame,
                                  text="💡 Activar Ayuda",
                                  font=('Segoe UI', 11, 'bold'),
                                  bg='#f9e2af',
                                  fg='#1e1e2e',
                                  activebackground='#f5e0a5',
                                  bd=0,
                                  cursor='hand2',
                                  command=self._toggle_help_mode)
        self.help_btn.pack(side='left', padx=5, fill='x', expand=True)

        # Botón verificar
        verify_btn = tk.Button(control_frame,
                              text="🔍 Verificar",
                              font=('Segoe UI', 11, 'bold'),
                              bg=self.colors['button'],
                              fg='#1e1e2e',
                              activebackground=self.colors['button_hover'],
                              bd=0,
                              cursor='hand2',
                              command=self._verify_board)
        verify_btn.pack(side='left', padx=5, fill='x', expand=True)

        # Botón finalizar
        finish_btn = tk.Button(control_frame,
                              text="✅ Finalizar",
                              font=('Segoe UI', 11, 'bold'),
                              bg=self.colors['correct'],
                              fg='#1e1e2e',
                              activebackground='#94e2d5',
                              bd=0,
                              cursor='hand2',
                              command=self._finish_game)
        finish_btn.pack(side='left', padx=5, fill='x', expand=True)

        # Botón nuevo juego
        new_btn = tk.Button(control_frame,
                           text="🔄 Nuevo Juego",
                           font=('Segoe UI', 11, 'bold'),
                           bg=self.colors['selected'],
                           fg='#1e1e2e',
                           activebackground='#f2cdcd',
                           bd=0,
                           cursor='hand2',
                           command=self._new_game)
        new_btn.pack(side='left', padx=5, fill='x', expand=True)

    def _on_cell_select(self, row: int, col: int):
        """Maneja la selección de una celda"""
        if self.game.is_cell_fixed(row, col):
            return

        self.selected_cell = (row, col)

        # Si el modo ayuda está activo, aplicar ayuda
        if self.help_mode:
            self._apply_help(row, col)
            self.help_mode = False
            self.help_btn.config(text="💡 Activar Ayuda", bg='#f9e2af')

    def _on_key_press(self, event, row: int, col: int):
        """Maneja las pulsaciones de teclas en las celdas"""
        if self.game.is_cell_fixed(row, col):
            return 'break'

        # Solo permitir números del 1-9 y teclas de control
        if event.char.isdigit() and event.char != '0':
            # Limpiar celda antes de insertar
            self.cells[row][col].delete(0, tk.END)
            self.cells[row][col].insert(0, event.char)
            self.game.set_value(row, col, int(event.char))
            self._update_cell_color(row, col)
            return 'break'
        elif event.keysym in ['BackSpace', 'Delete']:
            self.cells[row][col].delete(0, tk.END)
            self.game.set_value(row, col, 0)
            self._update_cell_color(row, col)
            return 'break'
        else:
            return 'break'

    def _insert_number(self, number: int):
        """Inserta un número en la celda seleccionada"""
        if self.selected_cell is None:
            messagebox.showwarning("⚠️ Advertencia", "Selecciona una celda primero")
            return

        row, col = self.selected_cell

        if self.game.is_cell_fixed(row, col):
            messagebox.showwarning("⚠️ Advertencia", "Esta celda no se puede modificar")
            return

        self.cells[row][col].delete(0, tk.END)
        self.cells[row][col].insert(0, str(number))
        self.game.set_value(row, col, number)
        self._update_cell_color(row, col)

    def _clear_cell(self):
        """Borra el contenido de la celda seleccionada"""
        if self.selected_cell is None:
            messagebox.showwarning("⚠️ Advertencia", "Selecciona una celda primero")
            return

        row, col = self.selected_cell

        if self.game.is_cell_fixed(row, col):
            messagebox.showwarning("⚠️ Advertencia", "Esta celda no se puede modificar")
            return

        self.cells[row][col].delete(0, tk.END)
        self.game.set_value(row, col, 0)
        self._update_cell_color(row, col)

    def _update_cell_color(self, row: int, col: int):
        """Actualiza el color de una celda según su estado"""
        if self.game.is_cell_fixed(row, col):
            return

        value = self.game.get_value(row, col)

        if value == 0:
            self.cells[row][col].config(bg=self.colors['editable'])
        else:
            # No cambiar color automáticamente, solo en verificación
            self.cells[row][col].config(bg=self.colors['editable'])

    def _toggle_help_mode(self):
        """Activa/desactiva el modo ayuda"""
        self.help_mode = not self.help_mode

        if self.help_mode:
            self.help_btn.config(text="💡 Modo Ayuda Activo", bg=self.colors['correct'])
            messagebox.showinfo("💡 Modo Ayuda",
                              "Haz clic en una celda vacía para ver el valor correcto.\n"
                              "Penalización: -10 puntos por ayuda.")
        else:
            self.help_btn.config(text="💡 Activar Ayuda", bg='#f9e2af')

    def _apply_help(self, row: int, col: int):
        """Aplica ayuda a una celda específica"""
        if self.game.is_cell_fixed(row, col):
            messagebox.showwarning("⚠️ Advertencia", "Esta celda ya tiene un valor fijo")
            return

        correct_value = self.game.use_help(row, col)

        if correct_value is not None:
            self.cells[row][col].delete(0, tk.END)
            self.cells[row][col].insert(0, str(correct_value))
            self.cells[row][col].config(bg=self.colors['correct'])
            self.help_label.config(text=str(self.game.helps_used))

    def _verify_board(self):
        """Verifica el estado actual del tablero"""
        cell_status = self.game.check_all_cells()

        # Colorear celdas según su estado
        for row, col in cell_status['correct']:
            if not self.game.is_cell_fixed(row, col):
                self.cells[row][col].config(bg=self.colors['correct'])

        for row, col in cell_status['incorrect']:
            self.cells[row][col].config(bg=self.colors['incorrect'])

        for row, col in cell_status['empty']:
            self.cells[row][col].config(bg=self.colors['empty'])

        # Mostrar resumen
        correct_count = len(cell_status['correct'])
        incorrect_count = len(cell_status['incorrect'])
        empty_count = len(cell_status['empty'])

        message = f"✅ Correctas: {correct_count}\n"
        message += f"❌ Incorrectas: {incorrect_count}\n"
        message += f"⬜ Vacías: {empty_count}"

        messagebox.showinfo("🔍 Verificación del Tablero", message)

    def _finish_game(self):
        """Finaliza el juego y muestra resultados"""
        self.timer_running = False
        result = self.game.finish_game()

        # Colorear todas las celdas
        for row, col in result['cell_status']['correct']:
            if not self.game.is_cell_fixed(row, col):
                self.cells[row][col].config(bg=self.colors['correct'])

        for row, col in result['cell_status']['incorrect']:
            self.cells[row][col].config(bg=self.colors['incorrect'])

        # Crear mensaje de resultado
        minutes = int(result['time'] // 60)
        seconds = int(result['time'] % 60)

        if result['correct']:
            title = "🎉 ¡FELICITACIONES!"
            message = "¡Has completado el Sudoku correctamente!\n\n"
        else:
            title = "📊 Juego Finalizado"
            message = "El Sudoku no está completamente correcto.\n\n"

        message += f"⏱️ Tiempo: {minutes:02d}:{seconds:02d}\n"
        message += f"🏆 Puntuación Final: {result['score']}\n\n"
        message += f"📈 Detalles:\n"
        message += f"  • Bonificación por tiempo: +{result['time_bonus']}\n"
        message += f"  • Penalización por errores: -{result['error_penalty']}\n"
        message += f"  • Penalización por ayudas: -{result['help_penalty']}\n\n"
        message += f"📊 Estadísticas:\n"
        message += f"  • Celdas correctas: {len(result['cell_status']['correct'])}\n"
        message += f"  • Celdas incorrectas: {result['errors']}\n"
        message += f"  • Celdas vacías: {result['empty']}\n"
        message += f"  • Ayudas usadas: {result['helps']}"

        messagebox.showinfo(title, message)

    def _new_game(self):
        """Inicia un nuevo juego"""
        if messagebox.askyesno("🔄 Nuevo Juego",
                               "¿Estás seguro de que quieres iniciar un nuevo juego?\n"
                               "Se perderá el progreso actual."):
            # Destruir widgets actuales
            for widget in self.master.winfo_children():
                widget.destroy()

            # Reiniciar variables
            self.game = None
            self.cells = []
            self.selected_cell = None
            self.help_mode = False
            self.timer_running = False

            # Mostrar pantalla de inicio
            self._show_start_screen()

    def _start_timer(self):
        """Inicia el temporizador"""
        self.timer_running = True
        self._update_timer()

    def _update_timer(self):
        """Actualiza el temporizador cada segundo"""
        if self.timer_running and self.game:
            elapsed = self.game.get_elapsed_time()
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

            # Continuar actualizando
            self.master.after(1000, self._update_timer)
