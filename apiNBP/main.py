import customtkinter as ctk
import requests
import threading

URL = "http://api.nbp.pl/api/exchangerates/tables/A/?format=json"

class CurrencyApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Przelicznik Walut NBP")
        self.geometry("400x300")

        # wpisanie kwoty
        self.amount_entry = ctk.CTkEntry(self, placeholder_text="podaj kwote pln")
        self.amount_entry.pack(pady=10)

        # tymczasowa lista 
        self.currency_menu = ctk.CTkOptionMenu(self, values=["Ładowanie..."])
        self.currency_menu.pack(pady=10)

        # buton
        self.convert_button = ctk.CTkButton(
            self,
            text="Przelicz",
            command=self.start_thread
        )
        self.convert_button.pack(pady=10)

        # wynik
        self.result_label = ctk.CTkLabel(self, text="to bedzie: ")
        self.result_label.pack(pady=10)

        # data kursu
        self.date_label = ctk.CTkLabel(self, text="")
        self.date_label.pack(pady=5)

        # wczytaj waluty
        threading.Thread(target=self.load_currencies).start()

    def load_currencies(self):
        try:
            response = requests.get(URL)
            data = response.json()

            rates = data[0]["rates"]
            currencies = [x["code"] for x in rates]

            self.currency_menu.configure(values=currencies)
            self.currency_menu.set(currencies[0])

        except:
            self.currency_menu.configure(values=["Błąd"])

    def start_thread(self):
        t = threading.Thread(target=self.convert_currency)
        t.start()

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            currency = self.currency_menu.get()

            response = requests.get(URL)
            data = response.json()

            rates = data[0]["rates"]
            date = data[0]["effectiveDate"]

            rate = [x["mid"] for x in rates if x["code"] == currency][0]

            result = amount / rate

            self.result_label.configure(
                text=f"{amount:.2f} PLN = {result:.2f} {currency}"
            )

            self.date_label.configure(
                text=f"Kurs z dnia: {date}"
            )

        except Exception:
            self.result_label.configure(
                text="blad, wprowadz prawdziwe dane lub sprawdz internet"
            )

if __name__ == "__main__":
    app = CurrencyApp()
    app.mainloop()