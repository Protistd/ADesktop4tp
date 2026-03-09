import customtkinter as ctk
import json
import os

SETTINGS_FILE = "settings.json"

#loading
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {"theme": "Dark"}

#saving settings
def save_settings(theme):
    settings = {"theme": theme}
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

settings = load_settings()

#settings
ctk.set_appearance_mode(settings["theme"])
ctk.set_default_color_theme("blue")

#app
app = ctk.CTk()
app.title("Professional Settings Manager")
app.geometry("700x400")

# sidebar
sidebar = ctk.CTkFrame(app, width=200)
sidebar.pack(side="left", fill="y", padx=10, pady=10)

title = ctk.CTkLabel(sidebar, text="Ustawienia", font=("Arial", 18))
title.pack(pady=10)

def change_theme(choice):
    ctk.set_appearance_mode(choice)
    save_settings(choice)

theme_option = ctk.CTkOptionMenu(
    sidebar,
    values=["Light", "Dark"],
    command=change_theme
)
theme_option.pack(pady=10)

theme_option.set(settings["theme"])

#main
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

label = ctk.CTkLabel(main_frame, text="dane uzytkownika")
label.pack(pady=5)

entry = ctk.CTkEntry(main_frame, placeholder_text="tekst")
entry.pack(pady=5)

checkbox = ctk.CTkCheckBox(main_frame, text="regulamin")
checkbox.pack(pady=5)

button = ctk.CTkButton(main_frame, text="zapisz")
button.pack(pady=10)

textbox = ctk.CTkTextbox(main_frame, width=400, height=150)
textbox.pack(pady=10)

textbox.insert("0.0", "Lista danych:\n- cos\n- kots\n- gdzies")


app.mainloop()