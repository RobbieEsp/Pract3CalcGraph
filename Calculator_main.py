import tkinter as tk 
from tkinter import messagebox 
from neg_num_err import NegativeNumberError # Importa la excepción personalizada.

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Mi Calculadora Única") # Personalización del diseño.
        master.geometry("300x450")
        master.resizable(False, False)
        master.configure(bg="#2c3e50")

        self.current_expression = ""
        self.result_displayed = False

        # Objeto gráfico: Entry para mostrar números y resultados (texto).
        self.display = tk.Entry(
            master, width=18, font=("Arial", 24), bd=5, relief="flat",
            bg="#ecf0f1", fg="#2c3e50", justify="right"
        )
        self.display.grid(row=0, column=0, columnspan=4, pady=20, padx=10)

        # Configuración y creación de botones (objetos gráficos).
        buttons_config = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3, True),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3, True),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3, True),
            ('0', 4, 0), ('.', 4, 1), ('C', 4, 2, False, "#c0392b"), ('+', 4, 3, True),
            ('=', 5, 0, False, "#c0392b", 4) # Botón '=' abarca 4 columnas.
        ]
        
        # Creación de los objetos gráficos Button.
        for item in buttons_config:
            text, row, col = item[0], item[1], item[2]
            is_operator = item[3] if len(item) > 3 else False
            bg_color = item[4] if len(item) > 4 else ("#e67e22" if is_operator else "#34495e")
            fg_color = "#ecf0f1"
            columnspan = item[5] if len(item) > 5 else 1

            button = tk.Button(
                master, text=text, font=("Arial", 16, "bold"), bg=bg_color, fg=fg_color,
                # Manejo de eventos: se asocia una función al comando del botón.
                command=lambda t=text: self.on_button_click(t),
                height=2, width=6 if text != '=' else None, relief="flat"
            )
            button.grid(row=row, column=col, columnspan=columnspan, sticky="nsew", padx=5, pady=5)

        # Configuración para que los botones se expandan uniformemente.
        for i in range(6): master.grid_rowconfigure(i, weight=1)
        for i in range(4): master.grid_columnconfigure(i, weight=1)

    # Manejo de eventos: función que se ejecuta al presionar un botón.
    def on_button_click(self, char):
        operators = ['+', '-', '*', '/']

        if char == 'C': # Limpiar pantalla.
            self.current_expression = ""
            self.display.delete(0, tk.END)
            self.result_displayed = False

        elif char == '=': # Mostrar resultado y manejar excepciones.
            try:
                # Validar que la expresión no termine con un operador.
                if self.current_expression and self.current_expression[-1] in operators:
                    raise SyntaxError("Expresión incompleta.")

                result = eval(self.current_expression) # Evalúa la expresión matemática.

                # Control de excepciones: lanzar NegativeNumberError si el resultado es negativo.
                if result < 0:
                    raise NegativeNumberError("El resultado de la operación no puede ser negativo.")

                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))
                self.current_expression = str(result)
                self.result_displayed = True

            # Control de excepciones: capturar y mostrar errores específicos.
            except NegativeNumberError as e:
                messagebox.showerror("Error", e.message)
                self.current_expression = ""
                self.display.delete(0, tk.END)
            except ZeroDivisionError:
                messagebox.showerror("Error", "¡No se puede dividir por cero!")
                self.current_expression = ""
                self.display.delete(0, tk.END)
            except SyntaxError:
                messagebox.showerror("Error", "¡Expresión inválida o incompleta!")
                self.current_expression = ""
                self.display.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
                self.current_expression = ""
                self.display.delete(0, tk.END)

        else: # Manejo de ingreso de números y operadores.
            # Lógica para iniciar nueva operación o continuar con el resultado.
            if self.result_displayed and char.isdigit():
                self.current_expression = char
                self.display.delete(0, tk.END)
                self.display.insert(0, char)
                self.result_displayed = False
            elif self.result_displayed and char in operators:
                self.current_expression = self.display.get() + char
                self.display.delete(0, tk.END)
                self.display.insert(0, self.current_expression)
                self.result_displayed = False
            elif char in operators:
                # Evitar operadores consecutivos o iniciar con operador (excepto '-' si se permite como inicio de negativo)
                if self.current_expression and self.current_expression[-1] in operators:
                    self.current_expression = self.current_expression[:-1] + char # Permite cambiar el operador.
                elif not self.current_expression and char == '-': # **No se permite iniciar con '-' para evitar números negativos directos.**
                    messagebox.showwarning("Advertencia", "No se permite el ingreso de números negativos directamente.")
                    return
                else:
                    self.current_expression += str(char)
                self.display.delete(0, tk.END)
                self.display.insert(0, self.current_expression)
            elif char.isdigit() or char == '.':
                self.current_expression += str(char)
                self.display.delete(0, tk.END)
                self.display.insert(0, self.current_expression)


if __name__ == "__main__":
    root = tk.Tk() # Se crea la ventana principal (elemento fundamental de la GUI).
    my_calculator = Calculator(root)
    root.mainloop() # Inicia el bucle principal de la GUI para manejar eventos.