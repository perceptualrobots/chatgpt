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

### LaTeX Command Options
```bash
# Generate LaTeX source file and compile to PDF (requires pdflatex)
python report_generator.py --latex

# Generate LaTeX source with force regeneration
python report_generator.py --force --latex

# Only compile existing LaTeX file to PDF (no content generation)
python report_generator.py --compile-latex-only

# Generate LaTeX with custom environment and directories
python report_generator.py --latex --environment "Robotic Arm" --input-dir "notes" --output-dir "latex_reports"

# Create initial samples and generate with LaTeX
python report_generator.py --create-samples --input-dir "project_notes"
python report_generator.py --force --latex --input-dir "project_notes" --output-dir "project_output"
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

### LaTeX-Specific Workflows
```bash
# LaTeX First Time Setup
python report_generator.py --create-samples
python report_generator.py --force --latex

# LaTeX Daily Workflow (smart generation with LaTeX)
python report_generator.py --latex

# LaTeX-only compilation (when you've manually edited the .tex file)
python report_generator.py --compile-latex-only

# Generate both PDF and LaTeX versions
python report_generator.py --force        # Creates regular PDF
python report_generator.py --compile-latex-only --output-dir "same_output"  # Compiles LaTeX

# LaTeX with custom environment and professional output
python report_generator.py --latex --environment "Autonomous Vehicle Control System"
```

### LaTeX Requirements and Setup
```bash
# Before using LaTeX options, ensure you have pdflatex installed
# On Windows with MiKTeX:
pdflatex --version

# On Windows with TeX Live:
pdflatex --version

# On Ubuntu/Debian:
sudo apt-get install texlive-latex-base texlive-latex-extra

# On macOS with MacTeX:
brew install --cask mactex
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

### LaTeX Troubleshooting Commands
```bash
# If LaTeX compilation fails, try regular PDF first
python report_generator.py --pdf-only

# If pdflatex is not found, check installation
where pdflatex          # Windows
which pdflatex          # Linux/macOS

# Compile LaTeX manually to see detailed errors
cd output
pdflatex technical_report.tex

# Force regenerate and try LaTeX again
python report_generator.py --force
python report_generator.py --compile-latex-only

# Generate content without LaTeX, then compile separately
python report_generator.py --force
python report_generator.py --compile-latex-only

# Check if LaTeX source was generated
dir output\*.tex        # Windows
ls output/*.tex         # Linux/macOS
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

Updated sections: introduction, background, methodology, experimental_results, discussion, recommendations_future_work, references
Generating PDF report...
✓ PDF report generated: output\technical_report.pdf

✓ Report generation completed successfully!
```

### LaTeX Generation Output
```
$ python report_generator.py --latex
Technical Report Generator
==================================================
Input file input\methodology.txt has changed. Will regenerate methodology.
Generating content for methodology...
✓ Generated methodology
Output file output\discussion.txt missing. Will regenerate discussion.
Generating content for discussion...
✓ Generated discussion

Updated sections: methodology, discussion
Generating LaTeX report...
✓ LaTeX source generated: output\technical_report.tex
Compiling LaTeX to PDF...
Running: pdflatex -interaction=nonstopmode technical_report.tex
✓ LaTeX compiled successfully: output\technical_report.pdf

✓ Report generation completed successfully!
```

### LaTeX Compile-Only Output
```
$ python report_generator.py --compile-latex-only
Technical Report Generator
==================================================
Compiling existing LaTeX to PDF...
Running: pdflatex -interaction=nonstopmode technical_report.tex
✓ LaTeX compiled successfully: output\technical_report.pdf

✓ Report generation completed successfully!
```

