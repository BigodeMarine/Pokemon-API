'use strict';
const $ = (id) => document.getElementById(id);
const state = {items: [], selected: null, offset: 0, total: 0, back: false, loading: false, mode: null};
const limit = 8;
const typeNames = {normal:'Normal',fire:'Fogo',water:'Água',electric:'Elétrico',grass:'Planta',ice:'Gelo',fighting:'Lutador',poison:'Veneno',ground:'Terra',flying:'Voador',psychic:'Psíquico',bug:'Inseto',rock:'Pedra',ghost:'Fantasma',dragon:'Dragão',dark:'Sombrio',steel:'Aço',fairy:'Fada'};
function message(text, error = false) { $('status').textContent = text; $('status').classList.toggle('error', error); }
async function request(path, options) {
  const response = await fetch(path, options);
  const body = response.status === 204 ? null : await response.json();
  if (!response.ok) {
    const error = new Error(response.status === 404 ? 'Pokémon não encontrado. Confira o nome oficial e tente novamente.' : response.status === 503 ? 'Não foi possível acessar a PokeAPI. Tente novamente em instantes.' : typeof body.detail === 'string' ? body.detail : 'Confira o nome ou o número informado.');
    error.status = response.status;
    throw error;
  }
  return body;
}
function number(id) { return '#' + String(id).padStart(3, '0'); }
function sprite(pokemon, back = false) {
  const url = pokemon.sprites?.[back ? 'back_default' : 'front_default'];
  if (!url) return null;
  try { const parsed = new URL(url); return parsed.protocol === 'https:' ? parsed.href : null; } catch { return null; }
}
function picture(pokemon, back = false) {
  const image = document.createElement('img');
  image.alt = `${pokemon.name} · vista ${back ? 'traseira' : 'frontal'}`;
  const url = sprite(pokemon, back);
  if (!url) { const fallback = document.createElement('p'); fallback.textContent = 'Imagem indisponível'; return fallback; }
  image.src = url;
  image.addEventListener('error', () => { const fallback = document.createElement('p'); fallback.textContent = 'Imagem indisponível'; image.replaceWith(fallback); }, {once:true});
  return image;
}
function types(pokemon) {
  return pokemon.types.map(type => { const badge = document.createElement('span'); badge.className = 'type'; badge.textContent = typeNames[type] || type; return badge; });
}
function renderSelected(pokemon) {
  state.selected = pokemon;
  state.back = false;
  $('portrait').replaceChildren(picture(pokemon));
  $('dex-number').textContent = number(pokemon.pokemon_id);
  $('screen-name').textContent = pokemon.name.toUpperCase();
  $('pokemon-title').textContent = pokemon.name;
  $('types').replaceChildren(...types(pokemon));
  $('info-copy').textContent = 'Encontro registrado! Use o botão circular para alternar a imagem e os controles para explorar sua coleção.';
  $('height').textContent = `${(pokemon.height / 10).toLocaleString('pt-BR')} m`;
  $('weight').textContent = `${(pokemon.weight / 10).toLocaleString('pt-BR')} kg`;
  $('national-id').textContent = number(pokemon.pokemon_id);
  renderCards();
  updateControls();
}
function renderCards() {
  if (!state.items.length) {
    const empty = document.createElement('div'); empty.className = 'collection-empty';
    empty.textContent = state.total ? 'Nenhum Pokémon nesta página.' : 'Sua aventura começa com o primeiro Pokémon. Pesquise um nome acima para registrá-lo.';
    $('collection-grid').replaceChildren(empty); return;
  }
  $('collection-grid').replaceChildren(...state.items.map(pokemon => {
    const card = document.createElement('button'); card.type = 'button';
    card.className = 'collection-card' + (state.selected?.id === pokemon.id ? ' selected' : '');
    card.setAttribute('aria-label', `Consultar ${pokemon.name}`);
    card.setAttribute('aria-pressed', String(state.selected?.id === pokemon.id));
    const label = document.createElement('span'); label.className = 'card-number'; label.textContent = number(pokemon.pokemon_id);
    const art = document.createElement('div'); art.className = 'card-picture'; art.append(picture(pokemon));
    const title = document.createElement('h3'); title.textContent = pokemon.name;
    const badges = document.createElement('div'); badges.className = 'types'; badges.append(...types(pokemon));
    card.append(label, art, title, badges);
    card.addEventListener('click', () => select(pokemon.id)); return card;
  }));
}
function updateControls() {
  const index = state.items.findIndex(p => p.id === state.selected?.id);
  $('previous').disabled = index <= 0 || state.loading;
  $('next').disabled = index < 0 || index >= state.items.length - 1 || state.loading;
  $('flip').disabled = !state.selected || !sprite(state.selected, true);
  $('page-prev').disabled = state.offset === 0 || state.loading;
  $('page-next').disabled = state.offset + limit >= state.total || state.loading;
  const locked = state.loading || state.mode !== null;
  for (const id of ['edit-pokemon', 'delete-pokemon']) $(id).disabled = !state.selected || locked;
  for (const id of ['search-button', 'refresh', 'page-prev', 'page-next', 'previous', 'next']) {
    if (locked) $(id).disabled = true;
  }
  $('refresh').disabled = locked;
  $('search-button').disabled = locked;
  $('pokemon-name').disabled = locked;
  for (const id of ['save-pokemon', 'cancel-edit', 'confirm-delete', 'cancel-delete', 'edit-name', 'edit-height', 'edit-weight']) $(id).disabled = state.loading;
  document.querySelector('.device').classList.toggle('is-busy', state.loading);
  document.querySelector('.info-screen').setAttribute('aria-busy', String(state.loading));
  for (const card of document.querySelectorAll('.collection-card')) card.disabled = locked;
  $('page-label').textContent = `Página ${Math.floor(state.offset / limit) + 1}`;
}
async function loadCollection(offset = state.offset) {
  const result = await request(`/pokemons?limit=${limit}&offset=${offset}`);
  state.items = result.data; state.total = result.pagination.total; state.offset = offset;
  $('total').textContent = state.total;
  $('collection-count').textContent = String(state.total).padStart(2, '0');
  renderCards(); updateControls();
}
async function select(id) {
  if (state.loading || state.mode) return;
  state.loading = true; updateControls();
  try { renderSelected(await request(`/pokemons/${id}`)); message('Dados recuperados da sua coleção.'); }
  catch (error) { message(error.message || 'Não foi possível consultar o Pokémon.', true); }
  finally { state.loading = false; updateControls(); }
}
$('search-form').addEventListener('submit', async event => {
  event.preventDefault(); if (state.loading || state.mode) return;
  const value = $('pokemon-name').value.trim().toLowerCase();
  if (!/^[a-z0-9-]+$/.test(value) || (/^\d+$/.test(value) && (!Number.isSafeInteger(Number(value)) || Number(value) < 1))) {
    message('Digite um nome oficial, como pikachu, ou um número maior que zero.', true); return;
  }
  state.loading = true; $('search-button').disabled = true; $('search-button').textContent = 'Buscando…'; updateControls();
  message('Consultando a PokeAPI e registrando seu encontro…');
  try {
    let pokemon;
    try { pokemon = await request('/pokemons', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(/^\d+$/.test(value) ? {pokemon_id:Number(value)} : {name:value})}); }
    catch (error) {
      if (error.status !== 409) throw error;
      // Find the already registered entry without creating duplicates.
      let offset = 0;
      while (true) {
        const page = await request(`/pokemons?limit=100&offset=${offset}`);
        pokemon = page.data.find(p => p.name === value || String(p.pokemon_id) === String(Number(value)));
        if (pokemon || !page.pagination.next) break;
        offset += 100;
      }
      if (!pokemon) { await loadCollection(0); message('Este Pokémon já está registrado. Consulte sua coleção.'); return; }
    }
    await loadCollection(0);
    renderSelected(await request(`/pokemons/${pokemon.id}`));
    message(`${pokemon.name.charAt(0).toUpperCase() + pokemon.name.slice(1)} está na sua Pokédex!`);
  } catch (error) { message(error.message || 'Falha de conexão. Tente novamente.', true); }
  finally { state.loading = false; $('search-button').disabled = false; $('search-button').textContent = 'Registrar'; updateControls(); }
});
$('flip').addEventListener('click', () => { if (!state.selected) return; state.back = !state.back; $('portrait').replaceChildren(picture(state.selected, state.back)); });
for (const [id, delta] of [['previous', -1], ['next', 1]]) $(id).addEventListener('click', () => { const index = state.items.findIndex(p => p.id === state.selected?.id); const pokemon = state.items[index + delta]; if (pokemon) select(pokemon.id); });
async function refresh(offset) {
  if (state.loading || state.mode) return;
  state.loading = true; updateControls();
  try { await loadCollection(offset); message('Coleção atualizada.'); }
  catch { message('Não foi possível carregar a coleção. Tente atualizar novamente.', true); }
  finally { state.loading = false; updateControls(); }
}
$('refresh').addEventListener('click', () => refresh(state.offset));
$('page-prev').addEventListener('click', () => refresh(Math.max(0, state.offset - limit)));
$('page-next').addEventListener('click', () => refresh(state.offset + limit));
function panel(mode) {
  state.mode = mode;
  $('pokemon-details').hidden = mode !== null;
  $('edit-form').hidden = mode !== 'edit';
  $('delete-confirmation').hidden = mode !== 'delete';
  $('edit-error').textContent = '';
  $('delete-error').textContent = '';
  updateControls();
}
$('edit-pokemon').addEventListener('click', () => {
  if (!state.selected || state.loading) return;
  $('edit-name').value = state.selected.name;
  $('edit-height').value = state.selected.height / 10;
  $('edit-weight').value = state.selected.weight / 10;
  panel('edit'); $('edit-name').focus();
});
$('cancel-edit').addEventListener('click', () => { panel(null); $('edit-pokemon').focus(); });
$('delete-pokemon').addEventListener('click', () => {
  if (!state.selected || state.loading) return;
  $('delete-name').textContent = `${state.selected.name} · ${number(state.selected.pokemon_id)}`;
  panel('delete'); $('cancel-delete').focus();
});
$('cancel-delete').addEventListener('click', () => { panel(null); $('delete-pokemon').focus(); });
$('edit-form').addEventListener('submit', async event => {
  event.preventDefault();
  if (state.loading || state.mode !== 'edit' || !state.selected) return;
  const name = $('edit-name').value.trim();
  const height = Number($('edit-height').value);
  const weight = Number($('edit-weight').value);
  if (!name || !Number.isFinite(height) || !Number.isFinite(weight) || height < 0 || weight < 0) {
    $('edit-error').textContent = 'Informe um nome e medidas válidas.'; return;
  }
  state.loading = true; updateControls();
  try {
    const pokemon = await request(`/pokemons/${state.selected.id}`, {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify({name, height:Math.round(height * 10), weight:Math.round(weight * 10)})});
    state.items = state.items.map(item => item.id === pokemon.id ? pokemon : item);
    panel(null); renderSelected(pokemon); message('Pokémon atualizado com sucesso.');
    try { await loadCollection(); } catch { message('Pokémon salvo. Não foi possível atualizar a coleção; tente Atualizar coleção.', true); }
  } catch (error) { $('edit-error').textContent = error.message || 'Não foi possível salvar. Tente novamente.'; }
  finally { state.loading = false; updateControls(); if (!state.mode) $('edit-pokemon').focus(); }
});
function clearSelected() {
  state.selected = null; state.back = false;
  $('portrait').replaceChildren(Object.assign(document.createElement('p'), {textContent:'Selecione ou registre um Pokémon.'}));
  $('dex-number').textContent = 'Nº —'; $('screen-name').textContent = 'AGUARDANDO ENCONTRO';
  $('pokemon-title').textContent = 'Nenhum Pokémon selecionado'; $('types').replaceChildren();
  $('info-copy').textContent = 'Sua próxima descoberta está por aí.';
  for (const id of ['height', 'weight', 'national-id']) $(id).textContent = '—';
}
$('confirm-delete').addEventListener('click', async () => {
  if (state.loading || state.mode !== 'delete' || !state.selected) return;
  const id = state.selected.id;
  state.loading = true; updateControls();
  try {
    await request(`/pokemons/${id}`, {method:'DELETE'});
    panel(null); clearSelected();
    state.items = state.items.filter(item => item.id !== id);
    state.total = Math.max(0, state.total - 1);
    $('total').textContent = state.total; $('collection-count').textContent = String(state.total).padStart(2, '0');
    renderCards(); message('Pokémon apagado da coleção.');
    try {
      await loadCollection(Math.min(state.offset, Math.max(0, Math.ceil(state.total / limit) - 1) * limit));
      if (state.items.length) renderSelected(state.items[0]);
    } catch { message('Pokémon apagado. Não foi possível recarregar a coleção; tente Atualizar coleção.', true); }
  } catch (error) { $('delete-error').textContent = error.message || 'Não foi possível apagar. Tente novamente.'; }
  finally { state.loading = false; updateControls(); if (!state.mode) $('refresh').focus(); }
});
document.querySelector('.info-screen').addEventListener('keydown', event => {
  if (event.key === 'Escape' && state.mode && !state.loading) {
    const previousMode = state.mode; panel(null); $(previousMode === 'edit' ? 'edit-pokemon' : 'delete-pokemon').focus();
  }
});
updateControls();
loadCollection(0).then(() => { if (state.items.length) return select(state.items[0].id); }).catch(() => message('Não foi possível carregar a coleção. Use Atualizar coleção para tentar novamente.', true));
