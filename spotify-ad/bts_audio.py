"""Soundtrack for the 30.5s making-of section: lo-fi house bed + UI sound effects
(mouse clicks, typing, whooshes, render chime), timed from bts_sfx.json."""
import numpy as np, wave, json, sys

SR = 44100; DUR = 30.5; N = int(SR * DUR)
rng = np.random.default_rng(3)
L = np.zeros(N); R = np.zeros(N); REV = np.zeros(N)
sfx = json.load(open('bts_sfx.json'))

def midi(n): return 440 * 2 ** ((n - 69) / 12)
def add(sig, t, g=1.0, pan=0.0, send=0.0):
    i = int(t * SR)
    if i >= N or i < 0: return
    sig = sig[:N - i]
    L[i:i+len(sig)] += sig * g * np.cos((pan + 1) * np.pi / 4)
    R[i:i+len(sig)] += sig * g * np.sin((pan + 1) * np.pi / 4)
    REV[i:i+len(sig)] += sig * g * send
def tt(d): return np.arange(int(d * SR)) / SR
def tone(f, d, harm=6, roll=.5):
    t = tt(d); return sum(np.sin(2*np.pi*f*k*t) * roll**(k-1) / k for k in range(1, harm+1))

# ---- music bed: 120 BPM, Fmaj7 Em7 Dm7 Cmaj7 ----
prog = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]
roots = [41, 40, 38, 36]
def kick():
    t = tt(.35); f = 48 + 90*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*9)
def hat():
    t = tt(.05); return np.diff(rng.standard_normal(len(t)+1)) * np.exp(-t*80) * .2
def snare():
    t = tt(.2); return (np.diff(rng.standard_normal(len(t)+1))*.5 + np.sin(2*np.pi*190*t)*.4) * np.exp(-t*22)

for bar in range(16):
    t0 = bar * 2.0
    if t0 >= 30.5: break
    c = prog[bar % 4]
    for n in c:
        s = tone(midi(n), 2.1, 5, .45) * np.minimum(1, tt(2.1)/.08) * np.exp(-tt(2.1)*.6)
        add(s, t0, .045, pan=(n % 5 - 2) * .2, send=.6)
    for b in range(4):
        tb = t0 + b * .5
        if tb >= 26.0: continue          # drums drop out for before/after
        add(kick(), tb, .7)
        if b % 2: add(snare(), tb, .35, send=.3)
        add(hat(), tb + .25, .45, pan=.3)
        add(hat(), tb + .375, .2, pan=-.3)
        bs = tone(midi(roots[bar % 4] - 12), .4, 3, .4) * np.exp(-tt(.4)*5)
        add(bs, tb + .25, .28)

# ---- UI SFX ----
def click():
    t = tt(.04); return (np.sin(2*np.pi*3200*t)*.6 + rng.standard_normal(len(t))*.5) * np.exp(-t*260)
def keytap():
    t = tt(.05); n = rng.standard_normal(len(t)); n = np.convolve(n, np.ones(4)/4, 'same')
    return (n + np.sin(2*np.pi*(900+rng.uniform(-150,150))*t)*.4) * np.exp(-t*120)
def whoosh(d=.45):
    t = tt(d); n = np.convolve(rng.standard_normal(len(t)), np.ones(10)/10, 'same')
    return n * np.sin(np.pi*t/d)**2 * 1.6
def pop():
    t = tt(.15); f = 300 + 500*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*25)
def chime():
    out = np.zeros(int(1.4*SR))
    for i, n in enumerate([76, 83, 88]):
        s = tone(midi(n), 1.2, 3, .3) * np.exp(-tt(1.2)*3.5); k = int(i*.09*SR)
        out[k:k+len(s)] += s
    return out
def riser(d):
    t = tt(d); n = rng.standard_normal(len(t)) - np.convolve(rng.standard_normal(len(t)), np.ones(5)/5, 'same')
    return (n*.4 + np.sin(2*np.pi*np.cumsum(300+1500*(t/d)**2)/SR)*.2) * (t/d)**2

for c in sfx.get('clicks', []): add(click(), c, .55, pan=.1)
for c in sfx.get('typing', []): add(keytap(), c, .5, pan=-.1)
for c in sfx.get('keys', []): add(keytap(), c, .35)
for w in (0.95, 2.1, 7.85, 10.75, 14.55, 20.65, 23.0, 26.0, 27.45, 28.6): add(whoosh(), w - .1, .22, send=.3)
add(pop(), 1.05, .5); add(pop(), 2.4, .4)
add(chime(), 25.25, .35, send=.5)
add(riser(1.0), 29.5, .45, send=.3)

# reverb
ir = int(1.8*SR); ti = np.arange(ir)/SR
M = 1 << int(np.ceil(np.log2(N + ir)))
Rf = np.fft.rfft(REV, M)
for ch, seed in ((L, 1), (R, 2)):
    h = np.random.default_rng(seed).standard_normal(ir) * np.exp(-ti*3.5); h /= np.sqrt((h**2).sum())
    ch += np.fft.irfft(Rf * np.fft.rfft(h, M), M)[:N] * .3

mix = np.stack([L, R], 1); mix /= np.abs(mix).max()
mix = np.tanh(mix*1.5)/np.tanh(1.5) * .85
fi = int(.03*SR); mix[:fi] *= np.linspace(0, 1, fi)[:, None]
with wave.open(sys.argv[1] if len(sys.argv) > 1 else 'bts_audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype('<i2').tobytes())
print('ok')
