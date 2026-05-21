import sys
import re
from pathlib import Path

try:
    from fpdf import FPDF
except Exception as e:
    print('MISSING_FPDF')
    raise


def md_to_text(md: str) -> str:
    # remove fenced code blocks
    md = re.sub(r'```.*?```', '', md, flags=re.S)
    # inline code markers
    md = re.sub(r'`([^`]*)`', r"\1", md)
    # headings -> uppercase line
    md = re.sub(r'^#{1,6}\s*(.*)', lambda m: m.group(1).upper(), md, flags=re.M)
    # lists: convert '- ' to bullet
    md = re.sub(r'^\s*-\s+', '• ', md, flags=re.M)
    return md


def make_pdf(input_md: Path, output_pdf: Path):
    text = input_md.read_text(encoding='utf-8')
    text = md_to_text(text)

    pdf = FPDF()
    pdf.set_auto_page_break(True, margin=15)
    pdf.add_page()
    pdf.set_font('Arial', size=12)

    for line in text.splitlines():
        # ensure no long unbroken text
        pdf.multi_cell(0, 6, line)

    pdf.output(str(output_pdf))


def main():
    if len(sys.argv) < 3:
        print('Usage: python markdown_to_pdf.py input.md output.pdf')
        sys.exit(2)
    inp = Path(sys.argv[1])
    out = Path(sys.argv[2])
    if not inp.exists():
        print('Input file not found:', inp)
        sys.exit(1)
    make_pdf(inp, out)
    print('WROTE', out)


if __name__ == '__main__':
    main()
