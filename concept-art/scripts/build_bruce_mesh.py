"""Reconstrucción aproximada por siluetas; no sustituye el modelado anatómico.

Dependencias: numpy, Pillow, scipy y scikit-image.
Las imágenes originales se leen sin modificarlas. Y arriba, frente hacia +Z.
"""

from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from scipy.interpolate import PchipInterpolator
from skimage.measure import marching_cubes

ART = Path(__file__).resolve().parents[1]
REFERENCES = ART / "assets" / "archive" / "meshy"
OUT = ART / "bruce-3d"
HEIGHT = 1.80  # Altura canónica de Bruce en metros; la reconstrucción sigue usando referencias antiguas.
PIXELS = 1431 / HEIGHT
GROUND = 1470
STEP = HEIGHT / 320


def load_view(name, center, direction=1):
    path = REFERENCES / name
    pixels = np.asarray(Image.open(path).convert("RGBA"))
    mask = pixels[:, :, 3] > 96
    mask = ndi.binary_fill_holes(mask)
    field = ndi.distance_transform_edt(mask) - ndi.distance_transform_edt(~mask)
    # Tolerancia reducida para diferencias de tinta/alineación entre dibujos.
    field = ndi.gaussian_filter(field, 1.0)
    _, nearest = ndi.distance_transform_edt(~mask, return_indices=True)
    extended = pixels[nearest[0], nearest[1], :3] / 255.0
    return {"name": name, "center": center, "direction": direction,
            "field": field, "pixels": pixels, "colors": extended, "mask": mask}


def sample(view, horizontal, vertical, source="field"):
    u = view["center"] + view["direction"] * horizontal * PIXELS
    v = GROUND - vertical * PIXELS
    coordinates = np.broadcast_arrays(v, u)
    data = view[source]
    if data.ndim == 2:
        return ndi.map_coordinates(data, coordinates, order=1, mode="constant", cval=-1000)
    return np.stack([ndi.map_coordinates(data[:, :, c], coordinates, order=1, mode="nearest")
                     for c in range(3)], axis=-1)


def smooth_minimum(a, b, radius):
    h = np.maximum(radius - np.abs(a - b), 0) / radius
    return np.minimum(a, b) - h * h * radius * 0.25


def rounded_anatomy(xs, ys, zs, silhouette):
    """Guía de volumen manual: secciones elípticas con proporciones del dibujo.

    La profundidad de cada extremidad se estima por separado. Esto evita que
    el brazo herede todo el espesor de torso/bolso visible en el perfil.
    Las cotas usan píxeles de la referencia, no medidas anatómicas reales.
    """
    x = 524 + xs[:, None, None] * PIXELS
    v = GROUND - ys[None, :, None] * PIXELS
    z = 460 + zs[None, None, :] * PIXELS
    result = np.full((len(xs), len(ys), len(zs)), -1000, dtype=np.float32)

    def loft(knots, blend=6):
        nonlocal result
        knots = np.asarray(knots, dtype=float)
        t = np.clip(v, knots[0, 0], knots[-1, 0])
        cx, cz, rx, rz = [PchipInterpolator(knots[:, 0], knots[:, i])(t).astype(np.float32)
                          for i in range(1, 5)]
        radial = (1 - np.sqrt(((x - cx) / rx) ** 2 + ((z - cz) / rz) ** 2)) * np.minimum(rx, rz)
        field = np.minimum(radial, np.minimum(v - knots[0, 0], knots[-1, 0] - v))
        result = -smooth_minimum(-result, -field, blend)

    # Cabeza, cuello y capucha: silueta redondeada sin extruir la nariz en una franja.
    loft([(42,540,554,2,2),(65,532,548,63,65),(100,524,538,114,118),
          (155,524,535,125,126),(195,524,525,108,110),(225,524,526,89,98),
          (257,524,536,68,83),(282,524,542,45,60),(302,524,542,2,2)])
    loft([(260,524,509,34,39),(310,524,500,44,45),(355,524,493,47,49)])
    loft([(283,524,423,3,3),(302,524,427,86,54),(345,524,426,130,85),
          (390,524,425,120,82),(430,524,434,55,35)])
    # Torso de la sudadera y pelvis.
    loft([(339,524,475,65,57),(371,524,476,130,95),(422,524,481,137,98),
          (510,524,484,128,93),(580,524,486,126,93),(635,524,486,133,98),
          (679,524,487,142,101),(718,524,488,133,94),(738,524,489,121,89)])
    loft([(706,524,480,117,82),(749,524,482,130,88),(793,524,484,128,85),
          (831,524,484,111,78),(856,524,484,51,43)])
    # Brazos y manos. Cada lado tiene su propio espesor, independiente del torso.
    for sign in (-1, 1):
        def side(offset):
            return 524 + sign * offset
        loft([(362,side(117),465,25,33),(400,side(151),460,51,54),
              (470,side(170),454,48,50),(547,side(181),458,45,48),
              (593,side(186),468,48,49),(651,side(185),486,42,43),
              (710,side(195),501,43,40),(756,side(195),507,30,32),
              (782,side(193),512,25,27)])
        loft([(762,side(193),512,22,26),(803,side(193),524,27,27),
              (840,side(190),538,32,27),(876,side(187),542,27,21),
              (915,side(173),534,7,7)], blend=4)
        # Pierna y calzado; leve desfase de profundidad presente en el perfil.
        depth = sign * 26
        loft([(780,side(68),479+depth,64,70),(851,side(72),480+depth,63,70),
              (934,side(77),482+depth,57,62),(1014,side(74),479+depth,52,56),
              (1062,side(79),460+depth,53,58),(1140,side(79),448+depth,55,61),
              (1227,side(79),442+depth,55,59),(1293,side(76),439+depth,51,51),
              (1335,side(76),441+depth,43,43),(1360,side(76),449+depth,35,39)])
        loft([(1320,side(77),448+depth,26,35),(1354,side(78),466+depth,43,67),
              (1390,side(79),497+depth,55,99),(1428,side(82),510+depth,62,108),
              (1458,side(84),508+depth,62,110),(1466,side(84),508+depth,54,101)], blend=4)
    # Bolso del lado izquierdo anatómico: bloque redondeado en la cadera.
    loft([(673,657,426,19,20),(709,661,421,35,42),(769,663,419,39,46),
          (813,659,420,33,39),(827,654,422,10,15)], blend=3)
    # Conserva los contornos frontal/trasero, permitiendo pequeños desacuerdos.
    result = smooth_minimum(result, silhouette[:, :, None] + 5, 3)
    return ndi.gaussian_filter(result.astype(np.float32), 0.85)


