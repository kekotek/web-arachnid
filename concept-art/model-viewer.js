/* Local GLB viewer. Load the vendored renderer only when a model is opened. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  let renderer, element, current, revision = 0;
  function status(text, busy = false, failed = false) {
    $('model-status').textContent = text;
    $('model-loading').hidden = !busy && !failed;
    $('model-progress').hidden = !busy;
    $('model-retry').hidden = !failed;
  }
  function hide() {
    revision++;
    if (element) element.removeAttribute('src');
    $('model-stage').replaceChildren();
    element = null;
    current = null;
    $('model-rotate').setAttribute('aria-pressed', 'false');
  }
  async function show(model, retry = false) {
    if (current?.file === model.file && !retry) return;
    hide();
    current = model;
    const request = revision;
    $('model-progress').value = 0;
    status('Cargando modelo 3D…', true);
    try {
      renderer ||= import('./vendor/model-viewer/model-viewer.min.js').catch(error => {
        renderer = null;
        throw error;
      });
      await renderer;
      if (revision !== request) return;
      const view = document.createElement('model-viewer');
      element = view;
      view.setAttribute('alt', model.title + '. Modelo 3D interactivo de Bruce.');
      view.setAttribute('camera-controls', '');
      view.setAttribute('camera-orbit', '0deg 90deg 105%');
      view.setAttribute('camera-target', 'auto auto auto');
      view.setAttribute('touch-action', 'pan-y');
      view.setAttribute('interaction-prompt', 'none');
      view.setAttribute('a11y', JSON.stringify({'front':'frente','back':'espalda','left':'izquierda','right':'derecha',
        'interaction-prompt':'. Usa el ratón, la pantalla táctil o las flechas para girar.'}));
      view.setAttribute('shadow-intensity', '.5');
      view.setAttribute('environment-image', 'neutral');
      view.setAttribute('exposure', '1');
      view.setAttribute('loading', 'eager');
      view.addEventListener('progress', event => {
        if (revision === request) $('model-progress').value = event.detail.totalProgress;
      });
      view.addEventListener('load', () => {
        if (revision === request) status('Modelo listo. Arrastra para girarlo.');
      });
      view.addEventListener('error', () => {
        if (revision === request) status('No se pudo abrir el modelo. Puedes descargarlo o volver a intentar.', false, true);
      });
      $('model-stage').append(view);
      view.setAttribute('src', model.file);
    } catch {
      if (revision === request) status(location.protocol === 'file:'
        ? 'Abre la galería en el servidor local para usar el visor 3D. Las descargas siguen disponibles.'
        : 'No se pudo iniciar el visor 3D. Puedes descargar el modelo o volver a intentar.', false, true);
    }
  }
  function camera(orbit) {
    if (!element) return;
    element.removeAttribute('auto-rotate');
    element.resetTurntableRotation();
    $('model-rotate').setAttribute('aria-pressed', 'false');
    // Removing first also resets an unchanged preset after a manual drag.
    element.removeAttribute('camera-target');
    element.removeAttribute('camera-orbit');
    element.removeAttribute('field-of-view');
    element.setAttribute('camera-target', 'auto auto auto');
    element.setAttribute('camera-orbit', orbit);
    element.setAttribute('field-of-view', 'auto');
    element.jumpCameraToGoal();
  }
  document.querySelectorAll('[data-orbit]').forEach(button => button.addEventListener('click', () => camera(button.dataset.orbit)));
  $('model-reset').addEventListener('click', () => camera('0deg 90deg 105%'));
  $('model-rotate').addEventListener('click', () => {
    if (!element) return;
    const active = element.toggleAttribute('auto-rotate');
    $('model-rotate').setAttribute('aria-pressed', String(active));
  });
  $('model-retry').addEventListener('click', () => {if (current) show(current, true);});
  window.WebArachnidModels = {show, hide};
})();
