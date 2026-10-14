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
             '## Alturas en reposo, con brazos junto al cuerpo', '', '| Punto | Altura |', '| --- | --- |']
    text += [f'| {LANDMARK_LABELS[key]} | {cm(value)} |' for key, value in sorted(points.items(), key=lambda item: -item[1])]
    pose_points = spec['modeling_landmarks']
    text += ['', '## Pose A obligatoria para modelado: brazos a 45°', '',
             'Los brazos rectos se separan 45° del torso vertical en el plano frontal. Hombro, codo, muñeca y mano conservan sus longitudes. En los perfiles, la misma pose se ve con escorzo.', '',
             '| Punto | Altura en pose A |', '| --- | --- |']
    text += [f'| {LANDMARK_LABELS[key]} | {cm(pose_points[key])} |' for key in ['shoulder','elbow','wrist','fingertips']]
    text += ['', 'Altura del punto = 146 cm − longitud acumulada del brazo × cos(45°). Las cotas de 114, 88 y 70 cm corresponden a brazos verticales en reposo; no se usan para la pose A.', '',
             f"La separación entre puntas de los dedos en pose A es {cm(spec['modeling_arm_span'])}. La envergadura de 188 cm corresponde a brazos horizontales.", '']
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
                   f"- La pose de modelado usa brazos a 45° del torso; codos a {cm(pose_points['elbow'])}, muñecas a {cm(pose_points['wrist'])} y dedos a {cm(pose_points['fingertips'])} del suelo.",
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
              'Identidad: conservar rostro, pelo, colores y ropa de las vistas vigentes en pose A. Proporciones del cuerpo: seguir el maniquí y las medidas de esta ficha, sin tomar las diferencias de dibujo como nuevas proporciones.',
              'Altura total 180 cm, desde las suelas hasta la parte superior de la cabeza de referencia. Misma escala, cámara ortográfica y suelo compartido para todas las vistas.']
    prompt += [f'{label}: {cm(value)}. {description}' for label, value, description in rows]
    prompt += ['Pose obligatoria de modelado: brazos rectos a 45° del torso vertical en el plano frontal.']
    prompt += [f'Altura en pose A de {LANDMARK_LABELS[key].lower()} sobre el suelo: {cm(value)}.' for key, value in sorted(pose_points.items(), key=lambda item: -item[1])]
    prompt += [f'Anchos del cuerpo (cm): {json.dumps(widths, ensure_ascii=False)}.', f'Profundidades del cuerpo (cm): {json.dumps(spec["depths"], ensure_ascii=False)}.']
    prompt += spec['rules']
    (ROOT / 'prompts/bruce-master-proportions.prompt.txt').write_text('\n'.join(prompt) + '\n')

    from render_body_reference import render_body_reference
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    source = next(asset for asset in manifest['assets'] if asset['id'] == 'bruce-a-pose-turnaround')
    render_body_reference(spec, source)
    print('Ficha, ideas, prompt y maniquí generados: altura 180 cm; brazo 76 cm; pierna hasta el suelo 95 cm.')


if __name__ == '__main__':
    main()
