# Instrucciones para trabajar en web-arachnid

## Rama de trabajo y commits

- Trabajar siempre directamente en la rama principal `main`.
- No crear otras ramas ni worktrees, salvo que el usuario cambie explícitamente esta instrucción.
- Conservar los cambios locales sin hacer commit. Crear commits solo cuando el usuario lo solicite explícitamente.
- Preservar los cambios existentes del usuario al realizar cualquier trabajo.

## Nombres de carpetas y archivos

Usar nombres en **inglés**, en minúsculas y separados por guiones cuando corresponda. Conservar los nombres convencionales `AGENTS.md` y `README.md`. Los textos de las ideas y los rótulos de la galería pueden permanecer en español. Al mover o renombrar archivos, actualizar catálogo, scripts, documentos y enlaces; conservar las versiones anteriores en `concept-art/assets/archive/`.

## Organización de las variantes de Bruce

Guardar el material vigente en `concept-art/assets/characters/bruce/`, con una carpeta por variante: `civilian`, `civilian-with-gloves`, `homemade-suit`, `standard-suit`, `alien-suit`, `neon-suit`, `rocker-suit` y `comic-suit`. Cada carpeta reúne el arte conceptual PNG, la lámina de medidas SVG y una subcarpeta `modeling-references` con las vistas sin rótulos para crear modelos 3D. Son referencias independientes de la herramienta de modelado; no llamar a esta carpeta `meshy`. El maniquí compartido se guarda en `body-reference`. Mantener el catálogo, los generadores y los enlaces de la galería sincronizados con esta estructura.

## Motor, estilo y plataformas del juego

- El juego se desarrollará en **Unreal Engine**, con un estilo **2.5D**.
- Las plataformas objetivo son **Nintendo Switch, PlayStation 5 y PC**.
- Tener estas tres plataformas en cuenta al proponer controles, interfaz, assets y decisiones de desarrollo. Considerar navegación con mando, legibilidad y rendimiento en cada destino.
- Mantener las proporciones de Bruce al adaptar la calidad visual a cada plataforma.
- Estas son las plataformas previstas; registrar por separado las pruebas realizadas en cada una.

## Proporciones de Bruce: obligatorias en todo el arte

Aplicar estas medidas al crear o editar dibujos, skins, láminas para modelado 3D y modelos de Bruce. Es el mismo personaje y el mismo cuerpo en todas las variantes. Son medidas de diseño del personaje.

Antes de trabajar con Bruce, consultar:

- [Medidas maestras](concept-art/bruce-proportions.json): fuente única de valores, en centímetros.
- [Ficha de proporciones](concept-art/bruce-proportions.md): definiciones de medición y alturas de articulaciones.
- [Maniquí de construcción](concept-art/assets/characters/bruce/body-reference/bruce-proportions-180cm.svg): referencia de dimensiones.
- [Guía de altura](concept-art/assets/characters/bruce/civilian/bruce-scale-180cm.svg): escala compartida de las vistas.
- [Cuatro vistas en pose A](concept-art/assets/characters/bruce/civilian/modeling-references/bruce-without-gloves-a-pose-turnaround.png): identidad, rostro, pelo y ropa.

### Medidas de referencia

| Parte | Longitud |
| --- | --- |
| Altura total, desde las suelas hasta la parte superior de la cabeza de referencia | **180 cm** |
| Cabeza, hasta el mentón | 26 cm |
| Cuello, mentón a línea de articulación de hombros | 8 cm |
| Torso, línea de hombros a línea de caderas | 51 cm |
| Brazo superior, hombro a codo | 32 cm |
| Antebrazo, codo a muñeca | 26 cm |
| Mano, muñeca a punta del dedo medio | 18 cm |
| Brazo completo, hombro a punta del dedo medio | **76 cm** |
| Muslo, cadera a rodilla | 46 cm |
| Rodilla a tobillo | 41 cm |
| Tobillo al suelo, incluyendo pie y calzado | 8 cm |
| Pierna, cadera al suelo | **95 cm** |
| Largo horizontal del pie | 27 cm |
| Envergadura con brazos extendidos | 188 cm |

| Parte | Ancho | Profundidad |
| --- | --- | --- |
| Cabeza, sin volumen lateral del pelo | 17,5 cm | 21 cm |
| Silueta lateral máxima del pelo | 23 cm | — |
| Cuello | 10 cm | — |
| Hombros, ancho exterior | 42 cm | — |
| Separación entre centros de articulación de hombros | 36 cm | — |
| Pecho | 32 cm | 22 cm |
| Cintura | 26 cm | — |
| Caderas | 30 cm | 20 cm |
| Separación entre centros de articulación de caderas | 17 cm | — |
| Brazo superior | 6 cm | — |
| Antebrazo | 5 cm | — |
| Mano | 8,5 cm | — |
| Muslo | 11 cm | — |
| Rodilla a tobillo | 8,5 cm | — |
| Pie | 10 cm | — |

