import tkinter as tk
from tkinter import ttk

def save_settings():
    """Funkcja symulująca i sterująca paskiem postępu."""
    status_bar.start(10)  # interwal ms
    save_button.config(state="disabled")  # blokada guzika
    root.after(3000, stop_progress)       # stop po 3s

def stop_progress():
    """Funkcja zatrzymująca pasek postępu."""
    status_bar.stop()
    save_button.config(state="normal")
    print("Ustawienia zapisane!")

root = tk.Tk()
root.title("Ustawienia Systemu")
root.geometry("400x300")

# noteboook - karty
notebook = ttk.Notebook(root)
notebook.pack(pady=10, padx=10, expand=True, fill="both")

# Karta "Wygląd":
tab_appearance = ttk.Frame(notebook, padding="10")
notebook.add(tab_appearance, text="Wygląd")

# combobox - motyw
ttk.Label(tab_appearance, text="Motyw:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
themes = ["Jasny", "Ciemny", "Systemowy"]
theme_combo = ttk.Combobox(tab_appearance, values=themes, state="readonly")
theme_combo.current(0)
theme_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# checkbutton kontrast
high_contrast_var = tk.BooleanVar()
high_contrast_check = ttk.Checkbutton(tab_appearance, text="Włącz Wysoki Kontrast", variable=high_contrast_var)
high_contrast_check.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)

# Karta "Prywatność":
tab_privacy = ttk.Frame(notebook, padding="10")
notebook.add(tab_privacy, text="Prywatność")

privacy_var = tk.StringVar(value="Wszystkie")

ttk.Label(tab_privacy, text="udostepnianie danych:").pack(anchor="w", pady=5)

ttk.Radiobutton(tab_privacy, text="Wszystkie", variable=privacy_var, value="Wszystkie").pack(anchor="w")
ttk.Radiobutton(tab_privacy, text="Anonimowe", variable=privacy_var, value="Anonimowe").pack(anchor="w")
ttk.Radiobutton(tab_privacy, text="Żadne", variable=privacy_var, value="Żadne").pack(anchor="w")

# pasek stanu i zapisz buton
status_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
status_bar.pack(pady=10)

save_button = ttk.Button(root, text="Zapisz Ustawienia", command=save_settings)
save_button.pack(pady=5)

root.mainloop()
