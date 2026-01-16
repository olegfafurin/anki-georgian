import argparse
import sys
import logging
from ocr import process_images
from transliteration import transliterate_file
from anki_maker import create_deck, update_deck

def extract_command(args):
    process_images(args.images, args.output)

def transliterate_command(args):
    transliterate_file(args.input, args.output)

def create_deck_command(args):
    if args.update:
        update_deck(args.input, args.update)
    else:
        create_deck(args.input, args.name)

def main():
    parser = argparse.ArgumentParser(description="Georgian Anki Card Generator")
    parser.add_argument("--log", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO", help="Set the logging level")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Extract subcommand
    extract_parser = subparsers.add_parser("extract", help="Extract Georgian text from images")
    extract_parser.add_argument("images", nargs="+", help="Path to image files")
    extract_parser.add_argument("-o", "--output", default="extracted_text.txt", help="Output text file")
    extract_parser.set_defaults(func=extract_command)

    # Transliterate subcommand
    trans_parser = subparsers.add_parser("transliterate", help="Transliterate Georgian text to Cyrillic")
    trans_parser.add_argument("input", help="Input text file with Georgian text")
    trans_parser.add_argument("-o", "--output", default="transliterated_text.txt", help="Output text file")
    trans_parser.set_defaults(func=transliterate_command)

    # Create-deck subcommand
    deck_parser = subparsers.add_parser("create-deck", help="Generate an Anki deck (.apkg)")
    deck_parser.add_argument("input", help="Input text file (Georgian - Cyrillic)")
    deck_parser.add_argument("-n", "--name", default="Georgian Alphabet", help="Name of the Anki deck")
    deck_parser.add_argument("--update", help="Path to an existing .apkg deck to update")
    deck_parser.set_defaults(func=create_deck_command)

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log),
        format='%(levelname)s: %(message)s'
    )

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
