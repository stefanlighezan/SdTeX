import re

class Processor:
    def __init__(self, content):
        self.content = content

    def parse_sdtitle_tags(self):
        # Define a regex pattern to find sdtitle tags and their content
        sdtitle_pattern = r'\(sdtitle\)(.*?)\(!sdtitle\)'

        def replace_sdtitle(match):
            title_text = match.group(1).strip()  # Get the title text inside sdtitle tags
            return f"# {title_text} /#"

        # Use re.sub to replace all sdtitle tags with # ... /# format
        parsed_content = re.sub(sdtitle_pattern, replace_sdtitle, self.content, flags=re.DOTALL)

        return parsed_content

    def process_content(self):
        parsed_content = self.parse_sdtitle_tags()
        return parsed_content
