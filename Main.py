import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
from barcode import Code128
from barcode.writer import ImageWriter

# Database setup
def setup_database():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        serial_number INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL
    )
    """)
    conn.commit()
    conn.close()

# Generate Code Function
def generate_code_gui():
    name = name_var.get()
    price = price_var.get()

    if not name or not price:
        messagebox.showerror("Input Error", "Please fill in all fields!")
        return

    try:
        price = float(price)
    except ValueError:
        messagebox.showerror("Input Error", "Price must be a valid number!")
        return

    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
    conn.commit()

    serial_number = cursor.lastrowid
    conn.close()

    barcode = Code128(str(serial_number), writer=ImageWriter())
    barcode.save(f"barcode_{serial_number}")
    messagebox.showinfo("Success", f"Barcode generated for Serial Number: {serial_number}\nSaved as barcode_{serial_number}.png")
    name_var.set("")
    price_var.set("")
    name_entry.focus_set()

# Display Product Function
def display_product_gui():
    barcode_input = barcode_var.get()

    if not barcode_input:
        messagebox.showerror("Input Error", "Please enter a barcode number!")
        return

    try:
        serial_number = int(barcode_input)
    except ValueError:
        messagebox.showerror("Input Error", "Barcode number must be a valid integer!")
        return

    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE serial_number = ?", (serial_number,))
    product = cursor.fetchone()
    conn.close()

    if product:
        messagebox.showinfo("Product Details", f"Serial Number: {product[0]}\nName: {product[1]}\nPrice: {product[2]}")
    else:
        messagebox.showerror("Not Found", "No product found with this barcode.")
    barcode_var.set("")
    barcode_entry.focus_set()

# Handle Enter Key Press
def handle_enter_price(event):
    name = name_var.get().strip()
    price = price_var.get().strip()

    if not name and not price:
        barcode_entry.focus_set()  # Jump to Barcode field if both fields are empty
    else:
        generate_code_gui()  # Generate the code if fields are filled

# GUI Setup
root = Tk()
root.title("Product Code Manager")
root.geometry("400x300")

setup_database()

# Variables
name_var = StringVar()
price_var = StringVar()
barcode_var = StringVar()

# Widgets
Label(root, text="Product Code Manager", font=("Arial", 16)).pack(pady=10)

Label(root, text="Product Name:").pack()
name_entry = Entry(root, textvariable=name_var)
name_entry.pack()

Label(root, text="Product Price:").pack()
price_entry = Entry(root, textvariable=price_var)
price_entry.pack()

Button(root, text="Generate Code", command=generate_code_gui).pack(pady=10)

Label(root, text="Enter Barcode Number:").pack()
barcode_entry = Entry(root, textvariable=barcode_var)
barcode_entry.pack()

Button(root, text="Display Product", command=display_product_gui).pack(pady=10)

# Bind Enter Key to Actions
name_entry.bind("<Return>", lambda event: price_entry.focus_set())  # Jump to Price on Enter
price_entry.bind("<Return>", handle_enter_price)  # Handle logic for Price field
barcode_entry.bind("<Return>", lambda event: display_product_gui())  # Display product on Enter

# Main Loop
root.mainloop()
