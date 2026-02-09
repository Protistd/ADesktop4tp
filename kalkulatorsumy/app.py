import tkinter as tk

class SumApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Kalkulator sumy")

        self.entry1 = tk.Entry(self)
        self.entry1.pack()

        self.entry2 = tk.Entry(self)
        self.entry2.pack()

        self.result_label = tk.Label(self, text="Wynik:")
        self.result_label.pack()

        self.btn = tk.Button(self, text="Oblicz", command=self.calculate)
        self.btn.pack()

    def calculate(self):
        try:
            a = float(self.entry1.get())
            b = float(self.entry2.get())
            self.result_label.config(text=str(a + b))
        except ValueError:
            self.result_label.config(text="Błąd danych")

if __name__ == "__main__":
    app = SumApp()
    app.mainloop()
