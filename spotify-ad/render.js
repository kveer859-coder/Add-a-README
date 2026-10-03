// Renders ad.html frame-by-frame into an MP4 (or stills with --stills t1,t2,...)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');

const FPS = Number(process.env.FPS || 60);
const DUR = 30;
const args = process.argv.slice(2);
const stillsArg = args.indexOf('--stills');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.join(__dirname, 'ad.html'));
  await page.waitForFunction(() => window.READY === true);

  if (stillsArg >= 0) {
    const times = args[stillsArg + 1].split(',').map(Number);
    const out = args[stillsArg + 2] || '.';
    for (const t of times) {
      await page.evaluate(t => window.render(t), t);
      await page.screenshot({ path: path.join(out, `still_${t.toFixed(2)}.jpg`), type: 'jpeg', quality: 85 });
    }
    await browser.close();
    return;
  }

  const outFile = args[0] || path.join(__dirname, 'video_noaudio.mp4');
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', outFile],
    { stdio: ['pipe', 'ignore', 'inherit'] });
  const total = FPS * DUR;
  for (let i = 0; i < total; i++) {
    await page.evaluate(t => window.render(t), i / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`frame ${i}/${total}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log('done', outFile);
})();
