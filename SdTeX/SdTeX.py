import os
import requests
from io import BytesIO
from PIL import Image as PILImage
from fpdf import FPDF
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np
import math
from Processor import Processor
import re

class SdTeX:
    def __init__(self, input_file):
        self.input_file = input_file
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.current_y = 0  # Initialize current_y to 0

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

    def download_image(self, url, output_path):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"Failed to download image from {url}. Status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error downloading image from {url}: {e}")
            return False

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
            self.add_attribute_to_pdf(pdf, attribute)

        pdf.output(output_file_path)
        print(f"PDF file has been saved to {output_file_path}")

    def add_attribute_to_pdf(self, pdf, attribute):
        if attribute['type'] == 'sdtitle':
            self.add_title(pdf, attribute)
        elif attribute['type'] == 'sdgraph':
            self.add_graph(pdf, attribute)
        elif attribute['type'] == 'sdimage':
            self.add_image(pdf, attribute)
        elif attribute['type'] == 'sdtex':
            for child_attribute in attribute['children']:
                self.add_attribute_to_pdf(pdf, child_attribute)
        elif attribute['type'] == 'text':
            self.add_text(pdf, attribute)
        elif attribute['type'] == 'sdbullet':
            self.add_bullet(pdf, attribute)
        elif attribute['type'] == 'sdquote':
            self.add_quote(pdf, attribute)
        elif attribute['type'] == 'sdauthor':
            self.add_author(pdf, attribute)
        elif attribute['type'] == 'sdcode':
            self.add_code(pdf, attribute)

    def add_title(self, pdf, attribute):
        content = attribute['content']
        style = attribute['style']
        font_size = int(style.get('font_size', '12').strip('"').replace('dp', '').strip())
        font_color = style.get('font_color', '#000000').strip('"')
        font_weight = style.get('font_weight', 'normal').strip('"')

        if font_color.startswith('#') and len(font_color) == 7:
            try:
                r = int(font_color[1:3], 16)
                g = int(font_color[3:5], 16)
                b = int(font_color[5:7], 16)
            except ValueError:
                r, g, b = 0, 0, 0
        else:
            r, g, b = 0, 0, 0

        if font_weight == 'bold':
            pdf.set_font("Arial", size=font_size, style='B')
        else:
            pdf.set_font("Arial", size=font_size)

        pdf.set_text_color(r, g, b)

        # Apply text formatting
        self.apply_text_formatting(pdf, content)

        # Calculate the height of the cell
        cell_height = pdf.font_size + 8

        # Check if the text will wrap
        text_width = pdf.get_string_width(content)
        page_width = pdf.w - 2 * pdf.l_margin
        num_lines = 1
        if text_width > page_width:
            # Calculate the number of lines
            num_lines = math.ceil(text_width / page_width)
            cell_height *= num_lines

        if self.current_y + cell_height > pdf.page_break_trigger:
            pdf.add_page()
            self.current_y = 0

        pdf.ln(cell_height)  # Move to the next line
        self.current_y += cell_height  # Increase current_y by the cell height + padding

    def add_text(self, pdf, attribute):
        content = attribute['content']
        self.apply_text_formatting(pdf, content)

    def add_image(self, pdf, attribute):
        src = attribute['content']
        image_file_name = os.path.basename(src)
        output_dir = os.path.join(self.script_dir, 'Output')
        image_file_path = os.path.join(output_dir, image_file_name)

        if self.download_image(src, image_file_path):
            with PILImage.open(image_file_path) as img:
                width, height = img.size
                resized_height = 180 * height / width  # Adjusting width to 180, maintaining aspect ratio

            if self.current_y + resized_height + 10 > pdf.page_break_trigger:
                pdf.add_page()
                self.current_y = 0

            pdf.image(image_file_path, x=10, y=self.current_y + 10, w=180, h=resized_height)
            self.current_y += resized_height

        else:
            print(f"Failed to download and embed image from {src}.")

    def add_graph(self, pdf, attribute):
        attributes = attribute['attributes']
        function = attributes.get('function', "x")
        first_point = int(attributes.get('first_point', -10))
        last_point = int(attributes.get('last_point', 10))
        quality = int(attributes.get('quality', 10))
        graph_color = attributes.get('graph_color', "#00ff00").strip('"').strip("'")

        output_dir = os.path.join(self.script_dir, 'Output')
        graph_file_path = os.path.join(output_dir, 'graph.png')
        self.save_as_graph(function, first_point, last_point, quality, graph_color, graph_file_path)

        with PILImage.open(graph_file_path) as img:
            width, height = img.size
            resized_height = 180 * height / width  # Adjusting width to 180, maintaining aspect ratio

        if self.current_y + resized_height + 10 > pdf.page_break_trigger:
            pdf.add_page()
            self.current_y = 0

        pdf.image(graph_file_path, x=10, y=self.current_y + 10, w=180, h=resized_height)
        self.current_y += resized_height  # Increase current_y by resized image height + padding

    def save_as_graph(self, function, first_point, last_point, quality, graph_color, graph_file_path):
        x_values = np.linspace(first_point, last_point, int((last_point - first_point) * quality))
        y_values = self.evaluate_function(function, x_values)

        rgb_color = matplotlib.colors.to_rgb(graph_color)

        plt.figure()
        plt.plot(x_values, y_values, color=rgb_color)
        plt.savefig(graph_file_path)
        plt.close()
        print(f"Graph image has been saved to {graph_file_path}")

    def evaluate_function(self, function, x_values):
        # Vectorized evaluation using NumPy
        return [eval(eval(function.replace('x', str(x)))) for x in x_values]

    def add_bullet(self, pdf, attribute):
        content = attribute['content']
        style = attribute['style']
        font_size = int(style.get('font_size', '12').strip('"').replace('dp', '').strip())
        font_color = style.get('font_color', '#000000').strip('"')

        if font_color.startswith('#') and len(font_color) == 7:
            try:
                r = int(font_color[1:3], 16)
                g = int(font_color[3:5], 16)
                b = int(font_color[5:7], 16)
            except ValueError:
                r, g, b = 0, 0, 0
        else:
            r, g, b = 0, 0, 0

        pdf.set_font("Arial", size=font_size)
        pdf.set_text_color(r, g, b)

        # Apply text formatting
        self.apply_text_formatting(pdf, f'- {content}')

        cell_height = pdf.font_size + 2
        if self.current_y + cell_height > pdf.page_break_trigger:
            pdf.add_page()
            self.current_y = 0

        pdf.ln(cell_height)
        self.current_y += cell_height

    def add_quote(self, pdf, attribute):
        content = attribute['content']
        style = attribute['style']
        font_size = int(style.get('font_size', '12').strip('"').replace('dp', '').strip())
        font_color = style.get('font_color', '#888888').strip('"')

        if font_color.startswith('#') and len(font_color) == 7:
            try:
                r = int(font_color[1:3], 16)
                g = int(font_color[3:5], 16)
                b = int(font_color[5:7], 16)
            except ValueError:
                r, g, b = 0, 0, 0
        else:
            r, g, b = 0, 0, 0

        pdf.set_font("Arial", size=font_size, style='I')  # Italics for quotes
        pdf.set_text_color(r, g, b)

        # Apply text formatting
        self.apply_text_formatting(pdf, content)

        cell_height = pdf.font_size + 6
        if self.current_y + cell_height > pdf.page_break_trigger:
            pdf.add_page()
            self.current_y = 0

        pdf.ln(cell_height)
        self.current_y += cell_height

    def add_author(self, pdf, attribute):
        content = attribute['content']
        style = attribute['style']
        font_size = int(style.get('font_size', '12').strip('"').replace('dp', '').strip())
        font_color = style.get('font_color', '#555555').strip('"')

        if font_color.startswith('#') and len(font_color) == 7:
            try:
                r = int(font_color[1:3], 16)
                g = int(font_color[3:5], 16)
                b = int(font_color[5:7], 16)
            except ValueError:
                r, g, b = 0, 0, 0
        else:
            r, g, b = 0, 0, 0

        pdf.set_font("Arial", size=font_size, style='I')  # Italics for author
        pdf.set_text_color(r, g, b)

        # Apply text formatting
        self.apply_text_formatting(pdf, content)

        cell_height = pdf.font_size + 6
        if self.current_y + cell_height > pdf.page_break_trigger:
            pdf.add_page()
            self.current_y = 0

        pdf.ln(cell_height)
        self.current_y += cell_height

    def add_code(self, pdf, attribute):
        content = attribute['content']
        style = attribute['style']
        font_size = int(style.get('font_size', '12').strip('"').replace('dp', '').strip())
        font_color = style.get('font_color', '#FF0000').strip('"')

        if font_color.startswith('#') and len(font_color) == 7:
            try:
                r = int(font_color[1:3], 16)
                g = int(font_color[3:5], 16)
                b = int(font_color[5:7], 16)
            except ValueError:
                r, g, b = 0, 0, 0
        else:
            r, g, b = 0, 0, 0

        pdf.set_font("Courier", size=font_size)  # Monospaced font for code
        pdf.set_text_color(r, g, b)

        # Apply text formatting
        self.apply_text_formatting(pdf, content)

        cell_height = pdf.font_size + 4
        if self.current_y + cell_height > pdf.page_break_trigger:
            pdf.add_page()
            self.current_y = 0

        pdf.ln(cell_height)
        self.current_y += cell_height

    def apply_text_formatting(self, pdf, text):
        # Apply any text formatting, like line breaks, spaces, etc.
        for line in text.split('\n'):
            pdf.cell(0, 10, line, ln=True)

if __name__ == "__main__":
    input_file = "../main.sdtex"  # Replace with the path to your input file
    sdtex = SdTeX(input_file)
    sdtex.run()
