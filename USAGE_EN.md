# Clinical Document Review Tool - Usage Guide

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd clinical-document-review

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or install as package
pip install -e .
```

### Basic Usage

```bash
# Review a Protocol document
python cli.py review protocol.pdf --type protocol

# Review an IB document with both HTML and text reports
python cli.py review ib_document.pdf --type ib --format both

# Review a SAP document with custom output path
python cli.py review sap.pdf --type sap --output reports/my_sap_report.html
```

## Command Reference

### 1. Review Document

```bash
python cli.py review <document_path> --type <type> [options]
```

**Arguments:**
- `document_path`: Path to the PDF document to review

**Required Options:**
- `--type, -t`: Document type (`protocol`, `ib`, `sap`)

**Optional Options:**
- `--output, -o`: Output report path (default: `reports/<filename>_report.html`)
- `--format, -f`: Report format (`html`, `text`, `both`) (default: `html`)

**Examples:**

```bash
# Protocol review with HTML report
python cli.py review documents/protocol_v2.pdf --type protocol

# IB review with both HTML and text reports
python cli.py review documents/ib.pdf --type ib --format both

# SAP review with custom output path
python cli.py review sap_final.pdf --type sap -o output/sap_review.html
```

### 2. Document Information

```bash
python cli.py info <document_path>
```

Display document metadata, page count, and detected sections.

```bash
python cli.py info protocol.pdf
```

### 3. Search Text

```bash
python cli.py search <document_path> --pattern <regex_pattern>
```

Search for specific patterns in the document.

```bash
# Search for version numbers
python cli.py search protocol.pdf --pattern "version.*\d+"

# Search for dates
python cli.py search protocol.pdf --pattern "\d{4}-\d{2}-\d{2}"
```

### 4. List Review Checks

```bash
python cli.py list-checks
```

Display all available review items for all document types.

## Programmatic Usage

You can also use the tool programmatically in your Python scripts:

```python
from pathlib import Path
from src.parsers import PDFParser
from src.reviewers import ProtocolReviewer
from src.reports import HTMLReportGenerator

# Parse document
parser = PDFParser("path/to/protocol.pdf")
parsed_doc = parser.parse()

# Review document
reviewer = ProtocolReviewer()
results = reviewer.review_document(parsed_doc)

# Generate report
report_gen = HTMLReportGenerator()
report_gen.generate(results, "output/report.html")

# Access results
print(f"Pass rate: {results['summary']['pass_rate']}%")
print(f"Critical issues: {results['summary']['critical_issues']}")
```

## Review Checklist Items

### Protocol Review (8 sections)

1. **Essential Information**: Title, version, date, sponsor
2. **Study Objectives and Design**: Primary/secondary objectives, study design, sample size
3. **Subject Selection**: Inclusion/exclusion/withdrawal criteria
4. **Treatment and Dosing**: Dosage, route, duration, concomitant medications
5. **Assessments and Procedures**: Endpoints, visit schedule
6. **Safety**: Adverse event reporting, SAE, safety monitoring
7. **Statistical Analysis**: Analysis plan, analysis sets
8. **Ethical Considerations**: IRB, informed consent, data protection

### IB Review (8 sections)

1. **Essential Information**: Title, version, sponsor
2. **Summary**: Drug summary, chemical name
3. **Physical and Chemical Properties**: Properties, formulation
4. **Nonclinical Data**: Pharmacology, PK, toxicology
5. **Clinical Data**: Clinical pharmacology, PK/PD, efficacy
6. **Safety Information**: Adverse reactions, SAE, contraindications, drug interactions
7. **Special Populations**: Pregnancy/lactation, pediatric/geriatric, renal/hepatic impairment
8. **References and Appendices**

### SAP Review (11 sections)

1. **Essential Information**: Title, version, statistician
2. **Study Objectives and Hypotheses**: Objectives, statistical hypotheses
3. **Endpoints**: Primary/secondary endpoint definitions
4. **Sample Size**: Rationale, power, effect size
5. **Analysis Sets**: ITT, PP, safety population
6. **Statistical Methods**: Tests, confidence intervals, multiplicity adjustments
7. **Missing Data Handling**: Missing data methods
8. **Interim Analysis**: Interim analysis, stopping rules
9. **Subgroup Analysis**: Subgroups, stratification factors
10. **Safety Analysis**: AE analysis, coding dictionary
11. **Statistical Software**: Software, tables/figures list

## Customization

### Modifying Review Checklists

Edit YAML files in the `config/` folder to customize review items:

```yaml
# config/protocol_checklist.yaml example
sections:
  custom_section:
    name: "Custom Section"
    checks:
      - id: "custom_001"
        category: "Custom"
        description: "Item to check"
        keywords: ["keyword1", "keyword2"]
        severity: "critical"  # critical, major, minor
