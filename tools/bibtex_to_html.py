
import re, html
from pathlib import Path
P=Path(__file__).resolve().parents[1]
B=P/'publications.bib'; O=P/'publications.html'
H='<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Publications — G.N. Tripathi</title><link rel="stylesheet" href="style.css"></head><body>'
NAV='''<header class="site-header" role="banner"><div class="container header-grid"><img src="assets/profile.jpg" alt="Portrait of Gyanendra Nath Tripathi" class="avatar" /><div><h1 class="name">Gyanendra Nath Tripathi</h1><p class="title">Researcher &amp; Educator</p><p class="affiliation">Yokohama, Japan</p><div class="actions"><a class="btn primary" href="contact.html">Contact</a><a class="btn" href="assets/CV_GyanendraNathTripathi.pdf" download>Download CV</a></div></div></div></header><nav class="navbar" aria-label="Primary"><div class="container"><a href="index.html">Home</a><a href="publications.html" aria-current="page">Publications</a><a href="lectures.html">Lectures</a><a href="teaching.html">Teaching</a><a href="awards.html">Awards</a><a href="grants.html">Grants</a><a href="blog.html">Blog</a><a href="cv.html">CV</a><a href="contact.html">Contact</a></div></nav>'''
F='<footer class="site-footer" role="contentinfo"><div class="container"><p>&copy; <span id="year"></span> Gyanendra Nath Tripathi. All rights reserved.</p><p class="small">This site is a lightweight, accessible template.</p></div></footer><script>document.getElementById("year").textContent=(new Date()).getFullYear()</script></body></html>'
ER=re.compile(r'@(?P<t>\w+)\s*\{\s*(?P<k>[^,]+),(?P<b>.*?)\n\}',re.S)
FR=re.compile(r'\n\s*(?P<f>\w+)\s*=\s*[\"\{](?P<v>.*?)[\"\}]\s*,?',re.S)

def parse(text):
  it=[]
  for m in ER.finditer(text):
    fs={fm.group('f').lower():fm.group('v').replace('\n',' ').strip() for fm in FR.finditer(m.group('b'))}
    it.append((m.group('t').lower(),m.group('k'),fs))
  return it

def fmt_auth(a):
  if not a: return ''
  out=[]
  for p in [x.strip() for x in a.split(' and ')]:
    names=p.replace('{','').replace('}','').split()
    if not names: out.append(p); continue
    last=names[-1]; init=''.join([w[0].upper()+'.' for w in names[:-1]])
    out.append(f"{last} {init}" if init else last)
  return ', '.join(out)

def item_html(t,k,f):
  ti=html.escape(f.get('title','Untitled'))
  au=html.escape(fmt_auth(f.get('author','')))
  yr=html.escape(f.get('year',''))
  ve=html.escape(f.get('journal') or f.get('booktitle') or '')
  doi=(f.get('doi') or '').strip(); url=(f.get('url') or '').strip(); link=''
  if doi: link=f'<a class="pub-link" target="_blank" href="https://doi.org/{html.escape(doi)}">DOI</a>'
  elif url: link=f'<a class="pub-link" target="_blank" href="{html.escape(url)}">Link</a>'
  return f'<li><span class="pub-title">{ti}</span><span class="pub-authors">{au}</span><span class="pub-venue">{ve}, {yr}</span>{(" "+link) if link else ""}</li>'

text=B.read_text(encoding='utf-8')
items=parse(text)
items.sort(key=lambda x: (-int(x[2].get('year','0') or '0'), x[2].get('title','')))
html_items='\n'.join(item_html(*it) for it in items)
body=f'<main class="container" role="main"><section class="card"><h2>Publications</h2><ol class="pub-list">{html_items}</ol><p class="meta">Source: <code>publications.bib</code>. Update and run <code>python tools/bibtex_to_html.py</code>.</p><p class="meta">More: <a target="_blank" href="https://scholar.google.com/citations?user=DT_rlwgAAAAJ&hl=en">Google Scholar</a> · <a target="_blank" href="https://dblp.org/pid/136/9441">dblp</a></p></section></main>'
O.write_text(H+NAV+body+F, encoding='utf-8')
