# Technical Report Generator

## Overview
This application generates PDF technical reports comparing control systems for OpenAI Gym environments, specifically comparing Perceptual Control Theory (PCT) hierarchies generated through evolutionary algorithms with controllers derived by Reinforcement Learning.

## Features
- **Smart Generation**: Only regenerates sections when input files change (based on file hash comparison)
- **OpenAI Integration**: Uses GPT-4 to generate technical content from your notes
- **Professional PDF Output**: Creates formatted PDFs with Times New Roman font and APA-style citations
- **Modular Sections**: Supports standard technical report structure
- **Change Tracking**: Maintains metadata to avoid unnecessary API calls

## Report Sections
1. Executive Summary
2. Introduction  
3. Background
4. Methodology
5. Experimental Results
6. Discussion
7. Recommendations & Future Work
8. References

## Setup

### Prerequisites
```bash
pip install openai reportlab python-dotenv
```

### Environment Configuration
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Directory Structure
```
report_generator/
├── input/                  # Your notes for each section (.txt files)
│   ├── executive_summary.txt
│   ├── introduction.txt
│   ├── background.txt
│   ├── methodology.txt
│   ├── experimental_results.txt
│   ├── discussion.txt
│   ├── recommendations_future_work.txt
│   └── references.txt
├── output/                 # Generated content and final PDF
│   ├── executive_summary.txt
│   ├── introduction.txt
│   ├── ...
│   ├── metadata.json
│   └── technical_report.pdf
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

### Advanced Usage

#### Custom Directories
```bash
# Use different input/output directories
python report_generator.py --input-dir "research_notes" --output-dir "final_reports"

# Relative paths work too
python report_generator.py --input-dir "../notes" --output-dir "./reports"

# Windows absolute paths
python report_generator.py --input-dir "C:\Research\Notes" --output-dir "C:\Research\Output"
```

#### Combined Options
```bash
# Create samples in custom directory
python report_generator.py --create-samples --input-dir "my_project_notes"

# Force regenerate with custom directories
python report_generator.py --force --input-dir "notes" --output-dir "reports"

# PDF only from custom output directory
python report_generator.py --pdf-only --output-dir "backup_reports"
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
