import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime


def generuj_pdf():
    produkt = entry_produkt.get()
    cena = entry_cena.get()
    vat = entry_vat.get()

    if not produkt or not cena or not vat:
        messagebox.showwarning("Błąd", "Uzupełnij wszystkie pola!")
        return

    try:
        cena = float(cena)
        vat = float(vat)

        wartosc_vat = (cena * vat) / 100
        brutto = cena + wartosc_vat

    except ValueError:
        messagebox.showerror("Błąd", "Cena i VAT muszą być liczbami!")
        return

    sciezka = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Pliki PDF", "*.pdf")],
        title="Zapisz fakturę"
    )

    if sciezka:
        try:
            c = canvas.Canvas(sciezka, pagesize=A4)
            szer, wys = A4

            # nagłówek
            c.setFont("Helvetica-Bold", 18)
            c.drawString(200, wys - 50, "FAKTURA UPROSZCZONA")

            # data
            data = datetime.now().strftime("%Y-%m-%d %H:%M")
            c.setFont("Helvetica", 10)
            c.drawString(400, wys - 80, f"Data: {data}")

            # tabela nagłówki
            c.setFont("Helvetica-Bold", 12)

            start_y = wys - 150

            c.drawString(80, start_y, "Produkt")
            c.drawString(200, start_y, "Cena Netto")
            c.drawString(300, start_y, "VAT %")
            c.drawString(360, start_y, "VAT")
            c.drawString(430, start_y, "Brutto")

            # linia
            c.line(70, start_y - 5, 520, start_y - 5)

            # dane
            c.setFont("Helvetica", 11)

            c.drawString(80, start_y - 30, produkt)
            c.drawString(200, start_y - 30, f"{cena:.2f} zł")
            c.drawString(300, start_y - 30, f"{vat:.0f}%")
            c.drawString(360, start_y - 30, f"{wartosc_vat:.2f} zł")
            c.drawString(430, start_y - 30, f"{brutto:.2f} zł")

            # zapis
            c.save()

            messagebox.showinfo("Sukces", "Faktura została wygenerowana!")

        except Exception as e:
            messagebox.showerror("Błąd", str(e))


# --- GUI ---
root = tk.Tk()
root.title("Generator Faktur")
root.geometry("350x300")

tk.Label(root, text="Nazwa produktu").pack(pady=5)
entry_produkt = tk.Entry(root, width=30)
entry_produkt.pack()

tk.Label(root, text="Cena netto").pack(pady=5)
entry_cena = tk.Entry(root, width=30)
entry_cena.pack()

tk.Label(root, text="VAT (%)").pack(pady=5)
entry_vat = tk.Entry(root, width=30)
entry_vat.pack()

tk.Button(root, text="Generuj PDF", command=generuj_pdf).pack(pady=20)

root.mainloop()