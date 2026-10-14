"""Importa la malla recibida, calibra su altura y crea archivos de revisión en Blender."""
from pathlib import Path
import json
import math
import bpy
from mathutils import Vector, Matrix

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'assets/characters/bruce/civilian/models/hunyuan3d-2mv'
SPEC = json.loads((ROOT / 'bruce-proportions.json').read_text())


def bounds(objects):
    points = [obj.matrix_world @ Vector(corner) for obj in objects for corner in obj.bound_box]
    return [[min(p[i] for p in points) for i in range(3)],
            [max(p[i] for p in points) for i in range(3)]]


def aim(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(OUTPUT / 'bruce-hunyuan-raw.glb'))
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    assert meshes and all(len(o.data.vertices) > 0 for o in meshes)
    before = bounds(meshes)
    original_height = before[1][2] - before[0][2]
    target_height = SPEC['height'] / 100
    factor = target_height / original_height
    center = [(before[0][i] + before[1][i]) / 2 for i in range(2)]
    transform = Matrix.Translation((-center[0] * factor, -center[1] * factor, -before[0][2] * factor)) @ Matrix.Scale(factor, 4)
    matrices = [(o, o.matrix_world.copy()) for o in meshes]
    for obj, world in matrices:
        obj.parent = None
        obj.matrix_world = transform @ world
    bpy.context.view_layer.update()
    bpy.ops.object.select_all(action='DESELECT')
    for obj in meshes:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    after = bounds(meshes)
    assert math.isclose(after[1][2] - after[0][2], target_height, abs_tol=1e-5)
    assert abs(after[0][2]) < 1e-5
    for index, obj in enumerate(meshes):
        obj.name = f'Bruce_Civilian_Hunyuan_{index:02d}'
        for face in obj.data.polygons:
            face.use_smooth = True
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1
    bpy.ops.export_scene.gltf(filepath=str(OUTPUT / 'bruce-hunyuan-180cm.glb'), export_format='GLB', use_selection=True, export_apply=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT / 'bruce-hunyuan-180cm.blend'))
    report = {'source': 'bruce-hunyuan-raw.glb', 'normalized': 'bruce-hunyuan-180cm.glb',
              'blender_file': 'bruce-hunyuan-180cm.blend', 'units': 'meters',
              'blender_up_axis': 'Z', 'gltf_up_axis': 'Y', 'height_meters': after[1][2] - after[0][2],
              'uniform_scale_factor': factor, 'original_bounds_blender': before,
              'normalized_bounds_blender': after,
              'vertices': sum(len(o.data.vertices) for o in meshes),
              'polygons': sum(len(o.data.polygons) for o in meshes),
              'mesh_objects': len(meshes), 'textures': False, 'armature': False,
              'measurement_validation': 'Altura total y suelo verificados. Las longitudes anatómicas y el ángulo de los brazos no están validados por un esqueleto; requiere revisión de modelado.'}
    (OUTPUT / 'model-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')

    # Render a neutral review view without changing the saved model's materials.
    material = bpy.data.materials.new('Review_Clay')
    material.diffuse_color = (.58, .63, .67, 1)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (.58, .63, .67, 1)
    bsdf.inputs['Roughness'].default_value = .8
    for obj in meshes:
        obj.data.materials.clear()
        obj.data.materials.append(material)
        for face in obj.data.polygons:
            face.use_smooth = True
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 24
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1100
    scene.render.resolution_y = 1100
    scene.render.resolution_percentage = 100
    scene.world = bpy.data.worlds.new('Review_World')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (.13, .16, .19, 1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .65
    for location, energy, size in [((2,-3,4),650,4),((-3,-1,2),450,3),((0,3,3),550,3)]:
        data = bpy.data.lights.new('Review_Light', 'AREA');data.energy=energy;data.shape='DISK';data.size=size
        lamp=bpy.data.objects.new('Review_Light',data);scene.collection.objects.link(lamp);lamp.location=location;aim(lamp,(0,0,.9))
    camera_data=bpy.data.cameras.new('Review_Camera');camera=bpy.data.objects.new('Review_Camera',camera_data)
    scene.collection.objects.link(camera);scene.camera=camera
    camera_data.type='ORTHO';camera_data.ortho_scale=2.1
    # GLTF faces +Z, mapped by the Blender importer to -Y.
    for name,location in [('front',(0,-4,.9)),('three-quarter',(2.5,-4,1.4)),('back',(0,4,.9))]:
        camera.location=location;aim(camera,(0,0,.9))
        scene.render.filepath=str(OUTPUT/f'bruce-hunyuan-{name}-preview.png')
        bpy.ops.render.render(write_still=True)
    print(json.dumps(report,ensure_ascii=False))


main()
