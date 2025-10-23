const toJsOptions = { dict_converter: Object.fromEntries };
let pyFns = {};
let activeSession = null;
let pollHandle = null;
let awaitingPrompt = false;

const statusEl = document.getElementById('status');
const profileEl = document.getElementById('profile-content');
const dailyEl = document.getElementById('daily-content');
const leaderboardEl = document.getElementById('leaderboard-list');
const recommendationsEl = document.getElementById('recommendations-list');
const catalogueEl = document.getElementById('catalogue-grid');
const terminalEl = document.getElementById('terminal-output');
const promptWrapper = document.getElementById('prompt-wrapper');
const promptLabel = document.getElementById('prompt-label');
const inputForm = document.getElementById('input-form');
const inputField = document.getElementById('user-input');

document.addEventListener('pyscript:ready', async () => {
  setStatus('Loading Python modules…');
  const pyodide = await window.pyodideReadyPromise;
  pyFns = {
    getLauncher: pyodide.globals.get('get_launcher_payload'),
    getCatalogue: pyodide.globals.get('get_catalogue_payload'),
    startGame: pyodide.globals.get('start_game'),
    sendInput: pyodide.globals.get('send_input'),
    pollEvents: pyodide.globals.get('poll_events'),
    closeGame: pyodide.globals.get('close_game')
  };

  const launcher = consumeProxy(pyFns.getLauncher());
  renderLauncher(launcher);

  const catalogue = consumeProxy(pyFns.getCatalogue());
  renderCatalogue(catalogue);

  setStatus('Ready. Choose a game to begin.');
});

inputForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!activeSession || !awaitingPrompt) {
    return;
  }
  const value = inputField.value.trim();
  inputField.value = '';
  hidePrompt();
  appendOutput(`> ${value}\n`);
  const events = consumeProxy(pyFns.sendInput(activeSession, value));
  appendEvents(events);
});

function renderLauncher(payload) {
  renderProfile(payload.profile);
  renderDaily(payload.daily_challenge);
  renderLeaderboard(payload.leaderboard);
  renderRecommendations(payload.recommendations);
}

function renderProfile(profile) {
  profileEl.innerHTML = `
    <strong>${profile.name}</strong> (Level ${profile.level})<br />
    XP: ${profile.experience} &mdash; Next level in ${profile.experience_to_next}<br />
    Achievements: ${profile.achievements_unlocked}/${profile.achievements_total} (${profile.achievement_points} pts)<br />
    Daily streak: ${profile.daily_streak} (best ${profile.best_daily_streak})
  `;
}

function renderDaily(challenge) {
  const status = challenge.completed ? 'Completed' : 'Available';
  dailyEl.innerHTML = `
    <strong>${challenge.pack_name}</strong><br />
    ${challenge.challenge_title} &middot; ${challenge.difficulty.toUpperCase()}<br />
    ${challenge.description}<br />
    <em>Status: ${status}</em>
  `;
}

function renderLeaderboard(entries) {
  leaderboardEl.innerHTML = '';
  if (!entries.length) {
    leaderboardEl.innerHTML = '<li>No leaderboard data yet.</li>';
    return;
  }
  entries.forEach((entry, index) => {
    const li = document.createElement('li');
    const marker = entry.is_self ? '★ ' : '';
    li.textContent = `${marker}${index + 1}. ${entry.display_name} — ${entry.total_wins} wins, ${entry.achievement_points} pts`;
    leaderboardEl.appendChild(li);
  });
}

function renderRecommendations(items) {
  recommendationsEl.innerHTML = '';
  if (!items.length) {
    recommendationsEl.innerHTML = '<li>Play more games to unlock personalised tips.</li>';
    return;
  }
  items.forEach((item) => {
    const li = document.createElement('li');
    const reasons = item.reasons.length ? `Reasons: ${item.reasons.join(', ')}` : 'Suggested for you';
    li.innerHTML = `<strong>${item.game_name}</strong><br /><span>${reasons}</span>`;
    recommendationsEl.appendChild(li);
  });
}

function renderCatalogue(catalogue) {
  catalogueEl.innerHTML = '';
  catalogue.games.forEach((game) => {
    const card = document.createElement('button');
    card.type = 'button';
    card.className = 'game-card';
    const synopsis = game.synopsis || game.description;
    card.innerHTML = `
      <span class="tag">${game.genre.toUpperCase()}</span>
      <h3>${game.name}</h3>
      <p>${synopsis}</p>
    `;
    card.addEventListener('click', () => startGame(game.slug, game.name));
    catalogueEl.appendChild(card);
  });
}

async function startGame(slug, name) {
  clearTerminal();
  hidePrompt();
  if (activeSession) {
    safeCall(pyFns.closeGame, activeSession);
    activeSession = null;
  }
  setStatus(`Launching ${name}…`);
  const result = consumeProxy(pyFns.startGame(slug));
  activeSession = result.session_id;
  appendEvents(result.events);
  startPolling();
  setStatus(`Playing ${name}.`);
}

function appendEvents(events) {
  if (!events || !events.length) {
    return;
  }
  events.forEach((event) => {
    switch (event.kind) {
      case 'output':
        appendOutput(event.payload || '');
        break;
      case 'prompt':
        showPrompt(event.payload || 'Enter your move:');
        break;
      case 'error':
        appendOutput(`\n[error]\n${event.payload || 'An error occurred.'}\n`);
        setStatus('An error interrupted the session.');
        stopPolling();
        activeSession = null;
        hidePrompt();
        break;
      case 'finished':
        appendOutput('\n[session complete]\n');
        setStatus('Session complete. Choose another game.');
        stopPolling();
        activeSession = null;
        hidePrompt();
        break;
      default:
        break;
    }
  });
}

function startPolling() {
  stopPolling();
  pollHandle = setInterval(() => {
    if (!activeSession) {
      stopPolling();
      return;
    }
    const events = consumeProxy(pyFns.pollEvents(activeSession));
    appendEvents(events);
  }, 600);
}

function stopPolling() {
  if (pollHandle) {
    clearInterval(pollHandle);
    pollHandle = null;
  }
}

function appendOutput(text) {
  if (!text) {
    return;
  }
  terminalEl.textContent += text;
  terminalEl.scrollTop = terminalEl.scrollHeight;
}

function clearTerminal() {
  terminalEl.textContent = '';
}

function showPrompt(message) {
  awaitingPrompt = true;
  promptLabel.textContent = message;
  promptWrapper.classList.remove('hidden');
  inputField.focus();
}

function hidePrompt() {
  awaitingPrompt = false;
  promptWrapper.classList.add('hidden');
}

function setStatus(message) {
  statusEl.textContent = message;
}

function consumeProxy(proxy) {
  if (!proxy) {
    return proxy;
  }
  const value = proxy.toJs(toJsOptions);
  if (proxy.destroy) {
    proxy.destroy();
  }
  return value;
}

function safeCall(fn, ...args) {
  if (!fn) {
    return;
  }
  const result = fn(...args);
  if (result && typeof result.destroy === 'function') {
    result.destroy();
  }
}

window.addEventListener('beforeunload', () => {
  Object.values(pyFns).forEach((fn) => {
    if (fn && typeof fn.destroy === 'function') {
      fn.destroy();
    }
  });
});
