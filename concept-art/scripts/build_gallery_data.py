"""Actualiza los datos de la galería local a partir de manifest.json."""
from pathlib import Path
import json
import struct
import html
import re
import posixpath
import xml.etree.ElementTree as ET
from character_dimensions import load_dimensions

ROOT = Path(__file__).resolve().parents[1]


def render_document(text, base):
    """Renderiza el Markdown utilizado por los documentos locales, sin HTML crudo."""
    tokens = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)|\[([^\]]+)\]\(([^)]+)\)|\*\*(.+?)\*\*|`([^`]+)`')
    def url(target):
        if target.startswith(('https://', 'http://', '#')):
            return target
        path, separator, fragment = target.partition('#')
        resolved = posixpath.normpath(posixpath.join(base, path))
        routes = {'../ideas.md': '#vista=ideas', '../README.md': '#vista=juego',
                  'README.md': '#vista=guia', 'index.html': '#vista=arte',
                  '../concept-art/index.html': '#vista=arte', '../concept-art/README.md': '#vista=guia',
                  'bruce-proportions.md': '#vista=proporciones', '../concept-art/bruce-proportions.md': '#vista=proporciones'}
        route = routes.get(resolved, resolved)
        if separator:
            return '#'+fragment if route.startswith('#') else route+'#'+fragment
        return route
    def inline(source):
        output, cursor = [], 0
        for match in tokens.finditer(source):
            output.append(html.escape(source[cursor:match.start()]))
            if match.group(1) is not None:
                output.append(f'<img loading="lazy" src="{html.escape(url(match.group(2)), quote=True)}" alt="{html.escape(match.group(1), quote=True)}">')
            elif match.group(3) is not None:
                output.append(f'<a href="{html.escape(url(match.group(4)), quote=True)}">{html.escape(match.group(3))}</a>')
            elif match.group(5) is not None:
                output.append(f'<strong>{html.escape(match.group(5))}</strong>')
            else:
                output.append(f'<code>{html.escape(match.group(6))}</code>')
            cursor = match.end()
        output.append(html.escape(source[cursor:]))
        return ''.join(output)
    lines, output, outline = text.splitlines(), [], []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        heading = re.match(r'^(#{1,6}) (.+)$', line)
        if heading:
            level, title = len(heading.group(1)), heading.group(2)
            anchor = 'section-' + str(len(outline))
            outline.append({'title': re.sub(r'[*`]', '', title), 'id': anchor, 'level': level})
            output.append(f'<h{level} id="{anchor}">{inline(title)}</h{level}>')
            i += 1
        elif line.startswith('|') and i+1 < len(lines) and re.match(r'^\|[\s:|\-]+\|$', lines[i+1].strip()):
            cells = lambda row: [inline(c.strip()) for c in row.strip().strip('|').split('|')]
            output.append('<div class="table-scroll"><table><thead><tr>' + ''.join('<th>'+c+'</th>' for c in cells(line)) + '</tr></thead><tbody>')
            i += 2
            while i < len(lines) and lines[i].strip().startswith('|'):
                output.append('<tr>'+''.join('<td>'+c+'</td>' for c in cells(lines[i]))+'</tr>')
                i += 1
            output.append('</tbody></table></div>')
        elif line.startswith('- '):
            output.append('<ul>')
            while i < len(lines) and lines[i].strip().startswith('- '):
                output.append('<li>'+inline(lines[i].strip()[2:])+'</li>')
                i += 1
            output.append('</ul>')
        else:
            paragraph = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^(#|- |\|)', lines[i].strip()):
                paragraph.append(lines[i].strip())
                i += 1
            output.append('<p>'+inline(' '.join(paragraph))+'</p>')
    return {'html': ''.join(output), 'outline': outline}


def main():
    catalog = json.loads((ROOT / 'manifest.json').read_text())
    catalog['characterSpec'] = load_dimensions()
    ids = set()
    for asset in catalog['assets']:
        assert asset['id'] not in ids, f"ID duplicado: {asset['id']}"
        ids.add(asset['id'])
        path = ROOT / asset['file']
        if path.suffix == '.svg':
            element = ET.parse(path).getroot()
            asset['width'], asset['height'] = int(element.attrib['width']), int(element.attrib['height'])
            asset['format'] = 'SVG'
        else:
            with path.open('rb') as image:
                header = image.read(24)
            assert header[:8] == b'\x89PNG\r\n\x1a\n', path
            asset['width'], asset['height'] = struct.unpack('>II', header[16:24])
            asset['format'] = 'PNG'
        for key in ('prompt', 'repairPrompt', 'finalRepairPrompt', 'consistencyPrompt', 'heightRepairPrompt'):
            if key in asset:
                assert (ROOT / asset[key]).is_file(), asset[key]
        for reference in asset.get('references', []) + asset.get('consistencyReferences', []):
            assert (ROOT / reference).is_file(), reference
    catalog['documents'] = {
        'ideas': render_document((ROOT.parent / 'ideas.md').read_text(), '..'),
        'juego': render_document((ROOT.parent / 'README.md').read_text(), '..'),
        'proporciones': render_document((ROOT / 'bruce-proportions.md').read_text(), '.'),
        'guia': render_document((ROOT / 'README.md').read_text(), '.')
    }
    data = json.dumps(catalog, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    (ROOT / 'gallery-data.js').write_text('// Generado desde manifest.json. Abrir index.html.\nwindow.WEB_ARACHNID_ART = ' + data + ';\n')
    print(f"Galería actualizada: {len(catalog['assets'])} imágenes y todas las rutas verificadas.")


if __name__ == '__main__':
    main()
