from barcode import EAN13
from barcode.writer import ImageWriter
from IPython.display import Image, display
import os

def gen_and_display_barcode(number):
    # To check whether the length of number is 13 or not
    if len(number) != 13:  
        print("Error: EAN13 barcode requires a 13-digit number.")
        return

    barcode = EAN13(number, writer=ImageWriter())
    filename = f"barcode_{number}"  # unique filename based on the number
    barcode.save(filename)

    # Ensure the file is saved with '.png' extension
    barcode_image_path = f"{filename}.png"
    
    # Display the image
    if os.path.exists(barcode_image_path):
        display(Image(filename=barcode_image_path))
    else:
        print(f"Error: Failed to save the barcode image.")

if __name__ == "__main__":
    number = input("Enter :")  # Ensure this is a 13-digit number
    gen_and_display_barcode(number)