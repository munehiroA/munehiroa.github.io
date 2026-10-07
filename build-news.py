#!/usr/bin/env python3
"""Generate static EN/JA news and home teasers from content/news/*.json.
Run at the repository root before uploading or as the host's build command.
"""
from __future__ import annotations
from datetime import date
from html import escape
from pathlib import Path
import json,re,sys
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parent
SITE=ROOT
START='<!-- NEWS_GENERATED_START -->'
END='<!-- NEWS_GENERATED_END -->'
DATE=re.compile(r'^\d{4}-\d{2}(?:-\d{2})?$')

def h(s):return escape(s,quote=True)
def display_date(raw,lang):
 y,m,*d=raw.split('-');month=date(int(y),int(m),1).strftime('%B')
 return f'{y}年{int(m)}月'+(f'{int(d[0])}日' if d else '') if lang=='ja' else (f'{int(d[0])} {month} {y}' if d else f'{month} {y}')
def safe_link(raw):
 if not raw:return ''
 u=urlsplit(raw)
 if u.scheme and u.scheme not in ('https','http'):raise ValueError('Link must be HTTP(S)')
 if not u.scheme and (u.netloc or raw.startswith('/') or '..' in u.path.split('/')):raise ValueError('Invalid relative link')
 return raw

def load_posts():
 posts=[]
 for path in sorted((SITE/'content/news').glob('*.json')):
  x=json.loads(path.read_text());raw=x.get('date','')
  if not DATE.fullmatch(raw):raise ValueError(f'{path}: date must be YYYY-MM or YYYY-MM-DD')
  y,m,*day=map(int,raw.split('-'));date(y,m,day[0] if day else 1)
  for lang in ('en','ja'):
   for key in ('title','body','summary'):
    if not x.get(lang,{}).get(key,'').strip():raise ValueError(f'{path}: missing {lang}.{key}')
   safe_link(x[lang].get('link',''))
  for im in x.get('images',[]):
   if not im.startswith('/images/') or '..' in im.split('/') or not (SITE/im.lstrip('/')).is_file():raise ValueError(f'{path}: invalid or missing image {im}')
  if x.get('published') is True:posts.append((path.name,x))
 return sorted(posts,key=lambda pair:pair[1]['date'],reverse=True)

def article(filename,x,lang):
 z=x[lang];prefix='../' if lang=='ja' else '';href=safe_link(z.get('link',''))
 if href.startswith('http'):url=href
 elif href:url=prefix+href
 else:url=''
 l=f'<p><a href="{h(url)}">{h(z.get("link_label") or url)}</a></p>' if url else ''
 imgs=''.join(f'<img loading="lazy" src="{h(prefix+im.lstrip("/"))}" alt="{h(z["title"])}">' for im in x.get('images',[]))
 gallery=f'<div class="news-images">{imgs}</div>' if imgs else ''
 return f'<article class="news-item" id="{h(filename[:-5])}"><time datetime="{h(x["date"])}">{h(display_date(x["date"],lang))}</time><div><h2>{h(z["title"])}</h2><p>{h(z["body"])}</p>{gallery}{l}</div></article>'
def mini(filename,x,lang):
 z=x[lang]
 return f'<div class="news-mini"><time datetime="{h(x["date"])}">{h(display_date(x["date"],lang))}</time><p><a href="news.html#{h(filename[:-5])}">{h(z["summary"])}</a></p></div>'

def replacement(path,fragment,check=False):
 current=path.read_text()
 if current.count(START)!=1 or current.count(END)!=1:raise ValueError(f'Missing or duplicate news markers: {path}')
 before,tail=current.split(START);_,after=tail.split(END)
 output=before+START+'\n'+fragment+'\n'+END+after
 if not check and output!=current:path.write_text(output)
 return output!=current

def main(check=False):
 posts=load_posts()
 for lang in ('en','ja'):
  directory=SITE/('ja' if lang=='ja' else '')
  replacement(directory/'news.html','\n'.join(article(fn,x,lang) for fn,x in posts),check)
  replacement(directory/'index.html','\n'.join(mini(fn,x,lang) for fn,x in posts[:2]),check)
 print(f'Generated four static sections from {len(posts)} published posts'+(' (check only)' if check else ''))
if __name__=='__main__':main('--check' in sys.argv)
