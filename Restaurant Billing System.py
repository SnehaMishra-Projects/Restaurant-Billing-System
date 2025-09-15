from tkinter import *
from tkinter import ttk, messagebox
import random
import time
import datetime
import csv
import os
import platform
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

root = Tk()
root.geometry("1600x8000")
root.title("Restaurant Management System")

# === Elegant Cafe Theme Colors ===
BG_COLOR = "#2C2C2C"       # Dark Grey
TEXT_COLOR = "#FFD700"     # Gold
BTN_COLOR = "#FF6347"      # Tomato Red
ENTRY_COLOR = "#FFFACD"    # Lemon Chiffon
BTN_TEXT = "white"

root.configure(bg=BG_COLOR)

Tops = Frame(root, width=1600, relief=SUNKEN, bg=BG_COLOR)
Tops.pack(side=TOP)

f1 = Frame(root, width=800, height=700, relief=SUNKEN, bg=BG_COLOR)
f1.pack(side=LEFT)

# =================================================================================
#                  TIME
# =================================================================================
localtime = time.asctime(time.localtime(time.time()))

lblInfo = Label(Tops, font=('helvetica', 50, 'bold'),
                text="SUNSET CAFE", fg=TEXT_COLOR, bg=BG_COLOR, bd=10, anchor='w')
lblInfo.grid(row=0, column=0)

lblInfo = Label(Tops, font=('arial', 20, 'bold'),
                text=localtime, fg=TEXT_COLOR, bg=BG_COLOR, bd=10, anchor='w')
lblInfo.grid(row=1, column=0)


