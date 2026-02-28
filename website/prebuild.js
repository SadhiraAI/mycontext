const fs = require('fs');
const path = require('path');

const src = path.join(__dirname, 'static', 'notebooks');
const tmp = path.join(__dirname, '.notebooks-tmp');

if (process.env.NODE_ENV === 'production' && fs.existsSync(src)) {
  fs.renameSync(src, tmp);
  console.log('[prebuild] Moved static/notebooks/ to .notebooks-tmp/ (hidden from prod build)');
} else {
  console.log('[prebuild] Dev mode or no notebooks folder — skipping');
}
