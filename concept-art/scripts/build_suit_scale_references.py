"""Monta las seis láminas de trajes con el mismo formato de escala de Bruce."""
import json
from build_scale_reference import ROOT, VIEW_LABELS, render_scale_sheet


def main():
    catalog = json.loads((ROOT / 'manifest.json').read_text())
    assets = {asset['id']: asset for asset in catalog['assets']}
    guides = [asset for asset in assets.values()
              if asset.get('generator') == 'scripts/build_suit_scale_references.py'
              and asset['status'] == 'vigente']
    assert len(guides) == 6, 'Deben existir seis láminas de trajes vigentes.'
    for guide in guides:
        source = assets[guide['sourceAssetId']]
        bounds = source['viewBounds']
        assert len(bounds) == 4
        views = []
        for box, label in zip(bounds, VIEW_LABELS):
            left, top, right, bottom = box
            assert 0 <= left < right and 0 <= top < bottom
            views.append(({'file': source['file'], 'displayBounds': box}, label))
        title = guide['title'].split(' · ')[0]
        render_scale_sheet(views, title, guide['file'], clean_alpha=True)


if __name__ == '__main__':
    main()
