"""Carga las medidas de Bruce y deriva articulaciones desde una sola fuente."""
from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parents[1]


def load_dimensions():
    spec = json.loads((ROOT / 'bruce-proportions.json').read_text())
    lengths, widths = spec['lengths'], spec['widths']
    assert spec['units'] == 'cm'
    assert spec['height'] == 180, 'La altura canónica de Bruce es 180 cm.'
    assert all(value > 0 for group in ('lengths', 'widths', 'depths') for value in spec[group].values())
    points = {'ground': 0}
    points['ankle'] = lengths['ankle_to_ground']
    points['knee'] = points['ankle'] + lengths['calf']
    points['hip'] = points['knee'] + lengths['thigh']
    points['shoulder'] = points['hip'] + lengths['torso_shoulder_to_hip']
    points['chin'] = points['shoulder'] + lengths['neck']
    points['crown'] = points['chin'] + lengths['head']
    assert points['crown'] == spec['height'], 'La suma de cabeza, cuello, torso y piernas debe coincidir con la altura total.'
    points['elbow'] = points['shoulder'] - lengths['upper_arm']
    points['wrist'] = points['elbow'] - lengths['forearm']
    points['fingertips'] = points['wrist'] - lengths['hand']
    points['waist'] = points['hip'] + spec['landmark_offsets']['waist_above_hip']
    points['crotch'] = points['hip'] - spec['landmark_offsets']['crotch_below_hip']
    assert 0 < points['ankle'] < points['knee'] < points['hip'] < points['waist'] < points['shoulder'] < points['chin'] < points['crown']
    assert points['knee'] < points['fingertips'] < points['wrist'] < points['elbow'] < points['shoulder']
    assert widths['shoulder_joint_spacing'] < widths['shoulders_outer']
    assert widths['shoulder_joint_spacing'] + widths['upper_arm'] == widths['shoulders_outer']
    assert widths['hip_joint_spacing'] < widths['hips']
    spec['landmarks'] = points
    spec['arm_total'] = lengths['upper_arm'] + lengths['forearm'] + lengths['hand']
    spec['leg_to_ground'] = lengths['thigh'] + lengths['calf'] + lengths['ankle_to_ground']
    spec['arm_span'] = widths['shoulder_joint_spacing'] + 2 * spec['arm_total']
    angle = spec['modeling_pose']['arm_angle_from_torso_degrees']
    assert angle == 45, 'La pose de modelado requiere brazos a 45° del torso.'
    radians = math.radians(angle)
    pose_points = dict(points)
    arm_offsets = {'shoulder': widths['shoulder_joint_spacing'] / 2}
    cumulative = 0
    for key, segment in [('elbow', 'upper_arm'), ('wrist', 'forearm'), ('fingertips', 'hand')]:
        cumulative += lengths[segment]
        pose_points[key] = points['shoulder'] - cumulative * math.cos(radians)
        arm_offsets[key] = arm_offsets['shoulder'] + cumulative * math.sin(radians)
    spec['modeling_landmarks'] = pose_points
    spec['modeling_arm_offsets'] = arm_offsets
    spec['modeling_arm_span'] = 2 * arm_offsets['fingertips']
    return spec


def cm(value):
    return f'{value:.2f}'.rstrip('0').rstrip('.').replace('.', ',') + ' cm'


def measurement_rows(spec):
    length = spec['lengths']
    return [
        ('Altura total', spec['height'], 'Desde las suelas hasta la parte superior de la cabeza de referencia.'),
        ('Cabeza', length['head'], 'Desde la parte superior de la cabeza de referencia hasta el mentón.'),
        ('Cuello', length['neck'], 'Desde el mentón hasta la línea de articulación de los hombros.'),
        ('Torso', length['torso_shoulder_to_hip'], 'Desde la línea de articulación de los hombros hasta la de las caderas.'),
        ('Brazo superior', length['upper_arm'], 'Desde el centro del hombro hasta el centro del codo.'),
        ('Antebrazo', length['forearm'], 'Desde el centro del codo hasta el centro de la muñeca.'),
        ('Mano', length['hand'], 'Desde la muñeca hasta la punta del dedo medio.'),
        ('Brazo completo', spec['arm_total'], f"Hombro a punta del dedo medio: {length['upper_arm']:g} + {length['forearm']:g} + {length['hand']:g}."),
        ('Muslo', length['thigh'], 'Desde el centro de la cadera hasta el centro de la rodilla.'),
        ('Rodilla a tobillo', length['calf'], 'Desde el centro de la rodilla hasta el centro del tobillo.'),
        ('Tobillo al suelo', length['ankle_to_ground'], 'Distancia vertical hasta las suelas; incluye pie y calzado.'),
        ('Pierna hasta el suelo', spec['leg_to_ground'], 'Desde la articulación de la cadera hasta el suelo.'),
        ('Largo del pie', length['foot'], 'Desde el talón hasta el dedo más largo; no se suma como altura.'),
        ('Ancho exterior de hombros', spec['widths']['shoulders_outer'], 'Ancho frontal del cuerpo; distinto de la separación entre articulaciones.'),
        ('Separación entre articulaciones de hombros', spec['widths']['shoulder_joint_spacing'], 'Distancia entre los dos centros de hombro.'),
        ('Envergadura', spec['arm_span'], f"Con ambos brazos extendidos horizontalmente: {spec['widths']['shoulder_joint_spacing']:g} + 2 × {spec['arm_total']:g}.")
    ]


LANDMARK_LABELS = {
    'crown': 'Parte superior de la cabeza', 'chin': 'Mentón', 'shoulder': 'Hombros',
    'elbow': 'Codos', 'waist': 'Cintura', 'hip': 'Articulación de las caderas',
    'crotch': 'Entrepierna', 'wrist': 'Muñecas', 'fingertips': 'Puntas de los dedos',
    'knee': 'Rodillas', 'ankle': 'Tobillos', 'ground': 'Suelo'
}
