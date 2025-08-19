# Technical Report Generator

## Overview
This application generates PDF technical reports comparing control systems for OpenAI Gym environments, specifically comparing Perceptual Control Theory (PCT) hierarchies generated through evolutionary algorithms with controllers derived by Reinforcement Learning.

## Features
- **Smart Generation**: Only regenerates sections when input files change (based on file hash comparison)
- **OpenAI Integration**: Uses GPT-4 to generate technical content from your notes
- **Professional PDF Output**: Creates formatted PDFs with Times New Roman font and APA-style citations
- **Modular Sections**: Supports standard technical report structure
- **Change Tracking**: Maintains metadata to avoid unnecessary API calls
- **Input Concatenation**: Automatically creates a single file with all your notes in the correct order
- **Version Control**: Automatically increments version numbers on each generation
- **Auto-Generated Abstract**: Creates abstract based on content from other sections and displays it on the title page
- **Author Attribution**: Includes author information on title page

## Report Sections
1. Title Page (with Abstract, Version, and Author)
2. Executive Summary
3. Introduction  
4. Background
5. Methodology
6. Experimental Results
7. Discussion
8. Recommendations & Future Work
9. References

**Note**: The Abstract is auto-generated from other sections and displayed on the title page.

## Setup

### Prerequisites
```bash
pip install openai reportlab python-dotenv
```

### Environment Configuration
The application will automatically look for your OpenAI API key in these locations (in order):
1. `.env` file in the VS Code root folder (recommended)
2. `.env` file in the current directory
3. System environment variables

Create a `.env` file in your VS Code root folder:
```
OPENAI_API_KEY=your_openai_api_key_here
REPORT_AUTHOR=Your Name
```

Or if you prefer, create it in the report_generator directory:
```
OPENAI_API_KEY=your_openai_api_key_here
REPORT_AUTHOR=Your Name
```

### Directory Structure
```
report_generator/
├── input/                  # Your notes for each section (.txt files)
│   ├── executive_summary.txt
│   ├── abstract.txt        # Optional - will be auto-generated
│   ├── introduction.txt
│   ├── background.txt
│   ├── methodology.txt
│   ├── experimental_results.txt
│   ├── discussion.txt
│   ├── recommendations_future_work.txt
│   ├── references.txt
│   └── all_sections_notes.txt  # Auto-generated concatenated file
├── output/                 # Generated content and final PDF
│   ├── executive_summary.txt
│   ├── abstract.txt        # Auto-generated from other sections
│   ├── introduction.txt
│   ├── ...
│   ├── metadata.json       # Version tracking and file hashes
│   └── technical_report.pdf # Final PDF with version and author
└── report_generator.py
```

## Usage

### Basic Commands

#### 1. Create Sample Input Files
```bash
python report_generator.py --create-samples
```
Creates template input files with sample content in the `input/` directory.

#### 2. Generate Report (Smart Mode - Recommended)
```bash
python report_generator.py
```
**What it does:**
- Checks which input files have changed since last generation
- Regenerates only sections that need updating
- Creates PDF if any sections were updated
- Saves API costs by avoiding unnecessary regeneration

#### 2a. Generate Report with Custom Environment
```bash
python report_generator.py --environment "Lunar Lander"
```
**What it does:**
- Same as above but customizes the environment name in title and content
- Environment name appears in PDF title and AI-generated content

#### 3. Force Regenerate All Sections
```bash
python report_generator.py --force
```
**When to use:**
- First time generation
- After major changes to prompts or structure
- When you want to refresh all content regardless of changes

#### 4. Generate PDF Only
```bash
python report_generator.py --pdf-only
```
**When to use:**
- You've manually edited output files
- Want to regenerate PDF with different formatting
- Troubleshooting PDF generation issues

#### 5. Concatenate Input Files Only
```bash
python report_generator.py --concatenate-only
```
**What it does:**
- Creates a single file with all input notes in the correct order
- Useful for overview, backup, or sharing your notes
- No AI generation or PDF creation

### Advanced Usage

#### Custom Directories
```bash
# Use different input/output directories
python report_generator.py --input-dir "research_notes" --output-dir "final_reports"

# Specify custom environment name
python report_generator.py --environment "Lunar Lander"

# Combine environment with other options
python report_generator.py --environment "CartPole" --force

# Relative paths work too
python report_generator.py --input-dir "../notes" --output-dir "./reports"

# Windows absolute paths with environment
python report_generator.py --input-dir "C:\Research\Notes" --output-dir "C:\Research\Output" --environment "MountainCar"
```

#### Combined Options
```bash
# Create samples in custom directory
python report_generator.py --create-samples --input-dir "my_project_notes"

# Force regenerate with custom directories and environment
python report_generator.py --force --input-dir "notes" --output-dir "reports" --environment "Lunar Lander"

# PDF only from custom output directory
python report_generator.py --pdf-only --output-dir "backup_reports"

# Concatenate input files only with environment context
python report_generator.py --concatenate-only --input-dir "research_notes" --environment "CartPole"
```

