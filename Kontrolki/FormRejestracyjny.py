import tkinter as tk
from tkinter import messagebox


def submit_form():
    imie = entry_imie.get()
    email = entry_email.get()
    wiek = wiek_var.get()
    zainteresowania = []
    if sport_var.get():
        zainteresowania.append("gry")
    if ksiazki_var.get():
        zainteresowania.append("sport")
    uwagi = text_uwagi.get("1.0", tk.END).strip()

    dane = f"imie: {imie}\nemail: {email}\nwiek: {wiek}\nzainteresowania: {', '.join(zainteresowania)}\nuwagi: {uwagi}"
    messagebox.showinfo("Dane uzytkownika", dane)


root = tk.Tk()
root.title("Formularz Rejestracyjny")

# imie
tk.Label(root, text="imie:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_imie = tk.Entry(root, width=30)
entry_imie.grid(row=0, column=1, padx=10, pady=5)

# email
tk.Label(root, text="email:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_email = tk.Entry(root, width=30)
entry_email.grid(row=1, column=1, padx=10, pady=5)

# wiek (radio)
tk.Label(root, text="wiek (kategoria):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
wiek_var = tk.StringVar(value="18-30")
tk.Radiobutton(root, text="18-30", variable=wiek_var, value="18-30").grid(row=2, column=1, sticky="w")
tk.Radiobutton(root, text="31-50", variable=wiek_var, value="31-50").grid(row=3, column=1, sticky="w")
tk.Radiobutton(root, text="50+", variable=wiek_var, value="50+").grid(row=4, column=1, sticky="w")

# zainteresowania (checkboxy)
tk.Label(root, text="zainteresowania:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
sport_var = tk.BooleanVar()
ksiazki_var = tk.BooleanVar()
tk.Checkbutton(root, text="gry", variable=sport_var).grid(row=5, column=1, sticky="w")
tk.Checkbutton(root, text="sport", variable=ksiazki_var).grid(row=6, column=1, sticky="w")

# uwagi (text)
tk.Label(root, text="uwagi:").grid(row=7, column=0, padx=10, pady=5, sticky="ne")
text_uwagi = tk.Text(root, width=30, height=5)
text_uwagi.grid(row=7, column=1, padx=10, pady=5)

# przycisk
tk.Button(root, text="zarejestruj", command=submit_form).grid(row=8, column=0, columnspan=2, pady=10)

root.mainloop()
