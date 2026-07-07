// JSON 格式化助手 — 纯前端，零依赖
const input = document.getElementById('input');
const output = document.getElementById('output');
const status = document.getElementById('status');
const indent = document.getElementById('indent');

function setStatus(msg, type) {
  status.textContent = msg;
  status.className = 'status' + (type ? ' ' + type : '');
}

function getIndent() {
  const v = indent.value;
  return v === '\\t' ? '\t' : parseInt(v, 10);
}

function format() {
  const raw = input.value.trim();
  if (!raw) { setStatus('等待输入…'); output.textContent = ''; return; }
  try {
    const parsed = JSON.parse(raw);
    output.textContent = JSON.stringify(parsed, null, getIndent());
    setStatus('✓ 有效 JSON，已格式化', 'ok');
  } catch (e) {
    output.textContent = '';
    setStatus('✗ ' + e.message, 'err');
  }
}

function minify() {
  const raw = input.value.trim();
  if (!raw) { setStatus('等待输入…'); output.textContent = ''; return; }
  try {
    const parsed = JSON.parse(raw);
    output.textContent = JSON.stringify(parsed);
    setStatus('✓ 已压缩', 'ok');
  } catch (e) {
    output.textContent = '';
    setStatus('✗ ' + e.message, 'err');
  }
}

function copy() {
  if (!output.textContent) return;
  navigator.clipboard.writeText(output.textContent).then(
    () => setStatus('✓ 已复制到剪贴板', 'ok'),
    () => setStatus('复制失败，请手动选择', 'err')
  );
}

function download() {
  if (!output.textContent) return;
  const blob = new Blob([output.textContent], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'formatted.json';
  a.click();
  URL.revokeObjectURL(a.href);
}

function clearAll() {
  input.value = '';
  output.textContent = '';
  setStatus('等待输入…');
}

document.getElementById('formatBtn').addEventListener('click', format);
document.getElementById('minifyBtn').addEventListener('click', minify);
document.getElementById('copyBtn').addEventListener('click', copy);
document.getElementById('downloadBtn').addEventListener('click', download);
document.getElementById('clearBtn').addEventListener('click', clearAll);
indent.addEventListener('change', () => { if (output.textContent && !status.classList.contains('err')) format(); });
