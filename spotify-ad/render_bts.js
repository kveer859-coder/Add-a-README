// Renders bts.html (1080x1920) to MP4, or stills with --stills t1,t2,... <outdir>
// Needs a static server on :8765 serving this folder (python3 -m http.server 8765).
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const FPS = Number(process.env.FPS || 60);
const DUR = Number(process.env.DUR || 30.5);
const PAGE = process.env.PAGE || 'bts.html';
const args = process.argv.slice(2);
const si = args.indexOf('--stills');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('pageerror', e => console.error('PAGEERROR', e.message));
  page.on('console', m => { if (m.type() === 'error') console.error('CONSOLE', m.text()); });
  await page.goto(`http://localhost:8765/${PAGE}`);
  await page.waitForFunction(() => window.READY === true, null, { timeout: 30000 });
  fs.writeFileSync(path.join(__dirname, 'bts_sfx.json'), JSON.stringify(await page.evaluate(() => window.SFX || {})));

  if (si >= 0) {
    const times = args[si + 1].split(',').map(Number);
    const out = args[si + 2] || '.';
    for (const t of times) {
      await page.evaluate(t => window.render(t), t);
      await page.screenshot({ path: path.join(out, `b_${t.toFixed(2)}.jpg`), type: 'jpeg', quality: 85 });
    }
    await browser.close();
    return;
  }

  const outFile = args[0] || 'bts_noaudio.mp4';
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', outFile],
    { stdio: ['pipe', 'ignore', 'ignore'] });
  const total = Math.round(FPS * DUR);
  for (let i = 0; i < total; i++) {
    await page.evaluate(t => window.render(t), i / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 93 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 300 === 0) console.log(`frame ${i}/${total}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log('done', outFile);
})();
