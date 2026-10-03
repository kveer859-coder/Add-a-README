"""Synthesises a 30s, 120 BPM soundtrack synced to ad.html's scene cuts."""
import numpy as np, wave, sys

SR = 44100
DUR = 30.0
N = int(SR * DUR)
BEAT = 0.5
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N); REV = np.zeros(N)

def midi(n): return 440.0 * 2 ** ((n - 69) / 12)
def idx(t): return int(round(t * SR))

def add(sig, t, gain=1.0, pan=0.0, send=0.0):
    i = idx(t)
    if i >= N: return
    sig = sig[:N - i]
    l = gain * np.cos((pan + 1) * np.pi / 4); r = gain * np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(sig)] += sig * l; R[i:i + len(sig)] += sig * r
    REV[i:i + len(sig)] += sig * send * gain

def saw(f, d, harm=14, detune=0.0):
    t = np.arange(int(d * SR)) / SR
    out = np.zeros_like(t)
    for k in range(1, harm + 1):
        if f * k > 16000: break
        out += np.sin(2 * np.pi * f * k * t * (1 + detune)) / k * (1 / (1 + 0.08 * k * k))
    return out

def env_adsr(n, a, d, s, r):
    e = np.ones(n) * s
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    na = max(1, min(na, n)); e[:na] = np.linspace(0, 1, na)
    if nd: e[na:na + nd] = np.linspace(1, s, len(e[na:na + nd]))
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e

def kick():
    d = 0.45; t = np.arange(int(d * SR)) / SR
    f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7) + 0.3 * np.exp(-t * 300) * rng.standard_normal(len(t)) * 0.3

def clap():
    d = 0.3; n = int(d * SR); t = np.arange(n) / SR
    nz = rng.standard_normal(n); nz = np.diff(nz, prepend=0)
    e = np.exp(-t * 18)
    for off in (0.01, 0.02):
        k = int(off * SR); e[:k] += 0
    return nz * e * 0.5

def hat(open_=False):
    d = 0.25 if open_ else 0.06; n = int(d * SR); t = np.arange(n) / SR
    nz = np.diff(np.diff(rng.standard_normal(n + 2)))
    return nz * np.exp(-t * (12 if open_ else 70)) * 0.25

def riser(d):
    n = int(d * SR); t = np.arange(n) / SR
    nz = rng.standard_normal(n); nz = nz - np.convolve(nz, np.ones(6) / 6, 'same')
    sweep = np.sin(2 * np.pi * np.cumsum(200 + 1800 * (t / d) ** 2) / SR)
    return (nz * 0.5 + sweep * 0.15) * (t / d) ** 2.2

def whoosh(d=0.5):
    n = int(d * SR); t = np.arange(n) / SR
    nz = rng.standard_normal(n); k = 12
    nz = np.convolve(nz, np.ones(k) / k, 'same')
    e = np.sin(np.pi * t / d) ** 2
    return nz * e * 1.4

def impact():
    d = 1.6; t = np.arange(int(d * SR)) / SR
    f = 30 + 70 * np.exp(-t * 6)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.5)
    nz = rng.standard_normal(len(t)) * np.exp(-t * 9) * 0.35
    return boom + nz

# chords: Am F C G (one per bar = 2s)
prog = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
roots = [45, 41, 48, 43]

def chord_at(t): return int(t // 2) % 4

# --- pads (whole track) ---
for bar in range(15):
    t0 = bar * 2.0
    c = prog[bar % 4]
    for n_ in c:
        for dt in (-0.004, 0.0, 0.004):
            s = saw(midi(n_), 2.05, harm=10, detune=dt)
            s *= env_adsr(len(s), 0.25, 0.3, 0.8, 0.3)
            g = 0.035 if t0 >= 4 else 0.05 * min(1, (t0 + 1) / 3)
            add(s, t0, g, pan=dt * 150, send=0.5)

# --- drums / bass / plucks ---
def full(t): return (4.0 <= t < 17.5) or (18.0 <= t < 27.4)
b = 0.0
while b < 30:
    beat_i = int(round(b / BEAT))
    if full(b):
        add(kick(), b, 0.95)
        if beat_i % 2 == 1: add(clap(), b, 0.55, send=0.35)
        add(hat(), b + 0.25, 0.5, pan=0.3)
        if beat_i % 4 == 3: add(hat(True), b + 0.25, 0.35, pan=-0.3)
        # offbeat bass with sidechain feel
        r = roots[chord_at(b)]
        bs = saw(midi(r - 12), 0.24, harm=6) + 0.6 * np.sin(2 * np.pi * midi(r - 12) * np.arange(int(.24 * SR)) / SR)
        add(bs * env_adsr(len(bs), 0.01, 0.1, 0.6, 0.05), b + 0.25, 0.32)
    b += BEAT

# plucks: 16th arps
step = 0.125; t = 0.0
while t < 29.0:
    if t >= 1.0 and not (17.5 <= t < 18.0):
        c = prog[chord_at(t)]
        k = int(round(t / step))
        notes = [c[0] + 12, c[1] + 12, c[2] + 12, c[1] + 24]
        n_ = notes[k % 4]
        s = saw(midi(n_), 0.22, harm=8)
        s *= np.exp(-np.arange(len(s)) / SR * 18)
        g = 0.07 if t >= 4 else 0.05 * (t / 4)
        if t >= 27.4: g *= max(0, 1 - (t - 27.4) / 1.6)
        add(s, t, g, pan=0.35 if k % 2 else -0.35, send=0.45)
    t += step

# --- transitions ---
add(riser(1.6), 2.4, 0.5, send=0.3)
add(riser(0.5), 17.5, 0.5, send=0.3)
for w in (3.55, 7.6, 10.95, 14.4, 17.55, 22.55, 27.1):
    add(whoosh(0.5), w - 0.05, 0.22, pan=0.0, send=0.4)
for im in (4.0, 8.0, 18.0, 23.0, 27.4):
    add(impact(), im, 0.55 if im in (4.0, 18.0, 27.4) else 0.35, send=0.3)
# final chord stab
for n_ in prog[0] + [69, 72]:
    s = saw(midi(n_), 2.4, harm=12); s *= np.exp(-np.arange(len(s)) / SR * 1.6)
    add(s, 27.5, 0.06, send=0.8)

# --- reverb (FFT convolution with decaying noise IR) ---
ir_n = int(2.2 * SR); ti = np.arange(ir_n) / SR
irL = rng.standard_normal(ir_n) * np.exp(-ti * 3.2); irR = rng.standard_normal(ir_n) * np.exp(-ti * 3.2)
irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
M = 1 << int(np.ceil(np.log2(N + ir_n)))
Rf = np.fft.rfft(REV, M)
L += np.fft.irfft(Rf * np.fft.rfft(irL, M), M)[:N] * 0.35
R += np.fft.irfft(Rf * np.fft.rfft(irR, M), M)[:N] * 0.35

# master: fade, soft clip, normalise
fade = np.ones(N); fn = int(1.2 * SR); fade[-fn:] = np.linspace(1, 0, fn) ** 1.5
fi = int(0.05 * SR); fade[:fi] = np.linspace(0, 1, fi)
mix = np.stack([L, R], 1) * fade[:, None]
mix /= np.abs(mix).max()
mix = np.tanh(mix * 1.6) / np.tanh(1.6)
mix *= 0.89
pcm = (mix * 32767).astype('<i2')
out = sys.argv[1] if len(sys.argv) > 1 else 'music.wav'
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('wrote', out)
