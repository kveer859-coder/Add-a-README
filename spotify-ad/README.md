# Spotify — 30s Motion Graphics Ad

A 30-second, 1920×1080 @ 60fps motion graphics ad. All the animation is code: `ad.html`, rendered frame by frame.

## Storyboard (120 BPM, cuts land on the beat)

| Time | Scene |
|------|-------|
| 0–4s | Equalizer bars → the Spotify logo draws itself → "Spotify" wordmark → "Music for everyone." → a green burst |
| 4–8s | Kinetic type on green: **100M+ songs**, **6M+ podcast titles**, **+ Audiobooks. All in one app.** |
| 8–18s | Phone mockup with the app UI: Home (Made for you) → Now Playing (lyrics, like, offline) → Search (Browse all, typing "lofi beats"), with floating UI cards and tap ripples |
| 18–23s | Feature grid: Offline Mode, Live Lyrics, Podcasts, Jam, Spotify Connect, Made For You |
| 23–27.4s | Available on every device (phone, tablet, desktop, TV, speakers, car, watch) + **Google Play** and **App Store** badges |
| 27.4–30s | End card: logo, wordmark, "Listen free. Download now.", store badges |

## Files

- `ad.html` holds every scene and the timeline. `render(t)` draws any moment `t` (in seconds). Open `ad.html?play` in a browser for a live preview.
- `render.js` uses Playwright to capture frames and pipes them to ffmpeg.
- `music.py` synthesises the 120 BPM soundtrack, with whooshes and impacts on the cuts.
- `montserrat.woff2` is the font.

## Rebuild

```bash
pip install numpy
python3 music.py music.wav
FPS=60 node render.js video_noaudio.mp4
ffmpeg -i video_noaudio.mp4 -i music.wav -c:v copy -c:a aac -b:a 256k -shortest Spotify_Ad_30s.mp4
```

> This is a fan/spec concept ad. Spotify, Google Play and App Store are trademarks of their owners. Don't present it as an official Spotify ad.
