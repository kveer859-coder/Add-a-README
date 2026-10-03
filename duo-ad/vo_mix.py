"""Adds the Punjabi voiceover to iPhone_Duo_Ad_9x16.mp4.

Inputs in the working dir: l0.mp3 … l9.mp3 (the lines in VOICEOVER.md, Higgsfield TTS,
ElevenLabs engine, voice "KARAN-1") and iPhone_Duo_Ad_9x16.mp4.
J-cuts: lines 2 and 4 start just before their scene cut; L-cuts: lines 2, 5 and 9 run past it.
"""
import subprocess

S = [0.4, 3.3, 6.5, 10.0, 13.75, 17.3, 20.75, 24.2, 27.1, 30.6]
WIN = [2.6, 2.9, 2.3, 3.6, 3.4, 3.5, 3.0, 2.8, 3.2, 3.6]
DUR = 34.5


def dur(f):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]))


def ff(*a):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *a], check=True)


for i in range(10):
    trim = 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,' * 2
    ff('-i', f'l{i}.mp3', '-af', trim.rstrip(','), '-ac', '1', '-ar', '44100', f't{i}.wav')
    d = dur(f't{i}.wav')
    tempo = max(1.0, min(1.4, d / WIN[i]))
    ff('-i', f't{i}.wav', '-af', f'atempo={tempo:.3f}', f'f{i}.wav')
    print(i, round(d, 2), round(tempo, 2), round(dur(f'f{i}.wav'), 2))

inp, g = [], []
for i in range(10):
    inp += ['-i', f'f{i}.wav']
    g.append(f'[{i}]adelay={int(S[i] * 1000)}[d{i}]')
g.append(''.join(f'[d{i}]' for i in range(10)) +
         f'amix=inputs=10:normalize=0,apad=whole_dur={DUR + .1},atrim=0:{DUR},loudnorm=I=-16:TP=-1.5[o]')
ff(*inp, '-filter_complex', ';'.join(g), '-map', '[o]', '-ar', '48000', 'vo.wav')

ff('-i', 'iPhone_Duo_Ad_9x16.mp4', '-i', 'vo.wav', '-filter_complex',
   '[0:a]aresample=48000,volume=0.9[bg];'
   '[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=1.2,asplit=2[v1][v2];'
   '[bg][v1]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[duck];'
   '[duck][v2]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]',
   '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart',
   'iPhone_Duo_Ad_9x16_PunjabiVO.mp4')
print('done', dur('iPhone_Duo_Ad_9x16_PunjabiVO.mp4'))
