from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import ast

# Function to parse text file and convert it to a list of dictionaries
def parse_text_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    data = []
    for line in lines:
        try:
            item = ast.literal_eval(line.strip())
            if isinstance(item, dict):  # Ensure it is a dictionary
                data.append(item)
            else:
                print(f"Skipped line (not a dictionary): {line.strip()}")
        except (ValueError, SyntaxError) as e:
            print(f"Error parsing line: {line.strip()} - {e}")
    
    return data

# Function to generate an invoice PDF
def generate_invoice_pdf(data, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Set title and header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1 * inch, height - 1 * inch, "Invoice")

    # Set font for the rest of the document
    c.setFont("Helvetica", 12)

    # Add items to the PDF
    y_position = height - 2 * inch
    total_price = 0

    for item in data:
        item_name = item.get('item_name', 'Unknown Item')
        quantity = item.get('quantity', 0)
        price = item.get('price', 0)
        item_total = quantity * price
        total_price += item_total

        line = f"{item_name} x{quantity} @ Rs. {price} each = Rs. {item_total}"
        c.drawString(1 * inch, y_position, line)
        y_position -= 0.5 * inch

    # Add total amount
    c.drawString(1 * inch, y_position, f"\nTotal Amount: Rs. {total_price}")

    c.save()

# Main function to create the invoice
def main():
    input_filename = 'example.txt'  # Change to your file's name
    output_filename = 'invoice.pdf'
    data = parse_text_file(input_filename)
    if data:
        generate_invoice_pdf(data, output_filename)
        print(f"Invoice has been generated and saved to {output_filename}")
    else:
        print("No valid data to generate the invoice.")

if __name__ == "__main__":
    main()