def write_ply(path, vertices, colors, faces=None):
    with path.open("w") as output:
        output.write("ply\nformat ascii 1.0\ncomment Bruce - aproximacion por siluetas\n")
        output.write(f"element vertex {len(vertices)}\nproperty float x\nproperty float y\nproperty float z\n")
        output.write("property uchar red\nproperty uchar green\nproperty uchar blue\n")
        if faces is not None:
            output.write(f"element face {len(faces)}\nproperty list uchar int vertex_indices\n")
        output.write("end_header\n")
        for point, color in zip(vertices, colors):
            rgb = np.clip(np.rint(color * 255), 0, 255).astype(int)
            output.write(" ".join([*(f"{value:.6f}" for value in point), *(str(value) for value in rgb)]) + "\n")
        if faces is not None:
            for face in faces:
                output.write("3 " + " ".join(map(str, face)) + "\n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    views = {
        "front": load_view("bruce-for-meshy-front.png", 524),
        "back": load_view("bruce-for-meshy-back.png", 524, -1),
        "left": load_view("bruce-for-meshy.png", 460),
        "right": load_view("bruce-for-meshy-right.png", 560, -1),
    }
    xs = np.arange(-0.39, 0.39 + STEP, STEP, dtype=np.float32)
    ys = np.arange(-STEP * 3, HEIGHT + STEP * 4, STEP, dtype=np.float32)
    zs = np.arange(-0.29, 0.40 + STEP, STEP, dtype=np.float32)
    front = sample(views["front"], xs[:, None], ys[None, :])
    back = sample(views["back"], xs[:, None], ys[None, :])
    left = sample(views["left"], zs[None, :], ys[:, None])
    right = sample(views["right"], zs[None, :], ys[:, None])
    # Consenso entre vistas opuestas para evitar cortes por pequeños desacuerdos.
    width_field = (front + back) * 0.5
    depth_field = (left + right) * 0.5
    volume = rounded_anatomy(xs, ys, zs, width_field)
    inside = volume > 0
    labels, count = ndi.label(inside)
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    keep = np.where(sizes >= 80)[0]
    removed = int(inside.sum() - sizes[keep].sum())
    keep_mask = np.isin(labels, keep)
    volume[inside & ~keep_mask] = -5
    vertices, faces, _, _ = marching_cubes(volume, level=0, spacing=(STEP, STEP, STEP),
                                          step_size=2, allow_degenerate=False, gradient_direction="ascent")
    vertices += np.array([xs[0], ys[0], zs[0]])
    # Suavizado ligero de los escalones de discretización, conservando siluetas.
    edges = np.vstack((faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]))
    edges = np.vstack((edges, edges[:, ::-1]))
    edges = np.unique(edges, axis=0)
    degrees = np.bincount(edges[:, 0], minlength=len(vertices))
    for _ in range(3):
        for factor in (0.3, -0.31):
            sums = np.zeros_like(vertices)
            np.add.at(sums, edges[:, 0], vertices[edges[:, 1]])
            averages = sums / np.maximum(degrees[:, None], 1)
            vertices += factor * (averages - vertices)
    a, b, c = vertices[faces[:, 0]], vertices[faces[:, 1]], vertices[faces[:, 2]]
    face_normals = np.cross(b - a, c - a)
    signed_volume = np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6
    if signed_volume < 0:
        faces = faces[:, [0, 2, 1]]
        face_normals *= -1
    normals = np.zeros_like(vertices)
    for corner in range(3):
        np.add.at(normals, faces[:, corner], face_normals)
    normals /= np.maximum(np.linalg.norm(normals, axis=1, keepdims=True), 1e-10)
    # Color de referencia sin duplicar los ojos/brazos de los perfiles.
    # Frente y espalda dominan sus hemisferios; los laterales usan color base.
    row = GROUND - vertices[:, 1] * PIXELS
    col = 524 + vertices[:, 0] * PIXELS
    colors = np.tile([0.77, 0.28, 0.12], (len(vertices), 1))
    colors[row > 722] = [0.075, 0.22, 0.40]
    colors[(row > 1330)] = [0.87, 0.85, 0.77]
    colors[(row > 1443)] = [0.07, 0.09, 0.10]
    hands = (row > 769) & (row < 928) & (np.abs(col - 524) > 145)
    colors[hands] = [0.94, 0.64, 0.36]
    colors[(row < 288) | ((row < 340) & (np.abs(col - 524) < 46))] = [0.94, 0.64, 0.36]
    colors[row < 184] = [0.26, 0.15, 0.075]
    bag = (col > 633) & (row > 675) & (row < 829)
    colors[bag] = [0.42, 0.25, 0.12]
    projected_front = sample(views["front"], vertices[:, 0], vertices[:, 1], "colors")
    projected_back = sample(views["back"], vertices[:, 0], vertices[:, 1], "colors")
    face_direction = np.clip((np.abs(normals[:, 2]) - .22) / .45, 0, 1)
    projection = np.where((normals[:, 2] > 0)[:, None], projected_front, projected_back)
    colors = colors * (1-face_direction[:, None]) + projection * face_direction[:, None]
    mesh = {
        "name": "Bruce · volumen guiado por las referencias",
        "status": "Base aproximada; sin rig ni topología de animación.",
        "vertices": np.round(vertices, 6).tolist(),
        "faces": faces.tolist(),
        "colors": np.round(np.clip(colors, 0, 1), 4).tolist(),
    }
    encoded = json.dumps(mesh, ensure_ascii=False, separators=(",", ":"))
    (OUT / "bruce-mesh.json").write_text(encoded + "\n")
    (OUT / "bruce-mesh.js").write_text("window.BRUCE_MESH=" + encoded + ";\n")
    write_ply(OUT / "bruce-points.ply", vertices, colors)
    with (OUT / "bruce-mesh.obj").open("w") as output:
        output.write("# Bruce: superficie aproximada por siluetas; Y arriba\n")
        for v in vertices:
            output.write("v " + " ".join(f"{value:.6f}" for value in v) + "\n")
        for f in faces:
            output.write("f " + " ".join(str(index + 1) for index in f) + "\n")
    # Validación topológica de la superficie exportada.
    unique_edges, edge_counts = np.unique(np.sort(np.vstack((faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]])), axis=1), axis=0, return_counts=True)
    report = {
        "method": "Secciones elípticas por región corporal guiadas por proporciones de frente/perfil; contornos frontal/trasero, unión suavizada y marching cubes. Profundidad aproximada manualmente.",
        "sources": [view["name"] for view in views.values()],
        "excludedFromCalibration": ["bruce-for-meshy-top.png", "bruce-for-meshy-bottom.png"],
        "limitations": ["Los dibujos no son vistas calibradas de un objeto 3D real.",
                        "El método no recupera concavidades ni detalles anatómicos ocultos.",
                        "Puede unir regiones que se tocan en las siluetas, como brazos y torso.",
                        "La nube de puntos corresponde a vértices de la reconstrucción, no a un escaneo.",
                        "No contiene esqueleto, animación ni topología preparada para deformarse."],
        "vertices": len(vertices), "triangles": len(faces),
        "boundaryEdges": int((edge_counts == 1).sum()),
        "nonManifoldEdges": int((edge_counts > 2).sum()),
        "volumeComponentsBeforeCleanup": int(count), "smallVoxelsRemoved": removed,
        "bounds": [vertices.min(axis=0).tolist(), vertices.max(axis=0).tolist()],
        "reference": "https://cgvg.polito.it/vhull.html"
    }
    (OUT / "reconstruction.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ["vertices", "triangles", "boundaryEdges", "nonManifoldEdges", "bounds"]}))


if __name__ == "__main__":
    main()
