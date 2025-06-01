import tkinter as tk
from tkinter import messagebox
import math
import statistics
from typing import List, Tuple

class CalculatorApp:
    def __init__(self, root):
        # Aqui guardo a janela principal do Tkinter. É tipo a "casa" onde tudo vai acontecer.
        self.root = root
        self.root.title("Mega Calculadora do Savyo Rocha")
        self.root.geometry("500x500")  # Tamanho da janela, pra ficar bonitinha e funcional.

        # Lista pra armazenar o histórico das operações (o que fiz e o resultado).
        self.history: List[Tuple[str, float]] = []

        # Configurando o layout principal com um frame pra deixar tudo organizado.
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill="both", expand=True)

        # Aqui crio a área de texto onde vou mostrar os resultados e o histórico. Usei um widget Text pra ser mais flexível.
        self.result_text = tk.Text(self.main_frame, height=10, width=50, state="disabled")
        self.result_text.grid(row=0, column=0, columnspan=2, pady=10)

        # Frame pros botões de operações. Quis separar pra ficar mais fácil de organizar.
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Botões pra cada tipo de operação. Cada um chama uma função que monta a interface específica.
        tk.Button(self.button_frame, text="Operações Básicas", command=self.show_basic_ops).grid(row=0, column=0, padx=5)
        tk.Button(self.button_frame, text="Avançadas", command=self.show_advanced_ops).grid(row=0, column=1, padx=5)
        tk.Button(self.button_frame, text="Trigonométricas", command=self.show_trig_ops).grid(row=0, column=2, padx=5)
        tk.Button(self.button_frame, text="Estatísticas", command=self.show_stats_ops).grid(row=0, column=3, padx=5)
        tk.Button(self.button_frame, text="Conversões", command=self.show_conversion_ops).grid(row=0, column=4, padx=5)
        tk.Button(self.button_frame, text="Histórico", command=self.show_history).grid(row=1, column=0, columnspan=5, pady=5)

        # Frame pros inputs dinâmicos. Aqui coloco os campos de entrada dependendo da operação escolhida.
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.grid(row=2, column=0, columnspan=2, pady=10)

    # Função pra adicionar operação ao histórico. Limitei a 10 pra não lotar a memória.
    def add_to_history(self, operation: str, result: float) -> None:
        self.history.append((operation, result))
        if len(self.history) > 10:
            self.history.pop(0)
        self.update_result_text(f"{operation} = {result}\n")

    # Atualiza a área de texto com o resultado ou mensagem. Desabilito o estado pra evitar edição direta.
    def update_result_text(self, message: str) -> None:
        self.result_text.config(state="normal")
        self.result_text.insert(tk.END, message)
        self.result_text.config(state="disabled")
        self.result_text.see(tk.END)  # Rola pro final pra mostrar o último resultado.

    # Limpa o frame de inputs pra mostrar novos campos. Uso isso quando mudo de operação.
    def clear_input_frame(self) -> None:
        for widget in self.input_frame.winfo_children():
            widget.destroy()

    # Função pra mostrar o histórico. Simples, mas útil pra ver o que já calculei.
    def show_history(self) -> None:
        self.clear_input_frame()
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        if not self.history:
            self.update_result_text("Nenhuma operação no histórico.\n")
        else:
            self.update_result_text("\nHistórico de Operações:\n")
            for op, res in self.history:
                self.update_result_text(f"{op} = {res}\n")
        self.result_text.config(state="disabled")

    # Interface pras operações básicas (+, -, *, /). Criei campos pros números e um menu pras operações.
    def show_basic_ops(self) -> None:
        self.clear_input_frame()
        tk.Label(self.input_frame, text="Primeiro número:").grid(row=0, column=0, padx=5)
        num1_entry = tk.Entry(self.input_frame)
        num1_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.input_frame, text="Operação (+, -, *, /):").grid(row=1, column=0, padx=5)
        op_var = tk.StringVar(value="+")
        tk.OptionMenu(self.input_frame, op_var, "+", "-", "*", "/").grid(row=1, column=1, padx=5)

        tk.Label(self.input_frame, text="Segundo número:").grid(row=2, column=0, padx=5)
        num2_entry = tk.Entry(self.input_frame)
        num2_entry.grid(row=2, column=1, padx=5)

        tk.Button(self.input_frame, text="Calcular", command=lambda: self.calculate_basic(num1_entry.get(), op_var.get(), num2_entry.get())).grid(row=3, column=0, columnspan=2, pady=5)

    # Calcula as operações básicas. Fiz um tratamento de erro pra evitar crashes.
    def calculate_basic(self, num1: str, op: str, num2: str) -> None:
        try:
            a = float(num1)
            b = float(num2)
            if op == "/" and b == 0:
                raise ValueError("Divisão por zero não é permitida!")
            if op == "+":
                result = a + b
            elif op == "-":
                result = a - b
            elif op == "*":
                result = a * b
            elif op == "/":
                result = a / b
            else:
                raise ValueError("Operação inválida!")
            self.add_to_history(f"{a} {op} {b}", result)
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    # Interface pras operações avançadas (potência, raiz, log). Um menu dropdown pra escolher a operação.
    def show_advanced_ops(self) -> None:
        self.clear_input_frame()
        tk.Label(self.input_frame, text="Operação Avançada:").grid(row=0, column=0, padx=5)
        op_var = tk.StringVar(value="potência")
        tk.OptionMenu(self.input_frame, op_var, "potência", "raiz quadrada", "logaritmo").grid(row=0, column=1, padx=5)

        tk.Label(self.input_frame, text="Número:").grid(row=1, column=0, padx=5)
        num1_entry = tk.Entry(self.input_frame)
        num1_entry.grid(row=1, column=1, padx=5)

        tk.Label(self.input_frame, text="Expoente/Base (se aplicável):").grid(row=2, column=0, padx=5)
        num2_entry = tk.Entry(self.input_frame)
        num2_entry.grid(row=2, column=1, padx=5)

        tk.Button(self.input_frame, text="Calcular", command=lambda: self.calculate_advanced(op_var.get(), num1_entry.get(), num2_entry.get())).grid(row=3, column=0, columnspan=2, pady=5)

    # Calcula as operações avançadas. Incluí validações pra evitar erros como raiz de número negativo.
    def calculate_advanced(self, op: str, num1: str, num2: str) -> None:
        try:
            num1 = float(num1)
            if op == "potência":
                num2 = float(num2)
                result = math.pow(num1, num2)
                self.add_to_history(f"{num1} ^ {num2}", result)
            elif op == "raiz quadrada":
                if num1 < 0:
                    raise ValueError("Raiz quadrada de número negativo não é permitida!")
                result = math.sqrt(num1)
                self.add_to_history(f"√{num1}", result)
            elif op == "logaritmo":
                if num1 <= 0:
                    raise ValueError("Logaritmo de número não positivo não é permitido!")
                base = num2.lower()
                if base not in ["10", "e"]:
                    raise ValueError("Base deve ser '10' ou 'e'!")
                result = math.log10(num1) if base == "10" else math.log(num1)
                self.add_to_history(f"log_{base}({num1})", result)
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    # Interface pras funções trigonométricas. Adicionei opção pra escolher graus ou radianos.
    def show_trig_ops(self) -> None:
        self.clear_input_frame()
        tk.Label(self.input_frame, text="Função:").grid(row=0, column=0, padx=5)
        op_var = tk.StringVar(value="sin")
        tk.OptionMenu(self.input_frame, op_var, "sin", "cos", "tan").grid(row=0, column=1, padx=5)

        tk.Label(self.input_frame, text="Ângulo:").grid(row=1, column=0, padx=5)
        angle_entry = tk.Entry(self.input_frame)
        angle_entry.grid(row=1, column=1, padx=5)

        tk.Label(self.input_frame, text="Unidade:").grid(row=2, column=0, padx=5)
        unit_var = tk.StringVar(value="degrees")
        tk.OptionMenu(self.input_frame, unit_var, "degrees", "radians").grid(row=2, column=1, padx=5)

        tk.Button(self.input_frame, text="Calcular", command=lambda: self.calculate_trig(op_var.get(), angle_entry.get(), unit_var.get())).grid(row=3, column=0, columnspan=2, pady=5)

    # Calcula seno, cosseno e tangente. Converti graus pra radianos quando necessário.
    def calculate_trig(self, op: str, angle: str, unit: str) -> None:
        try:
            angle = float(angle)
            if unit == "degrees":
                angle = math.radians(angle)
            if op == "sin":
                result = math.sin(angle)
                self.add_to_history(f"sin({angle} {unit})", result)
            elif op == "cos":
                result = math.cos(angle)
                self.add_to_history(f"cos({angle} {unit})", result)
            elif op == "tan":
                if math.cos(angle) == 0:
                    raise ValueError("Tangente indefinida para este ângulo!")
                result = math.tan(angle)
                self.add_to_history(f"tan({angle} {unit})", result)
            else:
                raise ValueError("Função trigonométrica inválida!")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    # Interface pras operações estatísticas. Aqui o usuário digita uma lista de números.
    def show_stats_ops(self) -> None:
        self.clear_input_frame()
        tk.Label(self.input_frame, text="Operação:").grid(row=0, column=0, padx=5)
        op_var = tk.StringVar(value="mean")
        tk.OptionMenu(self.input_frame, op_var, "mean", "median", "stdev").grid(row=0, column=1, padx=5)

        tk.Label(self.input_frame, text="Números (separados por espaço):").grid(row=1, column=0, padx=5)
        numbers_entry = tk.Entry(self.input_frame)
        numbers_entry.grid(row=1, column=1, padx=5)

        tk.Button(self.input_frame, text="Calcular", command=lambda: self.calculate_stats(op_var.get(), numbers_entry.get())).grid(row=2, column=0, columnspan=2, pady=5)

    # Calcula média, mediana ou desvio padrão. Validei pra garantir que a lista não tá vazia.
    def calculate_stats(self, op: str, numbers: str) -> None:
        try:
            nums = [float(x) for x in numbers.split()]
            if not nums:
                raise ValueError("Lista de números vazia!")
            if op == "mean":
                result = statistics.mean(nums)
                self.add_to_history(f"Média({nums})", result)
            elif op == "median":
                result = statistics.median(nums)
                self.add_to_history(f"Mediana({nums})", result)
            elif op == "stdev":
                if len(nums) < 2:
                    raise ValueError("Desvio padrão requer ao menos 2 números!")
                result = statistics.stdev(nums)
                self.add_to_history(f"Desvio Padrão({nums})", result)
            else:
                raise ValueError("Operação estatística inválida!")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    # Interface pras conversões de unidades. Separei em comprimento e temperatura.
    def show_conversion_ops(self) -> None:
        self.clear_input_frame()
        tk.Label(self.input_frame, text="Tipo de Conversão:").grid(row=0, column=0, padx=5)
        type_var = tk.StringVar(value="length")
        tk.OptionMenu(self.input_frame, type_var, "length", "temperature").grid(row=0, column=1, padx=5)

        tk.Label(self.input_frame, text="Valor:").grid(row=1, column=0, padx=5)
        value_entry = tk.Entry(self.input_frame)
        value_entry.grid(row=1, column=1, padx=5)

        tk.Label(self.input_frame, text="De:").grid(row=2, column=0, padx=5)
        from_unit_var = tk.StringVar(value="m")
        from_unit_menu = tk.OptionMenu(self.input_frame, from_unit_var, "m", "km", "miles", "C", "F", "K")
        from_unit_menu.grid(row=2, column=1, padx=5)

        tk.Label(self.input_frame, text="Para:").grid(row=3, column=0, padx=5)
        to_unit_var = tk.StringVar(value="km")
        to_unit_menu = tk.OptionMenu(self.input_frame, to_unit_var, "m", "km", "miles", "C", "F", "K")
        to_unit_menu.grid(row=3, column=1, padx=5)

        # Atualiza as opções dos menus dinamicamente com base no tipo de conversão.
        def update_units(*args):
            if type_var.get() == "length":
                from_unit_menu['menu'].delete(0, 'end')
                to_unit_menu['menu'].delete(0, 'end')
                for unit in ["m", "km", "miles"]:
                    from_unit_menu['menu'].add_command(label=unit, command=lambda u=unit: from_unit_var.set(u))
                    to_unit_menu['menu'].add_command(label=unit, command=lambda u=unit: to_unit_var.set(u))
            else:
                from_unit_menu['menu'].delete(0, 'end')
                to_unit_menu['menu'].delete(0, 'end')
                for unit in ["C", "F", "K"]:
                    from_unit_menu['menu'].add_command(label=unit, command=lambda u=unit: from_unit_var.set(u))
                    to_unit_menu['menu'].add_command(label=unit, command=lambda u=unit: to_unit_var.set(u))
            from_unit_var.set("m" if type_var.get() == "length" else "C")
            to_unit_var.set("km" if type_var.get() == "length" else "F")

        type_var.trace("w", update_units)
        tk.Button(self.input_frame, text="Calcular", command=lambda: self.calculate_conversion(type_var.get(), value_entry.get(), from_unit_var.get(), to_unit_var.get())).grid(row=4, column=0, columnspan=2, pady=5)

    # Calcula conversões de comprimento e temperatura. Fiz as fórmulas pra cobrir as principais conversões.
    def calculate_conversion(self, conv_type: str, value: str, from_unit: str, to_unit: str) -> None:
        try:
            value = float(value)
            if conv_type == "length":
                conversions = {
                    ("m", "km"): lambda x: x / 1000,
                    ("km", "m"): lambda x: x * 1000,
                    ("m", "miles"): lambda x: x / 1609.34,
                    ("miles", "m"): lambda x: x * 1609.34,
                    ("km", "miles"): lambda x: x / 1.60934,
                    ("miles", "km"): lambda x: x * 1.60934,
                }
                key = (from_unit, to_unit)
                if key not in conversions:
                    raise ValueError("Conversão de comprimento inválida!")
                result = conversions[key](value)
                self.add_to_history(f"{value} {from_unit} -> {to_unit}", result)
            else:
                if from_unit == "C" and to_unit == "F":
                    result = (value * 9/5) + 32
                elif from_unit == "F" and to_unit == "C":
                    result = (value - 32) * 5/9
                elif from_unit == "C" and to_unit == "K":
                    result = value + 273.15
                elif from_unit == "K" and to_unit == "C":
                    result = value - 273.15
                elif from_unit == "F" and to_unit == "K":
                    result = (value - 32) * 5/9 + 273.15
                elif from_unit == "K" and to_unit == "F":
                    result = (value - 273.15) * 9/5 + 32
                else:
                    raise ValueError("Conversão de temperatura inválida!")
                self.add_to_history(f"{value} °{from_unit} -> °{to_unit}", result)
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

# Aqui começa o programa! Criei a janela principal e instanciei a calculadora.
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
