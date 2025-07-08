const convo = document.querySelector('.conversation-view');
const input = document.getElementById('message');
const sendBtn = document.querySelector('.send-button');
const modelName = document.querySelector('.model-name');
const buttons = document.querySelectorAll('.conversation-button');

let currentMode = 'grammar'; // default

// UI: переключение вкладок
buttons.forEach((btn, i) => {
  btn.addEventListener('click', () => {
    buttons.forEach(b => b.parentElement.classList.remove('active'));
    btn.parentElement.classList.add('active');

    if (i === 0) {
      currentMode = 'grammar';
      modelName.innerHTML = '<i class="fa fa-check"></i> Grammar';
    } else if (i === 1) {
      currentMode = 'translate';
      modelName.innerHTML = '<i class="fa fa-language"></i> Translate';
    } else {
      currentMode = 'ask';
      modelName.innerHTML = '<i class="fa fa-robot"></i> QA & Template';
    }
  });
});

// Показать сообщение в чате
function add(msg, cls) {
  const d = document.createElement('div');
  d.className = `message ${cls}`;
  const c = document.createElement('div');
  c.className = 'content';
  c.textContent = msg;
  d.append(c);
  convo.append(d);
  convo.scrollTop = convo.scrollHeight;
}

// Отправить сообщение
sendBtn.addEventListener('click', async () => {
  const q = input.value.trim();
  if (!q) return;
  add(q, 'user');
  input.value = '';

  let url = 'http://localhost:8000/';
  let body = {};

  if (currentMode === 'grammar') {
    url += 'grammar';
    body = { text: q };
  } else if (currentMode === 'translate') {
    url += 'translate';
    body = { text: q };
  } else {
    url += 'ask';
    body = { question: q };
  }

  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    const json = await res.json();

    let msg;
    if (currentMode === 'grammar') {
      msg = json.corrected || 'Нет ответа';
    } else if (currentMode === 'translate') {
      msg = json.translated || 'Нет ответа';
    } else {
      msg = json.generated || 'Нет ответа';
    }

    add(msg, 'assistant');
  } catch (e) {
    add('Ошибка: ' + e.message, 'assistant');
  }
});
