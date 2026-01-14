import tkinter as tk
from tkinter import messagebox
import sqlite3
import threading
import queue
import time

# =========================
# MODEL
# =========================
class MaintenanceModel:
    def __init__(self):
        self.db_name = "maintenance.db"
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numer_maszyny TEXT,
                    opis TEXT,
                    czas_naprawy_estymowany INTEGER
                )
            """)

    def save_incident_worker(self, machine, description, repair_time, result_queue):
        try:
            # symulacja długiej operacji
            time.sleep(3)

            with sqlite3.connect(self.db_name) as conn:
                conn.execute(
                    "INSERT INTO incidents (numer_maszyny, opis, czas_naprawy_estymowany) VALUES (?, ?, ?)",
                    (machine, description, repair_time)
                )
                conn.commit()

            result_queue.put(("SUCCESS", "zgloszenie zapisane poprawnie"))
        except Exception as e:
            result_queue.put(("ERROR", str(e)))


# =========================
# VIEW + CONTROLLER
# =========================
class App(tk.Tk):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.result_queue = queue.Queue()

        self.title("System Monitorowania Awarii Maszyn")
        self.geometry("400x300")

        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="Numer maszyny:").pack(pady=5)

        self.machine_var = tk.StringVar(value="M1")
        tk.OptionMenu(self, self.machine_var, "M1", "M2", "M3").pack()

        tk.Label(self, text="Opis usterki:").pack(pady=5)
        self.desc_text = tk.Text(self, height=5, width=40)
        self.desc_text.pack()

        tk.Label(self, text="Szacowany czas naprawy (min):").pack(pady=5)
        self.time_entry = tk.Entry(self)
        self.time_entry.pack()

        self.save_btn = tk.Button(self, text="Zapisz", command=self.handle_save)
        self.save_btn.pack(pady=10)

        self.status_label = tk.Label(self, text="Gotowy", fg="green")
        self.status_label.pack()

    def handle_save(self):
        description = self.desc_text.get("1.0", tk.END).strip()
        repair_time = self.time_entry.get()

        if not description or not repair_time.isdigit():
            messagebox.showwarning("Błąd", "Uzupelnij poprawnie wszystkie pola")
            return

        self.save_btn.config(state="disabled")
        self.status_label.config(
            text="TRWA PRZESYŁANIE DANYCH...",
            fg="red"
        )

        thread = threading.Thread(
            target=self.model.save_incident_worker,
            args=(
                self.machine_var.get(),
                description,
                int(repair_time),
                self.result_queue
            )
        )
        thread.start()

        self.check_queue()

    def check_queue(self):
        try:
            status, msg = self.result_queue.get_nowait()

            if status == "SUCCESS":
                self.status_label.config(text=msg, fg="green")
                self.desc_text.delete("1.0", tk.END)
                self.time_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Błąd", msg)

            self.save_btn.config(state="normal")

        except queue.Empty:
            self.after(100, self.check_queue)

# START
if __name__ == "__main__":
    model = MaintenanceModel()
    app = App(model)
    app.mainloop()
