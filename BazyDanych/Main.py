import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# ---------------------- baza danych ----------------------

def polacz_z_baza():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="kino"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("blad polaczenia", f"nie mozna polaczyc z baza: {err}")
        return None


def dodaj_film(tytul, rezyser, rok, ocena):
    conn = polacz_z_baza()
    if not conn:
        return
    cursor = conn.cursor()
    sql = "INSERT INTO Filmy (tytul, rezyser, rok, ocena) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(sql, (tytul, rezyser, rok, ocena))
        conn.commit()
        messagebox.showinfo("Sukces", "Film dodany.")
    except mysql.connector.Error as err:
        messagebox.showerror("blad", err)
    finally:
        cursor.close()
        conn.close()


def pobierz_filmy(fraza=""):
    conn = polacz_z_baza()
    if not conn:
        return []
    cursor = conn.cursor()
    if fraza:
        sql = "SELECT * FROM Filmy WHERE tytul LIKE %s"
        cursor.execute(sql, (f"%{fraza}%",))
    else:
        cursor.execute("SELECT * FROM Filmy")
    wyniki = cursor.fetchall()
    cursor.close()
    conn.close()
    return wyniki


def usun_film(id_filmu):
    conn = polacz_z_baza()
    if not conn:
        return
    cursor = conn.cursor()
    sql = "DELETE FROM Filmy WHERE id=%s"
    try:
        cursor.execute(sql, (id_filmu,))
        conn.commit()
        messagebox.showinfo("usunieto", "film usuniety")
    except mysql.connector.Error as err:
        messagebox.showerror("blad", err)
    finally:
        cursor.close()
        conn.close()


def aktualizuj_film(id_filmu, tytul, rezyser, rok, ocena):
    conn = polacz_z_baza()
    if not conn:
        return
    cursor = conn.cursor()
    sql = "UPDATE Filmy SET tytul=%s, rezyser=%s, rok=%s, ocena=%s WHERE id=%s"
    try:
        cursor.execute(sql, (tytul, rezyser, rok, ocena, id_filmu))
        conn.commit()
        messagebox.showinfo("zaktualizowano", "film zostal zaktualizowany.")
    except mysql.connector.Error as err:
        messagebox.showerror("blad", err)
    finally:
        cursor.close()
        conn.close()


# ---------------------- GUI ----------------------

def odswiez(tree, fraza=""):
    for x in tree.get_children():
        tree.delete(x)
    for film in pobierz_filmy(fraza):
        tree.insert("", tk.END, values=film)


def otworz_okno_edycji(tree):
    try:
        wybrane = tree.item(tree.selection()[0])["values"]
    except:
        messagebox.showwarning("uwaga", "najpierw wybierz film z listy.")
        return

    id_filmu, tytul, rezyser, rok, ocena = wybrane

    okno = tk.Toplevel()
    okno.title("edytuj Film")

    # pola
    ttk.Label(okno, text="tytul:").grid(row=0, column=0)
    tyt_var = tk.StringVar(value=tytul)
    ttk.Entry(okno, textvariable=tyt_var).grid(row=0, column=1)

    ttk.Label(okno, text="rezyser:").grid(row=1, column=0)
    rez_var = tk.StringVar(value=rezyser)
    ttk.Entry(okno, textvariable=rez_var).grid(row=1, column=1)

    ttk.Label(okno, text="rok:").grid(row=2, column=0)
    rok_var = tk.StringVar(value=str(rok))
    ttk.Entry(okno, textvariable=rok_var).grid(row=2, column=1)

    ttk.Label(okno, text="ocena:").grid(row=3, column=0)
    oc_var = tk.StringVar(value=str(ocena))
    ttk.Entry(okno, textvariable=oc_var).grid(row=3, column=1)

    def zapisz():
        try:
            aktualizuj_film(
                id_filmu,
                tyt_var.get(),
                rez_var.get(),
                int(rok_var.get()),
                float(oc_var.get())
            )
            odswiez(tree)
            okno.destroy()
        except ValueError:
            messagebox.showerror("blad", "rok musi byc liczba, ocena float.")

    ttk.Button(okno, text="zapisz", command=zapisz).grid(row=4, column=0, columnspan=2, pady=10)


# ---------------------- main ----------------------

root = tk.Tk()
root.title("katalog filmow")


# ---- formularz ----

frame = ttk.Frame(root, padding=10)
frame.pack(fill="x")

tyt_var = tk.StringVar()
rez_var = tk.StringVar()
rok_var = tk.StringVar()
oc_var = tk.StringVar()
szukaj_var = tk.StringVar()

ttk.Label(frame, text="tytul:").grid(row=0, column=0)
ttk.Entry(frame, textvariable=tyt_var, width=30).grid(row=0, column=1)

ttk.Label(frame, text="rezyser:").grid(row=1, column=0)
ttk.Entry(frame, textvariable=rez_var, width=30).grid(row=1, column=1)

ttk.Label(frame, text="rok:").grid(row=2, column=0)
ttk.Entry(frame, textvariable=rok_var, width=10).grid(row=2, column=1, sticky="w")

ttk.Label(frame, text="ocena:").grid(row=3, column=0)
ttk.Entry(frame, textvariable=oc_var, width=10).grid(row=3, column=1, sticky="w")


def obsluga_dodawania():
    try:
        dodaj_film(tyt_var.get(), rez_var.get(), int(rok_var.get()), float(oc_var.get()))
        odswiez(tree)
        tyt_var.set(""); rez_var.set(""); rok_var.set(""); oc_var.set("")
    except ValueError:
        messagebox.showerror("blad", "rok musi być liczba, ocena liczba.")


ttk.Button(frame, text="dodaj film", command=obsluga_dodawania)\
    .grid(row=4, column=0, columnspan=2, pady=10)


# ---- wyszukiwanie ----

ttk.Label(frame, text="szukaj tytulu:").grid(row=5, column=0)
ttk.Entry(frame, textvariable=szukaj_var, width=30).grid(row=5, column=1)

ttk.Button(frame, text="szukaj", command=lambda: odswiez(tree, szukaj_var.get()))\
    .grid(row=6, column=0, columnspan=2, pady=5)


# ---- treeview ----

columns = ("id", "tytul", "rezyser", "rok", "ocena")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, width=120)

tree.pack(fill="both", expand=True, padx=10, pady=10)


# ---- update/delete ----

btn_frame = ttk.Frame(root, padding=10)
btn_frame.pack()

ttk.Button(btn_frame, text="edytuj wybrany", command=lambda: otworz_okno_edycji(tree))\
    .grid(row=0, column=0, padx=10)

ttk.Button(btn_frame, text="usun wybrany",
           command=lambda: (
               usun_film(tree.item(tree.selection()[0])["values"][0]),
               odswiez(tree)
           ))\
    .grid(row=0, column=1, padx=10)


# Start
odswiez(tree)
root.mainloop()
