// 极速图压 — 纯前端图片压缩 / 格式转换
// 零依赖、零服务器、零成本。所有处理在浏览器本地完成。

const fileInput = document.getElementById('fileInput');
const dropZone = document.getElementById('dropZone');
const pickBtn = document.getElementById('pickBtn');
const controls = document.getElementById('controls');
const results = document.getElementById('results');
const grid = document.getElementById('grid');
const summary = document.getElementById('summary');
const formatSel = document.getElementById('format');
const quality = document.getElementById('quality');
const qualityVal = document.getElementById('qualityVal');
const maxSize = document.getElementById('maxSize');
const recompressBtn = document.getElementById('recompressBtn');
const downloadAllBtn = document.getElementById('downloadAllBtn');
const clearBtn = document.getElementById('clearBtn');

let items = []; // { file, url, blob, name, origSize, newSize }

pickBtn.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('click', (e) => { if (e.target === dropZone || e.target.closest('.uploader-inner')) fileInput.click(); });
dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('drag'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag'));
dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('drag');
  if (e.dataTransfer.files.length) handleFiles(e.dataTransfer.files);
});
fileInput.addEventListener('change', () => { if (fileInput.files.length) handleFiles(fileInput.files); });
quality.addEventListener('input', () => qualityVal.textContent = quality.value);

recompressBtn.addEventListener('click', () => processAll());
clearBtn.addEventListener('click', reset);
downloadAllBtn.addEventListener('click', downloadAll);

function reset() {
  items.forEach(it => URL.revokeObjectURL(it.url));
  items = [];
  grid.innerHTML = '';
  fileInput.value = '';
  controls.hidden = true;
  results.hidden = true;
  summary.innerHTML = '';
}

function handleFiles(fileList) {
  const files = Array.from(fileList).filter(f => f.type.startsWith('image/'));
  if (!files.length) return;
  files.forEach(f => items.push({ file: f, name: f.name, origSize: f.size, blob: null, url: null, newSize: 0 }));
  controls.hidden = false;
  results.hidden = false;
  processAll();
}

function fmtBytes(b) {
  if (b < 1024) return b + ' B';
  if (b < 1024 * 1024) return (b / 1024).toFixed(1) + ' KB';
  return (b / 1024 / 1024).toFixed(2) + ' MB';
}

function loadImage(file) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    const url = URL.createObjectURL(file);
    img.onload = () => { URL.revokeObjectURL(url); resolve(img); };
    img.onerror = reject;
    img.src = url;
  });
}

async function processAll() {
  grid.innerHTML = '';
  summary.innerHTML = '处理中…';
  const fmt = formatSel.value;
  const q = parseInt(quality.value, 10) / 100;
  const max = parseInt(maxSize.value, 10) || 0;

  let totalOrig = 0, totalNew = 0;

  for (const it of items) {
    const img = await loadImage(it.file);
    let { width, height } = img;
    if (max > 0 && Math.max(width, height) > max) {
      const ratio = max / Math.max(width, height);
      width = Math.round(width * ratio);
      height = Math.round(height * ratio);
    }
    const canvas = document.createElement('canvas');
    canvas.width = width; canvas.height = height;
    canvas.getContext('2d').drawImage(img, 0, 0, width, height);

    const outFmt = fmt === 'auto' ? (it.file.type === 'image/png' ? 'image/png' : 'image/jpeg') : fmt;
    const blob = await new Promise(res => canvas.toBlob(res, outFmt, outFmt === 'image/png' ? undefined : q));

    if (it.url) URL.revokeObjectURL(it.url);
    it.blob = blob;
    it.url = URL.createObjectURL(blob);
    it.newSize = blob.size;
    totalOrig += it.origSize;
    totalNew += it.newSize;

    renderCard(it, outFmt);
  }

  const saved = totalOrig - totalNew;
  const pct = totalOrig ? ((saved / totalOrig) * 100).toFixed(1) : 0;
  summary.innerHTML = `共 <b>${items.length}</b> 张图片 · 原始 <b>${fmtBytes(totalOrig)}</b> → 压缩后 <b>${fmtBytes(totalNew)}</b> · 节省 <b>${fmtBytes(saved)}（${pct}%）</b>`;
}

function renderCard(it, outFmt) {
  const ext = outFmt === 'image/png' ? 'png' : outFmt === 'image/webp' ? 'webp' : 'jpg';
  const base = it.name.replace(/\.[^.]+$/, '');
  const dlName = `${base}-compressed.${ext}`;
  const saved = it.origSize - it.newSize;
  const pct = it.origSize ? ((saved / it.origSize) * 100).toFixed(0) : 0;

  const card = document.createElement('div');
  card.className = 'card';
  card.innerHTML = `
    <img class="thumb" src="${it.url}" alt="">
    <div class="meta">
      <div class="name">${it.name}</div>
      <div class="stat"><span>原始</span><span>${fmtBytes(it.origSize)}</span></div>
      <div class="stat"><span>压缩后</span><span>${fmtBytes(it.newSize)}</span></div>
      <div class="stat"><span>节省</span><span class="save">${pct}%</span></div>
      <div class="dl"><a class="btn btn-accent" download="${dlName}" href="${it.url}">下载</a></div>
    </div>`;
  grid.appendChild(card);
}

function downloadAll() {
  items.forEach((it, i) => {
    const ext = (formatSel.value === 'auto'
      ? (it.file.type === 'image/png' ? 'png' : 'jpg')
      : formatSel.value.split('/')[1]);
    const a = document.createElement('a');
    a.href = it.url;
    a.download = it.name.replace(/\.[^.]+$/, '') + '-compressed.' + ext;
    document.body.appendChild(a);
    setTimeout(() => { a.click(); a.remove(); }, i * 300);
  });
}
