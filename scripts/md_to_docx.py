import sys
from pathlib import Path
from docx import Document
from docx.shared import Pt


def md_to_docx(md_path: Path, docx_path: Path):
    text = md_path.read_text(encoding='utf-8')
    doc = Document()

    # set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)

    in_code = False
    for line in text.splitlines():
        line = line.rstrip()
        if not line and not in_code:
            # blank line -> paragraph break
            doc.add_paragraph('')
            continue

        # fenced code block start/end
        if line.strip().startswith('```'):
            in_code = not in_code
            if in_code:
                # start code block
                code_para = doc.add_paragraph()
                code_para.style = doc.styles['No Spacing']
            continue

        if in_code:
            # add code line in monospace paragraph
            p = doc.add_paragraph(line)
            p.style = doc.styles['No Spacing']
            run = p.runs[0]
            run.font.name = 'Courier New'
            run.font.size = Pt(9)
            continue

        # Headings
        if line.startswith('# '):
            doc.add_heading(line[2:].strip(), level=1)
            continue
        if line.startswith('## '):
            doc.add_heading(line[3:].strip(), level=2)
            continue
        if line.startswith('### '):
            doc.add_heading(line[4:].strip(), level=3)
            continue

        # Horizontal rule
        if line.strip().startswith('---'):
            doc.add_paragraph('')
            continue

        # Bullet lists
        if line.strip().startswith('- '):
            item = line.strip()[2:]
            p = doc.add_paragraph(item, style='List Bullet')
            continue

        # Numbered lists
        if line.strip()[0:3].isdigit() if len(line) >= 3 else False and line.strip()[3] == '.':
            # fallback: just add as normal paragraph
            doc.add_paragraph(line.strip())
            continue

        # Fallback paragraph
        doc.add_paragraph(line)

    doc.save(str(docx_path))


def main():
    if len(sys.argv) < 3:
        print('Usage: python md_to_docx.py input.md output.docx')
        sys.exit(2)
    md = Path(sys.argv[1])
    out = Path(sys.argv[2])
    if not md.exists():
        print('Input not found:', md)
        sys.exit(1)
    out.parent.mkdir(parents=True, exist_ok=True)
    md_to_docx(md, out)
    print('WROTE', out)


if __name__ == '__main__':
    main()
