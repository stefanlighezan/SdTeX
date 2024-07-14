import re

class Processor:
    def __init__(self, content):
        self.content = content
        self.styles = {}
        self.tags = []

    def parse_stylesheet(self):
        pattern = r'\((.*?)\s*style=\s*\{(.*?)\}\)'
        match = re.search(pattern, self.content, flags=re.DOTALL)
        if match:
            tag_type = match.group(1).strip()
            style_string = match.group(2).strip()
            styles = {}
            for line in style_string.split(','):
                parts = line.strip().split(':')
                if len(parts) == 2:
                    key, value = parts
                    styles[key.strip()] = value.strip()
            self.styles[tag_type] = styles
        return self.styles

    def parse_tags(self):
        tag_pattern = r'\((.*?)\)(.*?)\(!\1\)'
        tag_pattern_with_style = r'\((.*?)\s*style=\s*\{(.*?)\}\)(.*?)\(!\1\)'
        tag_pattern_with_attributes = r'\((.*?)\s+attributes\s*=\s*{([^}]*)}\s*\)(.*?)\(!\1\)'
        
        for match in re.finditer(tag_pattern_with_style, self.content, flags=re.DOTALL):
            tag_type = match.group(1).strip()
            style_string = match.group(2).strip()
            tag_content = match.group(3).strip()
            styles = {}
            for line in style_string.split(','):
                parts = line.strip().split(':')
                if len(parts) == 2:
                    key, value = parts
                    styles[key.strip()] = value.strip()
            self.tags.append({
                'type': tag_type,
                'content': tag_content,
                'style': styles
            })
        
        for match in re.finditer(tag_pattern_with_attributes, self.content, flags=re.DOTALL):
            tag_type = match.group(1).strip()
            attributes_string = match.group(2).strip()
            tag_content = match.group(3).strip()
            attributes = {}
            for line in attributes_string.split(','):
                parts = line.strip().split(':')
                if len(parts) == 2:
                    key, value = parts
                    attributes[key.strip()] = value.strip()
            self.tags.append({
                'type': tag_type,
                'content': attributes,  # Store attributes as a dictionary
                'style': {},  # Assuming no style for sdgraph with attributes in this context
            })
        
        for match in re.finditer(tag_pattern, self.content, flags=re.DOTALL):
            tag_type = match.group(1).strip()
            tag_content = match.group(2).strip()
            self.tags.append({
                'type': tag_type,
                'content': tag_content,
                'style': self.styles.get(tag_type, {})  # Get style for the tag type, default to empty dict
            })

    def replace_tag(self, match):
        tag_type = match.group(1).strip()
        tag_content = match.group(2).strip()
        style = self.styles.get(tag_type, {})  # Get style for the tag type, default to empty dict
        self.tags.append({
            'type': tag_type,
            'content': tag_content,
            'style': style  # Ensure 'style' matches the key used when accessing in 'save_as_pdf'
        })
        return ''

    def process_content(self):
        self.parse_stylesheet()
        self.parse_tags()

        return self.tags
