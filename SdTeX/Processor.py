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
        tag_pattern = re.compile(
            r'\((\w+)'                               
            r'(?:\s+style\s*=\s*\{([^}]*)\})?'       
            r'(?:\s+attributes\s*=\s*\{([^}]*)\})?'  
            r'(?:\s+src\s*=\s*"([^"]*)")?'          
            r'\)(.*?)\(!\1\)',
            re.DOTALL
        )

        for match in re.finditer(tag_pattern, self.content):
            tag_type = match.group(1).strip()
            style_string = match.group(2)
            attributes_string = match.group(3)
            src = match.group(4)
            tag_content = match.group(5).strip()

            styles = {}
            if style_string:
                for line in style_string.split(','):
                    parts = line.strip().split(':')
                    if len(parts) == 2:
                        key, value = parts
                        styles[key.strip()] = value.strip()

            attributes = {}
            if attributes_string:
                for line in attributes_string.split(','):
                    parts = line.strip().split(':')
                    if len(parts) == 2:
                        key, value = parts
                        attributes[key.strip()] = value.strip()

            if src:
                self.tags.append({
                    'type': tag_type,
                    'content': src,
                    'style': styles,
                    'attributes': attributes
                })
            else:
                self.tags.append({
                    'type': tag_type,
                    'content': tag_content,
                    'style': styles,
                    'attributes': attributes
                })

    def replace_tag(self, match):
        tag_type = match.group(1).strip()
        tag_content = match.group(2).strip()
        style = self.styles.get(tag_type, {})
        self.tags.append({
            'type': tag_type,
            'content': tag_content,
            'style': style
        })
        return ''

    def process_content(self):
        self.parse_stylesheet()
        self.parse_tags()

        return self.tags
