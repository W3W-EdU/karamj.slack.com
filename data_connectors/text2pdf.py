from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def text_to_pdf(text, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)

    # Define the font and size
    font_name = 'Helvetica'
    font_size = 12

    # Set the starting position for the text
    x, y = 50, 750

    # Split the text into lines and write to the PDF
    for line in text.split('\n'):
        c.setFont(font_name, font_size)
        c.drawString(x, y, line)
        y -= 20  # Move to the next line

    c.save()

def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == '__main__':
    text_file_path = 'LL_RN.txt'
    text_to_convert = read_text_from_file(text_file_path)

    output_file_path = 'output.pdf'
    text_to_pdf(text_to_convert, output_file_path)

    print(f"Text from '{text_file_path}' has been converted to '{output_file_path}' as a PDF.")
