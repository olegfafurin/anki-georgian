import genanki
import random
import os
import sys
import zipfile
import sqlite3
import tempfile
import logging

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

def get_notes_from_apkg(apkg_path):
    """
    Extracts notes from an existing .apkg file.
    Returns a dictionary {georgian_text: cyrillic_text}.
    """
    notes = {}
    
    if not os.path.exists(apkg_path):
        logging.error(f"Existing deck file {apkg_path} not found.")
        return {}

    with tempfile.TemporaryDirectory() as tmp_dir:
        try:
            with zipfile.ZipFile(apkg_path, 'r') as z:
                z.extract('collection.anki2', path=tmp_dir)
            
            db_path = os.path.join(tmp_dir, 'collection.anki2')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Select fields from notes table
            cursor.execute("SELECT flds FROM notes")
            rows = cursor.fetchall()
            
            for row in rows:
                fields_str = row[0]
                # Anki splits fields with unit separator \x1f
                fields = fields_str.split('\x1f')
                
                # We assume the first field is Georgian (Expression) 
                # and the second is Cyrillic (Pronunciation)
                if len(fields) >= 2:
                    georgian = fields[0]
                    cyrillic = fields[1]
                    notes[georgian] = cyrillic
            
            conn.close()
            
        except Exception as e:
            logging.warning(f"Could not read existing deck {apkg_path}: {e}")
            return {}

    return notes

def create_deck(input_file, output_deck_name):
    """
    Reads 'Georgian - Cyrillic' file and generates an Anki deck (.apkg).
    """
    if not os.path.exists(input_file):
        logging.error(f"Input file {input_file} not found.")
        return

    # Use a unique deck ID based on the deck name
    deck_id = random.randrange(1 << 30, 1 << 31)
    deck = genanki.Deck(deck_id, output_deck_name)

    try:
        added_count = 0
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
                added_count += 1

        output_file = f"{output_deck_name.replace(' ', '_')}.apkg"
        genanki.Package(deck).write_to_file(output_file)
        logging.info(f"Anki deck created successfully: {output_file}, added notes: {added_count}")

    except Exception as e:
        logging.error(f"Error creating Anki deck: {e}")

def update_deck(input_file, existing_deck_path, output_deck_name):
    """
    Merges new cards from input_file into existing_deck_path, preserving existing entries.
    Generates a new .apkg file.
    """
    # 1. Read new notes
    new_notes = {}
    if os.path.exists(input_file):
         with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or ' - ' not in line:
                    continue
                georgian, cyrillic = line.split(' - ', 1)
                new_notes[georgian] = cyrillic
    else:
        logging.error(f"Input file {input_file} not found.")
        return

    # 2. Read existing notes
    existing_notes = get_notes_from_apkg(existing_deck_path)
    if not existing_notes and not os.path.exists(existing_deck_path):
         return # Error printed in helper

    logging.info(f"Found {len(existing_notes)} existing notes in {existing_deck_path}")

    # 3. Merge (Preference to existing)
    # Start with existing notes
    merged_notes = existing_notes.copy()
    added_count = 0
    
    for geo, cyr in new_notes.items():
        if geo not in merged_notes:
            merged_notes[geo] = cyr
            added_count += 1
            
    logging.info(f"Adding {added_count} new notes.")

    # 4. Generate Deck
    deck_id = random.randrange(1 << 30, 1 << 31)
    deck = genanki.Deck(deck_id, output_deck_name)

    for geo, cyr in merged_notes.items():
        note = genanki.Note(
            model=GEORGIAN_MODEL,
            fields=[geo, cyr]
        )
        deck.add_note(note)

    output_file = f"{output_deck_name.replace(' ', '_')}.apkg"
    genanki.Package(deck).write_to_file(output_file)
    logging.info(f"Updated deck created successfully: {output_file}")