### LaTeX Compilation Error
```
$ python report_generator.py --latex
Technical Report Generator
==================================================
No sections needed updating.
Generating LaTeX report...
✓ LaTeX source generated: output\technical_report.tex
Compiling LaTeX to PDF...
Running: pdflatex -interaction=nonstopmode technical_report.tex
✗ LaTeX compilation failed! Check output\technical_report.log for details
Generated LaTeX source file: output\technical_report.tex
You can try compiling manually: cd output && pdflatex technical_report.tex

✗ Report generation failed.
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

## LaTeX Examples for Technical Reports

### Mathematical Equations

#### Inline Mathematics
Use single dollar signs for inline equations:
- Control system gain: $K_p = 2.5$
- Phase margin: $\phi_m = 45°$
- Damping ratio: $\zeta = 0.707$

#### Display Mathematics
Use double dollar signs for centered equations:

**Control Transfer Function:**
$$H(s) = \frac{K_p (1 + \tau_i s)}{s(\tau s + 1)}$$

**Quadratic Formula:**
$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

**Matrix Operations:**
$$\mathbf{A} = \begin{bmatrix}
a_{11} & a_{12} & a_{13} \\
a_{21} & a_{22} & a_{23} \\
a_{31} & a_{32} & a_{33}
\end{bmatrix}$$

**System of Equations:**
$$\begin{align}
\dot{x} &= Ax + Bu \\
y &= Cx + Du
\end{align}$$

### Statistical Formulas

**Mean and Standard Deviation:**
$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

$$\sigma = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2}$$

**Confidence Interval:**
$$CI = \bar{x} \pm t_{\alpha/2} \frac{s}{\sqrt{n}}$$

### Engineering Formulas

**PID Controller:**
$$u(t) = K_p e(t) + K_i \int_0^t e(\tau) d\tau + K_d \frac{de(t)}{dt}$$

**Frequency Response:**
$$|H(j\omega)| = \frac{K}{\sqrt{1 + (\omega \tau)^2}}$$

**Root Mean Square Error:**
$$RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2}$$

### Specialized Symbols

**Greek Letters:**
- $\alpha, \beta, \gamma, \delta, \epsilon$
- $\theta, \lambda, \mu, \sigma, \omega, \phi$
- $\Omega, \Theta, \Lambda, \Sigma, \Phi$

**Mathematical Operators:**
- Partial derivatives: $\frac{\partial f}{\partial x}$
- Integrals: $\int_a^b f(x) dx$
- Summations: $\sum_{i=1}^n x_i$
- Products: $\prod_{i=1}^n x_i$
- Limits: $\lim_{x \to \infty} f(x)$

**Sets and Logic:**
- $\in, \notin, \subset, \supset, \cup, \cap$
- $\forall, \exists, \implies, \iff$
- $\mathbb{R}, \mathbb{N}, \mathbb{Z}, \mathbb{Q}$

### Subscripts and Superscripts

**Control Systems:**
- $K_{p,max}$ (proportional gain maximum)
- $\omega_n^2$ (natural frequency squared)
- $T_{settling}$ (settling time)
- $e_{ss}$ (steady-state error)

**Chemical Engineering:**
- $C_A^0$ (initial concentration)
- $k_{cat}/K_M$ (catalytic efficiency)
- $\Delta H_{rxn}$ (heat of reaction)

### Common LaTeX Formatting Tips

1. **Fractions:** Use `\frac{numerator}{denominator}`
2. **Square roots:** Use `\sqrt{expression}` or `\sqrt[n]{expression}`
3. **Exponents:** Use `^{expression}` 
4. **Subscripts:** Use `_{expression}`
5. **Vectors:** Use `\mathbf{v}` or `\vec{v}`
6. **Matrices:** Use `\begin{bmatrix}...\end{bmatrix}`
7. **Aligned equations:** Use `\begin{align}...\end{align}`

### Units and Scientific Notation

**Physical Units (use with care in LaTeX):**
- Temperature: $25°C$ or $298K$
- Pressure: $1.013 \times 10^5 Pa$
- Flow rate: $2.5 \text{ L/min}$
- Concentration: $0.1 \text{ mol/L}$

**Scientific Notation:**
$$1.234 \times 10^{-6} = 1.234e^{-6}$$

### Complex Examples

**Control System Analysis:**
$$G(s)H(s) = \frac{K(s+2)}{s(s+1)(s+3)} = \frac{K(s+2)}{s^3 + 4s^2 + 3s}$$

**Signal Processing:**
$$X(j\omega) = \int_{-\infty}^{\infty} x(t) e^{-j\omega t} dt$$

**Optimization Problem:**
$$\min_{x} f(x) \text{ subject to } g_i(x) \leq 0, \quad i = 1,2,\ldots,m$$

**Probability Density Function:**
$$f(x|\mu,\sigma^2) = \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$

### LaTeX Best Practices for Reports

1. **Use consistent notation** throughout your document
2. **Define variables** before using them in equations
3. **Number important equations** for reference
4. **Use appropriate spacing** around operators
5. **Break long equations** across multiple lines when necessary
6. **Include units** where applicable
7. **Use descriptive variable names** when possible
