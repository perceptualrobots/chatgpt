import os
import re
from datetime import datetime

class LaTeXSplitter:
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir
        self.sections = []

    def read_file(self):
        with open(self.input_file, 'r') as file:
            content = file.read()
        return content

    def split_sections(self, content):
        # Regex pattern to match LaTeX sections
        section_pattern = re.compile(r'\\section{(.*?)}')
        sections = section_pattern.split(content)
        
        # The first element of the split content is the text before the first section
        # Following pairs of elements are section names and section content
        for i in range(1, len(sections), 2):
            section_name = sections[i]
            section_content = sections[i + 1]
            # Remove non-alphanumeric characters from section name
            cleaned_section_name = re.sub(r'\W+', '', section_name)
            self.sections.append((section_name, cleaned_section_name, section_content))

    def write_sections(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        for idx, (original_name, cleaned_name, content) in enumerate(self.sections, 1):
            # Replace spaces with underscores in section names for filenames
            safe_name = cleaned_name.replace(' ', '_')
            output_filename = f"{idx}_{safe_name}.txt"
            output_path = os.path.join(self.output_dir, output_filename)
            with open(output_path, 'w') as file:
                file.write(f"\\section{{{original_name}}}\n")
                file.write(content)

    def process(self):
        content = self.read_file()
        self.split_sections(content)
        self.write_sections()


class LaTeXConcatenator:
    def __init__(self, input_dir, output_file):
        self.input_dir = input_dir
        self.output_file = output_file

    def concatenate_files(self):
        with open(self.output_file, 'w') as outfile:
            for filename in sorted(os.listdir(self.input_dir)):
                if filename.endswith('.txt'):
                    file_path = os.path.join(self.input_dir, filename)
                    with open(file_path, 'r') as infile:
                        outfile.write(infile.read())
                        outfile.write('\n')


if __name__ == '__main__':
    test = 'split'   
    # Usage example

    if test == 'split':
        splitter = LaTeXSplitter('G:\\My Drive\\PR\\Consciousness\\chatgpt\\paper\\body-202405.tex', 'G:\\My Drive\\PR\\Consciousness\\chatgpt\\paper\\text')
        splitter.process()
    else:
        input_dir = 'G:\\My Drive\\PR\\Consciousness\\chatgpt\\paper\\responses\\generic\\rewrite'
        last_two_folders = os.path.basename(os.path.dirname(input_dir)) + '-' + os.path.basename(input_dir)
        date_str = datetime.now().strftime('%Y%m%d')
        output_file = f"G:\\My Drive\\PR\\Consciousness\\chatgpt\\paper\\body-{last_two_folders}-{date_str}.tex"

        concatenator = LaTeXConcatenator(input_dir, output_file)
        concatenator.concatenate_files()
