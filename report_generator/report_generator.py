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
        # Try environment variable first
        author = os.getenv("REPORT_AUTHOR")
        if author:
            return author
            
        # Try metadata
        metadata = self.load_metadata()
        author = metadata.get("author")
        if author:
            return author
            
        # Default fallback
        return "Research Team"
        
    def ensure_directories(self):
        """Create input and output directories if they don't exist."""
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
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
        input_file = self.input_dir / f"{section}.txt"
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
        """

        section_specific_prompts = {
            "introduction": "Write an introduction that frames the report as a presentation of PCT applied to the target environment, with a secondary comparison to an RL baseline. Clearly state the objectives and why PCT is an appropriate approach.",

            "background": f"Provide comprehensive background emphasizing Perceptual Control Theory (principles, hierarchy, and control units), the {self.environment} environment, and briefly summarize RL concepts used as a comparator. Establish the theoretical foundation with a PCT-first emphasis.",

            "methodology": f"Describe the methodology with PCT as the primary focus: the {self.environment} setup, PCT hierarchy design and training (e.g., evolutionary algorithm parameters), followed by a concise RL baseline configuration, evaluation metrics, and procedures.",

            "experimental_results": f"Present results primarily for the PCT controller in the {self.environment} environment, including performance, stability, and interpretability aspects; then compare against the RL baseline. Include descriptions of where figures and tables would be placed (e.g., '[Figure 1: Performance comparison graph would be inserted here]').",

            "discussion": "Analyze and interpret results with a PCT-first lens: strengths, limitations, implications, and design insights of PCT; then contrast with RL to highlight advantages/trade-offs.",

            "recommendations_future_work": "Provide specific recommendations focusing on advancing PCT (architecture, training, analysis) and outline future research, including more rigorous RL baselines for comparison.",

            "references": "Generate a comprehensive reference list in APA format with emphasis on PCT literature, along with relevant works on evolutionary algorithms, reinforcement learning, and control systems (use realistic but placeholder citations).",

            "abstract": "Write a concise abstract (150-250 words) that summarizes PCT applied to the target environment, followed by a brief comparison with an RL baseline. Include objective, methodology overview, key findings, and main conclusions."
        }

        prompt = f"{base_context}\n\n{section_specific_prompts[section]}\n\nNotes for this section:\n{notes}\n\nGenerate the content for this section:"

        return prompt
    
    def generate_section_content(self, section: str) -> Optional[str]:
        """Generate content for a specific section using OpenAI."""
        input_file = self.input_dir / f"{section}.txt"
        
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
            
            print(f"✓ Generated {section}")
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
            Based on the following technical report sections, write a concise abstract (150-250 words) that summarizes the research study comparing control systems for the {self.environment} environment. The abstract should include:
            1. Research objective and problem statement
            2. Methodology overview (PCT vs RL comparison)
            3. Key findings and results
            4. Main conclusions and implications
            
            Make it a standalone summary that gives readers a complete overview of the work.
            
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
            
            print("✓ Generated abstract from existing sections")
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
    
    def concatenate_input_files(self, output_filename: str = "all_sections_notes.txt") -> bool:
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
                    input_file = self.input_dir / f"{section}.txt"
                    
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
            
            print(f"✓ Input files concatenated: {output_path}")
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
        story.append(Paragraph(f"PCT Applied to {self.environment}:", styles['title']))
        story.append(Paragraph("with Comparative RL Baseline", styles['title']))
        story.append(Spacer(1, 0.3*inch))
        meta_line = f"Author: {author} — Version {version} — {datetime.now().strftime('%B %d, %Y')}"
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
            print(f"✓ PDF report generated: {pdf_path}")
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
                    print(f"✓ PDF report generated (fallback): {fallback_path}")
                    return True
                except Exception as e2:
                    print(f"Error generating PDF (fallback): {e2}")
                    return False
            else:
                print(f"Error generating PDF: {e}")
                return False
    
    def run(self, force_regenerate: bool = False, pdf_only: bool = False, concatenate_only: bool = False) -> bool:
        """Main execution method."""
        print("Technical Report Generator")
        print(f"Environment: {self.environment}")
        print("=" * 50)
        
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
        
        # Generate PDF if any sections were updated or if explicitly requested
        if not pdf_only:
            any_sections_exist = any((self.output_dir / f"{section}.txt").exists() for section in self.sections)
        else:
            any_sections_exist = True
            
        if any_sections_exist:
            success = self.generate_pdf()
            return success
        else:
            print("No output sections found. Please ensure input files exist and run generation first.")
            return False

def create_sample_input_files(input_dir: Path):
    """Create sample input files for demonstration."""
    sample_content = {
        "abstract": """
