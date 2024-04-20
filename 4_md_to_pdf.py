import markdown
from weasyprint import HTML, CSS

# MarkdownファイルをHTMLに変換
with open('combined.md', 'r', encoding='utf-8') as f:
    html_text = markdown.markdown(f.read())

# CSSスタイルを定義
css = CSS(string='''
@page { size: A4; margin: 1in; }
body { font-family: "Hiragino Mincho ProN", serif; line-height: 1.5; }
h1, h2, h3, h4, h5, h6 { font-family: "Hiragino Kaku Gothic ProN", sans-serif; }
''')

# HTMLをPDFに変換、CSSを適用
html = HTML(string=html_text)
html.write_pdf('combined.pdf', stylesheets=[css])
