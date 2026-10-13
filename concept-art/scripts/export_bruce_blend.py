"""Exporta la reconstrucción a Blender/GLB y renderiza una vista de revisión.

Ejecutar con Blender en segundo plano. Lee la geometría creada por
build_bruce_mesh.py; no altera las imágenes de referencia.
"""

import json
from pathlib import Path
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "bruce-3d"
data = json.loads((OUT / "bruce-mesh.json").read_text())
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bpy.context.preferences.filepaths.save_version = 0

mesh = bpy.data.meshes.new("Bruce_SilhouetteSurface")
# Visor: Y arriba, Z delante. Blender: Z arriba, -Y delante.
mesh.from_pydata([(x, -z, y) for x, y, z in data["vertices"]], [], data["faces"])
mesh.update()
obj = bpy.data.objects.new("Bruce · base por siluetas", mesh)
bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
for polygon in mesh.polygons:
    polygon.use_smooth = True

attribute = mesh.color_attributes.new(name="ReferenceColor", type="FLOAT_COLOR", domain="POINT")
# La referencia contiene sRGB; el atributo de Blender almacena valores lineales.
def linear(value):
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4

for slot, rgb in zip(attribute.data, data["colors"]):
    slot.color = (*[linear(c) for c in rgb], 1.0)
mesh.color_attributes.active_color = attribute
material = bpy.data.materials.new("Colores proyectados desde las referencias")
material.use_nodes = True
shader = material.node_tree.nodes.get("Principled BSDF")
shader.inputs["Roughness"].default_value = 0.78
vertex = material.node_tree.nodes.new("ShaderNodeVertexColor")
vertex.layer_name = "ReferenceColor"
material.node_tree.links.new(vertex.outputs["Color"], shader.inputs["Base Color"])
obj.data.materials.append(material)
obj["Método"] = "Volumen por secciones elípticas, guiado por referencias y contornos frontal/trasero."
obj["Estado"] = "Aproximación inicial. Sin rig ni retopología. No es un escaneo."
obj["Escala"] = "Metros. Altura canónica de Bruce: 1,80 m; reconstrucción aproximada desde las referencias anteriores."

# El GLB contiene únicamente el personaje, con color por vértice.
bpy.ops.export_scene.gltf(filepath=str(OUT / "bruce.glb"), export_format="GLB", use_selection=True)

review = bpy.data.collections.new("Revisión · cámara y luces")
bpy.context.scene.collection.children.link(review)
def review_object(name, datablock, location):
    item = bpy.data.objects.new(name, datablock)
    review.objects.link(item)
    item.location = location
    return item

def aim(item, target):
    item.rotation_euler = (Vector(target) - item.location).to_track_quat("-Z", "Y").to_euler()

camera = review_object("Cámara", bpy.data.cameras.new("Cámara"), (3.3, -6.0, 2.8))
camera.data.type = "ORTHO"
camera.data.ortho_scale = 2.14
aim(camera, (0, -0.03, 0.87))
scene = bpy.context.scene
scene.camera = camera
for name, location, power, size in [
    ("Principal", (-3, -4, 5), 420, 4),
    ("Relleno", (4, -2, 3), 220, 3),
    ("Contorno", (1, 3, 4), 350, 3),
]:
    light = bpy.data.lights.new(name, "AREA")
    light.energy, light.shape, light.size = power, "DISK", size
    item = review_object(name, light, location)
    aim(item, (0, 0, 0.85))
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.055, 0.075, 0.095, 1)
scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.6
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 24
scene.render.resolution_x = 800
scene.render.resolution_y = 1000
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(OUT / "bruce-preview.png")
scene.view_settings.view_transform = "Standard"

# Vista inicial útil al abrir el archivo editable.
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type == "VIEW_3D":
            area.spaces.active.region_3d.view_distance = 2.8
            area.spaces.active.region_3d.view_location = (0, 0, 0.9)
            area.spaces.active.region_3d.view_rotation = camera.rotation_euler.to_quaternion()
            area.spaces.active.shading.type = "SOLID"
            area.spaces.active.shading.color_type = "VERTEX"
            area.spaces.active.clip_end = 100
notes = bpy.data.texts.new("LEER · alcance de la malla")
notes.write("Bruce: volumen inicial guiado por cuatro referencias y secciones elípticas.\n"
            "La profundidad se estima por región corporal; no procede de un escaneo.\n"
            "Los colores son proyecciones de los dibujos, no detalles esculpidos.\n"
            "Las vistas de arriba/abajo tienen perspectiva y no calibran el volumen.\n"
            "Brazos, ropa y manos pueden compartir volumen donde se tocan en las imágenes.\n"
            "Esta base necesita modelado y retopología antes de crear un rig.\n"
            "Selecciona Bruce y entra en modo Edición para revisar los vértices.\n")
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "bruce.blend"))
bpy.ops.render.render(write_still=True)
print(json.dumps({"blend": str(OUT / "bruce.blend"), "glb": str(OUT / "bruce.glb"),
                  "vertices": len(mesh.vertices), "triangles": len(mesh.polygons)}))
