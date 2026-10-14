"""Prepara vistas independientes del asset vigente como entradas de inferencia."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def main():
    catalog = json.loads((ROOT / 'manifest.json').read_text())
    asset = next(a for a in catalog['assets'] if a['id'] == 'bruce-a-pose-turnaround')
    source = ROOT / asset['file']
    output = source.parent / 'hunyuan3d-2mv'
    output.mkdir(exist_ok=True)
    image = Image.open(source).convert('RGBA')
    spec = json.loads((ROOT / 'bruce-proportions.json').read_text())
    records = []
    for view, bounds in zip(['front', 'left', 'right', 'back'], asset['viewBounds']):
        # Use the approved SVG's alpha cutoff for inference, without repainting RGB.
        crop = image.crop(bounds)
        crop.putalpha(crop.getchannel('A').point(lambda v: 255 if v >= 128 else 0))
        body_height, floor = 900, 962
        factor = body_height / crop.height
        width = round(crop.width * factor)
        assert width < 1024
        crop = crop.resize((width, body_height), Image.Resampling.LANCZOS)
        canvas = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
        canvas.paste(crop, ((1024 - width) // 2, floor - body_height))
        target = output / f'{view}.png'
        canvas.save(target)
        records.append({'view': view, 'file': str(target.relative_to(ROOT)),
                        'source_bounds': bounds, 'image_dimensions': [1024, 1024],
                        'body_height_px': body_height, 'floor_px': floor,
                        'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
    metadata = {'character': 'Bruce', 'variant': 'civilian', 'model': 'tencent/Hunyuan3D-2mv',
                'source': asset['file'], 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                'pose': spec['modeling_pose'], 'target_height_meters': spec['height'] / 100,
                'preprocessing': 'Separación de vistas, máscara alfa del SVG aprobado y encuadre a escala común; sin redibujar el personaje.',
                'views': records}
    (output / 'inputs.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')
    print('Cuatro entradas de inferencia preparadas:', output)


if __name__ == '__main__':
    main()
