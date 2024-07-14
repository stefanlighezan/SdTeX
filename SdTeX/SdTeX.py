import os
from Processor import Processor
from fpdf import FPDF

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

    def create_output_directory(self):
        output_dir = os.path.join(self.script_dir, 'Output')
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    def run(self):
        input_file_path = self.input_file

        if not os.path.isfile(input_file_path):
            print(f"Error: {input_file_path} does not exist.")
            return

        output_dir = self.create_output_directory()
        processed_content = self.process_sdtex_file()

        self.save_as_pdf(processed_content, output_dir)

    def save_as_pdf(self, attributes, output_dir):
        output_file_path = os.path.join(output_dir, 'output.pdf')
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        for attribute in attributes:
            if attribute['type'] == 'sdtitle':
                content = attribute['content']
                style = attribute['style']
                
                # Extract style properties
                font_size = style.get('font_size', '').strip('"').replace('dp', '').strip()
                font_color = style.get('font_color', '').strip('"')
                font_weight = style.get('font_weight', '').strip('"')
                
                # Parse hex color values
                if font_color.startswith('#') and len(font_color) == 7:
                    try:
                        r = int(font_color[1:3], 16)
                        g = int(font_color[3:5], 16)
                        b = int(font_color[5:7], 16)
                    except ValueError:
                        r, g, b = 0, 0, 0  # Default to black if parsing fails
                else:
                    r, g, b = 0, 0, 0  # Default to black if format is incorrect

                # Set font and color in PDF
                if font_weight == 'bold':
                    pdf.set_font("Arial", size=int(font_size), style='B')
                else:
                    pdf.set_font("Arial", size=int(font_size))

                pdf.set_text_color(r, g, b)
                
                pdf.multi_cell(0, 10, content)
            
        pdf.output(output_file_path)
        print(f"PDF file has been saved to {output_file_path}")


def main():
    sdtex = SdTeX("../main.sdtex")
    sdtex.run()

if __name__ == "__main__":
    main()
