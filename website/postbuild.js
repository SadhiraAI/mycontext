const fs = require('fs');
const path = require('path');

const src = path.join(__dirname, '.notebooks-tmp');
const dst = path.join(__dirname, 'static', 'notebooks');

if (fs.existsSync(src)) {
  fs.renameSync(src, dst);
  console.log('[postbuild] Restored static/notebooks/ from .notebooks-tmp/');
} else {
  console.log('[postbuild] No .notebooks-tmp/ found — skipping');
}
