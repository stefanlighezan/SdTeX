import argparse
from SdTeX import SdTeX

def main():
    parser = argparse.ArgumentParser(description='SdTeX - A simple text formatter')
    parser.add_argument('input_file', help='The input .sdtex file to process')
    parser.add_argument('-md', action='store_true', help='Export as Markdown')
    parser.add_argument('-pdf', action='store_true', help='Export as PDF')

    args = parser.parse_args()

    sdtex = SdTeX(args.input_file)
    sdtex.run()

if __name__ == "__main__":
    main()
