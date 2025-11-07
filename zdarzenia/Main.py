import tkinter as tk

def na_najechaniu(event):
    status_panel.config(
        text="UZBROJENIE MOŻLIWE",
        bg="yellow"
    )

def na_kliknieciu(event):
    status_panel.config(
        text="SYSTEM UZBROJONY!!!",
        bg="red"
    )

def na_opuszczeniu(event):
    status_panel.config(
        text="SYSTEM ROZBROJONY 😎",
        bg="green"
    )

root = tk.Tk()
root.title("Panel Alarmowy")
root.geometry("350x150")

status_panel = tk.Label(
    root,
    text="SYSTEM ROZBROJONY 😎",
    bg="green",
    fg="white",
    font=('Arial', 16, 'bold'),
    width=25,
    height=3
)
status_panel.pack(padx=20, pady=20)

# powiązanie zdarzeń
status_panel.bind("<Enter>", na_najechaniu)
status_panel.bind("<Button-1>", na_kliknieciu)
status_panel.bind("<Leave>", na_opuszczeniu)

root.mainloop()
