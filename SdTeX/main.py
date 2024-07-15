import argparse
from SdTeX import SdTeX

def main():
    """
    Command-line arguments:
    - input_file: The .sdtex file to process.
    - -pdf: Optional flag to export as PDF.

    Usage example:
    python main.py main.sdtex -pdf
    """
    parser = argparse.ArgumentParser(description='SdTeX - A magical alternative to modern typesetting systems (I\'m looking at you, LaTeX), made in two days, by a high schooler😉')
    parser.add_argument('input_file', help='The .sdtex file to process')
    parser.add_argument('-pdf', action='store_true', help='Export as PDF (default)')

    args = parser.parse_args()

    # Initialize SdTeX processor with input file
    sdtex = SdTeX(args.input_file)

    # Run the SdTeX processing
    sdtex.run()

if __name__ == "__main__":
    main()
