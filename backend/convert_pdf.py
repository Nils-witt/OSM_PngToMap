"""
convert_pdf.py
Converts a given PDF file to PNG format.
Usage:
    python convert_pdf.py <path_to_pdf>
"""
import sys
import os

from PIL.Image import Image
from pdf2image import convert_from_path, convert_from_bytes

Image.MAX_IMAGE_PIXELS = None
# Main function to handle PDF to PNG conversion
def main():
    if len(sys.argv) != 2:
        print("Usage: python convert_pdf.py <path_to_pdf>")
        sys.exit(1)
    pdf_path = sys.argv[1]
    if not os.path.isfile(pdf_path):
        print(f"File not found: {pdf_path}")
        sys.exit(1)
    print(f"Converting PDF: {pdf_path}")
    images = convert_from_path(pdf_path, strict=True, use_cropbox=True, dpi=200)
    for i, image in enumerate(images):
        output_path = f"{os.path.splitext(pdf_path)[0]}_page{i+1}.jpg"
        image.save(output_path,  'JPEG')
        print(image.size)
        print(f"Saved: {output_path}")

if __name__ == "__main__":
    main()

