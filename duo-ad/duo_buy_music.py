"""120 BPM soundtrack for duo_buy.html (31s): quiet intro, unfold drop at 7.0s,
groove, break before colours, final hit at 30.5s. Whooshes/hinge clicks land on cuts."""
import numpy as np, wave, sys

SR = 44100; DUR = 31.0; N = int(SR * DUR)
rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N); REV = np.zeros(N)

def midi(n): return 440 * 2 ** ((n - 69) / 12)
def tt(d): return np.arange(int(d * SR)) / SR
def add(sig, t, g=1.0, pan=0.0, send=0.0):
    i = int(t * SR)
    if i >= N: return
    sig = sig[:N - i]
    L[i:i+len(sig)] += sig * g * np.cos((pan + 1) * np.pi / 4)
    R[i:i+len(sig)] += sig * g * np.sin((pan + 1) * np.pi / 4)
    REV[i:i+len(sig)] += sig * g * send
def saw(f, d, harm=10, det=0.0):
    t = tt(d); return sum(np.sin(2*np.pi*f*k*t*(1+det)) / k / (1 + .08*k*k) for k in range(1, harm+1) if f*k < 15000)
def env(n, a, r):
    e = np.ones(n); na = max(1, int(a*SR)); nr = int(r*SR)
    e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e

prog = [[50, 54, 57, 61], [47, 50, 54, 57], [43, 47, 50, 54], [45, 49, 52, 57]]
roots = [38, 35, 31, 33]
def chord(t): return int(t // 2) % 4

def kick():
    t = tt(.45); f = 45 + 120*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*7)
def clap():
    t = tt(.25); return np.diff(rng.standard_normal(len(t)+1)) * np.exp(-t*20) * .5
def hat(op=False):
    d = .22 if op else .05; t = tt(d)
    return np.diff(np.diff(rng.standard_normal(len(t)+2))) * np.exp(-t*(12 if op else 75)) * .22
def tick():
    t = tt(.03); return np.sin(2*np.pi*4200*t) * np.exp(-t*220)
def hinge():  # mechanical fold click
    t = tt(.12); return (np.sin(2*np.pi*1800*t)*.5 + rng.standard_normal(len(t))*.4) * np.exp(-t*90) + np.sin(2*np.pi*120*t)*np.exp(-t*40)*.6
def whoosh(d=.45):
    t = tt(d); n = np.convolve(rng.standard_normal(len(t)), np.ones(10)/10, 'same')
    return n * np.sin(np.pi*t/d)**2 * 1.5
def riser(d):
    t = tt(d); n = rng.standard_normal(len(t)) - np.convolve(rng.standard_normal(len(t)), np.ones(5)/5, 'same')
    return (n*.45 + np.sin(2*np.pi*np.cumsum(220+1600*(t/d)**2)/SR)*.2) * (t/d)**2.2
def impact(d=1.8):
    t = tt(d); f = 28 + 80*np.exp(-t*6)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.2) + rng.standard_normal(len(t))*np.exp(-t*8)*.3

groove = lambda t: (3.6 <= t < 22.6) or (23.0 <= t < 27.5)

# pads all the way, softer in the intro
for bar in range(18):
    t0 = bar * 2.0
    if t0 >= DUR: break
    for n in prog[bar % 4]:
        for det in (-.004, 0, .004):
            s = saw(midi(n), 2.1, 8, det); s *= env(len(s), .3, .4)
            g = .03 if 3.6 <= t0 < 27.5 else .045
            add(s, t0, g, pan=det*150, send=.6)

b = 0.0
while b < DUR:
    k = int(round(b / .5))
    if b < 3.5: add(tick(), b, .25, pan=.3*(1 if k % 2 else -1))
    if groove(b):
        add(kick(), b, .95)
        if k % 2: add(clap(), b, .5, send=.35)
        add(hat(), b + .25, .5, pan=.3)
        if k % 4 == 3: add(hat(True), b + .25, .3, pan=-.3)
        r = roots[chord(b)]
        s = saw(midi(r), .24, 5) + .7*np.sin(2*np.pi*midi(r)*tt(.24)); add(s*env(len(s), .01, .05), b + .25, .3)
    b += .5

st = .125; t = 0.0
while t < 29.5:
    if (1.0 <= t < 22.6) or (23.0 <= t < 28.0):
        c = prog[chord(t)]; k = int(round(t / st))
        n = [c[0]+12, c[2]+12, c[1]+24, c[3]+12][k % 4]
        s = saw(midi(n), .2, 7) * np.exp(-tt(.2)*20)
        g = .035 if t < 3.6 else .06
        add(s, t, g, pan=.35 if k % 2 else -.35, send=.45)
    t += st

add(riser(1.8), 1.8, .5, send=.3); add(riser(.45), 22.55, .5, send=.3)
for h in (3.55, 5.25, 6.35): add(hinge(), h, .6, send=.2)
for w in (3.4, 4.75, 5.85, 6.95, 10.4, 15.95, 19.45, 22.95, 25.25, 27.4): add(whoosh(), w - .1, .22, send=.4)
for im in (3.6, 10.5, 23.0, 27.5): add(impact(), im, .6 if im in (3.6, 27.5) else .35, send=.3)
for n in prog[0] + [66, 69]:
    s = saw(midi(n), 3.0, 10) * np.exp(-tt(3.0)*1.2); add(s, 27.5, .05, send=.8)

ir = int(2.2*SR); ti = np.arange(ir)/SR
M = 1 << int(np.ceil(np.log2(N + ir))); Rf = np.fft.rfft(REV, M)
for ch, seed in ((L, 1), (R, 2)):
    h = np.random.default_rng(seed).standard_normal(ir)*np.exp(-ti*3); h /= np.sqrt((h**2).sum())
    ch += np.fft.irfft(Rf*np.fft.rfft(h, M), M)[:N]*.35
mix = np.stack([L, R], 1)
fade = np.ones(N); fn = int(1.5*SR); fade[-fn:] = np.linspace(1, 0, fn)**1.5; mix *= fade[:, None]
mix /= np.abs(mix).max(); mix = np.tanh(mix*1.6)/np.tanh(1.6)*.89
with wave.open(sys.argv[1] if len(sys.argv) > 1 else 'duo_buy_music.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype('<i2').tobytes())
print('ok')
