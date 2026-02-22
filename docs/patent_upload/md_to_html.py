"""Convert PROVISIONAL_PATENT_APPLICATION.md to HTML for printing to PDF or saving as DOCX."""
import re
from pathlib import Path


def md_to_html(md_path: Path, out_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")

    # Replace filing date for consistency
    text = re.sub(r"February 8, 2026", "February 11, 2026", text)

    # Escape and preserve code blocks first (before other replacements)
    code_blocks = []
    def save_code(m):
        block = m.group(1).strip()
        block = block.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        code_blocks.append('<pre class="pre">' + block + '</pre>')
        return f"\x00CODE{len(code_blocks) - 1}\x00"
    text = re.sub(r'```(.*?)```', save_code, text, flags=re.DOTALL)

    # Horizontal rules
    text = re.sub(r'\n---\n', '\n<hr>\n', text)

    # Headers (must be after code block preservation)
    text = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)

    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

    # Restore code blocks
    for i, code in enumerate(code_blocks):
        text = text.replace(f"\x00CODE{i}\x00", code)

    # Build output: proper paragraphs and lists
    lines = text.split('\n')
    out = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Already-replaced block (code, hr, headers)
        if stripped.startswith('<') or stripped.startswith('</') or '\x00' in line:
            out.append(line)
            i += 1
            continue

        if not stripped:
            out.append('')
            i += 1
            continue

        # Numbered list: "1. " or "  a) "
        if re.match(r'^\s*(\d+\.|[a-z]\))\s+', line):
            out.append('<ol>')
            content = re.sub(r'^\s*(\d+\.|[a-z]\))\s+', '', line)
            out.append('<li>' + content + '</li>')
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if not next_line.strip():
                    i += 1
                    continue
                if next_line.strip().startswith('<'):
                    break
                if re.match(r'^\s*(\d+\.|[a-z]\))\s+', next_line):
                    content = re.sub(r'^\s*(\d+\.|[a-z]\))\s+', '', next_line)
                    out.append('<li>' + content + '</li>')
                    i += 1
                else:
                    break
            out.append('</ol>')
            continue

        # Bullet list: "- " at start
        if stripped.startswith('- ') and not stripped.startswith('--'):
            if '<ul>' not in (out[-1] if out else ''):
                out.append('<ul>')
            out.append('<li>' + stripped[2:].strip() + '</li>')
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if next_line.startswith('- ') and not next_line.startswith('--'):
                    out.append('<li>' + next_line[2:].strip() + '</li>')
                    i += 1
                else:
                    break
            out.append('</ul>')
            continue

        # Paragraph: collect consecutive non-empty, non-tag lines into one <p>
        para_lines = []
        while i < len(lines):
            ln = lines[i]
            if ln.strip().startswith('<') or ln.strip().startswith('</') or ln.strip() == '':
                break
            if re.match(r'^(\d+\.|\s*[a-z]\))\s+', ln) or (ln.strip().startswith('- ') and not ln.strip().startswith('--')):
                break
            para_lines.append(ln.strip())
            i += 1
        if para_lines:
            out.append('<p>' + ' '.join(para_lines) + '</p>')
            continue

        i += 1
    # Close any open list
    body = '\n'.join(out)

    # Clean up: ensure no <p></p> or double spaces
    body = re.sub(r'<p>\s*</p>', '', body)
    body = re.sub(r'  +', ' ', body)

    # Wrap header (everything before first <hr>) in .header-block for cleaner formatting
    if '<hr>' in body:
        before, after = body.split('<hr>', 1)
        body = '<div class="header-block">' + before.strip() + '</div>\n<hr>\n' + after.strip()
    else:
        body = '<div class="header-block">' + body.strip() + '</div>'

    html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Provisional Patent Application - Specification</title>
<style>
body {
  font-family: "Times New Roman", Times, serif;
  font-size: 12pt;
  line-height: 1.5;
  max-width: 8.5in;
  margin: 1in auto;
  padding: 0 1in;
  color: #000;
}
h1 {
  font-size: 14pt;
  text-align: center;
  margin: 0 0 18pt 0;
  font-weight: bold;
}
h2 {
  font-size: 12pt;
  margin: 14pt 0 6pt 0;
  font-weight: bold;
}
h3, h4 {
  font-size: 12pt;
  margin: 10pt 0 4pt 0;
  font-weight: bold;
}
p {
  margin: 0 0 8pt 0;
  text-align: justify;
}
.header-block {
  margin: 0 0 16pt 0;
  line-height: 1.4;
}
.header-block p { margin: 2pt 0; text-align: left; }
.pre {
  font-family: Consolas, "Courier New", monospace;
  font-size: 10pt;
  line-height: 1.35;
  white-space: pre-wrap;
  background: #f5f5f5;
  padding: 10pt;
  margin: 8pt 0;
  border: 1px solid #ccc;
  overflow-x: auto;
}
ul, ol {
  margin: 6pt 0 10pt 24pt;
  padding-left: 24pt;
}
li {
  margin: 2pt 0;
  text-align: justify;
}
hr {
  margin: 14pt 0;
  border: none;
  border-top: 1px solid #333;
}
@media print {
  body { margin: 0.75in; }
  .pre { break-inside: avoid; }
  h2 { page-break-after: avoid; }
  p { orphans: 2; widows: 2; }
}
</style>
</head>
<body>

''' + body + '''

</body>
</html>'''
    out_path.write_text(html, encoding="utf-8")
    print(f"Written: {out_path}")

if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent
    md_path = base / "PROVISIONAL_PATENT_APPLICATION.md"
    out_path = base / "patent_upload" / "Provisional_Patent_Specification_FULL_Dhiraj_Pokhrel.html"
    if not md_path.exists():
        print(f"Not found: {md_path}")
        exit(1)
    md_to_html(md_path, out_path)