def Ref():
    x = random.randint(10908, 500876)
    randomRef = str(x)
    rand.set(randomRef)

    CoFries = float(Fries.get() or 0)
    CoNoodles = float(Noodles.get() or 0)
    CoSoup = float(Soup.get() or 0)
    CoBurger = float(Burger.get() or 0)
    CoSandwich = float(Sandwich.get() or 0)
    CoD = float(Drinks.get() or 0)

    CostofFries = CoFries * 140
    CostofDrinks = CoD * 65
    CostofNoodles = CoNoodles * 90
    CostofSoup = CoSoup * 140
    CostBurger = CoBurger * 260
    CostSandwich = CoSandwich * 300

    TotalCost = (CostofFries + CostofDrinks + CostofNoodles +
                 CostofSoup + CostBurger + CostSandwich)

    PayTax = (TotalCost * 0.2)
    Ser_Charge = (TotalCost / 99)

    CostofMeal = "Rs", str('%.2f' % TotalCost)
    PaidTax = "Rs", str('%.2f' % PayTax)
    Service = "Rs", str('%.2f' % Ser_Charge)
    OverAllCost = "Rs", str('%.2f' % (PayTax + TotalCost + Ser_Charge))

    Service_Charge.set(Service)
    Cost.set(CostofMeal)
    Tax.set(PaidTax)
    SubTotal.set(CostofMeal)
    Total.set(OverAllCost)

    # ================= SAVE TO CSV =================
    with open("bills.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Write header only if file is new
            writer.writerow([
                "Reference", "DateTime", "Fries", "Noodles", "Soup", "Burger", "Sandwich", "Drinks",
                "Subtotal", "Tax", "Service Charge", "Total"
            ])
        writer.writerow([
            randomRef,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            Fries.get() or 0,
            Noodles.get() or 0,
            Soup.get() or 0,
            Burger.get() or 0,
            Sandwich.get() or 0,
            Drinks.get() or 0,
            SubTotal.get(),
            Tax.get(),
            Service_Charge.get(),
            Total.get()
        ])


def qExit():
    root.destroy()


def Reset():
    rand.set("")
    Fries.set("")
    Noodles.set("")
    Soup.set("")
    SubTotal.set("")
    Total.set("")
    Service_Charge.set("")
    Drinks.set("")
    Tax.set("")
    Cost.set("")
    Burger.set("")
    Sandwich.set("")


# ================= Print Current Bill =================
def printCurrentBill():
    if not rand.get() or not Total.get():
        messagebox.showwarning("Warning", "Please calculate the bill first!")
        return

    ref_no = rand.get()
    filename = f"Bill_{ref_no}_current.pdf"

    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, 770, "Lakeyard Restaurant")
    c.setFont("Helvetica", 12)
    c.drawString(200, 750, f"Bill Receipt - Reference: {ref_no}")
    c.drawString(200, 735, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Table headers
    y = 700
    c.setFont("Helvetica-Bold", 12)
    c.drawString(80, y, "Item")
    c.drawString(250, y, "Qty")
    c.drawString(320, y, "Price")
    c.drawString(400, y, "Total")
    c.line(70, y-5, 500, y-5)

    # Item details
    y -= 25
    c.setFont("Helvetica", 12)
    menu = [
        ("Fries", Fries.get() or 0, 140),
        ("Noodles", Noodles.get() or 0, 90),
        ("Soup", Soup.get() or 0, 140),
        ("Burger", Burger.get() or 0, 260),
        ("Sandwich", Sandwich.get() or 0, 300),
        ("Drinks", Drinks.get() or 0, 65)
    ]

    for item, qty, price in menu:
        qty = int(qty)
        if qty > 0:
            line_total = qty * price
            c.drawString(80, y, item)
            c.drawString(250, y, str(qty))
            c.drawString(320, y, f"Rs {price}")
            c.drawString(400, y, f"Rs {line_total}")
            y -= 20

    # Summary
    y -= 15
    c.line(70, y, 500, y)
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(300, y, "Subtotal:")
    c.drawString(400, y, SubTotal.get())

    y -= 20
    c.drawString(300, y, "Tax (20%):")
    c.drawString(400, y, Tax.get())

    y -= 20
    c.drawString(300, y, "Service Charge:")
    c.drawString(400, y, Service_Charge.get())

    y -= 20
    c.drawString(300, y, "Grand Total:")
    c.drawString(400, y, Total.get())

    # Footer
    y -= 40
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(200, y, "Thank you for dining with us!")

    c.save()

    # Auto-open PDF after saving
    try:
        if platform.system() == "Windows":
            os.startfile(filename)  # Opens in default PDF viewer
        elif platform.system() == "Darwin":  # macOS
            os.system(f"open {filename}")
        else:  # Linux
            os.system(f"xdg-open {filename}")
    except:
        messagebox.showinfo("Saved", f"Bill saved as PDF: {filename}\nPlease open manually.")


# ================= View Bills with Search, Export =================
def viewBills():
    try:
        bill_window = Toplevel(root)
        bill_window.title("Billing Records")
        bill_window.geometry("1000x500")

        search_frame = Frame(bill_window)
        search_frame.pack(pady=10)

        lblSearch = Label(search_frame, text="Search by Reference No:", font=("arial", 12, "bold"))
        lblSearch.grid(row=0, column=0, padx=5)

        search_var = StringVar()
        txtSearch = Entry(search_frame, textvariable=search_var, font=("arial", 12), width=20)
        txtSearch.grid(row=0, column=1, padx=5)

        cols = ("Reference", "DateTime", "Fries", "Noodles", "Soup", "Burger",
                "Sandwich", "Drinks", "Subtotal", "Tax", "Service Charge", "Total")
        tree = ttk.Treeview(bill_window, columns=cols, show="headings")

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=90, anchor="center")

        tree.pack(fill=BOTH, expand=True)

        scrollbar = ttk.Scrollbar(bill_window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        def load_data(ref_filter=None):
            tree.delete(*tree.get_children())
            with open("bills.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if ref_filter:
                        if row[0] == ref_filter:
                            tree.insert("", END, values=row)
                    else:
                        tree.insert("", END, values=row)

        load_data()

        def search_bill():
            ref = search_var.get().strip()
            if ref:
                load_data(ref)
            else:
                load_data()

        btnSearch = Button(search_frame, text="Search", font=("arial", 12, "bold"),
                           bg="powder blue", command=search_bill)
        btnSearch.grid(row=0, column=2, padx=5)

        def export_pdf():
            selected = tree.focus()
            if not selected:
                messagebox.showwarning("Warning", "Please select a bill first.")
                return

            bill_data = tree.item(selected, "values")
            ref_no = bill_data[0]
            filename = f"Bill_{ref_no}.pdf"

            qtys = {
                "Fries": int(bill_data[2]),
                "Noodles": int(bill_data[3]),
                "Soup": int(bill_data[4]),
                "Burger": int(bill_data[5]),
                "Sandwich": int(bill_data[6]),
                "Drinks": int(bill_data[7])
            }
            prices = {"Fries": 140, "Noodles": 90, "Soup": 140,
                      "Burger": 260, "Sandwich": 300, "Drinks": 65}

            subtotal = bill_data[8]
            tax = bill_data[9]
            service = bill_data[10]
            total = bill_data[11]
            date_time = bill_data[1]

            c = canvas.Canvas(filename, pagesize=letter)
            c.setFont("Helvetica-Bold", 18)
            c.drawString(200, 770, "Lakeyard Restaurant")
            c.setFont("Helvetica", 12)
            c.drawString(200, 750, f"Bill Receipt - Reference: {ref_no}")
            c.drawString(200, 735, f"Date: {date_time}")

            y = 700
            c.setFont("Helvetica-Bold", 12)
            c.drawString(80, y, "Item")
            c.drawString(250, y, "Qty")
            c.drawString(320, y, "Price")
            c.drawString(400, y, "Total")
            c.line(70, y-5, 500, y-5)

            y -= 25
            c.setFont("Helvetica", 12)
            for item, qty in qtys.items():
                if qty > 0:
                    line_total = qty * prices[item]
                    c.drawString(80, y, item)
                    c.drawString(250, y, str(qty))
                    c.drawString(320, y, f"Rs {prices[item]}")
                    c.drawString(400, y, f"Rs {line_total}")
                    y -= 20

            y -= 15
            c.line(70, y, 500, y)
            y -= 20
            c.setFont("Helvetica-Bold", 12)
            c.drawString(300, y, "Subtotal:")
            c.drawString(400, y, subtotal)

            y -= 20
            c.drawString(300, y, "Tax (20%):")
            c.drawString(400, y, tax)

            y -= 20
            c.drawString(300, y, "Service Charge:")
            c.drawString(400, y, service)

            y -= 20
            c.drawString(300, y, "Grand Total:")
            c.drawString(400, y, total)

            y -= 40
            c.setFont("Helvetica-Oblique", 10)
            c.drawString(200, y, "Thank you for dining with us!")

            c.save()

            try:
                if platform.system() == "Windows":
                    os.startfile(filename)
                elif platform.system() == "Darwin":
                    os.system(f"open {filename}")
                else:
                    os.system(f"xdg-open {filename}")
            except:
                messagebox.showinfo("Saved", f"Bill saved as PDF: {filename}\nPlease open manually.")

        btnExport = Button(search_frame, text="Export PDF", font=("arial", 12, "bold"),
                           bg="lightgreen", command=export_pdf)
        btnExport.grid(row=0, column=3, padx=5)

    except FileNotFoundError:
        messagebox.showerror("Error", "No billing records found!")


# ==================================== Variables ===========================================================
rand = StringVar()
Fries = StringVar()
Noodles = StringVar()
Soup = StringVar()
SubTotal = StringVar()
Total = StringVar()
Service_Charge = StringVar()
Drinks = StringVar()
Tax = StringVar()
Cost = StringVar()
Burger = StringVar()
Sandwich = StringVar()

# ==================================== Widgets ===========================================================
def make_label(frame, text, r, c):
    lbl = Label(frame, font=('arial', 16, 'bold'),
                text=text, bd=16, anchor="w", fg=TEXT_COLOR, bg=BG_COLOR)
    lbl.grid(row=r, column=c)
    return lbl

def make_entry(frame, var, r, c):
    ent = Entry(frame, font=('arial', 16, 'bold'),
                textvariable=var, bd=10, insertwidth=4,
                bg=ENTRY_COLOR, fg="black", justify='right')
    ent.grid(row=r, column=c)
    return ent

make_label(f1, "Reference", 0, 0)
make_entry(f1, rand, 0, 1)

make_label(f1, "Fries", 1, 0)
make_entry(f1, Fries, 1, 1)

make_label(f1, "Noodles", 2, 0)
make_entry(f1, Noodles, 2, 1)

make_label(f1, "Soup", 3, 0)
make_entry(f1, Soup, 3, 1)

make_label(f1, "Burger", 4, 0)
make_entry(f1, Burger, 4, 1)

make_label(f1, "Sandwich", 5, 0)
make_entry(f1, Sandwich, 5, 1)

make_label(f1, "Drinks", 0, 2)
make_entry(f1, Drinks, 0, 3)

make_label(f1, "Cost of Meal", 1, 2)
make_entry(f1, Cost, 1, 3)

make_label(f1, "Service Charge", 2, 2)
make_entry(f1, Service_Charge, 2, 3)

make_label(f1, "State Tax", 3, 2)
make_entry(f1, Tax, 3, 3)

make_label(f1, "Sub Total", 4, 2)
make_entry(f1, SubTotal, 4, 3)

make_label(f1, "Total Cost", 5, 2)
make_entry(f1, Total, 5, 3)

# ========================================== Buttons ========================================================
def make_button(frame, text, r, c, cmd, w=12, color=BTN_COLOR):
    btn = Button(frame, padx=16, pady=8, bd=16, fg=BTN_TEXT,
                 font=('arial', 16, 'bold'), width=w,
                 text=text, bg=color, command=cmd)
    btn.grid(row=r, column=c, padx=5, pady=5)
    return btn

make_button(f1, "View Bills", 7, 0, lambda: viewBills())
make_button(f1, "Total", 7, 1, lambda: Ref(), 10)
make_button(f1, "Reset", 7, 2, lambda: Reset(), 10)
make_button(f1, "Exit", 7, 3, lambda: qExit(), 10, "#DC143C")  # Crimson Exit
make_button(f1, "Save & Open Bill (PDF)", 8, 1, lambda: printCurrentBill(), 20, "#32CD32")  # Green

root.mainloop()
