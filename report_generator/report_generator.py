import os
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import argparse

from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, PageTemplate, Frame
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from dotenv import load_dotenv

class TechnicalReportGenerator:
    """
    Generates a PDF technical report presenting Perceptual Control Theory (PCT) applied to a target environment,
    with a comparison against a Reinforcement Learning (RL) controller.
    """
    
    def __init__(self, input_dir: str = "input", output_dir: str = "output", environment: str = "OpenAI Gym"):
        # Look for .env file in the VS Code root folder (parent of report_generator)
        vscode_root = Path(__file__).parent.parent
        env_path = vscode_root / ".env"
        
        # Try VS Code root first, then current directory, then default locations
        if env_path.exists():
            load_dotenv(env_path)
        else:
            load_dotenv()  # This will check current directory and standard locations
            
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.metadata_file = self.output_dir / "metadata.json"
        self.environment = environment
        
        # Load report metadata from environment variables
        self.report_author = os.getenv("REPORT_AUTHOR", "Research Team")
        self.report_email = os.getenv("REPORT_EMAIL", "")
        self.report_title = os.getenv("REPORT_TITLE", "")
        self.report_subtitle = os.getenv("REPORT_SUBTITLE", "")
        self.report_org = os.getenv("REPORT_ORG", "")
        
        # Report sections in order (Executive Summary removed)
        self.sections = [
            "abstract",  # Added abstract section
            "introduction", 
            "background",
            "methodology",
            "experimental_results",
            "discussion",
            "recommendations_future_work",
            "references"
        ]
        
        # Section titles for PDF
        self.section_titles = {
            "abstract": "Abstract",  # Added abstract section
            "introduction": "Introduction",
            "background": "Background", 
            "methodology": "Methodology",
            "experimental_results": "Experimental Results",
            "discussion": "Discussion",
            "recommendations_future_work": "Recommendations & Future Work",
            "references": "References"
        }
        
        self.ensure_directories()
        
    def get_version_number(self) -> str:
        """Get and increment version number."""
        metadata = self.load_metadata()
        current_version = metadata.get("version", "1.0.0")
        
        # Parse version (major.minor.patch)
        parts = current_version.split(".")
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        
        # Increment patch version
        patch += 1
        new_version = f"{major}.{minor}.{patch}"
        
        # Save new version
        metadata["version"] = new_version
        metadata["version_date"] = datetime.now().isoformat()
        self.save_metadata(metadata)
        
        return new_version
    
    def get_author_name(self) -> str:
        """Get author name from environment or metadata."""
        # Use the class property if it exists
        if self.report_author:
            return self.report_author
            
        # Try metadata as fallback
        metadata = self.load_metadata()
        author = metadata.get("author")
        if author:
            return author
            
        # Default fallback
        return "Research Team"
        
    def get_author_email(self) -> str:
        """Get author email from environment or metadata."""
        return self.report_email or ""

    def get_report_organization(self) -> str:
        """Get organization name from environment or metadata."""
        return self.report_org or ""
        
    def get_report_title(self) -> str:
        """Get report title from environment or metadata."""
        return self.report_title or f"PCT Applied to {self.environment}"
        
    def get_report_subtitle(self) -> str:
        """Get report subtitle from environment or metadata."""
        return self.report_subtitle or "with Comparative RL Baseline"
        
    def ensure_directories(self):
        """Create input and output directories if they don't exist."""
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
    def load_title_info(self):
        """Load title information from title.md if available."""
        title_file = self.input_dir / "title.md"
        if title_file.exists():
            try:
                with open(title_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Parse key-value pairs from the file
                for line in content.splitlines():
                    line = line.strip()
                    if line and ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip()
                        value = value.strip()
                        
                        if key.lower() == "subtitle":
                            self.report_subtitle = value or self.report_subtitle
                        elif key.lower() == "org":
                            self.report_org = value or self.report_org
                        elif key.lower() == "title":
                            self.report_title = value or self.report_title
                            
                print(f"Title information loaded from {title_file}")
            except Exception as e:
                print(f"Error loading title information: {e}")
        
    def get_file_hash(self, filepath: Path) -> str:
        """Calculate MD5 hash of a file."""
        if not filepath.exists():
            return ""
        
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def load_metadata(self) -> Dict:
        """Load metadata about file hashes and generation timestamps."""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_metadata(self, metadata: Dict):
        """Save metadata about file hashes and generation timestamps."""
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def needs_regeneration(self, section: str) -> bool:
        """
        Check if a section needs to be regenerated based on:
        1. Output file doesn't exist
        2. Input file has changed since last generation
        """
        input_file = self.input_dir / f"{section}.md"
        output_file = self.output_dir / f"{section}.txt"
        
        # If input file doesn't exist, skip this section
        if not input_file.exists():
            print(f"Warning: Input file {input_file} not found. Skipping {section}.")
            return False
            
        # If output file doesn't exist, always regenerate
        if not output_file.exists():
            print(f"Output file {output_file} missing. Will regenerate {section}.")
            return True
            
        # Check if input file has changed since last generation
        current_hash = self.get_file_hash(input_file)
        metadata = self.load_metadata()
        
        stored_hash = metadata.get(section, {}).get("input_hash", "")
        if current_hash != stored_hash:
            print(f"Input file {input_file} has changed. Will regenerate {section}.")
            return True
            
        # No regeneration needed
        return False
    
    def generate_section_prompt(self, section: str, notes: str) -> str:
        """Generate the OpenAI prompt for a specific section."""
        base_context = f"""
        You are writing a technical report that primarily presents a Perceptual Control Theory (PCT) controller applied to the {self.environment} environment,
        and secondarily provides a comparison against a Reinforcement Learning (RL) controller as a baseline.

        Emphasize the PCT approach, its rationale, architecture, implementation details, and performance in the environment.
        Use RL as a comparator to contextualize results and highlight similarities/differences.

        Write in an academic, technical style appropriate for a research paper. Use Times New Roman formatting conceptually.
        Include APA-style in-text citations where appropriate (use placeholder citations like (Author, Year)).
        
        IMPORTANT: Do NOT include the section title or any heading in your response. Start directly with the content paragraphs.
        The section title will be added automatically by the document generator.
        
        CITATION HANDLING: If the notes contain LaTeX citation commands like \\cite{{...}}, \\citep{{...}}, or \\citet{{...}}, 
        these MUST be included in your output text where appropriate. These are LaTeX commands that will be processed later.
        When you write about videos, results, or any referenced work that has a citation command in the notes, 
        include that citation command in your narrative text. For example, if notes mention "Video \\citep{{young2025}}", 
        you should write something like "as demonstrated in the video \\citep{{young2025}}" or "Video demonstrations \\citep{{young2025}} show..."
        
        IMAGE HANDLING: When referencing images, use the format: [Image: filename.png (Caption text goes here)]
        If the notes provide image references with captions, preserve the filename and include the caption in parentheses.
        Do NOT add quotes around filenames.
        If the notes specify a width parameter like [width=1.0\textwidth], include it immediately before the caption:
        [Image: filename.png [width=1.0\textwidth] (Caption text)]
        IMPORTANT: Include ALL images mentioned in the notes in your output, in the same order they appear.
        Do not omit any images or videos mentioned in the source notes.
        
        TABLE HANDLING: If the notes contain Markdown tables (with pipes | and dashes), preserve them EXACTLY in your output.
        Do NOT convert tables to prose or replace them with placeholders like [Table would be inserted here].
        Keep the complete table structure with all rows and columns intact.
        """

        section_specific_prompts = {
            "introduction": "Write an introduction that frames the report as a presentation of PCT applied to the target environment, with a secondary comparison to an RL baseline. Clearly state the objectives and why PCT is an appropriate approach.",

            "background": f"Provide comprehensive background emphasizing Perceptual Control Theory (principles, hierarchy, and control units), the {self.environment} environment, and briefly summarize RL concepts used as a comparator. Establish the theoretical foundation with a PCT-first emphasis.",

            "methodology": f"Describe the methodology with PCT as the primary focus: the {self.environment} setup, PCT hierarchy design and training (e.g., evolutionary algorithm parameters), followed by a concise RL baseline configuration, evaluation metrics, and procedures.",

            "experimental_results": f"Present results primarily for the PCT controller in the {self.environment} environment, including performance, stability, and interpretability aspects; then compare against the RL baseline. CRITICAL: When the notes mention images, tables, or videos with specific ordering (first, second, third), you MUST reference them in your narrative in EXACTLY that order. Do not rearrange visual elements for narrative flow. If the notes show Image A then Image B, your text must reference Image A before Image B.",

            "discussion": "Analyze and interpret results with a PCT-first lens: strengths, limitations, implications, and design insights of PCT; then contrast with RL to highlight advantages/trade-offs.",

            "recommendations_future_work": "Provide specific recommendations focusing on advancing PCT (architecture, training, analysis) and outline future research, including more rigorous RL baselines for comparison.",

            "references": "Generate ONLY a reference list in APA format. Do NOT include any introductory text, discussion, or conclusions. Just provide the properly formatted references cited in the report, with emphasis on PCT literature, along with relevant works on evolutionary algorithms, reinforcement learning, and control systems. Each reference should be on its own line or paragraph, properly formatted in APA style.",

            "abstract": "Write a concise abstract (maximum 250 words) that summarizes PCT applied to the target environment, followed by a brief comparison with an RL baseline. Include objective, methodology overview, key findings, and main conclusions."
        }

        prompt = f"{base_context}\n\n{section_specific_prompts[section]}\n\nNotes for this section:\n{notes}\n\nGenerate the content for this section:"

        return prompt
    
    def generate_section_content(self, section: str) -> Optional[str]:
        """Generate content for a specific section using OpenAI."""
        input_file = self.input_dir / f"{section}.md"
        
        if not input_file.exists():
            print(f"Input file {input_file} not found. Skipping {section}.")
            return None
            
        # Read notes from input file
        with open(input_file, 'r', encoding='utf-8') as f:
            notes = f.read().strip()
            
        if not notes:
            print(f"Input file {input_file} is empty. Skipping {section}.")
            return None
            
        print(f"Generating content for {section}...")
        
        try:
            prompt = self.generate_section_prompt(section, notes)
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert technical writer specializing in control systems and artificial intelligence research."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Save generated content
            output_file = self.output_dir / f"{section}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
            # Update metadata
            metadata = self.load_metadata()
            metadata[section] = {
                "input_hash": self.get_file_hash(input_file),
                "generated_at": datetime.now().isoformat(),
                "output_file": str(output_file)
            }
            self.save_metadata(metadata)
            
            print(f"[OK] Generated {section}")
            return content
            
        except Exception as e:
            print(f"Error generating {section}: {e}")
            return None
    
    def generate_abstract_from_sections(self) -> Optional[str]:
        """Generate abstract based on existing sections."""
        print("Generating abstract from existing sections...")
        
        # Collect content from key sections
        sections_for_abstract = [
            "introduction", "methodology", 
            "experimental_results", "discussion", "recommendations_future_work"
        ]
        
        combined_content = ""
        for section in sections_for_abstract:
            output_file = self.output_dir / f"{section}.txt"
            if output_file.exists():
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        combined_content += f"\n\n{self.section_titles[section]}:\n{content}"
        
        if not combined_content:
            print("No existing sections found for abstract generation.")
            return None
            
        try:
            prompt = f"""
            Based on the following technical report sections, write a concise abstract (maximum 250 words) that summarizes the research study comparing control systems for the {self.environment} environment. The abstract should include:
            1. Research objective and problem statement
            2. Methodology overview (PCT vs RL comparison)
            3. Key findings and results
            4. Main conclusions and implications
            
            Make it a standalone summary that gives readers a complete overview of the work. IMPORTANT: Keep the abstract to 250 words or fewer.
            
            Report content:
            {combined_content}
            
            Generate a professional abstract:
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert technical writer specializing in research abstracts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            abstract_content = response.choices[0].message.content
            
            # Save generated abstract
            output_file = self.output_dir / "abstract.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(abstract_content)
                
            # Update metadata
            metadata = self.load_metadata()
            metadata["abstract"] = {
                "generated_from_sections": True,
                "generated_at": datetime.now().isoformat(),
                "output_file": str(output_file)
            }
            self.save_metadata(metadata)
            
            print("[OK] Generated abstract from existing sections")
            return abstract_content
            
        except Exception as e:
            print(f"Error generating abstract: {e}")
            return None
    
    def generate_sections(self) -> List[str]:
        """Generate content for all sections that need updates."""
        updated_sections = []
        
        # First, generate all regular sections (excluding abstract)
        regular_sections = [s for s in self.sections if s != "abstract"]
        
        for section in regular_sections:
            if self.needs_regeneration(section):
                content = self.generate_section_content(section)
                if content:
                    updated_sections.append(section)
        
        # Generate abstract after other sections if any were updated
        if updated_sections and "abstract" in self.sections:
            abstract_content = self.generate_abstract_from_sections()
            if abstract_content:
                updated_sections.append("abstract")
                    
        return updated_sections
        """Generate content for all sections that need updates."""
        updated_sections = []
        
        for section in self.sections:
            if self.needs_regeneration(section):
                content = self.generate_section_content(section)
                if content:
                    updated_sections.append(section)
                    
        return updated_sections
    
    def create_pdf_styles(self):
        """Create custom styles for the PDF document."""
        styles = getSampleStyleSheet()
        
        # Title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=16,
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Times-Bold'
        )
        
        # Heading style
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading1'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            fontName='Times-Bold'
        )
        
        # Body style
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            fontName='Times-Roman',
            leading=14
        )
        
        return {
            'title': title_style,
            'heading': heading_style,
            'body': body_style
        }
    
    def add_page_number(self, canvas, doc):
        """Add page numbers to each page."""
        page_num = canvas.getPageNumber()
        text = f"{page_num}"  # Just the number, no "Page" prefix
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        # Center the page number at bottom of page
        text_width = canvas.stringWidth(text, 'Times-Roman', 10)
        x_position = (letter[0] - text_width) / 2
        canvas.drawString(x_position, 36, text)
        canvas.restoreState()
    
    def concatenate_input_files(self, output_filename: str = "all_sections_notes.md") -> bool:
        """Concatenate all input files in the correct order into a single file."""
        print("Concatenating input files...")
        
        output_path = self.input_dir / output_filename
        
        try:
            with open(output_path, 'w', encoding='utf-8') as output_file:
                # Write header
                output_file.write(f"# Technical Report - PCT Applied (with RL Comparison)\n")
                output_file.write(f"# Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}\n")
                output_file.write(f"# Environment: {self.environment}\n")
                output_file.write(f"# Focus: PCT primary; RL comparator baseline\n")
                output_file.write("=" * 80 + "\n\n")
                
                for section in self.sections:
                    input_file = self.input_dir / f"{section}.md"
                    
                    if input_file.exists():
                        # Write section header
                        section_title = self.section_titles[section]
                        output_file.write(f"## {section_title.upper()}\n")
                        output_file.write("-" * (len(section_title) + 3) + "\n\n")
                        
                        # Read and write section content
                        with open(input_file, 'r', encoding='utf-8') as section_file:
                            content = section_file.read().strip()
                            if content:
                                output_file.write(content)
                            else:
                                output_file.write("[No content provided]")
                        
                        output_file.write("\n\n" + "=" * 80 + "\n\n")
                    else:
                        # Write placeholder for missing files
                        section_title = self.section_titles[section]
                        output_file.write(f"## {section_title.upper()}\n")
                        output_file.write("-" * (len(section_title) + 3) + "\n\n")
                        output_file.write(f"[Input file {input_file.name} not found]\n\n")
                        output_file.write("=" * 80 + "\n\n")
            
            print(f"[OK] Input files concatenated: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error concatenating input files: {e}")
            return False
    
    def generate_pdf(self, output_filename: str = "technical_report.pdf") -> bool:
        """Generate the complete PDF report from all section files."""
        print("Generating PDF report...")

        # Get version and author info
        version = self.get_version_number()
        author = self.get_author_name()
        email = self.get_author_email()
        title = self.get_report_title()
        subtitle = self.get_report_subtitle()
        org = self.get_report_organization()

        pdf_path = self.output_dir / output_filename
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=54  # Increased bottom margin for page numbers
        )

        story = []
        styles = self.create_pdf_styles()

        # Title page with version, author, and abstract
        story.append(Paragraph(title, styles['title']))
        story.append(Paragraph(subtitle, styles['title']))
        story.append(Spacer(1, 0.3*inch))
        
        # Author line with organization and email if available
        author_parts = [f"Author: {author}"]
        if org:
            author_parts.append(f"Organization: {org}")
        if email:
            author_parts.append(f"Email: {email}")
        
        meta_line = f"{' — '.join(author_parts)} — Version {version} — {datetime.now().strftime('%B %d, %Y')}"
        story.append(Paragraph(meta_line, styles['body']))
        story.append(Spacer(1, 0.3*inch))

        # Add abstract to title page if it exists
        abstract_file = self.output_dir / "abstract.txt"
        if abstract_file.exists():
            story.append(Spacer(1, 0.4*inch))
            story.append(Paragraph("Abstract", styles['heading']))
            story.append(Spacer(1, 12))

            with open(abstract_file, 'r', encoding='utf-8') as f:
                abstract_content = f.read().strip()
                if abstract_content:
                    # Split abstract into paragraphs
                    paragraphs = abstract_content.split('\n\n')
                    for para in paragraphs:
                        if para.strip():
                            story.append(Paragraph(para.strip(), styles['body']))
                            story.append(Spacer(1, 12))

        story.append(PageBreak())

        # Add each section (excluding abstract since it's now on title page)
        section_counter = 0
        for section in self.sections:
            if section == "abstract":  # Skip abstract section
                continue

            output_file = self.output_dir / f"{section}.txt"

            if output_file.exists():
                # Add numbered section heading
                section_counter += 1
                heading_text = f"{section_counter}. {self.section_titles[section]}"
                story.append(Paragraph(heading_text, styles['heading']))
                story.append(Spacer(1, 12))

                # Read and add section content
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Split content into paragraphs and add to story
                paragraphs = content.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        story.append(Paragraph(para.strip(), styles['body']))
                        story.append(Spacer(1, 12))

                story.append(Spacer(1, 24))
            else:
                print(f"Warning: Output file {output_file} not found. Skipping {section} in PDF.")

        try:
            # Build PDF with page numbers
            doc.build(story, onFirstPage=self.add_page_number, onLaterPages=self.add_page_number)
            print(f"[OK] PDF report generated: {pdf_path}")
            return True
        except Exception as e:
            # On Windows, the PDF may be locked if open; try a timestamped filename
            msg = str(e)
            if isinstance(e, PermissionError) or "Permission denied" in msg:
                fallback_name = f"technical_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                fallback_path = self.output_dir / fallback_name
                try:
                    fallback_doc = SimpleDocTemplate(
                        str(fallback_path),
                        pagesize=letter,
                        rightMargin=72,
                        leftMargin=72,
                        topMargin=72,
                        bottomMargin=54
                    )
                    fallback_doc.build(story, onFirstPage=self.add_page_number, onLaterPages=self.add_page_number)
                    print(f"[OK] PDF report generated (fallback): {fallback_path}")
                    return True
                except Exception as e2:
                    print(f"Error generating PDF (fallback): {e2}")
                    return False
            else:
                print(f"Error generating PDF: {e}")
                return False
    
    def generate_bibtex(self, output_filename: str = "references.bib") -> bool:
        """Generate BibTeX file from references section."""
        references_file = self.output_dir / "references.txt"
        if not references_file.exists():
            print(f"References file {references_file} not found.")
            return False
        
        bibtex_path = self.output_dir / output_filename
        
        # Check if BibTeX file already exists and references.txt hasn't changed
        if bibtex_path.exists():
            current_hash = self.get_file_hash(references_file)
            metadata = self.load_metadata()
            stored_hash = metadata.get("bibtex", {}).get("input_hash", "")
            
            if current_hash == stored_hash:
                print(f"BibTeX file up to date (references.txt unchanged). Skipping regeneration.")
                return True
        
        print("Generating BibTeX file...")
        
        try:
            with open(references_file, 'r', encoding='utf-8') as f:
                refs_content = f.read().strip()
            
            # Use OpenAI to convert references to BibTeX format
            prompt = f"""Convert the following references to BibTeX format. 
            Generate proper BibTeX entries with appropriate citation keys (e.g., powers1973, sutton2018, etc.).
            Use standard BibTeX entry types (@article, @book, @inbook, @misc, etc.).
            Ensure all entries are properly formatted and complete.
            
            References:
            {refs_content}
            
            Generate only the BibTeX entries, no additional text:"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert in bibliographic formatting and BibTeX."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            bibtex_content = response.choices[0].message.content
            
            # Clean markdown code fences if present
            import re
            bibtex_content = re.sub(r'^```+bibtex\s*', '', bibtex_content, flags=re.MULTILINE)
            bibtex_content = re.sub(r'^```+\s*$', '', bibtex_content, flags=re.MULTILINE)
            bibtex_content = bibtex_content.strip()
            
            with open(bibtex_path, 'w', encoding='utf-8') as f:
                f.write(bibtex_content)
            
            # Update metadata to track references.txt hash
            metadata = self.load_metadata()
            metadata["bibtex"] = {
                "input_hash": self.get_file_hash(references_file),
                "generated_at": datetime.now().isoformat(),
                "output_file": str(bibtex_path)
            }
            self.save_metadata(metadata)
            
            print(f"[OK] BibTeX file generated: {bibtex_path}")
            return True
            
        except Exception as e:
            print(f"Error generating BibTeX: {e}")
            return False
    
    def generate_latex(self, output_filename: str = "technical_report.tex") -> bool:
        """Generate LaTeX source file from all section files."""
        print("Generating LaTeX report...")
        
        # Get version and author info
        version = self.get_version_number()
        author = self.get_author_name()
        email = self.get_author_email()
        title = self.get_report_title()
        subtitle = self.get_report_subtitle()
        org = self.get_report_organization()
        
        # Create latex_output directory
        latex_output_dir = self.output_dir / "latex_output"
        latex_output_dir.mkdir(exist_ok=True)
        
        latex_path = latex_output_dir / output_filename
        
        try:
            with open(latex_path, 'w', encoding='utf-8') as f:
                # LaTeX preamble
                f.write(r"""\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{times}
\usepackage[margin=1in]{geometry}
\usepackage{setspace}
\usepackage{parskip}
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{natbib}

% Configure hyperlinks
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    citecolor=blue,
    urlcolor=blue
}

% Configure section formatting
\titleformat{\section}{\Large\bfseries}{\thesection.}{0.5em}{}
\titleformat{\subsection}{\large\bfseries}{\thesubsection.}{0.5em}{}

% Line spacing
\onehalfspacing

\begin{document}

""")
                
                # Title page
                f.write(r"\begin{titlepage}" + "\n")
                f.write(r"\centering" + "\n")
                f.write(r"\vspace*{1cm}" + "\n\n")
                f.write(f"{{\\huge\\bfseries {self._escape_latex(title)}\\par}}\n\n")
                f.write(r"\vspace{0.5cm}" + "\n")
                f.write(f"{{\\Large {self._escape_latex(subtitle)}\\par}}\n\n")
                f.write(r"\vspace{1.5cm}" + "\n\n")
                
                # Author info - all on one line
                author_line = f"\\textbf{{Author:}} {self._escape_latex(author)}"
                if email:
                    author_line += f" \\quad \\textbf{{Email:}} \\texttt{{{self._escape_latex(email)}}}"
                author_line += f" \\quad \\textbf{{Version:}} {version}"
                author_line += f" \\quad \\textbf{{Date:}} {datetime.now().strftime('%B %d, %Y')}"
                f.write(f"{{{author_line}\\par}}\n\n")
                if org:
                    f.write(f"{{\\textbf{{Organization:}} {self._escape_latex(org)}\\par}}\n\n")
                
                # Abstract on title page
                abstract_file = self.output_dir / "abstract.txt"
                if abstract_file.exists():
                    f.write(r"\vspace{1.5cm}" + "\n")
                    f.write(r"\begin{abstract}" + "\n")
                    with open(abstract_file, 'r', encoding='utf-8') as af:
                        abstract_content = af.read().strip()
                        if abstract_content:
                            # Convert citations before escaping
                            abstract_content = self._convert_citations_to_latex(abstract_content)
                            abstract_content = self._escape_latex(abstract_content, protect_commands=True)
                            f.write(abstract_content + "\n")
                    f.write(r"\end{abstract}" + "\n")
                
                f.write(r"\end{titlepage}" + "\n\n")
                
                # New page for content
                f.write(r"\newpage" + "\n\n")
                
                # Add each section
                section_counter = 0
                for section in self.sections:
                    if section == "abstract":  # Skip abstract section
                        continue
                    
                    if section == "references":  # Handle references specially
                        # Use BibTeX instead of inline references
                        f.write(r"\bibliographystyle{apalike}" + "\n")
                        f.write(r"\bibliography{references}" + "\n\n")
                        continue
                    
                    output_file = self.output_dir / f"{section}.txt"
                    
                    if output_file.exists():
                        section_counter += 1
                        section_title = self.section_titles[section]
                        
                        # Add section
                        f.write(f"\\section{{{self._escape_latex(section_title)}}}\n\n")
                        
                        # Read and add content
                        with open(output_file, 'r', encoding='utf-8') as sf:
                            content = sf.read().strip()
                            if content:
                                # First convert code blocks to LaTeX verbatim
                                content = self._convert_code_blocks_to_latex(content)
                                # Then convert tables to LaTeX
                                content = self._convert_tables_to_latex(content)
                                # Then convert image references to LaTeX figures
                                content = self._convert_images_to_latex(content)
                                # Then convert citations to LaTeX cite commands
                                content = self._convert_citations_to_latex(content)
                                # Then escape LaTeX special characters (protecting cite commands)
                                content = self._escape_latex(content, protect_commands=True)
                                # Replace double newlines with paragraph breaks
                                paragraphs = content.split('\n\n')
                                for para in paragraphs:
                                    if para.strip():
                                        f.write(para.strip() + "\n\n")
                        
                        f.write("\n")
                    else:
                        print(f"Warning: Output file {output_file} not found. Skipping {section} in LaTeX.")
                
                # End document
                f.write(r"\end{document}" + "\n")
            
            print(f"[OK] LaTeX report generated: {latex_path}")
            return True
            
        except Exception as e:
            print(f"Error generating LaTeX: {e}")
            return False
    
    def _escape_latex(self, text: str, protect_commands: bool = False) -> str:
        """Escape special LaTeX characters in text.
        
        Args:
            text: Text to escape
            protect_commands: If True, don't escape text within \\cite{} and other LaTeX commands
        """
        # First, replace Unicode mathematical symbols with LaTeX equivalents
        unicode_math = {
            '≥': r'$\geq$', '≤': r'$\leq$', '≈': r'$\approx$', '≠': r'$\neq$',
            '×': r'$\times$', '÷': r'$\div$', '±': r'$\pm$', '∞': r'$\infty$',
            '°': r'$^\circ$',
        }
        for char, latex in unicode_math.items():
            text = text.replace(char, latex)
        
        if protect_commands:
            # Temporarily replace LaTeX commands with placeholders that won't be escaped
            import re
            
            # Protect verbatim environments (multi-line)
            verbatim_pattern = r'(\\begin\{verbatim\}.*?\\end\{verbatim\})'
            verbatims = re.findall(verbatim_pattern, text, re.DOTALL)
            verbatim_placeholders = {}
            for i, verbatim in enumerate(verbatims):
                placeholder = f'XXVERBATIMMARKER{i}XX'
                verbatim_placeholders[placeholder] = verbatim
                text = text.replace(verbatim, placeholder)
            
            # Protect table environments (multi-line)
            table_pattern = r'(\\begin\{table\}.*?\\end\{table\})'
            tables = re.findall(table_pattern, text, re.DOTALL)
            table_placeholders = {}
            for i, table in enumerate(tables):
                placeholder = f'XXTABLEMARKER{i}XX'
                table_placeholders[placeholder] = table
                text = text.replace(table, placeholder)
            
            # Protect figure environments (multi-line)
            figure_pattern = r'(\\begin\{figure\}.*?\\end\{figure\})'
            figures = re.findall(figure_pattern, text, re.DOTALL)
            figure_placeholders = {}
            for i, figure in enumerate(figures):
                placeholder = f'XXFIGUREMARKER{i}XX'
                figure_placeholders[placeholder] = figure
                text = text.replace(figure, placeholder)
            
            # Protect citations (\cite, \citep, \citet, etc.)
            cite_pattern = r'(~?\\cite[pt]?\{[^}]+\})'
            cites = re.findall(cite_pattern, text)
            cite_placeholders = {}
            for i, cite in enumerate(cites):
                placeholder = f'XXTEMPMARKER{i}XX'
                cite_placeholders[placeholder] = cite
                text = text.replace(cite, placeholder)
            
            # Protect math
            math_pattern = r'(\$[^$]+\$)'
            maths = re.findall(math_pattern, text)
            math_placeholders = {}
            for i, math in enumerate(maths):
                placeholder = f'XXMATHMARKER{i}XX'
                math_placeholders[placeholder] = math
                text = text.replace(math, placeholder)
        
        replacements = {
            '\\': r'\textbackslash{}',
            '{': r'\{',
            '}': r'\}',
            '$': r'\$',
            '&': r'\&',
            '%': r'\%',
            '#': r'\#',
            '_': r'\_',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}'
        }
        
        # First pass: escape backslash
        if '\\' in text:
            text = text.replace('\\', replacements['\\'])
        
        # Second pass: escape other characters
        for char, replacement in replacements.items():
            if char != '\\' and char in text:
                text = text.replace(char, replacement)
        
        if protect_commands:
            # Restore in reverse order
            # Restore math first
            for placeholder, math in math_placeholders.items():
                text = text.replace(placeholder, math)
            # Restore \cite{...} commands
            for placeholder, cite in cite_placeholders.items():
                text = text.replace(placeholder, cite)
            # Restore figures
            for placeholder, figure in figure_placeholders.items():
                text = text.replace(placeholder, figure)
            # Restore tables
            for placeholder, table in table_placeholders.items():
                text = text.replace(placeholder, table)
            # Restore verbatim last
            for placeholder, verbatim in verbatim_placeholders.items():
                text = text.replace(placeholder, verbatim)
        
        return text
    
    def _convert_citations_to_latex(self, text: str) -> str:
        """Convert (Author, Year) citations to LaTeX cite commands."""
        import re
        
        # Common citation patterns to convert - using raw strings for patterns, normal strings for LaTeX output
        citation_map = {
            r'\(Powers et al\., 1960\)': r'~\\cite{powers1960}',  # Using raw string with escaped backslash
            r'\(Powers, 1973\)': r'~\\cite{powers1973}',
            r'\(Sutton and Barto, 2018\)': r'~\\cite{sutton2018}',
            r'\(Sutton \& Barto, 2018\)': r'~\\cite{sutton2018}',
            r'\(Mnih et al\., 2015\)': r'~\\cite{mnih2015}',
            r'\(Young, 2017\)': r'~\\cite{young2017}',
            r'\(Young, 2020\)': r'~\\cite{young2020}',
            r'\(Young, 2025\)': r'~\\cite{young2025}',
            r'\(timurgepard, 2025\)': r'~\\cite{timurgepard2025}',
            # Keep generic placeholders as text for now
            r'\(Author, Year\)': '',  # Remove placeholder citations
        }
        
        for pattern, replacement in citation_map.items():
            text = re.sub(pattern, replacement, text)
        
        return text
    
    def _convert_images_to_latex(self, text: str) -> str:
        """Convert image references to LaTeX includegraphics commands.
        
        Detects patterns like:
        - [Image path/to/image.png]
        - [Image: path/to/image.png]
        - **Image**: `path/to/image.png`
        And converts them to LaTeX figure environments with labels and references.
        Figures are placed at the end of the text with references in the original location.
        """
        import re
        import os
        
        # Storage for figures to be added at the end
        figures = []
        figure_counter = 0
        
        # Pattern 1: [Image: path] or [Image: path [width=...] (caption)]
        image_pattern1 = r'\[Image:\s+([^\s\[\(]+)(?:\s+\[([^\]]+)\])?(?:\s+\(([^\)]+)\))?\]'
        
        # Pattern 2: **Image**: `filename.png` with optional width and caption on next lines
        # Format: - **Image**: `file.png`
        #         - [width=1.0\textwidth]
        #         - Caption: text
        image_pattern2 = r'-\s+\*\*Image\*\*:\s+`([^`]+)`(?:\s*\n\s*-\s+\[([^\]]+)\])?(?:\s*\n\s*-\s+Caption:\s*([^\n]+))?'
        
        def replace_image(match):
            nonlocal figure_counter
            image_path = match.group(1).strip()
            width_spec = match.group(2).strip() if len(match.groups()) > 1 and match.group(2) else None
            caption = match.group(3).strip() if len(match.groups()) > 2 and match.group(3) else None
            
            # Strip quotes and backticks from image path if present
            image_path = image_path.strip('\'"` ')
            
            # Handle Windows paths with backslashes and spaces
            # Convert to forward slashes for LaTeX
            latex_path = image_path.replace('\\', '/')
            
            # Parse width specification (default to 0.8\textwidth)
            if width_spec:
                width_param = width_spec
            else:
                width_param = 'width=0.8\\textwidth'
            
            # Check if file exists in input directory
            input_file_path = self.input_dir / image_path
            file_exists = input_file_path.exists()
            
            # Generate unique label for this figure
            figure_counter += 1
            fig_label = f'fig:{os.path.splitext(os.path.basename(image_path))[0]}{figure_counter}'
            
            # Create figure environment
            latex_code = '\n\\begin{figure}[htbp]\n'
            latex_code += '\\centering\n'
            
            if file_exists:
                # Use includegraphics with specified width
                latex_code += f'\\includegraphics[{width_param}]{{{latex_path}}}\n'
            else:
                # Add placeholder text if image not found
                latex_code += f'\\fbox{{\\parbox{{0.8\\textwidth}}{{\\centering Image not found:\\\\{latex_path}}}}}\n'
            
            # Use provided caption or default
            if caption:
                latex_code += f'\\caption{{{caption}}}\n'
            else:
                latex_code += f'\\caption{{Figure from: {os.path.basename(image_path)}}}\n'
            
            latex_code += f'\\label{{{fig_label}}}\n'
            latex_code += '\\end{figure}\n'
            
            # Store the figure
            figures.append(latex_code)
            
            # Return a reference to the figure
            return f'Figure~\\ref{{{fig_label}}}'
        
        # Replace Pattern 1: [Image: path]
        text = re.sub(image_pattern1, replace_image, text)
        
        # Replace Pattern 2: **Image**: `path` with optional width and caption support
        def replace_image_with_caption(match):
            nonlocal figure_counter
            image_path = match.group(1).strip()
            width_spec = match.group(2).strip() if match.group(2) else None
            caption = match.group(3).strip() if match.group(3) else None
            
            # Strip quotes and backticks from image path if present
            image_path = image_path.strip('\'"` ')
            
            # Handle Windows paths with backslashes and spaces
            latex_path = image_path.replace('\\', '/')
            
            # Parse width specification (default to 0.8\textwidth)
            if width_spec:
                # Width spec should be like "width=1.0\textwidth"
                width_param = width_spec
            else:
                width_param = 'width=0.8\\textwidth'
            
            # Check if file exists in input directory
            input_file_path = self.input_dir / image_path
            file_exists = input_file_path.exists()
            
            # Generate unique label for this figure
            figure_counter += 1
            fig_label = f'fig:{os.path.splitext(os.path.basename(image_path))[0]}{figure_counter}'
            
            # Create figure environment
            latex_code = '\n\\begin{figure}[htbp]\n'
            latex_code += '\\centering\n'
            
            if file_exists:
                latex_code += f'\\includegraphics[{width_param}]{{{latex_path}}}\n'
            else:
                latex_code += f'\\fbox{{\\parbox{{0.8\\textwidth}}{{\\centering Image not found:\\\\{latex_path}}}}}\n'
            
            if caption:
                latex_code += f'\\caption{{{caption}}}\n'
            else:
                latex_code += f'\\caption{{Figure: {os.path.basename(image_path)}}}\n'
            
            latex_code += f'\\label{{{fig_label}}}\n'
            latex_code += '\\end{figure}\n'
            
            # Store the figure
            figures.append(latex_code)
            
            # Return a reference to the figure
            return f'Figure~\\ref{{{fig_label}}}'
        
        text = re.sub(image_pattern2, replace_image_with_caption, text, flags=re.MULTILINE)
        
        # Append all figures at the end
        if figures:
            text += '\n\n' + '\n'.join(figures)
        
        return text
    
    def _convert_code_blocks_to_latex(self, text: str) -> str:
        """Convert markdown code blocks (```) to LaTeX verbatim environment.
        
        Converts fenced code blocks like:
        ```
        code here
        ```
        
        to:
        \begin{verbatim}
        code here
        \end{verbatim}
        """
        import re
        
        # Pattern to match fenced code blocks with optional language identifier
        # Matches ``` or ```language at the start, content, and closing ```
        code_block_pattern = r'```(?:[a-zA-Z0-9_+-]*)?\n(.*?)\n```'
        
        def replace_code_block(match):
            code_content = match.group(1)
            # Return verbatim environment
            return f'\\begin{{verbatim}}\n{code_content}\n\\end{{verbatim}}'
        
        # Replace all code blocks
        text = re.sub(code_block_pattern, replace_code_block, text, flags=re.DOTALL)
        
        return text
    
    def _convert_tables_to_latex(self, text: str) -> str:
        """Convert markdown tables to LaTeX table environments.
        
        Detects markdown tables in the format:
        | Header 1 | Header 2 |
        |----------|----------|
        | Cell 1   | Cell 2   |
        
        Also detects captions in these formats:
        - Before table: **Table N:** Caption text
        - Before table: - Caption: Caption text
        - After table: Table: Caption text
        """
        import re
        
        # Pattern to match optional caption before table + table + optional caption after
        # Caption before: **Table N:** or - Caption:
        # Caption after: Table: or Caption:
        full_table_pattern = r'(?:(?:\*\*Table\s+\d+:\*\*|(?:^|\n)-\s*Caption:)\s*([^\n]+)\n+)?' \
                            r'(\|[^\n]+\|\n\|[-:\s|]+\|\n(?:\|[^\n]+\|\n?)+)' \
                            r'(?:\n+(?:Table:|Caption:)\s*([^\n]+))?'
        
        def replace_table(match):
            caption_before = match.group(1)
            table_text = match.group(2).strip()
            caption_after = match.group(3)
            
            # Use whichever caption exists (prefer before over after)
            caption = caption_before if caption_before else caption_after
            
            lines = table_text.split('\n')
            
            if len(lines) < 2:
                return table_text  # Not a valid table
            
            # Parse header
            header_line = lines[0]
            headers = [cell.strip() for cell in header_line.split('|')[1:-1]]
            num_cols = len(headers)
            
            # Skip separator line (lines[1])
            
            # Parse data rows
            data_rows = []
            for line in lines[2:]:
                if line.strip():
                    cells = [cell.strip() for cell in line.split('|')[1:-1]]
                    if len(cells) == num_cols:
                        data_rows.append(cells)
            
            # Build LaTeX table with better formatting
            latex_code = '\n\\begin{table}[h]\n'
            latex_code += '\\centering\n'
            latex_code += '\\small\n'  # Use smaller font for better fit
            # Use p{width} columns for text wrapping instead of c for centered
            # First column left-aligned, rest centered with wrapping
            col_spec = '|l|' + 'c|' * (num_cols - 1)
            latex_code += f'\\begin{{tabular}}{{{col_spec}}}\n'
            latex_code += '\\hline\n'
            
            # Add header with bold font
            header_formatted = ' & '.join([f'\\textbf{{{h}}}' for h in headers])
            latex_code += header_formatted + ' \\\\\n'
            latex_code += '\\hline\n'
            
            # Add data rows
            for row in data_rows:
                latex_code += ' & '.join(row) + ' \\\\\n'
            
            latex_code += '\\hline\n'
            latex_code += '\\end{tabular}\n'
            
            # Add caption if present
            if caption:
                latex_code += f'\\caption{{{caption.strip()}}}\n'
            
            latex_code += '\\end{table}\n'
            
            return latex_code
        
        text = re.sub(full_table_pattern, replace_table, text, flags=re.MULTILINE)
        
        return text
    
    def compile_latex_to_pdf(self, latex_filename: str = "technical_report.tex") -> bool:
        """Compile LaTeX file to PDF using pdflatex."""
        print("Compiling LaTeX to PDF...")
        
        latex_output_dir = self.output_dir / "latex_output"
        latex_path = latex_output_dir / latex_filename
        
        if not latex_path.exists():
            print(f"LaTeX file {latex_path} not found. Cannot compile.")
            return False
        
        # Copy references.bib to latex_output if it exists
        ref_source = self.output_dir / "references.bib"
        ref_dest = latex_output_dir / "references.bib"
        if ref_source.exists():
            import shutil
            shutil.copy2(ref_source, ref_dest)
        
        # Copy image files from input to latex_output
        import shutil
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.pdf', '.eps']
        for image_file in self.input_dir.iterdir():
            if image_file.is_file() and image_file.suffix.lower() in image_extensions:
                dest_file = latex_output_dir / image_file.name
                shutil.copy2(image_file, dest_file)
                print(f"  Copied image: {image_file.name}")
        
        try:
            import subprocess
            
            # Run pdflatex -> bibtex -> pdflatex -> pdflatex for bibliography
            # Run from latex_output directory so all files stay there
            print(f"  Running pdflatex (pass 1/3)...")
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', latex_filename],
                capture_output=True,
                text=True,
                cwd=str(latex_output_dir)
            )
            
            if result.returncode != 0:
                print(f"pdflatex error output:")
                print(result.stdout)
            
            # Run bibtex
            print(f"  Running bibtex...")
            tex_basename = Path(latex_filename).stem
            bibtex_result = subprocess.run(
                ['bibtex', tex_basename],
                capture_output=True,
                text=True,
                cwd=str(latex_output_dir)
            )
            
            if bibtex_result.returncode != 0:
                print(f"bibtex warning (may be normal if no citations):")
                print(bibtex_result.stdout)
            
            # Run pdflatex two more times to resolve references
            for run in range(2, 4):
                print(f"  Running pdflatex (pass {run}/3)...")
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', latex_filename],
                    capture_output=True,
                    text=True,
                    cwd=str(latex_output_dir)
                )
                
                if result.returncode != 0:
                    print(f"pdflatex error output:")
                    print(result.stdout)
                    if run == 3:  # Only fail on final run
                        return False
            
            pdf_path = latex_output_dir / latex_filename.replace('.tex', '.pdf')
            if pdf_path.exists():
                print(f"[OK] LaTeX PDF compiled: {pdf_path}")
                return True
            else:
                print("PDF file not created after compilation.")
                return False
                
        except FileNotFoundError:
            print("Error: pdflatex not found. Please install a LaTeX distribution (e.g., MiKTeX or TeX Live).")
            print("For Windows: https://miktex.org/download")
            print("For more info, see: https://www.latex-project.org/get/")
            return False
        except Exception as e:
            print(f"Error compiling LaTeX: {e}")
            return False
    
    def run(self, force_regenerate: bool = False, pdf_only: bool = False, concatenate_only: bool = False, latex: bool = False, compile_latex_only: bool = False) -> bool:
        """Main execution method."""
        print("Technical Report Generator")
        print(f"Environment: {self.environment}")
        print("=" * 50)
        
        # Load title information from title.md
        self.load_title_info()
        
        # If only compiling LaTeX to PDF
        if compile_latex_only:
            return self.compile_latex_to_pdf()
        
        # If only concatenating input files
        if concatenate_only:
            return self.concatenate_input_files()
        
        if not pdf_only:
            if force_regenerate:
                print("Force regenerating all sections...")
                # Clear metadata to force regeneration
                if self.metadata_file.exists():
                    self.metadata_file.unlink()
                    
            updated_sections = self.generate_sections()
            
            if updated_sections:
                print(f"\nUpdated sections: {', '.join(updated_sections)}")
            else:
                print("\nNo sections needed updating.")
        
        # Generate concatenated input file
        self.concatenate_input_files()
        
        # Generate outputs based on flags
        if not pdf_only:
            any_sections_exist = any((self.output_dir / f"{section}.txt").exists() for section in self.sections)
        else:
            any_sections_exist = True
            
        if any_sections_exist:
            success = True
            
            # Generate LaTeX if requested
            if latex:
                # Generate BibTeX first
                bibtex_success = self.generate_bibtex()
                success = success and bibtex_success
                
                # Generate LaTeX
                latex_success = self.generate_latex()
                success = success and latex_success
                
                # Compile LaTeX to PDF if LaTeX generation succeeded
                if latex_success:
                    compile_success = self.compile_latex_to_pdf()
                    success = success and compile_success
            
            # Always generate ReportLab PDF
            pdf_success = self.generate_pdf()
            success = success and pdf_success
            
            return success
        else:
            print("No output sections found. Please ensure input files exist and run generation first.")
            return False