### Real-World Workflow Examples

#### First Time Setup
```bash
# 1. Create sample files
python report_generator.py --create-samples

# 2. Edit the input files with your content
# (Edit files in input/ directory)

# 3. Generate initial report
python report_generator.py --force
```

#### Daily Workflow
```bash
# Edit some input files, then run smart generation
python report_generator.py

# Example output:
# Input file input\methodology.txt has changed. Will regenerate methodology.
# ✓ Generated methodology
# ✓ PDF report generated: output\technical_report.pdf
```

#### Project Management
```bash
# Different projects in separate directories
python report_generator.py --input-dir "project_alpha\notes" --output-dir "project_alpha\reports"
python report_generator.py --input-dir "project_beta\notes" --output-dir "project_beta\reports"
```

#### Troubleshooting Scenarios
```bash
# If generation fails, try PDF-only to isolate the issue
python report_generator.py --pdf-only

# If you want fresh content but keep existing structure
python report_generator.py --force

# Get an overview of all your notes in one file
python report_generator.py --concatenate-only

# Check what would be generated without actually doing it
python report_generator.py --help
```

### Command Line Help
```bash
python report_generator.py --help
```
Shows all available options and their descriptions.

## Input File Format
Each input file should contain your notes and key points for that section. The AI will expand these into full technical content.

Example `input/methodology.txt`:
```
Methodology details:
- Environment: CartPole-v1 and MountainCar-v0
- PCT hierarchy: 3-level control system
- Evolutionary algorithm: NSGA-II with population 100
- RL approach: DQN with experience replay
- Evaluation metrics: episode rewards, stability measures
- Statistical analysis: t-tests, effect sizes
```

## Features

### Smart Regeneration
The system tracks file changes using MD5 hashes. Sections are only regenerated when:
- The output file doesn't exist
- The input file has been modified since last generation

### PDF Formatting
- Times New Roman font family
- Professional academic layout
- APA-style citation placeholders
- Proper spacing and margins
- Automatic page breaks between sections
- Centered page numbers on every page

### Error Handling
- Graceful handling of missing input files
- OpenAI API error management
- Detailed progress reporting
- Metadata corruption recovery

## Customization

### Modifying Sections
Edit the `sections` and `section_titles` lists in the `TechnicalReportGenerator` class to change report structure.

### Adjusting Prompts
Modify the `section_specific_prompts` dictionary in `generate_section_prompt()` to customize how each section is generated.

### PDF Styling
Customize the `create_pdf_styles()` method to adjust fonts, spacing, and formatting.

## Troubleshooting

### OpenAI API Issues
- Ensure your API key is correctly set in `.env`
- Check your OpenAI account has sufficient credits
- Verify internet connectivity

### PDF Generation Problems
- Ensure reportlab is properly installed
- Check file permissions in the output directory
- Verify all required output files exist

### File Encoding Issues
- Ensure input files are UTF-8 encoded
- Check for special characters that might cause issues

### Author and Version Configuration
- Set `REPORT_AUTHOR` in your `.env` file to customize the author name on the title page
- If no author is specified, "Research Team" will be used as the default
- Version numbers start at 1.0.0 and increment automatically with each PDF generation
- Version history is tracked in the metadata.json file

## Cost Optimization
- The system avoids regenerating unchanged sections to minimize API costs
- Use `--pdf-only` when you only need to regenerate the PDF
- Consider using GPT-3.5-turbo for cost savings (modify the model in `generate_section_content()`)

### Expected Output Examples

#### Successful Generation
```bash
$ python report_generator.py
Technical Report Generator
==================================================
Input file input\methodology.txt has changed. Will regenerate methodology.
Generating content for methodology...
✓ Generated methodology
Output file output\discussion.txt missing. Will regenerate discussion.
Generating content for discussion...
✓ Generated discussion

Updated sections: methodology, discussion
Generating PDF report...
✓ PDF report generated: output\technical_report.pdf

✓ Report generation completed successfully!
```

#### No Changes Detected
```bash
$ python report_generator.py
Technical Report Generator
==================================================

No sections needed updating.
✓ PDF report generated: output\technical_report.pdf

✓ Report generation completed successfully!
```

#### First Time with Samples
```bash
$ python report_generator.py --create-samples
Sample input files created in input

$ python report_generator.py --force
Technical Report Generator
==================================================
Force regenerating all sections...
Generating content for executive_summary...
✓ Generated executive_summary
Generating content for introduction...
✓ Generated introduction
[... continues for all sections ...]

Updated sections: executive_summary, introduction, background, methodology, experimental_results, discussion, recommendations_future_work, references
Generating PDF report...
✓ PDF report generated: output\technical_report.pdf

✓ Report generation completed successfully!
```