```

### Adding New Document Types

1. Create a new checklist YAML file in `config/`
2. Create a new reviewer class in `src/reviewers/`
3. Add to the `REVIEWERS` dictionary in `cli.py`

## Local LLM Integration (Optional)

For advanced analysis, integrate [Ollama](https://ollama.ai) for local LLM capabilities.

### Setup Ollama

```bash
# 1. Install Ollama (https://ollama.ai)

# 2. Pull a model
ollama pull llama2

# 3. Verify installation
ollama list
```

### Using LLM Features

```python
from src.llm import OllamaClient

client = OllamaClient(model="llama2")

# Check if Ollama is running
if client.is_available():
    # Summarize document
    summary = client.summarize_document(document_text)

    # Analyze section
    analysis = client.analyze_section(section_text, "Study Objectives", "Protocol")
```

**Note:** LLM integration is optional; the core review functionality works without it.

## Security Considerations

1. **Fully Local Processing**: All document processing happens locally
2. **No External Transmission**: No network connection required (except for optional LLM)
3. **Data Preservation**: Original documents are never modified
4. **Report Storage**: Generated reports are saved only to local `reports/` folder

### Preventing Accidental Commits

Sensitive documents are excluded in `.gitignore`:

```
*.pdf
*.docx
test_documents/
reports/
```

## Troubleshooting

### Common Issues

**Issue: "pdfplumber not found"**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue: "File not found"**
```bash
# Solution: Check file path
python cli.py info path/to/document.pdf
```

**Issue: "No sections detected"**
```bash
# Solution: The PDF might be scanned (image-based)
# Only text-based PDFs are supported. OCR support coming soon.
```

## Performance Tips

1. **Large Documents**: For documents >100 pages, processing may take a few minutes
2. **Batch Processing**: Process multiple documents in parallel using shell scripts
3. **Report Format**: HTML reports are larger but more readable; use text format for quick checks

## Exit Codes

- `0`: Review completed successfully (no critical issues)
- `1`: Review failed or critical issues found

Use in scripts:

```bash
python cli.py review protocol.pdf --type protocol
if [ $? -eq 0 ]; then
    echo "Review passed!"
else
    echo "Review has critical issues!"
fi
```

## Getting Help

```bash
# General help
python cli.py --help

# Command-specific help
python cli.py review --help
python cli.py search --help
```

## Examples

### Example 1: Automated Review Pipeline

```bash
#!/bin/bash
# review_pipeline.sh

for doc in documents/*.pdf; do
    echo "Reviewing $doc..."
    python cli.py review "$doc" --type protocol --format both
done
```

### Example 2: Integration with Git Hooks

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Review all modified protocol documents
for file in $(git diff --cached --name-only | grep protocol.*\.pdf); do
    python cli.py review "$file" --type protocol
    if [ $? -ne 0 ]; then
        echo "Critical issues found in $file"
        exit 1
    fi
done
```

### Example 3: Python Script

```python
#!/usr/bin/env python3
"""Batch review multiple documents"""

import sys
from pathlib import Path
from src.parsers import PDFParser
from src.reviewers import ProtocolReviewer
from src.reports import HTMLReportGenerator

def review_document(doc_path):
    """Review a single document"""
    parser = PDFParser(doc_path)
    parsed = parser.parse()

    reviewer = ProtocolReviewer()
    results = reviewer.review_document(parsed)

    # Generate report
    output = f"reports/{Path(doc_path).stem}_report.html"
    HTMLReportGenerator().generate(results, output)

    return results['summary']['critical_issues'] == 0

# Review all documents
docs = Path("documents").glob("*.pdf")
for doc in docs:
    print(f"Reviewing {doc}...")
    if not review_document(str(doc)):
        print(f"  ⚠ Critical issues found!")
```

## FAQ

**Q: Can I review scanned PDFs?**
A: No, currently only text-extractable PDFs are supported. OCR support is planned.

**Q: Do I need an internet connection?**
A: No, the core review functionality works offline. Only the optional Ollama LLM feature requires Ollama running locally.

**Q: Are the review results 100% accurate?**
A: This is an assistive tool using keyword-based automated review. Final review and approval must be performed by qualified professionals.

**Q: Can I review DOCX files?**
A: Not yet, currently only PDF is supported. DOCX support is planned for future versions.

**Q: Can I modify the checklists?**
A: Yes, edit the YAML files in the `config/` folder to customize to your institution's requirements.

---

**Disclaimer**: This tool assists in clinical document review. Final review and approval of regulatory submission documents must be performed by qualified professionals.
