import genanki
import random
import os
import sys

# Define the Anki model
# We use a unique model ID
MODEL_ID = 1607392319
GEORGIAN_MODEL = genanki.Model(
    MODEL_ID,
    'Georgian to Cyrillic Model',
    fields=[
        {'name': 'Expression'},
        {'name': 'Pronunciation'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '<div style="font-family: Arial; font-size: 60px; text-align: center;">{{Expression}}</div>',
            'afmt': '{{FrontSide}}<hr id="answer"><div style="font-family: Arial; font-size: 40px; text-align: center;">{{Pronunciation}}</div>',
        },
    ],
    css='.card { font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white; }'
)

def create_deck(input_file, output_deck_name):
    """
    Reads 'Georgian - Cyrillic' file and generates an Anki deck (.apkg).
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.", file=sys.stderr)
        return

    # Use a unique deck ID based on the deck name
    deck_id = random.randrange(1 << 30, 1 << 31)
    deck = genanki.Deck(deck_id, output_deck_name)

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or ' - ' not in line:
                    continue
                
                georgian, cyrillic = line.split(' - ', 1)
                
                note = genanki.Note(
                    model=GEORGIAN_MODEL,
                    fields=[georgian, cyrillic]
                )
                deck.add_note(note)

        output_file = f"{output_deck_name.replace(' ', '_')}.apkg"
        genanki.Package(deck).write_to_file(output_file)
        print(f"Anki deck created successfully: {output_file}")

    except Exception as e:
        print(f"Error creating Anki deck: {e}", file=sys.stderr)
