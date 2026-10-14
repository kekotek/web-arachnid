(() => {
  'use strict';
  const catalog = window.WEB_ARACHNID_ART;
  if (!catalog || !Array.isArray(catalog.assets)) return;
  const labels = {todas:'Todo el arte',personajes:'Personajes',trajes:'Trajes',menus:'Menús',equipo:'Equipo',escenarios:'Aster City',historia:'Historia',modeling:'Modelado 3D'};
  const order = ['suit-homemade-scale-180cm','suit-standard-scale-180cm','suit-alien-scale-180cm','suit-neon-scale-180cm','suit-rocker-scale-180cm','suit-comic-scale-180cm','main-menu','suit-neon','suit-rocker','suit-comic','aster-city-three-layers','suit-homemade','bruce-proportions-180cm','bruce-scale-180cm','bruce-a-pose-turnaround','bruce-without-gloves-v2','bruce-with-gloves-v3','bruce-with-gloves-scale-180cm','bruce-with-gloves-turnaround','gloves-v2','suit-standard','suit-alien','aster-city-under-v2','aster-city-rich-v2','aster-city-alien-01-panorama','bruce-origin-one-year','bruce-modeling-left-v3','bruce-modeling-right-v3','bruce-modeling-back-v3','bruce-for-meshy-top-v2','bruce-for-meshy-bottom-v2'];
  const assets = [...catalog.assets].sort((a,b) => {
    const rank = id => order.includes(id) ? order.indexOf(id) : 100;
    return rank(a.id)-rank(b.id) || a.title.localeCompare(b.title,'es');
  });
  const $ = id => document.getElementById(id);
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  const models = [...new Map(assets.filter(asset => asset.modelFile && asset.status === 'vigente').map(asset => [asset.modelFile, {
    id: asset.modelFile.split('/').pop().replace(/\.glb$/i,''), file: asset.modelFile,
    blender: asset.blenderFile,
    title: asset.modelStatus === 'texture-projection-draft' ? 'Bruce civil · Con textura' : 'Bruce civil · Sin textura',
    description: asset.modelStatus === 'texture-projection-draft'
      ? 'Textura de color 4K proyectada desde el arte aprobado. Conserva la malla de 1,80 m. Las manos, el bolso y las uniones de la textura necesitan retoques.'
      : 'Malla base generada con Hunyuan3D-2mv y ajustada a 1,80 m. Sin textura ni esqueleto. El rostro, los dedos y las proporciones anatómicas necesitan revisión.',
    textured: asset.modelStatus === 'texture-projection-draft'
  }])).values()].sort((a,b) => Number(b.textured)-Number(a.textured));
  const state = {view:'arte',status:'vigente',category:'todas',query:'',model:models[0]?.id || ''};
  let visible = [], viewerItems = [], viewerIndex = 0, zoomed = false;
  const viewer = $('viewer');
  const total = status => assets.filter(asset => asset.status === status).length;
  $('current-count').textContent = total('vigente');
  $('archive-count').textContent = total('archivo');
  $('catalog-summary').textContent = `${assets.length} imágenes · ${total('vigente')} vigentes · ${total('archivo')} anteriores`;
  const matches = (asset, includeCategory = true) =>
    (state.status === 'todas' || asset.status === state.status) &&
    (!includeCategory || state.category === 'todas' || asset.category === state.category) &&
    normalize(`${asset.title} ${asset.description} ${labels[asset.category]} ${asset.file}`).includes(normalize(state.query.trim()));

  function make(tag, className, text) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text != null) element.textContent = text;
    return element;
  }
  function readLocation() {
    const params = new URLSearchParams(location.hash.slice(1));
    state.view = ['arte','modelos','ideas','proporciones','juego','guia'].includes(params.get('vista')) ? params.get('vista') : 'arte';
    state.model = models.some(model => model.id === params.get('modelo')) ? params.get('modelo') : models[0]?.id || '';
    state.status = ['vigente','archivo','todas'].includes(params.get('version')) ? params.get('version') : 'vigente';
    const category = params.get('tema') === 'meshy' ? 'modeling' : params.get('tema');
    state.category = Object.hasOwn(labels,category) ? category : 'todas';
    state.query = params.get('buscar') || '';
    $('search').value = state.query;
  }
  function saveLocation() {
    const params = new URLSearchParams();
    if (state.view !== 'arte') params.set('vista',state.view);
    if (state.view === 'modelos' && state.model) params.set('modelo',state.model);
    if (state.status !== 'vigente') params.set('version',state.status);
    if (state.category !== 'todas') params.set('tema',state.category);
    if (state.query) params.set('buscar',state.query);
    try {history.replaceState(null,'',`${location.pathname}${location.search}${params.size ? '#'+params : ''}`);} catch { /* Some file browsers restrict history updates. */ }
  }
  function render() {
    renderView();
    document.querySelectorAll('[data-status]').forEach(button => button.setAttribute('aria-pressed',String(button.dataset.status === state.status)));
    for (const button of $('categories').children) {
      button.setAttribute('aria-pressed',String(button.dataset.category === state.category));
      const count = assets.filter(asset => matches(asset,false) && (button.dataset.category === 'todas' || asset.category === button.dataset.category)).length;
      button.querySelector('span').textContent = count;
    }
    visible = assets.filter(asset => matches(asset));
    const grid = $('art-grid');
    grid.replaceChildren();
    visible.forEach((asset,index) => {
      const card = make('article','art-card');
      const button = make('button');
      button.type = 'button'; button.setAttribute('aria-label',`Ampliar ${asset.title}`);
      const frame = make('span',`card-image${asset.transparent ? ' transparent' : ''}${asset.category === 'escenarios' ? ' environment' : ''}`);
      const img = make('img'); img.src = asset.file; img.alt = asset.title; img.loading = 'lazy'; img.decoding = 'async'; img.width = asset.width; img.height = asset.height;
      frame.append(img);
      if (asset.status === 'archivo') frame.append(make('span','card-tag','VERSIÓN ANTERIOR'));
      const icon = make('span','card-open','↗'); icon.setAttribute('aria-hidden','true'); frame.append(icon);
      const info = make('span','card-info');
      const text = make('span'); text.append(make('h3',null,asset.title),make('p',null,labels[asset.category]));
      info.append(text,make('span','card-index',String(index+1).padStart(2,'0')));
      button.append(frame,info); button.addEventListener('click',() => openViewer(visible,index)); card.append(button); grid.append(card);
    });
    $('results-count').textContent = `${visible.length} ${visible.length === 1 ? 'imagen' : 'imágenes'}${state.category !== 'todas' ? ' / '+labels[state.category] : ''}`;
    $('empty').hidden = visible.length > 0;
    $('results-note').textContent = state.status === 'archivo' ? 'Exploraciones anteriores conservadas para comparar.' : 'Haz clic en una imagen para ampliarla.';
  }
  for (const [category,label] of Object.entries(labels)) {
    const button = make('button',null,label); button.type = 'button'; button.dataset.category = category; button.setAttribute('aria-pressed',String(category === 'todas')); button.append(make('span',null,'0'));
    button.addEventListener('click',() => {state.category = category;render();saveLocation();}); $('categories').append(button);
  }
  document.querySelectorAll('[data-status]').forEach(button => button.addEventListener('click',() => {state.status = button.dataset.status;render();saveLocation();}));
  $('search').addEventListener('input',event => {state.query = event.target.value;render();saveLocation();});
  $('reset').addEventListener('click',() => {Object.assign(state,{status:'vigente',category:'todas',query:''});$('search').value='';render();saveLocation();$('search').focus();});
  function setZoom(value) {
    zoomed = value; $('image-stage').classList.toggle('is-zoomed',zoomed); $('zoom').setAttribute('aria-pressed',String(zoomed)); $('zoom').textContent = zoomed ? 'Ajustar imagen' : 'Tamaño real'; $('image-stage').scrollTo(0,0);
  }
  function showImage() {
    const asset = viewerItems[viewerIndex];
    setZoom(false);
    $('viewer-image').src = asset.file; $('viewer-image').alt = asset.title;
    $('image-stage').classList.toggle('transparent',asset.transparent);
    $('viewer-title').textContent = asset.title; $('viewer-description').textContent = asset.description;
    $('viewer-category').textContent = `WEB-ARACHNID / ${labels[asset.category].toUpperCase()}`;
    $('viewer-state').textContent = asset.status === 'archivo' ? 'VERSIÓN ANTERIOR' : 'ARTE VIGENTE'; $('viewer-state').classList.toggle('archived',asset.status === 'archivo');
    $('viewer-resolution').textContent = `${asset.width} × ${asset.height}`; $('viewer-format').textContent = asset.transparent ? 'PNG · Transparente' : asset.format;
    $('download').href = asset.file; $('download').download = asset.file.split('/').pop(); $('original').href = asset.file;
    for (const [id,key] of [['download-model','modelFile'],['download-blender','blenderFile']]) {
      const link = $(id); link.hidden = !asset[key];
      if (asset[key]) {link.href = asset[key];link.download = asset[key].split('/').pop();}
      else link.removeAttribute('href');
    }
    $('view-model').hidden = !asset.modelFile;
    if (asset.modelFile) $('view-model').href = '#vista=modelos&modelo='+encodeURIComponent(models.find(model => model.file === asset.modelFile).id);
    $('viewer-position').textContent = `${String(viewerIndex+1).padStart(2,'0')} / ${String(viewerItems.length).padStart(2,'0')}`;
    $('previous').disabled = viewerItems.length < 2; $('next').disabled = viewerItems.length < 2;
  }
  function openViewer(items,index) {
    viewerItems = [...items]; viewerIndex = index; showImage();
    viewer.showModal(); document.body.classList.add('no-scroll'); $('close').focus();
  }
  function step(direction) {viewerIndex = (viewerIndex+direction+viewerItems.length)%viewerItems.length;showImage();}
  $('hero-art').addEventListener('click',() => {const items = assets.filter(asset => asset.status === 'vigente' && asset.category === 'escenarios');openViewer(items,items.findIndex(asset => asset.id === 'aster-city-three-layers'));});
  $('close').addEventListener('click',() => viewer.close());
  $('view-model').addEventListener('click',event => {
    event.preventDefault();
    const model = models.find(model => model.file === viewerItems[viewerIndex].modelFile);
    if (!model) return;
    viewer.close();state.view='modelos';state.model=model.id;render();saveLocation();
    $('models-panel').scrollIntoView({behavior:'smooth'});$('model-select').focus();
  });
  viewer.addEventListener('close',() => {document.body.classList.remove('no-scroll');setZoom(false);});
  viewer.addEventListener('click',event => {if (event.target === viewer) {const rect = viewer.getBoundingClientRect();if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) viewer.close();}});
  $('previous').addEventListener('click',() => step(-1)); $('next').addEventListener('click',() => step(1)); $('zoom').addEventListener('click',() => setZoom(!zoomed));
  viewer.addEventListener('keydown',event => {if (event.key === 'ArrowRight') {event.preventDefault();step(1);} if (event.key === 'ArrowLeft') {event.preventDefault();step(-1);}});
  window.addEventListener('hashchange',() => {if (location.hash === '#gallery') return;readLocation();render();});
  function renderView() {
    const modeling = state.view === 'modelos';
    const reading = state.view !== 'arte' && !modeling;
    $('art-panel').hidden = state.view !== 'arte'; $('document-panel').hidden = !reading;
    $('models-panel').hidden = !modeling;
    document.querySelectorAll('[data-view]').forEach(link => {
      if (link.dataset.view === state.view) link.setAttribute('aria-current','page'); else link.removeAttribute('aria-current');
    });
    if (modeling) {
      const model = models.find(model => model.id === state.model) || models[0];
      if (!model) {$('model-status').textContent='Todavía no hay modelos 3D disponibles.';return;}
      $('model-select').value=model.id;
      $('model-title').textContent=model.title;$('model-description').textContent=model.description;
      $('model-glb-download').href=model.file;$('model-glb-download').download=model.file.split('/').pop();
      $('model-blend-download').hidden=!model.blender;
      if (model.blender) {$('model-blend-download').href=model.blender;$('model-blend-download').download=model.blender.split('/').pop();}
      $('model-folder').textContent='concept-art/'+model.file.slice(0,model.file.lastIndexOf('/')+1);
      window.WebArachnidModels.show(model);
      return;
    }
    window.WebArachnidModels.hide();
    if (!reading) return;
    const doc = catalog.documents[state.view];
    const kickers = {ideas:'CUADERNO DE IDEAS',proporciones:'PROPORCIONES MAESTRAS · BRUCE',juego:'SOBRE EL JUEGO',guia:'GUÍA DEL ARCHIVO VISUAL'};
    $('document-kicker').textContent = kickers[state.view];
    // HTML is generated from escaped local Markdown by build_gallery_data.py.
    $('document-content').innerHTML = doc.html;
    $('document-outline').replaceChildren();
    doc.outline.filter(heading => heading.level === 2).forEach(heading => {
      const link = make('a',null,heading.title); link.href = '#'+heading.id;
      link.addEventListener('click',event => {event.preventDefault();document.getElementById(heading.id).scrollIntoView({behavior:'smooth'});});
      $('document-outline').append(link);
    });
  }
  document.querySelectorAll('[data-view]').forEach(link => link.addEventListener('click',event => {
    event.preventDefault();state.view = link.dataset.view;render();saveLocation();window.scrollTo({top:0,behavior:'smooth'});
  }));
  for (const model of models) {
    const option=make('option',null,model.title);option.value=model.id;$('model-select').append(option);
  }
  $('model-select').addEventListener('change',event => {state.model=event.target.value;render();saveLocation();});
  document.querySelector('.skip-link').addEventListener('click',event => {
    event.preventDefault(); const target = $(state.view === 'arte' ? 'gallery' : state.view === 'modelos' ? 'models-panel' : 'document-content');
    target.focus(); target.scrollIntoView({behavior:'smooth'});
  });
  const scaleSource = assets.find(asset => asset.id === 'bruce-a-pose-turnaround');
  const scaleNames = ['FRENTE','PERFIL IZQUIERDO','PERFIL DERECHO','ESPALDA'];
  const bodyHeight = 480, topMargin = 25, characterHeight = catalog.characterSpec.height;
  const canvas = $('scale-canvas');
  const views = make('div','scale-views');
  scaleSource.viewBounds.forEach((bounds,index) => {
    const asset = scaleSource;
    const [left,top,right,bottom] = bounds;
    const width = right-left, height = bottom-top;
    const figure = make('div','scale-figure');
    const box = make('div','scale-image-box');
    box.style.width = `${bodyHeight * width / height}px`;
    const img = make('img'); img.src = asset.file; img.alt = `${scaleNames[index]} de Bruce, alineado a 1,80 metros`;
    img.style.width = `${asset.width/width*100}%`;img.style.height = `${asset.height/height*100}%`;
    img.style.left = `${-left/width*100}%`;img.style.top = `${-top/height*100}%`;
    box.append(img);figure.append(box,make('span','scale-view-name',scaleNames[index]));views.append(figure);
  });
  canvas.append(views);
  for (let centimeters = 0; centimeters <= 180; centimeters += 10) {
    const line = make('div',`scale-line${centimeters % 30 === 0 ? ' major' : ''}`);
    line.style.top = `${topMargin + bodyHeight * (1-centimeters/characterHeight)}px`;
    if (centimeters % 30 === 0) line.append(make('span',null,centimeters === 180 ? '1,80 m' : `${centimeters} cm`));
    canvas.append(line);
  }
  $('scale-toggle').addEventListener('click',() => {
    const open = $('scale-board').hidden; $('scale-board').hidden = !open;
    $('scale-toggle').setAttribute('aria-expanded',String(open));$('scale-toggle').textContent = open ? 'Ocultar comparación' : 'Comparar las vistas ↗';
  });
  for (const [key,label] of [['shoulder','Hombros'],['elbow','Codos'],['hip','Caderas'],['wrist','Muñecas'],['fingertips','Dedos'],['knee','Rodillas']]) {
    const centimeters = catalog.characterSpec.modeling_landmarks[key];
    const line = make('div','scale-line joint');
    line.style.top = `${topMargin + bodyHeight * (1-centimeters/characterHeight)}px`;
    line.append(make('span',null,`${Number(centimeters.toFixed(2)).toLocaleString('es')} · ${label}`));
    if (key === 'hip') line.classList.add('hip-target');
    if (key === 'fingertips') line.classList.add('finger-target');
    canvas.append(line);
  }
  readLocation(); render();
})();
