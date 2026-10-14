# Arte conceptual de web-arachnid

Abre [index.html](index.html) en un navegador para explorar la galería. Funciona directamente desde el archivo, sin instalar dependencias ni iniciar un servidor. Incluye búsqueda, filtros por tema y versión, vista ampliada, tamaño real y descarga, comparación de altura de Bruce, ficha de proporciones y lectura de las ideas y ambos README. En la vista ampliada, usa las flechas del teclado para recorrer las imágenes y Esc para cerrar.

## Organización de la carpeta

| Carpeta | Contenido |
| --- | --- |
| [assets/characters/bruce/](assets/characters/bruce/README.md) | Bruce y sus ocho variantes: arte, medidas y referencias de modelado juntos. |
| [assets/menus/](assets/menus/) | Concepto del menú principal del juego. |
| [assets/equipment/](assets/equipment/) | Guantes y habilidades. |
| [assets/environments/](assets/environments/) | Aster City y sus tres capas. |
| [assets/story/](assets/story/) | Origen y desarrollo de los guantes. |
| [assets/archive/](assets/archive/) | Versiones anteriores, separadas por los mismos temas. |
| [prompts/](prompts/) | Instrucciones de generación; las antiguas están en `prompts/archive/`. |
| [scripts/](scripts/) | Herramientas auxiliares y actualización de los datos de la galería. |

`manifest.json` es el catálogo de las 104 imágenes: 38 vigentes y 66 anteriores (84 PNG y 20 SVG). `gallery-data.js` se genera desde ese catálogo para que la página funcione también al abrirla como archivo local. Las ideas y ambos README también se incorporan a los datos de la página. Las medidas maestras se guardan en `bruce-proportions.json`. Después de cambiarlas, ejecutar `python3 scripts/build_character_spec.py` para regenerar ficha, ideas, maniquí y prompt, y luego actualizar la galería. Después de cambiar las referencias para modelado 3D, ejecutar `python3 scripts/build_scale_reference.py` para renovar la guía de altura. Después de cambiar las vistas de los trajes, ejecutar `python3 scripts/build_suit_scale_references.py` para renovar sus seis láminas. Después de cambiar el catálogo o los documentos, ejecutar `python3 scripts/build_gallery_data.py` desde esta carpeta.

Revisión del 14 de octubre de 2026 basada en [ideas.md](../ideas.md). Las imágenes de esta página son las referencias vigentes. Se conserva el arte anterior para comparar la evolución del diseño.

Los nombres de carpetas y archivos están en inglés; los rótulos de la página y los documentos permanecen en español. [file-renames.json](file-renames.json) registra los cambios de rutas.

## Carpetas por variante de Bruce

Cada carpeta incluye el PNG de arte conceptual, un SVG de escala y `modeling-references/` con imágenes para crear el modelo 3D. La denominación no depende de Meshy ni de otra herramienta.

| Variante | Carpeta |
| --- | --- |
| Bruce sin guantes | [assets/characters/bruce/civilian/](assets/characters/bruce/civilian/README.md) |
| Bruce con guantes | [assets/characters/bruce/civilian-with-gloves/](assets/characters/bruce/civilian-with-gloves/README.md) |
| Traje casero | [assets/characters/bruce/homemade-suit/](assets/characters/bruce/homemade-suit/README.md) |
| Traje normal | [assets/characters/bruce/standard-suit/](assets/characters/bruce/standard-suit/README.md) |
| Traje alienígena | [assets/characters/bruce/alien-suit/](assets/characters/bruce/alien-suit/README.md) |
| Traje neón | [assets/characters/bruce/neon-suit/](assets/characters/bruce/neon-suit/README.md) |
| Traje roquero | [assets/characters/bruce/rocker-suit/](assets/characters/bruce/rocker-suit/README.md) |
| Traje cómic | [assets/characters/bruce/comic-suit/](assets/characters/bruce/comic-suit/README.md) |

El maniquí común se guarda en `assets/characters/bruce/body-reference/`. Las ocho variantes tienen un PNG `turnaround` en pose A con las cuatro vistas; el SVG usa esas mismas figuras para comparar la escala.

Las láminas de las ocho variantes se han revisado con pose A de 45° y las proporciones maestras. Las cotas se concentran en los SVG; las láminas anteriores de poses y detalles se conservan en el archivo.

## Bruce para modelado 3D: pose A a 45°

Todas las ocho variantes usan brazos rectos separados lateralmente **45° del torso vertical**. Las longitudes anatómicas se conservan. Los perfiles muestran la misma pose de frente y espalda con escorzo, sin girar los brazos hacia delante.

