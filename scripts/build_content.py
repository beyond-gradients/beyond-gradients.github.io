"""Regenerate homepage content from JSON using only Python's standard library."""
from html import escape
from pathlib import Path
import json
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'content/site.json').read_text())


def safe_url(value):
    parsed = urlparse(value)
    if parsed.scheme != 'https' or not parsed.netloc:
        raise ValueError(f'Expected an absolute HTTPS URL: {value!r}')
    return escape(value, quote=True)


def illustration(kind):
    base = '<svg viewBox="0 0 380 180" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="#30415b" stroke-width="1"><path d="M30 45H350M30 90H350M30 135H350"/></g>'
    text = lambda x, y, s, color='#b9c7dc', size=12: f'<text x="{x}" y="{y}" fill="{color}" font-family="monospace" font-size="{size}">{escape(s)}</text>'
    if kind == 'prediction':
        body = text(30, 34, 'The next token is…', size=13)
        for y, width, label, value in [(61,174,'a', '58%'),(98,82,'the','27%'),(135,45,'one','15%')]:
            body += text(31,y+13,label) + f'<rect x="82" y="{y-1}" width="{width}" height="21" rx="2" fill="#689cff" opacity="{1 if y==61 else .45}"/>' + text(272,y+14,value)
    elif kind == 'attention':
        body = ''
        for i in range(5):
            for j in range(5):
                opacity = [.13,.25,.44,.66,.93][(i*3+j*2)%5]
                body += f'<rect x="{112+j*30}" y="{18+i*29}" width="24" height="23" rx="2" fill="#689cff" opacity="{opacity}"/>'
        body += text(30,95,'Q') + text(277,95,'Kᵀ')
    elif kind == 'vectors':
        body = '<path d="M65 143H327M91 160V22M67 162L283 29" stroke="#50617d" fill="none"/>'
        for x,y,label in [(207,64,'cat'),(246,43,'dog'),(169,112,'word')]:
            body += f'<path d="M91 143L{x} {y}" stroke="#689cff" stroke-width="1.5"/><circle cx="{x}" cy="{y}" r="4" fill="#689cff"/>' + text(x+10,y+5,label)
    elif kind == 'descent':
        body = '<path d="M42 33Q155 235 335 30" stroke="#536c92" stroke-width="2" fill="none"/><path d="M67 72L105 111L142 135L174 145L199 143" stroke="#689cff" stroke-width="2" fill="none"/>'
        for x,y in [(67,72),(105,111),(142,135),(174,145)]: body += f'<circle cx="{x}" cy="{y}" r="4" fill="#689cff"/>'
        body += '<circle cx="199" cy="143" r="5" fill="#ef9b8c"/>' + text(225,106,'−η∇L', '#d9e2f0',19)
    elif kind == 'confidence':
        body = text(33,45,'Fluent ≠ factual', '#d9e2f0',17)
        for y,w in [(67,264),(80,223),(93,248)]: body += f'<rect x="34" y="{y}" width="{w}" height="4" rx="2" fill="#4a6285"/>'
        body += '<path d="M35 130H234" stroke="#689cff" stroke-width="2"/><circle cx="266" cy="130" r="15" fill="none" stroke="#ef9b8c"/>' + text(261,135,'?', '#ef9b8c',16)
    elif kind == 'qkv':
        body = '<path d="M91 79H291M191 79V140" stroke="#506d99" fill="none"/>'
        for x,label in [(67,'Q'),(166,'K'),(265,'V')]:
            body += f'<rect x="{x}" y="52" width="48" height="48" rx="3" fill="#192b46" stroke="#689cff"/>' + text(x+16,83,label,'#b9d1fc',23)
        body += text(101,147,'match → weight → combine',size=12)
    else:
        raise ValueError(f'Unknown illustration: {kind}')
    return base + body + '</svg>'


def main():
    page_path = ROOT / 'index.html'
    page = page_path.read_text()
    cards = []
    for item in DATA['explanations']:
        platform = item['platform']
        platform_label = {'instagram':'Instagram','youtube':'YouTube'}[platform]
        url = safe_url(item.get('url') or DATA['platforms'][platform])
        link_label = f'View explanation on {platform_label}' if item.get('url') else f'Explore our {platform_label}'
        status = item.get('format', 'Visual explainer') if item.get('url') else 'Topic preview'
        title = escape(item['title'])
        visual = illustration(item['visual'])
        if item.get('thumbnail'):
            thumbnail = Path(item['thumbnail'])
            if thumbnail.is_absolute() or '..' in thumbnail.parts or not (ROOT / thumbnail).is_file():
                raise ValueError('Thumbnail must name an existing file inside this repository')
            visual = f'<img src="{escape(thumbnail.as_posix(), quote=True)}" alt="" width="380" height="180" loading="lazy" decoding="async">'
        cards.append(f'''          <article class="content-card">
            <div class="card-visual">{visual}</div>
            <div class="card-body">
              <div class="card-meta"><span>{escape(item['category'])}</span><span>{escape(status)}</span></div>
              <h3>{title}</h3><p>{escape(item['description'])}</p>
              <a class="card-link" href="{url}" target="_blank" rel="noopener noreferrer" aria-label="{escape(link_label + ': ' + item['title'], quote=True)}">{link_label}<span aria-hidden="true">↗</span></a>
            </div>
          </article>''')
    markup = '<!-- EXPLANATIONS:START -->\n        <div class="content-grid">\n' + '\n'.join(cards) + '\n        </div>\n        <!-- EXPLANATIONS:END -->'
    page, count = re.subn(r'<!-- EXPLANATIONS:START -->.*?<!-- EXPLANATIONS:END -->', lambda _: markup, page, flags=re.S)
    assert count == 1, 'Homepage content markers missing or duplicated'
    # Static links are explicitly marked, so profile changes never affect direct post links.
    for platform in ('instagram', 'youtube'):
        url = safe_url(DATA['platforms'][platform])
        pattern = r'(data-platform="' + platform + r'" href=")[^"]*(")'
        page = re.sub(pattern, lambda match: match[1] + url + match[2], page)
    metadata = re.search(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)
    organization = json.loads(metadata.group(1))
    organization['sameAs'] = [DATA['platforms'][name] for name in ('instagram', 'youtube')]
    page = re.sub(r'(<script type="application/ld\+json">).*?(</script>)', lambda m: m[1]+'\n    '+json.dumps(organization).replace('<','\\u003c')+'\n  '+m[2], page, flags=re.S)
    page_path.write_text(page)
    print(f'Rendered {len(cards)} explanations and platform links.')


if __name__ == '__main__':
    main()
