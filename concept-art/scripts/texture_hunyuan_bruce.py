"""Bake the four approved reference views onto the existing Bruce mesh.

This is local multiview projection, not Hunyuan3D-Paint inference. Geometry is
preserved; the output is a review draft with UVs and an embedded base-color map.
Run inside Blender from the project root.
"""
from pathlib import Path
import json
import math
import bpy
import numpy as np
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'assets/characters/bruce/civilian/models/hunyuan3d-2mv'
INPUT = ROOT / 'assets/characters/bruce/civilian/modeling-references/hunyuan3d-2mv'
PREFIX = 'bruce-hunyuan-textured'


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()


def main():
    bpy.ops.wm.open_mainfile(filepath=str(OUTPUT / 'bruce-hunyuan-180cm.blend'))
    obj = next(o for o in bpy.context.scene.objects if o.type == 'MESH')
    mesh = obj.data
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    count = len(mesh.vertices)
    xyz = np.empty(count * 3, dtype=np.float32)
    normals = np.empty_like(xyz)
    mesh.vertices.foreach_get('co', xyz)
    mesh.vertices.foreach_get('normal', normals)
    xyz = xyz.reshape(-1, 3)
    normals = normals.reshape(-1, 3)
    original_xyz = xyz.copy()
    low, high = xyz.min(axis=0), xyz.max(axis=0)
    assert math.isclose(float(high[2] - low[2]), 1.8, abs_tol=1e-5)
    loops = np.empty(len(mesh.loops), dtype=np.int32)
    mesh.loops.foreach_get('vertex_index', loops)
    material = bpy.data.materials.new('Bruce_Reference_Projection')
    material.use_nodes = True
    tree = material.node_tree
    tree.nodes.clear()
    output = tree.nodes.new('ShaderNodeOutputMaterial')
    emission = tree.nodes.new('ShaderNodeEmission')
    tree.links.new(emission.outputs[0], output.inputs['Surface'])

    # Four orthographic reference cameras: front -Y, back +Y, left -X,
    # right +X. Profile arms remain foreshortened as in the approved views.
    # The profiles overlap the arms with the hip and pouch. Restrict their
    # contribution to the head, so painted profile hands cannot appear on
    # the trousers. For the body, blend front/back by surface depth.
    head_mix = np.clip((xyz[:, 2] - 1.48) / .08, 0, 1)
    front_depth = 1 / (1 + np.exp(np.clip(xyz[:, 1] / .015, -40, 40)))
    front_weight = head_mix * np.maximum(-normals[:, 1], 0) ** 4 + (1 - head_mix) * front_depth
    back_weight = head_mix * np.maximum(normals[:, 1], 0) ** 4 + (1 - head_mix) * (1 - front_depth)
    settings = [('front', 0, 1, front_weight),
                ('back', 0, -1, back_weight),
                ('left', 1, -1, head_mix * np.maximum(-normals[:, 0], 0) ** 4),
                ('right', 1, 1, head_mix * np.maximum(normals[:, 0], 0) ** 4)]
    uv_maps, confidence, pictures = [], [], []
    for name, axis, sign, facing in settings:
        picture = bpy.data.images.load(str(INPUT / f'{name}.png'), check_existing=True)
        pixels = np.empty(1024 * 1024 * 4, dtype=np.float32)
        picture.pixels.foreach_get(pixels)
        alpha = pixels.reshape(1024, 1024, 4)[:, :, 3] > .5
        rows, cols = np.where(alpha)
        left, right = cols.min(), cols.max()
        center = (left + right) / 2
        width = right - left
        u = center + sign * (xyz[:, axis] - (low[axis] + high[axis]) / 2) / (high[axis] - low[axis]) * width
        v = 62 + xyz[:, 2] * 500
        # Generated fingertips sit below their painted reference counterparts.
        # Limit the hand lookup to the reference hand zone, so the trousers
        # are not projected onto the ends of the fingers.
        hands = (np.abs(xyz[:, 0]) > .44) & (xyz[:, 2] < 1.08)
        v[hands] = np.maximum(v[hands], 540)
        px = np.clip(np.rint(u), 0, 1023).astype(int)
        py = np.clip(np.rint(v), 62, 961).astype(int)
        valid = alpha[py, px]
        confidence.append(facing * np.where(valid, 1.0, .05))
        # Where the generated silhouette misses the reference silhouette,
        # project to the nearest foreground on the same height row. This
        # avoids baking transparent background into exposed mesh surfaces.
        for row in np.unique(py):
            indices = np.where(py == row)[0]
            # Project silhouette edges into the colored interior. Otherwise
            # the illustration's black outer contour becomes a broad black
            # stripe on the sides and undersides of the 3D mesh.
            occupied = np.flatnonzero(alpha[row])
            if not len(occupied):
                continue
            runs = np.split(occupied, np.flatnonzero(np.diff(occupied) > 1) + 1)
            # Keep a center strip even for narrow fingers, rather than
            # allowing the nearest larger region (jeans) to win the lookup.
            occupied = np.concatenate([run[min(8, len(run) // 3):len(run) - min(8, len(run) // 3)] for run in runs])
            positions = np.searchsorted(occupied, px[indices])
            a = occupied[np.clip(positions - 1, 0, len(occupied) - 1)]
            b = occupied[np.clip(positions, 0, len(occupied) - 1)]
            px[indices] = np.where(abs(a - px[indices]) < abs(b - px[indices]), a, b)
            u[indices] = px[indices]
        layer = mesh.uv_layers.new(name=f'Projection_{name}')
        uv = np.column_stack(((u + .5) / 1024, (v + .5) / 1024)).astype(np.float32)
        layer.data.foreach_set('uv', uv[loops].ravel())
        uv_maps.append(layer.name)
        pictures.append(picture)

    weights = np.column_stack(confidence)
    missing = weights.sum(axis=1) < 1e-10
    weights[missing, 0] = 1
    weights /= weights.sum(axis=1)[:, None]
    attribute = mesh.color_attributes.new(name='Projection_Weights', type='FLOAT_COLOR', domain='POINT')
    attribute.data.foreach_set('color', weights.astype(np.float32).ravel())
    color = tree.nodes.new('ShaderNodeVertexColor')
    color.layer_name = attribute.name
    separate = tree.nodes.new('ShaderNodeSeparateColor')
    tree.links.new(color.outputs['Color'], separate.inputs['Color'])
    accumulator = None
    for index, (uv_name, picture) in enumerate(zip(uv_maps, pictures)):
        uv_node = tree.nodes.new('ShaderNodeUVMap')
        uv_node.uv_map = uv_name
        texture = tree.nodes.new('ShaderNodeTexImage')
        texture.image = picture
        tree.links.new(uv_node.outputs['UV'], texture.inputs['Vector'])
        multiply = tree.nodes.new('ShaderNodeMixRGB')
        multiply.blend_type = 'MULTIPLY'
        multiply.inputs[0].default_value = 1
        tree.links.new(texture.outputs['Color'], multiply.inputs[1])
        weight = separate.outputs[index] if index < 3 else color.outputs['Alpha']
        tree.links.new(weight, multiply.inputs[2])
        if accumulator is None:
            accumulator = multiply.outputs[0]
        else:
            add = tree.nodes.new('ShaderNodeMixRGB')
            add.blend_type = 'ADD'
            add.inputs[0].default_value = 1
            tree.links.new(accumulator, add.inputs[1])
            tree.links.new(multiply.outputs[0], add.inputs[2])
            accumulator = add.outputs[0]
    tree.links.new(accumulator, emission.inputs['Color'])
    mesh.materials.clear()
    mesh.materials.append(material)

    print('Creating UV atlas', flush=True)
    atlas_uv = mesh.uv_layers.new(name='BaseColor_UV')
    mesh.uv_layers.active = atlas_uv
    atlas_uv.active_render = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=.003)
    bpy.ops.object.mode_set(mode='OBJECT')
    atlas = bpy.data.images.new('Bruce_BaseColor', width=4096, height=4096, alpha=False)
    target = tree.nodes.new('ShaderNodeTexImage')
    target.image = atlas
    tree.nodes.active = target
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 1
    scene.render.bake.margin = 12
    print('Baking approved reference colors', flush=True)
    bpy.ops.object.bake(type='EMIT')
    textures = OUTPUT / 'textures'
    textures.mkdir(exist_ok=True)
    atlas.filepath_raw = str(textures / 'bruce-base-color.png')
    atlas.file_format = 'PNG'
    atlas.save()
    atlas.pack()

    # A conventional PBR material and a single UV map export cleanly to GLB.
    mesh.materials.clear()
    material = bpy.data.materials.new('Bruce_Civilian_Textured')
    material.use_nodes = True
    tree = material.node_tree
    bsdf = tree.nodes.get('Principled BSDF')
    bsdf.inputs['Roughness'].default_value = .85
    texture = tree.nodes.new('ShaderNodeTexImage')
    texture.image = atlas
    tree.links.new(texture.outputs['Color'], bsdf.inputs['Base Color'])
    mesh.materials.append(material)
    for layer in list(mesh.uv_layers):
        if layer.name != 'BaseColor_UV':
            mesh.uv_layers.remove(layer)
    mesh.color_attributes.remove(attribute)
    bpy.ops.export_scene.gltf(filepath=str(OUTPUT / f'{PREFIX}-180cm.glb'), export_format='GLB', use_selection=True, export_apply=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT / f'{PREFIX}-180cm.blend'))
    check = np.empty(count * 3, dtype=np.float32)
    mesh.vertices.foreach_get('co', check)
    assert np.array_equal(original_xyz.ravel(), check), 'Texturing must not change geometry'
    report = {
        'method': 'Local Blender four-view projection and UV baking; NOT Hunyuan3D-Paint',
        'source_mesh': 'bruce-hunyuan-180cm.blend',
        'model': f'{PREFIX}-180cm.glb', 'blender_file': f'{PREFIX}-180cm.blend',
        'base_color': 'textures/bruce-base-color.png', 'texture_size': [4096, 4096],
        'geometry_unchanged': True, 'height_meters': float(high[2] - low[2]),
        'vertices': count, 'triangles': len(mesh.polygons), 'armature': False,
        'status': 'Projection draft for visual review; seams and projected details need refinement',
        'reference_views': [str(INPUT.relative_to(ROOT) / f'{s[0]}.png') for s in settings],
        'api_limitation': 'Current Spark API exposes geometry-only /generate; texture inference requires a Hunyuan3D-Paint service.'
    }
    (OUTPUT / 'texture-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    scene.cycles.samples = 24
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1100
    scene.render.resolution_y = 1100
    scene.render.resolution_percentage = 100
    scene.view_settings.view_transform = 'Standard'
    scene.world = bpy.data.worlds.new('Review_World')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (.13, .16, .19, 1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .45
    for location, energy, size in [((2, -3, 4), 300, 4), ((-3, -1, 2), 200, 3), ((0, 3, 3), 250, 3)]:
        data = bpy.data.lights.new('Review_Light', 'AREA')
        data.energy, data.shape, data.size = energy, 'DISK', size
        lamp = bpy.data.objects.new('Review_Light', data)
        scene.collection.objects.link(lamp)
        lamp.location = location
        aim(lamp, (0, 0, .9))
    data = bpy.data.cameras.new('Review_Camera')
    camera = bpy.data.objects.new('Review_Camera', data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    data.type, data.ortho_scale = 'ORTHO', 2.1
    for name, location in [('front', (0, -4, .9)), ('three-quarter', (2.5, -4, 1.4)), ('back', (0, 4, .9))]:
        camera.location = location
        aim(camera, (0, 0, .9))
        scene.render.filepath = str(OUTPUT / f'{PREFIX}-{name}-preview.png')
        bpy.ops.render.render(write_still=True)
    print(json.dumps(report), flush=True)


main()