[Cuatro vistas de Bruce sin guantes](assets/characters/bruce/civilian/modeling-references/bruce-without-gloves-a-pose-turnaround.png) · [SVG de escala](assets/characters/bruce/civilian/bruce-scale-180cm.svg).

La altura sigue siendo **180 cm**. Brazo superior **32 cm**, antebrazo **26 cm**, mano **18 cm**; el brazo completo mide **76 cm**. En pose A, las alturas objetivo son hombros **146 cm**, codos **123,37 cm**, muñecas **104,99 cm** y dedos **92,26 cm**. Se calculan con las mismas longitudes y cos(45°); las cotas de brazos verticales en reposo siguen en la ficha para distinguir ambas poses.

Las ocho referencias son PNG con transparencia y cuatro vistas por archivo. El arte conceptual usa las mismas ilustraciones. Las cotas vectoriales gobiernan la construcción; las ilustraciones generadas se revisan contra ellas y pueden tener pequeñas diferencias.

Las vistas anteriores se conservan en `assets/archive/characters/bruce/` y `assets/archive/modeling-references/`.

## Medidas maestras del cuerpo

La [ficha de proporciones](bruce-proportions.md) define las medidas objetivo de Bruce: brazo superior de 32 cm, antebrazo de 26 cm, mano de 18 cm, muslo de 46 cm y rodilla a tobillo de 41 cm. Incluye anchos y alturas de articulaciones desde el suelo. El torso, cuello, cabeza y piernas suman exactamente 180 cm.

[La lámina de construcción](assets/archive/characters/bruce/body-reference/bruce-proportions-180cm.svg) distingue el maniquí de medidas de la referencia visual. Usar el maniquí para dimensiones y las vistas de modelado 3D para rostro, pelo, ropa e identidad. Las ilustraciones existentes deben comprobarse con estas cotas; para vistas idénticas, generar todas desde un único modelo 3D.

## Láminas de escala de los seis trajes

Cada traje tiene el mismo formato que Bruce: fondo claro, cuatro vistas, suelas alineadas a 0 cm y parte superior de la silueta a 1,80 m. Las líneas cian marcan las alturas objetivo de hombros, codos, caderas, muñecas, dedos y rodillas.

| Traje | Lámina |
| --- | --- |
| Casero | [suit-homemade-scale-180cm.svg](assets/archive/characters/bruce/homemade-suit/suit-homemade-scale-180cm.svg) |
| Normal | [suit-standard-scale-180cm.svg](assets/archive/characters/bruce/standard-suit/suit-standard-scale-180cm.svg) |
| Alienígena | [suit-alien-scale-180cm.svg](assets/archive/characters/bruce/alien-suit/suit-alien-scale-180cm.svg) |
| Neón | [suit-neon-scale-180cm.svg](assets/archive/characters/bruce/neon-suit/suit-neon-scale-180cm.svg) |
| Roquero | [suit-rocker-scale-180cm.svg](assets/archive/characters/bruce/rocker-suit/suit-rocker-scale-180cm.svg) |
| Cómic | [suit-comic-scale-180cm.svg](assets/archive/characters/bruce/comic-suit/suit-comic-scale-180cm.svg) |

