# Bruce civil · Malla base de Hunyuan3D-2mv

Generado el 14 de octubre de 2026 en el Spark de la oficina, con `tencent/Hunyuan3D-2mv` sobre NVIDIA GB10. Solo se procesó a Bruce civil sin guantes.

## Archivos

- [Modelo GLB de 1,80 m](bruce-hunyuan-180cm.glb).
- [Archivo Blender](bruce-hunyuan-180cm.blend).
- [Respuesta original del modelo](bruce-hunyuan-raw.glb), conservada sin modificaciones.
- [Frente](bruce-hunyuan-front-preview.png), [tres cuartos](bruce-hunyuan-three-quarter-preview.png) y [espalda](bruce-hunyuan-back-preview.png).
- [Solicitud y resultados del servicio](generation-request.json).
- [Informe de escala y geometría](model-report.json).

## Generación

Servicio: `http://192.168.40.243:8001/generate`. Se enviaron cuatro PNG independientes, separados del turnaround vigente: frente, perfil izquierdo, espalda y perfil derecho. Las entradas están en [modeling-references/hunyuan3d-2mv](../../modeling-references/hunyuan3d-2mv/inputs.json). Conservan el dibujo original, usan el recorte y la máscara alfa del SVG aprobado y comparten altura y línea de suelo.

Parámetros: 30 pasos, resolución de octree 380, 20.000 chunks y semilla 12345. La inferencia tardó 82,862 segundos; el servicio informó un pico de GPU de 5,684 GB. Identificador: `210b3eff-ac1d-43f2-bd43-610db7ccfb73`.

El formato de vistas corresponde al [uso oficial del modelo](https://huggingface.co/tencent/Hunyuan3D-2mv). La interfaz local devuelve un GLB binario.

## Validación y estado

La malla contiene 160.323 vértices y 320.650 triángulos. Se aplicó una escala uniforme, conservando su geometría relativa, para que la altura total desde las suelas hasta la parte superior de la cabeza sea **1,80 m**, con las suelas en el suelo. El GLB usa Y como eje vertical; Blender usa Z.

Es una **malla base sin texturas, UV ni rig**. Mantiene la ropa, el bolso y la pose de las referencias. Los dedos quedaron fusionados y el rostro es poco definido: requieren refinamiento. La altura total está comprobada; las longitudes de cada extremidad y el ángulo preciso de los brazos no se han validado con un esqueleto. Contrastarlos con las [medidas maestras](../../../../../../bruce-proportions.json) antes de convertirla en un personaje animable.

Las vistas grises son renders de revisión con iluminación neutra; ese material se utiliza únicamente para mostrar la geometría.

## Copia con textura proyectada

- [GLB con textura incluida](bruce-hunyuan-textured-180cm.glb).
- [Blender con textura empaquetada](bruce-hunyuan-textured-180cm.blend).
- [Mapa de color 4096 × 4096](textures/bruce-base-color.png).
- [Frente](bruce-hunyuan-textured-front-preview.png), [tres cuartos](bruce-hunyuan-textured-three-quarter-preview.png) y [espalda](bruce-hunyuan-textured-back-preview.png).
- [Informe de texturizado](texture-report.json).

Método: proyección local de las cuatro vistas aprobadas y horneado UV en Blender. No se cambian los vértices, la pose ni la altura de la malla original. El GLB incluye un material con mapa de color; Blender contiene ese mismo mapa empaquetado. No hay mapas de normales, metalicidad ni rugosidad derivados del dibujo; la rugosidad se mantiene uniforme. El arte contiene sombras pintadas.

La interfaz del Spark expone únicamente la generación de geometría. Hunyuan separa la generación de forma y el [módulo de texturas Hunyuan3D-Paint](https://github.com/Tencent-Hunyuan/Hunyuan3D-2); esta copia no es una inferencia de Paint.

**Borrador de proyección para revisión**, sin rig ni optimización para el juego: aparecen desajustes en manos, uniones y detalles del bolso al combinar vistas. La identidad y los colores se pueden revisar, pero esos detalles requieren retoque antes de usarlo como modelo final. Las limitaciones anatómicas de la malla original siguen vigentes.

Para reproducir el texturizado: ejecutar Blender en segundo plano con `concept-art/scripts/texture_hunyuan_bruce.py` desde la raíz del proyecto.

## Ver los modelos en la galería

[Con textura](../../../../../../index.html#vista=modelos&modelo=bruce-hunyuan-textured-180cm) · [Sin textura](../../../../../../index.html#vista=modelos&modelo=bruce-hunyuan-180cm). El visor permite girar, acercar, elegir una vista y descargar los archivos. Abrir desde el servidor local de la galería.
