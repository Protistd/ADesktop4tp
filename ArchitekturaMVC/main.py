import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# ====================================================================
# 1. MODEL (Logika Danych)
# ====================================================================

class KwadratModel:
    """Model Danych: Przechowuje stan liczby i oblicza jej kwadrat."""

    def oblicz(self, liczba):
        """Oblicza kwadrat liczby."""
        return liczba ** 2


# ====================================================================
# 2. VIEW (Interfejs Graficzny)
# ====================================================================

class KwadratView(tk.Tk):
    """Widok: Tworzy i wyświetla interfejs Tkinter."""

    def __init__(self, controller):
        super().__init__()
        self.title("Kalkulator Kwadratu")
        self.geometry("300x200")

        self.controller = controller

        # Zmienna do dynamicznej aktualizacji wyniku
        self.wynik_var = tk.StringVar(value="Wynik: 0")

        self._utworz_widzety()

    def _utworz_widzety(self):
        """Buduje interfejs."""

        self.liczba_entry = ttk.Entry(self, font=("Arial", 14))
        self.liczba_entry.pack(pady=10)

        self.wynik_label = ttk.Label(self, textvariable=self.wynik_var, font=("Arial", 16))
        self.wynik_label.pack(pady=10)

        # Przycisk "Oblicz": Użycie 'command' do podpięcia metody Kontrolera
        self.oblicz_button = ttk.Button(self, text="Oblicz", command=self.controller.obsluz_oblicz)
        self.oblicz_button.pack(pady=10)

    def ustaw_wynik(self, wynik):
        """Metoda wywoływana przez Kontroler do aktualizacji GUI z wynikiem."""
        self.wynik_var.set(f"Wynik: {wynik}")

    def pobierz_liczbe(self):
        """Zwraca liczbę wprowadzaną przez użytkownika."""
        try:
            return float(self.liczba_entry.get())
        except ValueError:
            return None

    def wyswietl_blad(self, komunikat):
        """Wyświetla komunikat błędu."""
        messagebox.showerror("Błąd", komunikat)
        self.liczba_entry.delete(0, tk.END)  # Czyści pole wejściowe po błędzie


# ====================================================================
# 3. CONTROLLER (Pośrednik)
# ====================================================================

class KwadratController:
    """Kontroler: Koordynuje Model i View."""

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def obsluz_oblicz(self):
        """Obsługuje kliknięcie przycisku 'Oblicz'."""
        liczba = self.view.pobierz_liczbe()

        if liczba is None:
            self.view.wyswietl_blad("Proszę wprowadzić liczbę!")
            return

        wynik = self.model.oblicz(liczba)
        self.view.ustaw_wynik(wynik)


# ====================================================================
# 4. PUNKT STARTOWY
# ====================================================================

if __name__ == "__main__":
    # 1. Tworzenie Modelu
    model = KwadratModel()

    # 2. Tworzenie Kontrolera i View (ustawienie referencji)
    controller_instance = KwadratController(model, view=None)

    # Tworzymy View, przekazując mu gotowy Controller
    view_instance = KwadratView(controller_instance)

    # Uzupełniamy referencję View w Kontrolerze
    controller_instance.view = view_instance

    # 3. Uruchomienie aplikacji
    view_instance.mainloop()