[Ver las seis láminas en la galería](index.html#tema=trajes&buscar=medidas). Los PNG `*-a-pose-turnaround.png` contienen las cuatro vistas ilustradas que alimentan estas guías. El SVG normaliza la altura de cada silueta y dibuja las cotas desde `bruce-proportions.json`; no modifica las medidas del cuerpo automáticamente. Las cotas son objetivos de construcción para contrastar el dibujo y el modelo 3D.

Las nuevas vistas se generaron con la herramienta integrada. Los prompts y correcciones están en `prompts/*-a-pose.prompt.txt`. Las láminas de materiales y detalles están en la carpeta de cada traje, junto a su SVG y sus `modeling-references/`.

## Personaje, guantes y skins

| Lámina | Archivo vigente | Qué muestra |
| --- | --- | --- |
| Bruce sin guantes | [bruce-without-gloves-a-pose-concept.png](assets/characters/bruce/civilian/bruce-without-gloves-a-pose-concept.png) | Cuatro vistas en pose A de 45°, manteniendo rostro, ropa y proporciones maestras. |
| Bruce con guantes | [bruce-with-gloves-a-pose-concept.png](assets/characters/bruce/civilian-with-gloves/bruce-with-gloves-a-pose-concept.png) | Cuatro vistas en pose A de 45°, con ropa cotidiana y guantes tecnológicos. |
| Guantes | [assets/equipment/gloves-v2.png](assets/equipment/gloves-v2.png) | Diseño independiente, hilos, escudo, núcleo y nanobots formando una manga. |
| Skin casera | [suit-homemade-a-pose-concept.png](assets/characters/bruce/homemade-suit/suit-homemade-a-pose-concept.png) | Primer traje de ropa vieja, costuras, azul, bufanda y cuello de tela. |
| Skin normal | [suit-standard-a-pose-concept.png](assets/characters/bruce/standard-suit/suit-standard-a-pose-concept.png) | Evolución tecnológica del traje, hilos y formación con nanobots. |
| Skin alienígena | [suit-alien-a-pose-concept.png](assets/characters/bruce/alien-suit/suit-alien-a-pose-concept.png) | Apariencia alienígena adaptada al héroe, con los mismos guantes. |
| Skin neón | [suit-neon-a-pose-concept.png](assets/characters/bruce/neon-suit/suit-neon-a-pose-concept.png) | Pecho limpio, azul oscuro y luces cian y magenta en el contorno del traje. |
| Skin roquera | [suit-rocker-a-pose-concept.png](assets/characters/bruce/rocker-suit/suit-rocker-a-pose-concept.png) | Chaqueta de cuero, tachuelas, bufanda y pelo castaño puntiagudo visible sobre la máscara. |
| Skin cómic | [suit-comic-a-pose-concept.png](assets/characters/bruce/comic-suit/suit-comic-a-pose-concept.png) | Estructura del traje normal con tinta gruesa, sombras negras planas y puntos de impresión pronunciados. |
| Origen | [assets/story/bruce-origin-one-year.png](assets/story/bruce-origin-one-year.png) | Invasión vista desde el taller, un año de desarrollo y guantes terminados. |

Los guantes conservan sus placas claras, articulaciones oscuras y núcleos cian, y destacan con todas las skins. El azul y el contraste del traje casero proceden de las ideas; la bufanda naranja y los detalles violetas de la skin alienígena son propuestas visuales de estas láminas.

![suit-homemade-a-pose-concept.png](assets/characters/bruce/homemade-suit/suit-homemade-a-pose-concept.png)

La skin cómic utiliza el mismo diseño del traje normal: máscara, paneles, azul predominante y zonas oscuras, con tratamiento de tinta y halftone. Sus versiones anteriores se conservan en el archivo. El acabado actual refuerza los contornos, sombras planas, tramas de puntos y líneas de acción.

La skin neón deja el pecho limpio, sin araña ni emblema central. Mantiene el traje oscuro, las luces cian y magenta en hombros, brazos, costados y piernas, y los guantes de Bruce. Las propuestas anteriores se conservan en el archivo.

## Menú principal

[La propuesta del menú](assets/menus/main-menu.png) presenta las tres capas de Aster City, a web-arachnid con su traje normal y las opciones Nueva partida, Continuar, Trajes, Opciones y Salir. La selección usa cian. Es una lámina de interfaz para orientar el diseño del juego.

## Aster City: tres capas verticales

| Lámina | Archivo vigente | Criterio |
| --- | --- | --- |
| Ciudad completa | [assets/environments/aster-city-three-layers.png](assets/environments/aster-city-three-layers.png) | Capas apiladas en vertical: subterránea, intermedia y alienígena. |
| Capa subterránea | [assets/environments/aster-city-under-v2.png](assets/environments/aster-city-under-v2.png) | Barrio pobre con neón bajo un techo de roca y estructuras de soporte. |
| Capa intermedia | [assets/environments/aster-city-rich-v2.png](assets/environments/aster-city-rich-v2.png) | Zona rica, construcciones minimalistas de ladrillo y espacios amplios. |
| Capa alienígena | [assets/environments/aster-city-alien-01-panorama.png](assets/environments/aster-city-alien-01-panorama.png) | Ciudad en el cielo, solo alienígenas, plataformas abiertas y naves. |

![Aster City en tres capas](assets/environments/aster-city-three-layers.png)

## Revisión del material anterior

| Material anterior | Resultado de la revisión |
| --- | --- |
| `assets/archive/characters/bruce-without-gloves-before-proportion-update.png` | Archivado al revisar las proporciones con las vistas v3; usar el estudio nuevo en `civilian/`. |
| `assets/archive/characters/bruce-with-gloves.png`, `assets/archive/equipment/gloves.png` | Sustituidos como referencias vigentes por sus versiones v2, que muestran las nuevas habilidades. |
| `assets/archive/suits/first-suit.png` | Su diseño avanzado sirve de base a `assets/characters/bruce/standard-suit/suit-standard-a-pose-concept.png`. El primer traje ahora es `assets/characters/bruce/homemade-suit/suit-homemade-a-pose-concept.png`. |
| `assets/archive/environments/aster-city-under-01-panorama.png`, `assets/archive/environments/aster-city-under-02-commercial-street.png`, `assets/archive/environments/aster-city-under-03-rooftops-and-metro.png` | Conservados como exploraciones de ambiente y neón. Su cielo abierto no corresponde a la capa subterránea actual. |
| `assets/archive/environments/aster-city-rich-01-panorama.png`, `assets/archive/environments/aster-city-rich-02-square.png`, `assets/archive/environments/aster-city-rich-03-terraces.png` | Conservados como exploraciones anteriores. La referencia vigente usa arquitectura más simple y ladrillo. |
| `assets/archive/environments/aster-city-connection-panorama.png` | Sustituido como referencia geográfica por la vista de tres capas verticales. |
| `assets/archive/modeling-references/bruce-modeling.png` y las cinco vistas anteriores | Las versiones originales, v2 y v3 están archivadas; usar las cuatro vistas vigentes en pose A. |

## Instrucciones de generación

Se utilizó la herramienta integrada de generación y edición de imágenes. Los prompts completos y las correcciones están guardados en [prompts/](prompts/), con el mismo nombre base que cada lámina. [manifest.json](manifest.json) relaciona archivos, referencias y prompts.

Las láminas de personaje, skins y origen conservan la identidad de Bruce. Las vistas vigentes en pose A son ahora la referencia para revisar las longitudes de brazos y piernas de nuevas ilustraciones. La altura total de Bruce es 1,80 m, desde las suelas hasta la parte superior de la cabeza. Las versiones previas a esta unificación se conservan en `assets/archive/`.

Estas láminas desarrollan visualmente las ideas existentes; los detalles de formas y materiales que todavía no están definidos en `ideas.md` se mantienen como propuestas de diseño.


## Primera malla de Bruce generada con Hunyuan3D-2mv

[Modelo GLB de 1,80 m](assets/characters/bruce/civilian/models/hunyuan3d-2mv/bruce-hunyuan-180cm.glb) · [Archivo Blender](assets/characters/bruce/civilian/models/hunyuan3d-2mv/bruce-hunyuan-180cm.blend) · [Informe de generación](assets/characters/bruce/civilian/models/hunyuan3d-2mv/README.md). Se generó en el Spark de la oficina a partir de las cuatro vistas civiles en pose A. Es una malla base sin texturas ni rig; rostro y dedos requieren refinamiento. Las vistas de revisión están en la categoría Modelado 3D e incluyen enlaces al modelo.

## Bruce con textura de color · Borrador

[Modelo GLB texturizado](assets/characters/bruce/civilian/models/hunyuan3d-2mv/bruce-hunyuan-textured-180cm.glb) · [Archivo Blender](assets/characters/bruce/civilian/models/hunyuan3d-2mv/bruce-hunyuan-textured-180cm.blend). Conserva la misma malla y altura de 1,80 m. El mapa de color de 4096 × 4096 se obtuvo en Blender proyectando las cuatro vistas aprobadas; queda incluido en el GLB y en el archivo Blender. Es un borrador para revisar: las uniones laterales, las manos y el bolso necesitan retoque. La API actual del Spark solo genera geometría; esta textura no procede de Hunyuan3D-Paint. Las tres vistas y las descargas están en Modelado 3D.

## Visor interactivo de modelos 3D

En [Modelos 3D](index.html#vista=modelos) se pueden girar y acercar las dos mallas de Bruce civil, con y sin textura. El selector cambia de modelo; los botones muestran frente, perfiles y espalda, restablecen la vista y activan el giro automático. Las imágenes vinculadas a una malla incluyen «Ver modelo en 3D». También se pueden descargar el GLB y el archivo Blender y consultar su carpeta.

Los archivos se conservan en `assets/characters/bruce/civilian/models/hunyuan3d-2mv/`; el visor no modifica su geometría. El renderizador [model-viewer](https://modelviewer.dev/) 4.4.0 está guardado localmente en `vendor/model-viewer/`, con su licencia. Se carga únicamente al abrir un modelo. Para el visor 3D, abrir la galería mediante el servidor local (`http://127.0.0.1:8765/`), ya que los navegadores restringen la carga de modelos desde `file://`.