Alturas de control desde el suelo, en reposo: cabeza 180 cm, mentón 154 cm, hombros 146 cm, codos 114 cm, cintura 106 cm, caderas 95 cm, entrepierna 90 cm, muñecas 88 cm, puntas de los dedos 70 cm, rodillas 49 cm y tobillos 8 cm.

### Pose obligatoria del arte para modelado

Todo el arte conceptual de control, los SVG de medidas y las referencias de modelado de las ocho variantes deben usar **pose A: ambos brazos rectos a 45° del torso vertical**, separados lateralmente en el plano frontal. Conservar las longitudes definidas: brazo superior 32 cm, antebrazo 26 cm y mano 18 cm; no cambiar el cuerpo para acomodar la pose. Los codos no se flexionan. Mantener las manos relajadas y los dedos legibles.

Las cotas anteriores de codos, muñecas y dedos describen brazos junto al cuerpo. En pose A, calcular la altura como `146 − longitud acumulada × cos(45°)`: hombros 146 cm, codos **123,37 cm**, muñecas **104,99 cm** y dedos **92,26 cm**. Cabeza, cuello, torso, piernas y altura total de 180 cm conservan sus valores. La separación entre puntas de los dedos es 143,48 cm; los 188 cm de envergadura corresponden a brazos horizontales.

Frente y espalda muestran las diagonales de 45°. Los perfiles muestran esa misma pose con escorzo: no girar los brazos hacia delante para dibujar otra diagonal de 45° en la imagen lateral. Las cotas de longitud del brazo deben seguir sus segmentos diagonales; su caída vertical no es su longitud anatómica. Las escenas narrativas y poses de acción siguen conservando las longitudes del mismo cuerpo.

La suma vertical debe ser **26 + 8 + 51 + 46 + 41 + 8 = 180 cm**. El largo horizontal del pie no se suma a la altura. El brazo completo mide **32 + 26 + 18 = 76 cm**.

### Reglas de creación y revisión

1. Las extremidades se miden entre centros de articulación. Ambos lados del cuerpo conservan las mismas longitudes. Mantener la complexión delgada, las manos y los pies proporcionados y una cabeza de aproximadamente una séptima parte de la altura.
2. El maniquí y las medidas maestras gobiernan las proporciones. Las pequeñas diferencias de dibujo entre imágenes anteriores no definen un cuerpo nuevo. Usar las vistas vigentes de modelado 3D para conservar la identidad de Bruce.
3. Los trajes y los guantes añaden volumen exterior; no cambian longitudes ni posiciones de articulaciones. Mantener el bolso en la cadera izquierda cuando forme parte del diseño. Bruce lleva sus guantes siempre que use un traje.
4. Las vistas de control de frente, perfil y espalda usan cámara ortográfica, escala común y la misma línea de suelo. La marca de **1,80 m corresponde a la parte más alta de la cabeza de referencia**, nunca a los ojos o al cuello. Alinear las suelas con 0 cm. El peinado y el calzado deben respetar el límite total de la referencia.
5. En escenas y poses de acción, conservar las longitudes anatómicas aunque la perspectiva o la flexión cambien la altura aparente. Las vistas superiores e inferiores tienen escorzo y no sirven para redefinir medidas.
6. Al generar una imagen, incluir las medidas pertinentes de la ficha en las instrucciones y adjuntar referencias vigentes. Al editar, pedir explícitamente que se conserven las proporciones y modificar solo lo solicitado por el usuario.
7. Revisar el resultado antes de incorporarlo como arte vigente: altura y alineación en las vistas de control, cabeza, brazos, manos, piernas, pies y coherencia entre vistas. Corregir desviaciones visibles; una cifra escrita en la lámina no demuestra que el dibujo esté bien proporcionado.
8. Las medidas son objetivos de construcción. Una ilustración generada puede tener pequeñas diferencias; no afirmar que tiene dimensiones exactas sin comprobarlas. Para vistas exactamente coincidentes, utilizar un único modelo 3D con estas medidas y cambiar la cámara.

Las láminas de todos los trajes usan el mismo formato de `bruce-scale-180cm.svg`: fondo claro, frente, ambos perfiles, espalda y cotas cian. El catálogo guarda los cuatro recortes de cada PNG en `viewBounds`; comprobarlos al sustituir esas imágenes.

### Si el usuario cambia una medida

Actualizar primero `concept-art/bruce-proportions.json` y comprobar la suma de 180 cm, salvo que el usuario cambie expresamente la altura total. Actualizar este resumen y regenerar las referencias desde la raíz del proyecto:

```sh
python3 concept-art/scripts/build_character_spec.py
python3 concept-art/scripts/build_scale_reference.py
python3 concept-art/scripts/build_suit_scale_references.py
python3 concept-art/scripts/build_gallery_data.py
```

Estos generadores actualizan la ficha, el maniquí, las ideas, la guía de altura, las seis láminas de trajes y los datos de la galería. No reajustan automáticamente las ilustraciones PNG; revisar las imágenes afectadas por separado. Si hay una discrepancia entre esta tabla y el JSON, usar el JSON y corregir la documentación.