Abstract notes (this will be auto-generated from other sections):
- Research objective: Compare PCT vs RL control systems
- Methodology: Environment testing and evaluation
- Key findings: Trade-offs between interpretability and convergence
- Conclusions: Each approach has distinct advantages
Note: This section will be automatically generated from your other sections.
""",
        
        "introduction": """
Introduction notes:
- Control systems critical for autonomous agents
- Traditional control vs modern AI approaches
- PCT offers biological inspiration and interpretability, a realistic rationale and a simpler architecture and computational footprint.
- RL provides data-driven learning capabilities
- RL input-action mapping is not biologically credible, R's concept of reward efficacy is not psychologically coherent.
- Research gap: direct comparison in standardized environment
- Specific environment provides consistent evaluation platform
""",
        
        "background": """
Background information to cover:
- Perceptual Control Theory fundamentals - elegant and powerful hierarchical architecure, self-correcting feedback loop, adapts to environment (Powers, 1973)
- Evolutionary algorithms for hierarchy optimization
- Reinforcement learning theory and deep Q-networks
- Environment characteristics and challenges
- Previous comparative studies limitations
- Control system evaluation metrics
""",
        
        "methodology": """
Methodology details:
- Environment: Specify your target environment 
- PCT hierarchy: optimally generated by evolutionary algorithm, guided by rewards and specific fitness function. 
- Evolutionary algorithm: DEAP framework with Optuna hyperparameter optimization.
- RL approach: Simphony taken from OpenAI Gym leaderboard.
- Evaluation metrics: episodes, success of retries out of 100, steps, #nodes, #weights
- Statistical analysis: t-tests, effect sizes
- Hardware: spec of this machine
""",
        
        "experimental_results": """
Results to present:
- Performance comparison across 100 episodes
- Results summary table
- Results reproduction
-- TODO: PCT example
-- Simphony model
- Videos
- Environment image
- Key findings and insights
""",
        
        "discussion": """
Discussion points:
- PCT advantages: interpretability (break down into control units), biological plausibility, psychologically credible, smaller computational footprint
- RL advantages: sample efficiency, generalization, scalability
- Comparative analysis: strengths and weaknesses of each approach
- Trade-offs between approaches
- Implications for real-world applications
- Limitations of current study
- Unexpected findings and their explanations
""",
        
        "recommendations_future_work": """
Recommendations and future work:
- Hybrid approaches combining PCT and RL
- Testing on more complex and realistic world environments
- Real-world robotics applications
- Computational optimization strategies - implement EPCT in deep learning framework, parallel processing and GPUs
- Human-interpretable AI systems

""",
        
        "references": """
Key references to include:
- Powers, W. T., Clark, R., and McFarland, R. (1960). A general feedback theory of human behavior: Part i. Perceptual and motor skills, 11(1):71–88.
- Powers, W. T. (1973). Behavior: The control of perception. Aldine de Gruyter.
- Sutton, R. S., & Barto, A. G. (2018). Reinforcement Learning: An Introduction. MIT Press.
- Mnih, V., Kavukcuoglu, K., Silver, D., Rusu, A. A., Veness, J., Bellemare, M. G., ... & Hassabis, D. (2015). Human-level control through deep reinforcement learning. Nature, 518(7540), 529-533.
- Young, R. (2017). A General Architecture for Robotics Systems: A Perception-Based Approach to Artificial Life. Artificial Life, 23(2):236–286.
- Young, R. (2020). Robotics in the real world: the perceptual control theory approach. In Mansell, W., editor, The Interdisciplinary Handbook of Perceptual Control Theory, chapter 14, pages 517–556. Academic Press.
- OpenAI Gym benchmarking studies
"""
    }
    
    for section, content in sample_content.items():
        filepath = input_dir / f"{section}.txt"
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
  %(prog)s --concatenate-only                 Only concatenate input files
  %(prog)s --environment "Lunar Lander"       Specify environment name
  %(prog)s --input-dir notes --output-dir reports    Use custom directories
  
Workflow:
  1. %(prog)s --create-samples                 # Create template files
  2. Edit files in input/ directory            # Add your content
  3. %(prog)s --force                          # Generate initial report
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
    parser.add_argument("--concatenate-only", action="store_true",
                        help="Only concatenate input files into a single file (no AI generation or PDF)")
    parser.add_argument("--create-samples", action="store_true", 
                        help="Create sample input files with template content")
    
    args = parser.parse_args()
    
    generator = TechnicalReportGenerator(args.input_dir, args.output_dir, args.environment)
    
    if args.create_samples:
        create_sample_input_files(generator.input_dir)
        return
    
    success = generator.run(force_regenerate=args.force, pdf_only=args.pdf_only, concatenate_only=args.concatenate_only)
    
    if success:
        print("\n✓ Report generation completed successfully!")
    else:
        print("\n✗ Report generation failed.")

if __name__ == "__main__":
    main()
