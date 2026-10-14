"""Dibuja un maniquí vectorial con longitudes exactas y pose A a 45°."""
import base64
import math
import struct
from html import escape
from character_dimensions import ROOT, cm


def render_body_reference(spec, source):
    lengths, widths = spec['lengths'], spec['widths']
    points, offsets = spec['modeling_landmarks'], spec['modeling_arm_offsets']
    scale, floor, center = 4.4, 972, 1290
    x = lambda offset: center + offset * scale
    y = lambda height: floor - height * scale
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="1150" viewBox="0 0 2400 1150" role="img" aria-labelledby="title desc">',
           '<title id="title">Bruce: medidas maestras y pose A de 45 grados</title>',
           '<desc id="desc">Altura 180 cm, brazos de 32, 26 y 18 cm. Maniquí calculado con brazos rectos a 45 grados del torso.</desc>',
           '<rect width="2400" height="1150" fill="#eeeae1"/>',
           '<g font-family="Arial, sans-serif" fill="#24313b">',
           '<text x="55" y="60" font-size="38" font-weight="700">BRUCE · MEDIDAS MAESTRAS · POSE A: 45°</text>',
           '<text x="55" y="105" font-size="20" fill="#52616c">Mismas medidas de diseño · Altura total: 180 cm · Brazo: 32 + 26 + 18 = 76 cm · Pierna: 46 + 41 + 8 = 95 cm</text>',
           '<text x="520" y="153" text-anchor="middle" font-size="18" font-weight="700">IDENTIDAD VISUAL</text>',
           '<text x="1290" y="153" text-anchor="middle" font-size="18" font-weight="700">MANIQUÍ · GEOMETRÍA DE CONSTRUCCIÓN</text>']
    data = (ROOT / source['file']).read_bytes()
    width, height = struct.unpack('>II', data[16:24])
    left, top, right, bottom = source['viewBounds'][0]
    factor = spec['height'] * scale / (bottom - top)
    start = 520 - (right-left) * factor / 2
    svg.extend(['<defs><clipPath id="front"><rect x="'+str(start)+'" y="180" width="'+str((right-left)*factor)+'" height="792"/></clipPath>',
                '<filter id="cutout" color-interpolation-filters="sRGB"><feComponentTransfer><feFuncA type="discrete" tableValues="0 0 1 1"/></feComponentTransfer></filter></defs>',
                f'<g clip-path="url(#front)"><image x="{start-left*factor}" y="{180-top*factor}" width="{width*factor}" height="{height*factor}" href="data:image/png;base64,{base64.b64encode(data).decode()}" filter="url(#cutout)"/></g>'])
    for key,label in [('crown','Cabeza'),('shoulder','Hombros'),('elbow','Codos'),('wrist','Muñecas'),('hip','Caderas'),('fingertips','Dedos'),('knee','Rodillas'),('ground','Suelo')]:
        baseline = y(points[key]) + (-9 if key == 'hip' else 11 if key == 'fingertips' else 5)
        svg.extend([f'<line x1="188" x2="1660" y1="{y(points[key])}" y2="{y(points[key])}" stroke="#647581" stroke-opacity=".35" stroke-dasharray="6 6"/>',
                    f'<text x="55" y="{baseline}" font-size="16">{cm(points[key])} · {label}</text>'])
    svg.extend([f'<ellipse cx="{center}" cy="{y((points["crown"]+points["chin"])/2)}" rx="{widths["head"]*scale/2}" ry="{lengths["head"]*scale/2}" fill="#d7dce0" stroke="#405260" stroke-width="2"/>',
                f'<rect x="{x(-widths["neck"]/2)}" y="{y(points["chin"])}" width="{widths["neck"]*scale}" height="{lengths["neck"]*scale}" fill="#d7dce0" stroke="#405260"/>'])
    hs,hc,hw,hh = [widths[key]/2 for key in ['shoulder_joint_spacing','chest','waist','hips']]
    torso=[(-hs,points['shoulder']),(hs,points['shoulder']),(hc,points['shoulder']-10),
           (hw,points['waist']),(hh,points['hip']),(hw,points['crotch']),
           (-hw,points['crotch']),(-hh,points['hip']),(-hw,points['waist']),(-hc,points['shoulder']-10)]
    svg.append('<polygon points="'+' '.join(f'{x(a)},{y(b)}' for a,b in torso)+'" fill="#d7dce0" stroke="#405260" stroke-width="2"/>')
    # All segment endpoints come from the canonical lengths and sin/cos(45°).
    for sign in (-1,1):
        for high,low,thickness in [('shoulder','elbow',widths['upper_arm']),('elbow','wrist',widths['forearm']),('wrist','fingertips',widths['hand'])]:
            svg.append(f'<line data-segment="{high}-{low}" x1="{x(sign*offsets[high])}" x2="{x(sign*offsets[low])}" y1="{y(points[high])}" y2="{y(points[low])}" stroke="#adbcc5" stroke-width="{thickness*scale}" stroke-linecap="butt"/>')
        leg_x=x(sign*widths['hip_joint_spacing']/2)
        for high,low,thickness in [('hip','knee',widths['thigh']),('knee','ankle',widths['calf'])]:
            svg.append(f'<line x1="{leg_x}" x2="{leg_x}" y1="{y(points[high])}" y2="{y(points[low])}" stroke="#b5c3cb" stroke-width="{thickness*scale}" stroke-linecap="round"/>')
        svg.append(f'<rect x="{leg_x-widths["foot"]*scale/2}" y="{y(points["ankle"])}" width="{widths["foot"]*scale}" height="{lengths["ankle_to_ground"]*scale}" rx="8" fill="#cbd4da" stroke="#405260"/>')
        for key in ['shoulder','elbow','wrist']:
            svg.append(f'<circle cx="{x(sign*offsets[key])}" cy="{y(points[key])}" r="6" fill="#087e83"/>')
        for key in ['hip','knee','ankle']:
            svg.append(f'<circle cx="{leg_x}" cy="{y(points[key])}" r="6" fill="#087e83"/>')
    # Diagonal dimension lines measure actual limb length, not vertical drop.
    for high,low,key in [('shoulder','elbow','upper_arm'),('elbow','wrist','forearm'),('wrist','fingertips','hand')]:
        ax,ay=x(offsets[high])+20,y(points[high])-20
        bx,by=x(offsets[low])+20,y(points[low])-20
        svg.extend([f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="#087e83" stroke-width="2"/>',
                    f'<text x="{(ax+bx)/2+15}" y="{(ay+by)/2-8}" font-size="18" font-weight="700" fill="#087e83">{cm(lengths[key])}</text>'])
    shoulder_x=x(offsets['shoulder']); shoulder_y=y(points['shoulder'])
    svg.extend([f'<line x1="{shoulder_x}" x2="{shoulder_x}" y1="{shoulder_y}" y2="{shoulder_y+100}" stroke="#087e83" stroke-dasharray="4 4"/>',
                f'<path d="M {shoulder_x} {shoulder_y+60} A 60 60 0 0 0 {shoulder_x+60/math.sqrt(2)} {shoulder_y+60/math.sqrt(2)}" fill="none" stroke="#087e83" stroke-width="2"/>',
                f'<text x="{shoulder_x+14}" y="{shoulder_y+90}" font-size="20" font-weight="700" fill="#087e83">45°</text>'])
    svg.extend(['<rect x="1750" y="180" width="580" height="810" rx="18" fill="#faf8f3" stroke="#c5cdd1"/>',
                '<text x="1785" y="222" font-size="23" font-weight="700">LONGITUDES FIJAS</text>'])
    table=[('Cabeza',lengths['head']),('Cuello',lengths['neck']),('Torso: hombros a caderas',lengths['torso_shoulder_to_hip']),
           ('Brazo superior',lengths['upper_arm']),('Antebrazo',lengths['forearm']),('Mano',lengths['hand']),('Brazo completo',spec['arm_total']),
           ('Muslo',lengths['thigh']),('Rodilla a tobillo',lengths['calf']),('Tobillo al suelo',lengths['ankle_to_ground']),
           ('Largo horizontal del pie',lengths['foot']),('Ancho exterior de hombros',widths['shoulders_outer'])]
    for i,(label,value) in enumerate(table):
        baseline=265+i*43
        svg.extend([f'<text x="1785" y="{baseline}" font-size="18">{escape(label)}</text>',f'<text x="2295" y="{baseline}" text-anchor="end" font-size="20" font-weight="700" fill="#087e83">{cm(value)}</text>'])
    svg.extend(['<text x="1785" y="835" font-size="18" font-weight="700">ALTURA TOTAL: 180 cm</text>',
                '<text x="1785" y="871" font-size="18">26 + 8 + 51 + 46 + 41 + 8 = 180</text>',
                '<text x="1785" y="923" font-size="16">Las cotas diagonales miden entre articulaciones.</text>',
                '<text x="1785" y="954" font-size="16">Las líneas horizontales indican alturas en pose A.</text>',
                '<text x="55" y="1050" font-size="18" fill="#52616c">El maniquí fija longitudes y ángulos. Las ilustraciones se contrastan con esta geometría; no se miden automáticamente.</text>',
                '<text x="55" y="1083" font-size="17" fill="#52616c">En el perfil los brazos tienen escorzo: misma pose de 45° en el plano frontal, sin giro hacia delante.</text>',
                '<text x="55" y="1115" font-size="17" fill="#52616c">web-arachnid · Un mismo cuerpo para todas las variantes · Brazos a 45° del torso vertical</text></g></svg>'])
    (ROOT/'assets/characters/bruce/body-reference/bruce-proportions-180cm.svg').write_text('\n'.join(svg)+'\n')
