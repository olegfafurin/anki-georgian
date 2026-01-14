import pytesseract
from PIL import Image
import os
import sys

def process_images(image_paths, output_file):
    """
    Extracts Georgian text from images using Tesseract and writes it to an output file.
    Supports both modern ('kat') and old ('kat_old') Georgian scripts.
    """
    
    extracted_lines = set()

    for image_path in image_paths:
        if not os.path.exists(image_path):
            print(f"Warning: File not found: {image_path}", file=sys.stderr)
            continue
        
        print(f"Processing {image_path}...")
        try:
            # Load the image using Pillow
            image = Image.open(image_path)
            
            # Perform OCR using Tesseract
            # lang='kat+kat_old' enables both modern and old Georgian
            text = pytesseract.image_to_string(image, lang='kat')
            
            # Process the output text
            for line in text.split('\n'):
                clean_text = line.strip()
                if clean_text:
                    extracted_lines.add(clean_text)
                    
        except Exception as e:
            print(f"Error processing {image_path}: {e}", file=sys.stderr)

    # Write results to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in sorted(list(extracted_lines)):
                f.write(line + '\n')
        print(f"Extraction complete. Results saved to {output_file}")
    except IOError as e:
        print(f"Error writing to {output_file}: {e}", file=sys.stderr)