import argparse
from SdTeX import SdTeX

def main():
    parser = argparse.ArgumentParser(description='SdTeX - A simple text formatter')
    parser.add_argument('input_file', help='The input .sdtex file to process')

    args = parser.parse_args()
    input_file = args.input_file

    sdtex = SdTeX(input_file)
    sdtex.run()

if __name__ == "__main__":
    main()
