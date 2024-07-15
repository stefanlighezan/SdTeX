import re
from Errors import *

class Processor:
    def __init__(self, content):
        self.content = content
        self.styles = {}
        self.tags = {}
        self.variables = {}
        self.line_number = 0  # Track line numbers for error reporting

    def parse_variables(self):
        pattern = r'^(\w+)\s*:\s*"([^"]+)"$'
        matches = re.findall(pattern, self.content, flags=re.MULTILINE)
        self.variables = {name: value for name, value in matches}

    def replace_variables(self):
        for key, value in self.variables.items():
            self.content = self.content.replace(f"${key}", value)

    def parse_stylesheet(self):
        pattern = r"\((.*?)\s*style=\s*\{(.*?)\}\)"
        match = re.search(pattern, self.content, flags=re.DOTALL)
        if match:
            tag_type = match.group(1).strip()
            style_string = match.group(2).strip()
            styles = {}
            for line in style_string.split(","):
                parts = line.strip().split(":")
                if len(parts) == 2:
                    key, value = parts
                    styles[key.strip()] = value.strip()
            self.styles[tag_type] = styles
        return self.styles

    def parse_tags(self):
        tag_pattern = re.compile(
            r"\((\w+)"
            r"(?:\s+style\s*=\s*\{([^}]*)\})?"
            r"(?:\s+attributes\s*=\s*\{([^}]*)\})?"
            r'(?:\s+src\s*=\s*"([^"]*)")?'
            r"\)(.*?)\(!\1\)",
            re.DOTALL,
        )

        self.line_number = 0  # Reset line number tracker
        for match in re.finditer(tag_pattern, self.content):
            self.line_number += 1
            tag_type = match.group(1).strip()
            style_string = match.group(2)
            attributes_string = match.group(3)
            src = match.group(4)
            tag_content = match.group(5).strip()

            styles = {}
            if style_string:
                for line in style_string.split(","):
                    parts = line.strip().split(":")
                    if len(parts) == 2:
                        key, value = parts
                        styles[key.strip()] = value.strip()

            attributes = {}
            if attributes_string:
                for line in attributes_string.split(","):
                    parts = line.strip().split(":")
                    if line.strip().startswith('//'):
                        continue  # Ignore comments in attributes string
                    if len(parts) == 2:
                        key, value = parts
                        attributes[key.strip()] = value.strip()

            if src:
                self.tags[tag_type] = {
                    "type": tag_type,
                    "content": src,
                    "style": styles,
                    "attributes": attributes,
                    "line_number": self.line_number  # Track line number
                }
            else:
                self.tags[tag_type] = {
                    "type": tag_type,
                    "content": tag_content,
                    "style": styles,
                    "attributes": attributes,
                    "line_number": self.line_number  # Track line number
                }

    def process_content(self):
        try:
            self.parse_variables()
            self.replace_variables()
            self.parse_stylesheet()
            self.parse_tags()
        except re.error as e:
            raise SdTeXSyntaxError(f"Syntax error in regular expression: {e}")
        except Exception as e:
            raise SdTeXProcessingError(f"Error processing content: {e}")

        return list(self.tags.values())