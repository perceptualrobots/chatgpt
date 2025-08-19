# Command Line Examples for Technical Report Generator

## Quick Reference

### Basic Commands
```bash
# Get help and see all options
python report_generator.py --help

# Create sample input files (first time setup)
python report_generator.py --create-samples

# Smart generation - only updates changed sections (daily use)
python report_generator.py

# Force regenerate everything (when you want fresh content)
python report_generator.py --force

# Generate PDF only from existing output files
python report_generator.py --pdf-only

# Concatenate input files only (no AI generation or PDF)
python report_generator.py --concatenate-only

# Specify environment name for customized content
python report_generator.py --environment "Lunar Lander"
```

### Custom Directories
```bash
# Use custom input and output directories
python report_generator.py --input-dir "my_notes" --output-dir "my_reports"

# Create samples in custom directory
python report_generator.py --create-samples --input-dir "project_notes"

# Force regenerate with custom paths and environment
python report_generator.py --force --input-dir "notes" --output-dir "final_reports" --environment "Lunar Lander"
```

## Detailed Examples

### First Time Setup
```bash
# 1. Create the directory structure and sample files
python report_generator.py --create-samples

# 2. Edit the created files in input/ with your actual content
# (Use your favorite text editor)

# 3. Generate the initial report with all sections
python report_generator.py --force
```

### Daily Workflow
```bash
# After editing some input files, run smart generation
python report_generator.py

# The system will automatically detect which files changed and only regenerate those sections
```

### Project-Specific Directories
```bash
# Project Alpha
python report_generator.py --input-dir "alpha/notes" --output-dir "alpha/reports" --create-samples
python report_generator.py --input-dir "alpha/notes" --output-dir "alpha/reports" --force

# Project Beta  
python report_generator.py --input-dir "beta/notes" --output-dir "beta/reports" --create-samples
python report_generator.py --input-dir "beta/notes" --output-dir "beta/reports" --force
```

### Troubleshooting Commands
```bash
# If content generation fails but you want to try PDF generation
python report_generator.py --pdf-only

# If you want completely fresh content (clears change tracking)
python report_generator.py --force

# Get an overview of all your notes in one file
python report_generator.py --concatenate-only

# Generate from a backup output directory
python report_generator.py --pdf-only --output-dir "backup_output"
```

### Windows-Specific Examples
```bash
# Using Windows-style paths
python report_generator.py --input-dir "C:\Research\Notes" --output-dir "C:\Research\Reports"

# Using relative paths on Windows
python report_generator.py --input-dir "..\..\notes" --output-dir ".\reports"
```

### Batch Processing Examples
```bash
# Generate multiple reports in sequence
python report_generator.py --input-dir "q1_notes" --output-dir "q1_report" --force
python report_generator.py --input-dir "q2_notes" --output-dir "q2_report" --force  
python report_generator.py --input-dir "q3_notes" --output-dir "q3_report" --force
python report_generator.py --input-dir "q4_notes" --output-dir "q4_report" --force
```

## Expected Output

### Successful Smart Generation
```
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

### No Updates Needed
```
$ python report_generator.py
Technical Report Generator
==================================================

No sections needed updating.
✓ PDF report generated: output\technical_report.pdf

✓ Report generation completed successfully!
```

### Force Regeneration
```
$ python report_generator.py --force
Technical Report Generator
==================================================
Force regenerating all sections...
Generating content for executive_summary...
✓ Generated executive_summary
Generating content for introduction...
✓ Generated introduction
Generating content for background...
✓ Generated background
Generating content for methodology...
✓ Generated methodology
Generating content for experimental_results...
✓ Generated experimental_results
Generating content for discussion...
✓ Generated discussion
Generating content for recommendations_future_work...
✓ Generated recommendations_future_work
Generating content for references...
✓ Generated references

Updated sections: executive_summary, introduction, background, methodology, experimental_results, discussion, recommendations_future_work, references
Generating PDF report...
✓ PDF report generated: output\technical_report.pdf

✓ Report generation completed successfully!
```

### Help Output
```
$ python report_generator.py --help
usage: report_generator.py [-h] [--input-dir INPUT_DIR] [--output-dir OUTPUT_DIR] [--force] [--pdf-only] [--create-samples]

Generate technical report comparing PCT vs RL control systems

options:
  -h, --help            show this help message and exit
  --input-dir INPUT_DIR
                        Directory containing input notes files (default: input)
  --output-dir OUTPUT_DIR
                        Directory for generated output files (default: output)
  --force               Force regenerate all sections (ignores change detection)
  --pdf-only            Only generate PDF from existing output files (no AI generation)
  --create-samples      Create sample input files with template content

Examples:
  report_generator.py --create-samples                    Create sample input files
  report_generator.py                                     Smart generation (recommended)
  report_generator.py --force                            Force regenerate all sections
  report_generator.py --pdf-only                         Generate PDF from existing outputs
  report_generator.py --input-dir notes --output-dir reports    Use custom directories

Workflow:
  1. report_generator.py --create-samples                 # Create template files
  2. Edit files in input/ directory            # Add your content
  3. report_generator.py --force                          # Generate initial report
  4. report_generator.py                                  # Daily updates (smart mode)
```
