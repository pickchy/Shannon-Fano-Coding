import tkinter as tk
from tkinter import filedialog, messagebox
from math import log2
from ShannonFanoCoding import encode, decode

# GUI Приложение
class ShannonFanoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Шеннон-Фано Кодирование и Декодирование")
        self.root.geometry("900x600")  # Установить размер окна

        # Первый столбец
        self.first_column_label = tk.Label(root, text="Кодирование Алфавита", font=('Arial', 14))
        self.first_column_label.grid(row=0, column=0, padx=10, pady=10)

        self.load_alphabet_button = tk.Button(root, text="Загрузить файл с алфавитом", command=self.load_alphabet)
        self.load_alphabet_button.grid(row=1, column=0, padx=10, pady=10)

        self.load_probabilities_button = tk.Button(root, text="Загрузить файл с вероятностями", command=self.load_probabilities)
        self.load_probabilities_button.grid(row=2, column=0, padx=10, pady=10)

        self.encode_button = tk.Button(root, text="Кодировать алфавит", command=self.run_encode_symbols)
        self.encode_button.grid(row=3, column=0, padx=10, pady=10)

        self.encoded_result_label = tk.Label(root, text="Закодированный алфавит:")
        self.encoded_result_label.grid(row=4, column=0, padx=10, pady=10)

        self.encoded_message_display = tk.Text(root, height=5, width=40, state=tk.DISABLED)
        self.encoded_message_display.grid(row=5, column=0, padx=10, pady=10)

        self.kraft_label = tk.Label(root, text="Неравенство Крафта:")
        self.kraft_label.grid(row=6, column=0, padx=10, pady=10)

        self.kraft_display = tk.Text(root, height=1, width=40, state=tk.DISABLED)
        self.kraft_display.grid(row=7, column=0, padx=10, pady=10)

        self.avg_length_label = tk.Label(root, text="Средняя длина кодового слова:")
        self.avg_length_label.grid(row=8, column=0, padx=10, pady=10)

        self.avg_length_display = tk.Text(root, height=1, width=40, state=tk.DISABLED)
        self.avg_length_display.grid(row=9, column=0, padx=10, pady=10)

        self.redundancy_label = tk.Label(root, text="Избыточность:")
        self.redundancy_label.grid(row=10, column=0, padx=10, pady=10)

        self.redundancy_display = tk.Text(root, height=1, width=40, state=tk.DISABLED)
        self.redundancy_display.grid(row=11, column=0, padx=10, pady=10)

        # Второй столбец
        self.second_column_label = tk.Label(root, text="Кодирование Сообщения", font=('Arial', 14))
        self.second_column_label.grid(row=0, column=1, padx=10, pady=10)

        self.load_encode_message_button = tk.Button(root, text="Выбрать файл для кодирования", command=self.load_encode_message)
        self.load_encode_message_button.grid(row=1, column=1, padx=10, pady=10)

        self.encode_message_button = tk.Button(root, text="Кодировать сообщение", command=self.run_encode_message)
        self.encode_message_button.grid(row=2, column=1, padx=10, pady=10)

        self.encoded_message_label = tk.Label(root, text="Закодированный текст:")
        self.encoded_message_label.grid(row=3, column=1, padx=10, pady=10)

        self.encoded_message_display_text = tk.Text(root, height=5, width=40, state=tk.DISABLED)
        self.encoded_message_display_text.grid(row=4, column=1, padx=10, pady=10)

        # Третий столбец
        self.third_column_label = tk.Label(root, text="Декодирование Сообщения", font=('Arial', 14))
        self.third_column_label.grid(row=0, column=2, padx=10, pady=10)

        self.load_decode_message_button = tk.Button(root, text="Выбрать файл для декодирования", command=self.load_decode_message)
        self.load_decode_message_button.grid(row=1, column=2, padx=10, pady=10)

        self.decode_message_button = tk.Button(root, text="Декодировать сообщение", command=self.run_decode)
        self.decode_message_button.grid(row=2, column=2, padx=10, pady=10)

        self.decoded_message_label = tk.Label(root, text="Декодированный текст:")
        self.decoded_message_label.grid(row=3, column=2, padx=10, pady=10)

        self.decoded_message_display = tk.Text(root, height=5, width=40, state=tk.DISABLED)
        self.decoded_message_display.grid(row=4, column=2, padx=10, pady=10)

        # Хранение загруженных файлов и данных
        self.alphabet_file_path = ""
        self.probabilities_file_path = ""
        self.message_to_encode = ""
        self.encoded_message_to_decode = ""

    def load_alphabet(self):
        self.alphabet_file_path = filedialog.askopenfilename(title="Выберите файл с алфавитом")
        if self.alphabet_file_path:
            try:
                with open(self.alphabet_file_path, 'r') as f:
                    # Чтение алфавита из файла
                    self.alphabet = [line.strip() for line in f.readlines()]
                messagebox.showinfo("Файл алфавита", f"Файл загружен: {self.alphabet_file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при чтении файла: {e}")

    def load_probabilities(self):
        self.probabilities_file_path = filedialog.askopenfilename(title="Выберите файл с вероятностями")
        if self.probabilities_file_path:
            try:
                with open(self.probabilities_file_path, 'r') as f:
                    # Чтение вероятностей из файла
                    self.probabilities = [line.strip() for line in f.readlines()]
                messagebox.showinfo("Файл вероятностей", f"Файл загружен: {self.probabilities_file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при чтении файла: {e}")

    def run_encode_symbols(self):
            if not hasattr(self, 'alphabet') or not hasattr(self, 'probabilities'):
                messagebox.showerror("Ошибка", "Необходимо загрузить алфавит и вероятности.")
                return

            try:
                if len(self.alphabet) != len(self.probabilities):
                    messagebox.showerror("Ошибка", "Количество символов не соответствует количеству вероятностей.")
                    return

                probability_sum = sum(float(p) for p in self.probabilities)
                tolerance = 1e-9
                if probability_sum > 1 + tolerance:
                    messagebox.showerror("Ошибка", f"Сумма вероятностей превышает 1: {probability_sum}")
                    return

            # Кодирование символов
                encoded_symbols, avg_len, redundancy, kraft, sorted_alphabet = encode(self.alphabet, self.probabilities)

            # Создадим словарь для кодов
                self.symbol_to_code = dict(zip(sorted_alphabet, encoded_symbols))

            # Показ закодированных символов в формате "символ: код"
                self.encoded_message_display.config(state=tk.NORMAL)
                self.encoded_message_display.delete(1.0, tk.END)
                for symbol, code in self.symbol_to_code.items():
                    self.encoded_message_display.insert(tk.END, f"{symbol}: {code}\n")
                self.encoded_message_display.config(state=tk.DISABLED)

            # Запись кодов символов в файл CodeAlphabet.txt
                with open('CodeAlphabet.txt', 'w') as file:
                    for symbol, code in self.symbol_to_code.items():
                        file.write(f"{symbol}: {code}\n")

            # Показ дополнительной информации
                self.kraft_display.config(state=tk.NORMAL)
                self.kraft_display.delete(1.0, tk.END)
                self.kraft_display.insert(tk.END, "Выполнено" if kraft else "Не выполнено")
                self.kraft_display.config(state=tk.DISABLED)

                self.avg_length_display.config(state=tk.NORMAL)
                self.avg_length_display.delete(1.0, tk.END)
                self.avg_length_display.insert(tk.END, f"{avg_len:.2f}")
                self.avg_length_display.config(state=tk.DISABLED)

                self.redundancy_display.config(state=tk.NORMAL)
                self.redundancy_display.delete(1.0, tk.END)
                self.redundancy_display.insert(tk.END, f"{redundancy:.2f}")
                self.redundancy_display.config(state=tk.DISABLED)

                messagebox.showinfo("Успех", "Алфавит успешно закодирован и сохранён в файл CodeAlphabet.txt.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при кодировании алфавита: {e}")


    def load_encode_message(self):
        self.encode_message_path = filedialog.askopenfilename(title="Выберите файл с сообщением для кодирования")
        if self.encode_message_path:
            try:
                with open(self.encode_message_path, 'r') as f:
                    # Чтение сообщения для кодирования
                    self.message_to_encode = f.read().strip()
                messagebox.showinfo("Файл сообщения", f"Файл загружен: {self.encode_message_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при чтении файла: {e}")
        
    def run_encode_message(self):
        if not hasattr(self, 'message_to_encode') or not hasattr(self, 'symbol_to_code'):
            messagebox.showerror("Ошибка", "Необходимо загрузить сообщение и закодировать алфавит.")
            return

        try:
        # Кодируем сообщение, используя словарь `self.symbol_to_code`
            encoded_message = ''.join([self.symbol_to_code[char] for char in self.message_to_encode if char in self.symbol_to_code])

        # Показ закодированного сообщения
            self.encoded_message_display_text.config(state=tk.NORMAL)
            self.encoded_message_display_text.delete(1.0, tk.END)
            self.encoded_message_display_text.insert(tk.END, encoded_message.strip())
            self.encoded_message_display_text.config(state=tk.DISABLED)

        # Сохранение закодированного сообщения в файл
            with open('encoded_message.txt', 'w') as file:
                file.write(encoded_message.strip())

            messagebox.showinfo("Успех", "Сообщение успешно закодировано и сохранено в encoded_message.txt.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при кодировании сообщения: {e}")


    def load_decode_message(self):
        self.decode_message_path = filedialog.askopenfilename(title="Выберите файл с закодированным сообщением")
        if self.decode_message_path:
            try:
                with open(self.decode_message_path, 'r') as f:
                    # Чтение и обрезка закодированного сообщения
                    self.encoded_message_to_decode = f.read().strip()
                messagebox.showinfo("Файл закодированного сообщения", f"Файл загружен: {self.decode_message_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при чтении файла: {e}")

    def run_decode(self):
        if not hasattr(self, 'encoded_message_to_decode') or not hasattr(self, 'symbol_to_code'):
            messagebox.showerror("Ошибка", "Необходимо загрузить закодированное сообщение и закодировать алфавит.")
            return

        try:
        # Создаём обратный словарь "код: символ"
            self.code_to_symbol = {code: symbol for symbol, code in self.symbol_to_code.items()}
    
        # Декодируем сообщение побитно, проверяя каждый подстроку как возможный код
            decoded_message = ""
            buffer = ""  # Буфер для хранения битов, пока не найдём соответствующий код
            for bit in self.encoded_message_to_decode:
                buffer += bit
                if buffer in self.code_to_symbol:
                    decoded_message += self.code_to_symbol[buffer]
                    buffer = ""  # Сброс буфера после нахождения символа

            if buffer != "":
                messagebox.showerror("Ошибка", "Остались необработанные биты. Сообщение декодировано частично.")
        
        # Показ декодированного сообщения
            self.decoded_message_display.config(state=tk.NORMAL)
            self.decoded_message_display.delete(1.0, tk.END)
            self.decoded_message_display.insert(tk.END, decoded_message.strip())
            self.decoded_message_display.config(state=tk.DISABLED)

        # Сохранение декодированного сообщения в файл
            with open('decoded_message.txt', 'w') as file:
                file.write(decoded_message.strip())

            messagebox.showinfo("Успех", "Сообщение успешно декодировано и сохранено в decoded_message.txt.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при декодировании: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShannonFanoApp(root)
    root.mainloop()
