"""Crea una lámina SVG a escala sin modificar los PNG de Bruce."""
from pathlib import Path
import base64
import json
import struct
from html import escape
from character_dimensions import load_dimensions

ROOT = Path(__file__).resolve().parents[1]


VIEW_LABELS = ['FRENTE', 'PERFIL IZQUIERDO', 'PERFIL DERECHO', 'ESPALDA']


def render_scale_sheet(views, title, output, clean_alpha=False):
    spec = load_dimensions()
    character_height = spec['height']
    assert len(views) == 4
    top, body_height, floor = 135, 640, 775
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">',
           f'<title id="title">{escape(title)}: escala y proporciones de 1,80 metros</title>',
           '<desc id="desc">Frente, perfiles y espalda alineados desde las suelas a la parte superior de la cabeza, entre 0 y 180 centímetros.</desc>',
           '<rect width="1600" height="900" fill="#eeeae1"/>',
           '<g font-family="Arial, sans-serif" fill="#24313b">',
           f'<text x="60" y="58" font-size="32" font-weight="700">{escape(title.upper())} · ESCALA Y PROPORCIONES: 1,80 m</text>',
           '<text x="60" y="91" font-size="16" fill="#52616c">Vistas revisadas · Líneas cian: alturas objetivo de hombros, codos, caderas, muñecas, dedos y rodillas.</text>']
    # Embed each unchanged PNG once; four suit views share one source board.
    sources = {}
    svg.append('<defs>')
    if clean_alpha:
        svg.append('<filter id="cutout" color-interpolation-filters="sRGB"><feComponentTransfer><feFuncA type="discrete" tableValues="0 0 1 1"/></feComponentTransfer></filter>')
    for asset, _ in views:
        if asset['file'] in sources:
            continue
        data = (ROOT / asset['file']).read_bytes()
        width, height = struct.unpack('>II', data[16:24])
        source_id = f'source-{len(sources)}'
        sources[asset['file']] = source_id
        encoded = base64.b64encode(data).decode()
        svg.append(f'<image id="{source_id}" width="{width}" height="{height}" href="data:image/png;base64,{encoded}"/>')
    svg.append('</defs>')
    for index, (asset, label) in enumerate(views):
        left, upper, right, bottom = asset['displayBounds']
        factor = body_height / (bottom - upper)
        visible_width = (right - left) * factor
        center = 320 + index * 350
        start = center - visible_width / 2
        clip = f'figure-{index}'
        svg.append(f'<defs><clipPath id="{clip}"><rect x="{start}" y="{top}" width="{visible_width}" height="{body_height}"/></clipPath></defs>')
        filter_attribute = ' filter="url(#cutout)"' if clean_alpha else ''
        svg.append(f'<g clip-path="url(#{clip})"><use href="#{sources[asset["file"]]}" transform="translate({start-left*factor} {top-upper*factor}) scale({factor})"{filter_attribute}/></g>')
        svg.append(f'<text x="{center}" y="818" text-anchor="middle" font-size="15" font-weight="700" letter-spacing="1.5">{escape(label)}</text>')
    for centimeters in range(0, 181, 10):
        y = top + body_height * (1 - centimeters / character_height)
        major = centimeters % 30 == 0
        svg.append(f'<line x1="123" y1="{y}" x2="1510" y2="{y}" stroke="#536674" stroke-opacity="{0.48 if major else 0.18}" stroke-dasharray="5 5"/>')
        svg.append(f'<line x1="115" y1="{y}" x2="123" y2="{y}" stroke="#536674"/>')
        if major:
            label = '1,80 m' if centimeters == 180 else f'{centimeters} cm'
            svg.append(f'<text x="105" y="{y+5}" text-anchor="end" font-size="15">{label}</text>')
    svg.append(f'<line x1="123" y1="{top}" x2="123" y2="{floor}" stroke="#536674"/>')
    for key, label in [('shoulder','Hombros'),('elbow','Codos'),('hip','Caderas'),('wrist','Muñecas'),('fingertips','Dedos'),('knee','Rodillas')]:
        centimeters = spec['landmarks'][key]
        y = top + body_height * (1 - centimeters / character_height)
        svg.append(f'<line x1="222" y1="{y}" x2="1510" y2="{y}" stroke="#087e83" stroke-opacity=".6" stroke-dasharray="3 7"/>')
        svg.append(f'<text x="214" y="{y+4}" text-anchor="end" font-size="12" fill="#087e83">{centimeters:g} · {label}</text>')
    svg.append('<text x="800" y="863" text-anchor="middle" font-size="14" fill="#52616c">web-arachnid · Referencia de escala · 1,80 m = altura total del personaje</text></g></svg>')
    path = ROOT / output
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(svg) + '\n')
    print(f'{output}: cuatro siluetas de 640 px entre 0 y 180 cm.')


def main():
    catalog = json.loads((ROOT / 'manifest.json').read_text())
    assets = {asset['id']: asset for asset in catalog['assets']}
    ids = ['bruce-modeling-front-v3', 'bruce-modeling-left-v3',
           'bruce-modeling-right-v3', 'bruce-modeling-back-v3']
    views = [(assets[identifier], label) for identifier, label in zip(ids, VIEW_LABELS)]
    render_scale_sheet(views, 'Bruce', assets['bruce-scale-180cm']['file'])
    guide = assets.get('bruce-with-gloves-scale-180cm')
    if guide:
        source = assets[guide['sourceAssetId']]
        gloved_views = [({'file': source['file'], 'displayBounds': box}, label)
                        for box, label in zip(source['viewBounds'], VIEW_LABELS)]
        render_scale_sheet(gloved_views, 'Bruce con guantes', guide['file'], clean_alpha=True)


if __name__ == '__main__':
    main()