def create_sample_input_files(input_dir: Path):
    """Create sample input files for demonstration."""
    sample_content = {
        "abstract": """# Abstract Notes

**Note**: This section will be automatically generated from your other sections.

Abstract will include:
- **Research objective**: Compare PCT vs RL control systems
- **Methodology**: Environment testing and evaluation
- **Key findings**: Trade-offs between interpretability and convergence
- **Conclusions**: Each approach has distinct advantages
""",
        
        "introduction": """# Introduction Notes

## Key Points

- **Control systems** are critical for autonomous agents
- **Traditional control** vs **modern AI approaches**
- **PCT** offers:
  - Biological inspiration and interpretability
  - Realistic rationale
  - Simpler architecture and computational footprint
- **RL** provides:
  - Data-driven learning capabilities
  - *Limitations*: Input-action mapping not biologically credible, reward efficacy concept not psychologically coherent
- **Research gap**: Direct comparison in standardized environment
- Specific environment provides consistent evaluation platform
""",
        
        "background": """# Background Notes

## Topics to Cover

### Perceptual Control Theory
- **PCT fundamentals**: Elegant and powerful hierarchical architecture
  - Self-correcting feedback loop
  - Adapts to environment (Powers, 1973)

### Optimization & Learning
- **Evolutionary algorithms** for hierarchy optimization
- **Reinforcement learning** theory and deep Q-networks

### Environment
- **Characteristics and challenges** of the target environment

### Related Work
- Previous comparative studies **limitations**
- Control system **evaluation metrics**
""",
        
        "methodology": """# Methodology Notes

## Environment Setup
- **Target environment**: Specify your target environment

## PCT Implementation
- **PCT hierarchy**: Optimally generated by evolutionary algorithm
  - Guided by rewards and specific fitness function
- **Evolutionary algorithm**: DEAP framework with Optuna hyperparameter optimization

## RL Baseline
- **RL approach**: Simphony taken from OpenAI Gym leaderboard

## Evaluation
- **Metrics**:
  - Episodes
  - Success rate (out of 100 retries)
  - Steps
  - Number of nodes
  - Number of weights
- **Statistical analysis**: t-tests, effect sizes

## Hardware
- **Specs**: Specify this machine's specifications
""",
        
        "experimental_results": """# Experimental Results Notes

## Performance Data

### Comparison
- **Performance comparison** across 100 episodes
- **Results summary table**

### Reproducibility
- **Results reproduction**:
  - *TODO*: PCT example
  - Simphony model

### Visual Media
- **Videos** of controller performance
- **Environment images**

### Analysis
- **Key findings and insights**
""",
        
        "discussion": """# Discussion Notes

## PCT Advantages
- **Interpretability**: Break down into control units
- **Biological plausibility**
- **Psychologically credible**
- **Smaller computational footprint**

## RL Advantages
- **Sample efficiency**
- **Generalization**
- **Scalability**

## Analysis Points
- **Comparative analysis**: Strengths and weaknesses of each approach
- **Trade-offs** between approaches
- **Implications** for real-world applications
- **Limitations** of current study
- **Unexpected findings** and their explanations
""",
        
        "recommendations_future_work": """# Recommendations & Future Work Notes

## Recommendations

### Hybrid Approaches
- Combining **PCT and RL**

### Extended Testing
- Testing on more **complex and realistic** world environments
- **Real-world robotics** applications

### Computational Optimization
- Implement **EPCT in deep learning framework**
- **Parallel processing** and GPUs

### AI Interpretability
- **Human-interpretable AI systems**
""",
        
        "references": """# References Notes

## Key References to Include

### Perceptual Control Theory

- Powers, W. T., Clark, R., and McFarland, R. (1960). A general feedback theory of human behavior: Part i. *Perceptual and motor skills*, 11(1):71–88.

- Powers, W. T. (1973). *Behavior: The control of perception*. Aldine de Gruyter.

- Young, R. (2017). A General Architecture for Robotics Systems: A Perception-Based Approach to Artificial Life. *Artificial Life*, 23(2):236–286.

- Young, R. (2020). Robotics in the real world: the perceptual control theory approach. In Mansell, W., editor, *The Interdisciplinary Handbook of Perceptual Control Theory*, chapter 14, pages 517–556. Academic Press.

### Reinforcement Learning

- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction*. MIT Press.

- Mnih, V., Kavukcuoglu, K., Silver, D., Rusu, A. A., Veness, J., Bellemare, M. G., ... & Hassabis, D. (2015). Human-level control through deep reinforcement learning. *Nature*, 518(7540), 529-533.

### Benchmarking

- OpenAI Gym benchmarking studies
"""
    }
    
    for section, content in sample_content.items():
        filepath = input_dir / f"{section}.md"
        if not filepath.exists():
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content.strip())
    
    print(f"Sample input files created in {input_dir}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate technical report comparing PCT vs RL control systems",
        epilog="""
Examples:
  %(prog)s --create-samples                    Create sample input files
  %(prog)s                                     Smart generation (recommended)
  %(prog)s --force                            Force regenerate all sections
  %(prog)s --pdf-only                         Generate PDF from existing outputs
  %(prog)s --latex                            Generate LaTeX and compile to PDF
  %(prog)s --compile-latex-only               Compile existing LaTeX to PDF only
  %(prog)s --concatenate-only                 Only concatenate input files
  %(prog)s --environment "Lunar Lander"       Specify environment name
  %(prog)s --input-dir notes --output-dir reports    Use custom directories
  
Workflow:
  1. %(prog)s --create-samples                 # Create template files
  2. Edit files in input/ directory            # Add your content
  3. %(prog)s --force --latex                  # Generate initial report with LaTeX
  4. %(prog)s                                  # Daily updates (smart mode)
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--input-dir", default="input", 
                        help="Directory containing input notes files (default: input)")
    parser.add_argument("--output-dir", default="output", 
                        help="Directory for generated output files (default: output)")
    parser.add_argument("--environment", default="OpenAI Gym",
                        help="Environment name to include in title and content (default: OpenAI Gym)")
    parser.add_argument("--force", action="store_true", 
                        help="Force regenerate all sections (ignores change detection)")
    parser.add_argument("--pdf-only", action="store_true", 
                        help="Only generate PDF from existing output files (no AI generation)")
    parser.add_argument("--latex", action="store_true",
                        help="Generate LaTeX source file and compile to PDF (requires pdflatex)")
    parser.add_argument("--compile-latex-only", action="store_true",
                        help="Only compile existing LaTeX file to PDF (no generation, requires pdflatex)")
    parser.add_argument("--concatenate-only", action="store_true",
                        help="Only concatenate input files into a single file (no AI generation or PDF)")
    parser.add_argument("--create-samples", action="store_true", 
                        help="Create sample input files with template content")
    
    args = parser.parse_args()
    
    generator = TechnicalReportGenerator(args.input_dir, args.output_dir, args.environment)
    
    if args.create_samples:
        create_sample_input_files(generator.input_dir)
        return
    
    success = generator.run(force_regenerate=args.force, pdf_only=args.pdf_only, concatenate_only=args.concatenate_only, latex=args.latex, compile_latex_only=args.compile_latex_only)
    
    if success:
        print("\n[OK] Report generation completed successfully!")
    else:
        print("\n[ERROR] Report generation failed.")

if __name__ == "__main__":
    main()
