import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from barcode import Code128
from barcode.writer import ImageWriter
import os
from barcode.codex import Code128
from barcode.writer import ImageWriter


# File to store product data
DATA_FILE = 'product_data.csv'

# Initialize the data file if it doesn't exist
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=['Serial_Number', 'Name', 'Price']).to_csv(DATA_FILE, index=False)


# Function to generate a new product entry
def generate_code(name, price):
    try:
        # Load existing data
        data = pd.read_csv(DATA_FILE)
        serial_number = len(data) + 1  # Auto-increment serial number

        # Save the barcode as an image
        barcode = Code128(str(serial_number), writer=ImageWriter())
        barcode_filename = f"barcode_{serial_number}.png"
        barcode.save(barcode_filename)

        # Save the new entry to the CSV
        new_entry = {'Serial_Number': serial_number, 'Name': name, 'Price': price}
        data = data.append(new_entry, ignore_index=True)
        data.to_csv(DATA_FILE, index=False)

        messagebox.showinfo("Success", f"Product added!\nSerial Number: {serial_number}\nBarcode saved as {barcode_filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate code: {e}")


# Function to display a product based on serial number
def display_product(serial_number):
    try:
        # Load the data
        data = pd.read_csv(DATA_FILE)
        product = data[data['Serial_Number'] == int(serial_number)]

        if not product.empty:
            product_details = f"Serial Number: {serial_number}\nName: {product.iloc[0]['Name']}\nPrice: {product.iloc[0]['Price']}"
            messagebox.showinfo("Product Details", product_details)
        else:
            messagebox.showwarning("Not Found", "Product not found!")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid serial number!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to display product: {e}")


# Main GUI Application
class BarcodeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Product Management with Barcodes")
        self.geometry("400x400")
        self.resizable(False, False)

        # Tabs for Generate Code and Display Product
        self.tabs = ttk.Notebook(self)
        self.tab_generate = ttk.Frame(self.tabs)
        self.tab_display = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_generate, text="Generate Code")
        self.tabs.add(self.tab_display, text="Display Product")
        self.tabs.pack(expand=1, fill="both")

        self.create_generate_tab()
        self.create_display_tab()

    def create_generate_tab(self):
        # Widgets for Generate Code Tab
        ttk.Label(self.tab_generate, text="Enter Product Name:").pack(pady=10)
        self.name_entry = ttk.Entry(self.tab_generate, width=30)
        self.name_entry.pack()

        ttk.Label(self.tab_generate, text="Enter Product Price:").pack(pady=10)
        self.price_entry = ttk.Entry(self.tab_generate, width=30)
        self.price_entry.pack()

        ttk.Button(self.tab_generate, text="Generate Code", command=self.handle_generate).pack(pady=20)

    def create_display_tab(self):
        # Widgets for Display Product Tab
        ttk.Label(self.tab_display, text="Enter Serial Number (Barcode):").pack(pady=10)
        self.serial_entry = ttk.Entry(self.tab_display, width=30)
        self.serial_entry.pack()

        ttk.Button(self.tab_display, text="Display Product", command=self.handle_display).pack(pady=20)

    def handle_generate(self):
        name = self.name_entry.get().strip()
        price = self.price_entry.get().strip()

        if name and price:
            try:
                price = float(price)  # Validate price as a number
                generate_code(name, price)
                self.name_entry.delete(0, tk.END)
                self.price_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid price!")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def handle_display(self):
        serial_number = self.serial_entry.get().strip()

        if serial_number:
            display_product(serial_number)
            self.serial_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Serial number is required!")


if __name__ == "__main__":
    app = BarcodeApp()
    app.mainloop()
