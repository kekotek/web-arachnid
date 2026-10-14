# Bruce sin guantes · Pose A 45°

Pose ortográfica para modelado: los brazos se separan lateralmente **45° del torso**, sin doblar los codos. Frente y espalda muestran las diagonales; los perfiles muestran la misma pose con escorzo.

## Archivos vigentes

- [Arte conceptual](bruce-without-gloves-a-pose-concept.png): cuatro vistas en pose A.
- [Referencias para modelado 3D](modeling-references/bruce-without-gloves-a-pose-turnaround.png): el mismo conjunto sin rótulos, sobre fondo transparente.
- [Escala y proporciones](bruce-scale-180cm.svg): SVG con altura total y alturas objetivo de articulaciones.

Los dos PNG usan las mismas ilustraciones para conservar la correspondencia entre concepto y referencia de modelado. `turnaround` reúne frente, ambos perfiles y espalda en un mismo archivo.

## Medidas compartidas

Altura total: **180 cm**. Brazo superior: **32 cm**, antebrazo: **26 cm**, mano: **18 cm**. Muslo: **46 cm**, rodilla a tobillo: **41 cm**, tobillo al suelo: **8 cm**. Los anchos y profundidades se conservan.

Las alturas objetivo del brazo en esta pose son: hombros **146 cm**, codos **123,37 cm**, muñecas **104,99 cm** y dedos **92,26 cm**. Se calculan como altura del hombro menos longitud acumulada por cos(45°). Las cotas de reposo con brazos verticales permanecen documentadas en la ficha, pero no se aplican a estas láminas.

Consultar las [medidas maestras](../../../../bruce-proportions.json), la [ficha](../../../../bruce-proportions.md) y el [maniquí vectorial](../body-reference/bruce-proportions-180cm.svg). Las medidas y el ángulo del maniquí son exactos; las ilustraciones se contrastan con esa geometría.

## Instrucciones de generación

Creado con la herramienta integrada de edición de imágenes. [Prompt completo](../../../../prompts/bruce-without-gloves-a-pose.prompt.txt). Las versiones previas se conservan en `assets/archive/characters/bruce/`.

## Modelo 3D generado en el Spark

[Modelo GLB de 1,80 m](models/hunyuan3d-2mv/bruce-hunyuan-180cm.glb) · [Archivo Blender](models/hunyuan3d-2mv/bruce-hunyuan-180cm.blend) · [Informe](models/hunyuan3d-2mv/README.md). Malla base sin texturas ni rig. La altura total está comprobada; el rostro, los dedos y las medidas anatómicas todavía requieren revisión de modelado.

## Copia con textura · Borrador

[GLB texturizado](models/hunyuan3d-2mv/bruce-hunyuan-textured-180cm.glb) · [Blender texturizado](models/hunyuan3d-2mv/bruce-hunyuan-textured-180cm.blend). Misma geometría y altura; mapa de color 4K proyectado localmente desde las cuatro vistas. Requiere retoques en uniones, manos y bolso. Se conserva la versión sin textura.
