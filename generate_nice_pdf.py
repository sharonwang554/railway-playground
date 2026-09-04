import markdown2
import subprocess
import os

with open('combined-aeo.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Split the text into two parts: AEO Analysis and 30-Day Strategy
parts = text.split('# 30-Day AEO & SEO Execution Strategy')

part1_md = parts[0]
part2_md = '# 30-Day AEO & SEO Execution Strategy' + parts[1]

# Convert markdown to html with extras for better rendering
html_body1 = markdown2.markdown(part1_md, extras=["fenced-code-blocks", "tables", "header-ids"])
html_body2 = markdown2.markdown(part2_md, extras=["fenced-code-blocks", "tables", "header-ids"])

css = """
<style>
    @page { margin: 0.85cm; size: A4 portrait; }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.3;
        font-size: 10px;
        color: #24292e;
        margin: 0;
        padding: 0;
    }
    
    .page-section {
        column-count: 2;
        column-gap: 25px;
    }
    
    .page-break { 
        page-break-before: always; 
        break-before: page; 
    }

    h1 { 
        font-size: 1.6em; 
        padding-bottom: .2em; 
        border-bottom: 1px solid #eaecef; 
        column-span: all; 
        margin-top: 0; 
        margin-bottom: 12px;
    }
    h2 { font-size: 1.25em; padding-bottom: .1em; border-bottom: 1px solid #eaecef; margin-top: 0.9em; break-after: avoid; margin-bottom: 4px; }
    h3 { font-size: 1.1em; margin-top: 0.7em; break-after: avoid; margin-bottom: 4px; }
    p { margin-top: 0; margin-bottom: 6px; }
    ul, ol { padding-left: 1.5em; margin-bottom: 6px; }
    li { margin-top: 0.1em; }
    li > p { margin-top: 3px; margin-bottom: 3px; }
    code {
        font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
        font-size: 85%;
        background-color: rgba(27,31,35,.05);
        border-radius: 3px;
        padding: .1em .2em;
    }
    pre {
        background-color: #f6f8fa;
        border-radius: 4px;
        padding: 8px;
        margin-bottom: 6px;
        overflow: auto;
        break-inside: avoid;
    }
    pre code { background-color: transparent; padding: 0; font-size: 100%; }
    hr { height: 1px; padding: 0; margin: 10px 0; background-color: #e1e4e8; border: 0; }
    em { font-style: italic; }
    strong { font-weight: 600; }
    a { color: #0366d6; text-decoration: none; }
</style>
"""

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AEO Analysis and 30-Day Strategy</title>
    {css}
</head>
<body>
    <div class="page-section">
        {html_body1}
    </div>
    
    <div class="page-break"></div>
    
    <div class="page-section">
        {html_body2}
    </div>
</body>
</html>
"""

with open('combined-aeo.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--print-to-pdf=combined-aeo.pdf",
    "--no-pdf-header-footer",
    "file://" + os.path.abspath("combined-aeo.html")
]

try:
    subprocess.run(cmd, check=True)
    print("Beautiful two-page PDF generated successfully using Chrome Headless!")
except Exception as e:
    print(f"Error generating PDF with Chrome: {e}")
