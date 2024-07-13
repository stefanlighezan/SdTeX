import os

class SdTeX:
    def __init__(self, input_file):
        self.input_file = input_file
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    def process_sdtex_file(self):
        with open(self.input_file, 'r') as file:
            content = file.read()
            processor = Processor(content)
            processed_content = processor.process_content()

            return processed_content

        # Process the content as needed. Here we're just returning the content as is.
        return content

    def create_output_directory(self):
        output_dir = os.path.join(self.script_dir, 'Output')
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    def run(self):
        input_file_path = self.input_file

        if not os.path.isfile(input_file_path):
            print(f"Error: {input_file_path} does not exist.")
            return

        # Create the Output directory if it doesn't exist
        output_dir = self.create_output_directory()

        # Process the file
        output_content = self.process_sdtex_file()

        # Create the output file path
        output_file_path = os.path.join(output_dir, 'output.txt')

        # Write the processed content to the output file
        with open(output_file_path, 'w') as output_file:
            output_file.write(output_content)

        print(f"Processed file has been saved to {output_file_path}")
