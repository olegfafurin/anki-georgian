import sys
import os

# Mapping of the 33 modern Georgian characters to their Cyrillic approximations
GEORGIAN_TO_CYRILLIC = {
    'ა': 'а',
    'ბ': 'б',
    'გ': 'г',
    'დ': 'д',
    'ე': 'э',
    'ვ': 'в',
    'ზ': 'з',
    'თ': 'т',
    'ი': 'и',
    'კ': 'к',
    'ლ': 'л',
    'მ': 'м',
    'ნ': 'н',
    'ო': 'о',
    'პ': 'п',
    'ჟ': 'ж',
    'რ': 'р',
    'ს': 'с',
    'ტ': 'т',
    'უ': 'у',
    'ფ': 'п',
    'ქ': 'к',
    'ღ': 'г',
    'ყ': 'к',
    'შ': 'ш',
    'ჩ': 'ч',
    'ც': 'ц',
    'ძ': 'дз',
    'წ': 'ц',
    'ჭ': 'ч',
    'ხ': 'х',
    'ჯ': 'дж',
    'ჰ': 'х',
}

def transliterate_text(text):
    """Transliterates a string of Georgian text into Cyrillic."""
    result = ""
    for char in text:
        result += GEORGIAN_TO_CYRILLIC.get(char, char)
    return result

def transliterate_file(input_file, output_file):
    """
    Reads Georgian text from input_file and writes 
    'Georgian Text - Cyrillic Transliteration' to output_file.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.", file=sys.stderr)
        return

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        transliterated_lines = []
        for line in lines:
            georgian_text = line.strip()
            if georgian_text:
                cyrillic_text = transliterate_text(georgian_text)
                transliterated_lines.append(f"{georgian_text} - {cyrillic_text}")

        with open(output_file, 'w', encoding='utf-8') as f:
            for line in transliterated_lines:
                f.write(line + '\n')
        
        print(f"Transliteration complete. Results saved to {output_file}")
        
    except Exception as e:
         print(f"Error during transliteration: {e}", file=sys.stderr)
