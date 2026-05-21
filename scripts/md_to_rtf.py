import sys
from pathlib import Path


def rtf_escape(text: str) -> str:
    text = text.replace('\\', r'\\').replace('{', r'\{').replace('}', r'\}')
    return ''.join(f'\\u{ord(ch)}?' if ord(ch) > 127 else ch for ch in text)


def md_to_rtf(md_text: str) -> str:
    lines = []
    lines.append(r'{\rtf1\ansi\deff0')
    lines.append(r'{\fonttbl{\f0 Calibri;}{\f1 Consolas;}}')
    lines.append(r'\viewkind4\uc1\pard\sa180\sl240\slmult1\f0\fs22')

    in_code = False
    for raw in md_text.splitlines():
        line = raw.rstrip()

        if line.startswith('```'):
            in_code = not in_code
            if in_code:
                lines.append(r'\par\f1\fs18')
            else:
                lines.append(r'\par\f0\fs22')
            continue

        if in_code:
            lines.append(rtf_escape(line) + r'\par')
            continue

        if not line:
            lines.append(r'\par')
            continue

        if line.startswith('# '):
            lines.append(r'\par\b\fs32 ' + rtf_escape(line[2:].strip()) + r'\b0\fs22\par')
            continue
        if line.startswith('## '):
            lines.append(r'\par\b\fs28 ' + rtf_escape(line[3:].strip()) + r'\b0\fs22\par')
            continue
        if line.startswith('### '):
            lines.append(r'\par\b\fs24 ' + rtf_escape(line[4:].strip()) + r'\b0\fs22\par')
            continue

        if line.startswith('- '):
            lines.append(r'\par\tab• ' + rtf_escape(line[2:].strip()) + r'\par')
            continue

        if line.startswith('---'):
            lines.append(r'\par\pard\brdrb\brdrs\brdrw10\par')
            continue

        lines.append(rtf_escape(line) + r'\par')

    lines.append('}')
    return '\n'.join(lines)


def main():
    if len(sys.argv) < 3:
        print('Usage: python md_to_rtf.py input.md output.rtf')
        sys.exit(2)
    md = Path(sys.argv[1])
    out = Path(sys.argv[2])
    if not md.exists():
        print('Input not found:', md)
        sys.exit(1)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md_to_rtf(md.read_text(encoding='utf-8')), encoding='utf-8')
    print('WROTE', out)


if __name__ == '__main__':
    main()
