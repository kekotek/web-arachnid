"""Genera la ficha de Bruce, su maniquí y las instrucciones desde las medidas maestras."""
from pathlib import Path
import base64
import json
import struct
from html import escape
from character_dimensions import ROOT, load_dimensions, measurement_rows, LANDMARK_LABELS, cm


def main():
    spec = load_dimensions()
    lengths, widths, points = spec['lengths'], spec['widths'], spec['landmarks']
    chain = ' + '.join(f'{lengths[key]:g}' for key in ['head','neck','torso_shoulder_to_hip','thigh','calf','ankle_to_ground']) + f" = {spec['height']:g} cm"
    rows = measurement_rows(spec)
    text = ['# Proporciones maestras de Bruce', '',
            'Estas son las medidas de diseño de Bruce: un joven de 18 años, delgado, de **1,80 m** de altura total. Fijan las proporciones que debe conservar el cuerpo en todas las vistas y skins.', '',
            'Las longitudes de las extremidades se miden entre centros de articulación. La longitud de la mano termina en la punta del dedo medio. Los anchos corresponden al cuerpo; la ropa y los guantes pueden añadir volumen exterior.', '',
            '## Longitudes y medidas principales', '', '| Parte | Medida | Cómo medir |', '| --- | --- | --- |']
    text += [f'| {label} | {cm(value)} | {description} |' for label, value, description in rows]
    text += ['', f'La altura se cierra exactamente: **{chain}**. El largo horizontal del pie no se suma a esta altura. La cabeza ocupa aproximadamente una séptima parte de la altura total.', '',
             '## Alturas de referencia desde el suelo', '', '| Punto | Altura |', '| --- | --- |']
    text += [f'| {LANDMARK_LABELS[key]} | {cm(value)} |' for key, value in sorted(points.items(), key=lambda item: -item[1])]
    text += ['', '## Anchos y profundidades', '', '| Parte | Ancho | Profundidad |', '| --- | --- | --- |',
             f"| Cabeza, sin volumen lateral del pelo | {cm(widths['head'])} | {cm(spec['depths']['head'])} |",
             f"| Silueta lateral máxima del pelo | {cm(widths['hair_silhouette_max'])} | — |",
             f"| Cuello | {cm(widths['neck'])} | — |",
             f"| Pecho | {cm(widths['chest'])} | {cm(spec['depths']['chest'])} |",
             f"| Cintura | {cm(widths['waist'])} | — |",
             f"| Caderas | {cm(widths['hips'])} | {cm(spec['depths']['hips'])} |",
             f"| Mano | {cm(widths['hand'])} | — |",
             f"| Brazo superior | {cm(widths['upper_arm'])} | — |",
             f"| Antebrazo | {cm(widths['forearm'])} | — |",
             f"| Muslo | {cm(widths['thigh'])} | — |",
             f"| Rodilla a tobillo | {cm(widths['calf'])} | — |",
             f"| Pie | {cm(widths['foot'])} | — |", '',
             '## Reglas para mantener la coherencia', '']
    text += ['- ' + rule for rule in spec['rules']]
    text += ['', '- La fuente única de medidas es [bruce-proportions.json](bruce-proportions.json). Si cambia una medida, se debe regenerar la ficha y comprobar que la suma de alturas sigue siendo 180 cm.',
             '- El maniquí fija medidas objetivo. Las ilustraciones existentes se usan para la identidad visual; deben compararse con estas cotas al revisar sus proporciones.',
             '- Para obtener vistas exactamente iguales del personaje, usar un único modelo 3D con estas dimensiones y girar la cámara.', '',
             '## Lámina de construcción', '',
             '[Abrir la lámina de proporciones](assets/characters/bruce/body-reference/bruce-proportions-180cm.svg).', '']
    (ROOT / 'bruce-proportions.md').write_text('\n'.join(text))

    ideas_path = ROOT.parent / 'ideas.md'
    ideas = ideas_path.read_text()
    heading = '## Proporciones del personaje'
    idea_block = [heading, '',
                  'Bruce tendrá medidas de diseño fijas para conservar el mismo cuerpo en todas las vistas. Las extremidades se miden entre centros de articulación; la mano, desde la muñeca hasta la punta del dedo medio.', '',
                  '| Parte | Medida |', '| --- | --- |']
    keys = [('Cabeza', lengths['head']), ('Cuello', lengths['neck']), ('Torso: hombros a caderas', lengths['torso_shoulder_to_hip']),
            ('Brazo superior: hombro a codo', lengths['upper_arm']), ('Antebrazo: codo a muñeca', lengths['forearm']),
            ('Mano: muñeca a dedo medio', lengths['hand']), ('Brazo completo', spec['arm_total']),
            ('Muslo: cadera a rodilla', lengths['thigh']), ('Rodilla a tobillo', lengths['calf']),
            ('Tobillo al suelo, incluyendo pie y calzado', lengths['ankle_to_ground']), ('Largo del pie', lengths['foot']),
            ('Ancho exterior de hombros', widths['shoulders_outer'])]
    idea_block += [f'| {name} | {cm(value)} |' for name, value in keys]
    idea_block += ['', f'- La altura total se conserva mediante la suma **{chain}**.',
                   f"- En reposo, los hombros están a {cm(points['shoulder'])} del suelo; los codos a {cm(points['elbow'])}; las muñecas a {cm(points['wrist'])}; las puntas de los dedos a {cm(points['fingertips'])}; las caderas a {cm(points['hip'])} y las rodillas a {cm(points['knee'])}.",
                   '- Ambos lados del cuerpo tienen las mismas longitudes. Los trajes conservan el esqueleto y solo añaden volumen exterior.',
                   '- La ficha completa y las líneas de construcción están en [la guía de proporciones](concept-art/bruce-proportions.md).', '']
    block = '\n'.join(idea_block) + '\n'
    if heading in ideas:
        start = ideas.index(heading)
        end = ideas.find('\n## ', start + len(heading))
        ideas = ideas[:start] + block + (ideas[end+1:] if end >= 0 else '')
    else:
        ideas = ideas.replace('## Aster City', block + '## Aster City', 1)
    ideas_path.write_text(ideas)

    prompt = ['Referencia obligatoria de Bruce para nuevos dibujos y modelos.',
              'Identidad: conservar rostro, pelo, colores y ropa de las vistas de modelado 3D v3. Proporciones del cuerpo: seguir el maniquí y las medidas de esta ficha, sin tomar las diferencias de dibujo como nuevas proporciones.',
              'Altura total 180 cm, desde las suelas hasta la parte superior de la cabeza de referencia. Misma escala, cámara ortográfica y suelo compartido para todas las vistas.']
    prompt += [f'{label}: {cm(value)}. {description}' for label, value, description in rows]
    prompt += [f'Altura de {LANDMARK_LABELS[key].lower()} sobre el suelo: {cm(value)}.' for key, value in sorted(points.items(), key=lambda item: -item[1])]
    prompt += [f'Anchos del cuerpo (cm): {json.dumps(widths, ensure_ascii=False)}.', f'Profundidades del cuerpo (cm): {json.dumps(spec["depths"], ensure_ascii=False)}.']
    prompt += spec['rules']
    (ROOT / 'prompts/bruce-master-proportions.prompt.txt').write_text('\n'.join(prompt) + '\n')

    # The raster reference is embedded unchanged. All construction geometry is vector-based.
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    front = next(asset for asset in manifest['assets'] if asset['id'] == 'bruce-modeling-front-v3')
    data = (ROOT / front['file']).read_bytes()
    native_w, native_h = struct.unpack('>II', data[16:24])
    left, upper, right, bottom = front['displayBounds']
    scale, floor = 4.2, 980
    y = lambda height: floor - height * scale
    center = 1000
    x = lambda offset: center + offset * scale
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1900" height="1120" viewBox="0 0 1900 1120" role="img" aria-labelledby="title desc">',
           '<title id="title">Bruce: medidas maestras para un personaje de 1,80 m</title>',
           '<desc id="desc">Referencia visual de Bruce, maniquí con articulaciones y tablas de longitudes. Brazo superior 32 cm, antebrazo 26 cm, mano 18 cm, muslo 46 cm y rodilla a tobillo 41 cm.</desc>',
           '<rect width="1900" height="1120" fill="#eeeae1"/>',
           '<g font-family="Arial, sans-serif" fill="#24313b">',
           '<text x="55" y="62" font-size="38" font-weight="700">BRUCE · MEDIDAS MAESTRAS</text>',
           '<text x="55" y="102" font-size="20" fill="#52616c">Altura total: 1,80 m · Cuerpo joven y delgado · Medidas de diseño en centímetros</text>',
           '<text x="430" y="172" text-anchor="middle" font-size="18" font-weight="700">IDENTIDAD VISUAL</text>',
           '<text x="1000" y="172" text-anchor="middle" font-size="18" font-weight="700">MANIQUÍ · MEDIDAS OBJETIVO</text>',
           '<text x="55" y="193" font-size="13" fill="#52616c">ALTURAS DESDE EL SUELO</text>']
    body_height = spec['height'] * scale
    factor = body_height / (bottom - upper)
    start = 430 - (right - left) * factor / 2
    svg += [f'<defs><clipPath id="front"><rect x="{start}" y="{y(spec["height"])}" width="{(right-left)*factor}" height="{body_height}"/></clipPath></defs>',
            f'<image x="{start-left*factor}" y="{y(spec["height"])-upper*factor}" width="{native_w*factor}" height="{native_h*factor}" href="data:image/png;base64,{base64.b64encode(data).decode()}" clip-path="url(#front)"/>']

    guide_names = {'crown':'Cabeza', 'chin':'Mentón', 'shoulder':'Hombros', 'elbow':'Codos',
                   'waist':'Cintura', 'hip':'Caderas', 'wrist':'Muñecas', 'fingertips':'Dedos',
                   'knee':'Rodillas', 'ankle':'Tobillos', 'ground':'Suelo'}
    for key, name in guide_names.items():
        label = f'{points[key]:g} · {name}'
        svg += [f'<line x1="188" y1="{y(points[key])}" x2="1210" y2="{y(points[key])}" stroke="#647581" stroke-opacity=".35" stroke-dasharray="6 6"/>',
                f'<text x="55" y="{y(points[key])+5}" font-size="16">{escape(label)}</text>']

    # A neutral construction mannequin, not an alternative portrait of Bruce.
    svg.append(f'<ellipse cx="{center}" cy="{y((points["crown"]+points["chin"])/2)}" rx="{widths["head"]*scale/2}" ry="{lengths["head"]*scale/2}" fill="#d7dce0" stroke="#405260" stroke-width="2"/>')
    svg.append(f'<rect x="{x(-widths["neck"]/2)}" y="{y(points["chin"])}" width="{widths["neck"]*scale}" height="{lengths["neck"]*scale}" fill="#d7dce0" stroke="#405260" stroke-width="2"/>')
    half_shoulder, half_chest, half_waist, half_hip = [widths[key]/2 for key in ['shoulder_joint_spacing','chest','waist','hips']]
    torso = [(-half_shoulder,points['shoulder']), (half_shoulder,points['shoulder']),
             (half_chest,points['shoulder']-10), (half_waist,points['waist']), (half_hip,points['hip']),
             (half_waist,points['crotch']), (-half_waist,points['crotch']), (-half_hip,points['hip']),
             (-half_waist,points['waist']), (-half_chest,points['shoulder']-10)]
    svg.append('<polygon points="'+ ' '.join(f'{x(a)},{y(b)}' for a,b in torso) + '" fill="#d7dce0" stroke="#405260" stroke-width="2"/>')
    for sign in (-1, 1):
        arm_x = x(sign * widths['shoulder_joint_spacing']/2)
        leg_x = x(sign * widths['hip_joint_spacing']/2)
        for start_point, end_point, thickness in [('shoulder','elbow',widths['upper_arm']),('elbow','wrist',widths['forearm'])]:
            svg.append(f'<line x1="{arm_x}" x2="{arm_x}" y1="{y(points[start_point])}" y2="{y(points[end_point])}" stroke="#adbcc5" stroke-width="{thickness*scale}" stroke-linecap="round"/>')
        svg.append(f'<rect x="{arm_x-widths["hand"]*scale/2}" y="{y(points["wrist"])}" width="{widths["hand"]*scale}" height="{lengths["hand"]*scale}" rx="10" fill="#cbd4da" stroke="#405260" stroke-width="2"/>')
        for start_point,end_point,thickness in [('hip','knee',widths['thigh']),('knee','ankle',widths['calf'])]:
            svg.append(f'<line x1="{leg_x}" x2="{leg_x}" y1="{y(points[start_point])}" y2="{y(points[end_point])}" stroke="#b5c3cb" stroke-width="{thickness*scale}" stroke-linecap="round"/>')
        svg.append(f'<rect x="{leg_x-widths["foot"]*scale/2}" y="{y(points["ankle"])}" width="{widths["foot"]*scale}" height="{lengths["ankle_to_ground"]*scale}" rx="8" fill="#cbd4da" stroke="#405260" stroke-width="2"/>')
        for key in ['shoulder','elbow','wrist']:
            svg.append(f'<circle cx="{arm_x}" cy="{y(points[key])}" r="6" fill="#087e83"/>')
        for key in ['hip','knee','ankle']:
            svg.append(f'<circle cx="{leg_x}" cy="{y(points[key])}" r="6" fill="#087e83"/>')

    def dimension(offset, high, low, label, align='start'):
        px = x(offset)
        svg.extend([f'<line x1="{px}" x2="{px}" y1="{y(high)}" y2="{y(low)}" stroke="#087e83" stroke-width="2"/>',
                    f'<line x1="{px-7}" x2="{px+7}" y1="{y(high)}" y2="{y(high)}" stroke="#087e83" stroke-width="2"/>',
                    f'<line x1="{px-7}" x2="{px+7}" y1="{y(low)}" y2="{y(low)}" stroke="#087e83" stroke-width="2"/>',
                    f'<text x="{px+(13 if align=="start" else -13)}" y="{y((high+low)/2)+6}" text-anchor="{align}" font-size="19" font-weight="700" fill="#087e83">{escape(label)}</text>'])
    dimension(32,points['shoulder'],points['elbow'],cm(lengths['upper_arm']))
    dimension(32,points['elbow'],points['wrist'],cm(lengths['forearm']))
    dimension(32,points['wrist'],points['fingertips'],cm(lengths['hand']))
    dimension(-34,points['shoulder'],points['hip'],cm(lengths['torso_shoulder_to_hip']),'end')
    dimension(-30,points['hip'],points['knee'],cm(lengths['thigh']),'end')
    dimension(-30,points['knee'],points['ankle'],cm(lengths['calf']),'end')
    dimension(-30,points['ankle'],0,cm(lengths['ankle_to_ground']),'end')
    svg += ['<rect x="1325" y="215" width="520" height="810" rx="18" fill="#faf8f3" stroke="#c5cdd1"/>',
            '<text x="1360" y="260" font-size="23" font-weight="700">LONGITUDES FIJAS</text>']
    compact = [('Cabeza',lengths['head']),('Cuello',lengths['neck']),('Torso · hombros a caderas',lengths['torso_shoulder_to_hip']),('Brazo superior',lengths['upper_arm']),('Antebrazo',lengths['forearm']),('Mano',lengths['hand']),('Brazo completo',spec['arm_total']),('Muslo',lengths['thigh']),('Rodilla a tobillo',lengths['calf']),('Tobillo al suelo',lengths['ankle_to_ground']),('Largo del pie',lengths['foot']),('Ancho de hombros',widths['shoulders_outer'])]
    for index,(label,value) in enumerate(compact):
        row_y = 309 + index * 43
        svg += [f'<text x="1360" y="{row_y}" font-size="18">{escape(label)}</text>',
                f'<text x="1810" y="{row_y}" text-anchor="end" font-size="20" font-weight="700" fill="#087e83">{cm(value)}</text>',
                f'<line x1="1360" x2="1810" y1="{row_y+15}" y2="{row_y+15}" stroke="#d8dfe1"/>']
    svg += ['<text x="1360" y="860" font-size="17" font-weight="700">ALTURA TOTAL</text>',
            f'<text x="1360" y="891" font-size="17">{chain}</text>',
            '<text x="1360" y="942" font-size="16" fill="#52616c">Brazos y piernas: entre articulaciones.</text>',
            '<text x="1360" y="969" font-size="16" fill="#52616c">Mano: muñeca a punta del dedo medio.</text>',
            '<text x="55" y="1067" font-size="17" fill="#52616c">El maniquí fija las medidas objetivo. La imagen conserva la identidad visual; no es una medición automática de la ilustración.</text>',
            '<text x="55" y="1095" font-size="15" fill="#52616c">web-arachnid · Misma escala en frente, perfiles y espalda · Las skins conservan estas longitudes</text>', '</g></svg>']
    (ROOT / 'assets/characters/bruce/body-reference/bruce-proportions-180cm.svg').write_text('\n'.join(svg)+'\n')
    print('Ficha, ideas, prompt y maniquí generados: altura 180 cm; brazo 76 cm; pierna hasta el suelo 95 cm.')


if __name__ == '__main__':
    main()
