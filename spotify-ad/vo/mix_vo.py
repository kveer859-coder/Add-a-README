"""Builds the Punjabi voiceover track and mixes it into the making-of video.

Inputs: l0.mp3 … l9.mp3 (the 10 voiceover lines from ../voiceover_script.md, generated
with Higgsfield TTS, ElevenLabs engine, voice "KARAN-1") and Spotify_Ad_MakingOf_9x16.mp4.
Output: Spotify_Ad_MakingOf_9x16_VO.mp4 (the music ducks under the voice).
"""
import subprocess

S = [0.2, 3.0, 7.35, 11.7, 14.6, 18.1, 21.6, 26.1, 29.4, 58.0]   # start time of each line (s)
WIN = [2.8, 4.3, 3.8, 2.8, 3.3, 3.2, 4.0, 3.2, 2.6, 2.4]         # max length before it's sped up


def dur(f):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]))


def ff(*a):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *a], check=True)


for i in range(10):
    trim = 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,' * 2
    ff('-i', f'l{i}.mp3', '-af', trim.rstrip(','), '-ac', '1', '-ar', '44100', f't{i}.wav')
    tempo = max(1.0, min(1.45, dur(f't{i}.wav') / WIN[i]))
    ff('-i', f't{i}.wav', '-af', f'atempo={tempo:.3f}', f'f{i}.wav')

inputs, graph = [], []
for i in range(10):
    inputs += ['-i', f'f{i}.wav']
    graph.append(f'[{i}]adelay={int(S[i] * 1000)}[d{i}]')
graph.append(''.join(f'[d{i}]' for i in range(10)) +
             'amix=inputs=10:normalize=0,apad=whole_dur=60.6,atrim=0:60.55,loudnorm=I=-16:TP=-1.5[o]')
ff(*inputs, '-filter_complex', ';'.join(graph), '-map', '[o]', '-ar', '48000', '-c:a', 'libopus', '-b:a', '32k', 'vo_track.opus')

ff('-i', 'Spotify_Ad_MakingOf_9x16.mp4', '-i', 'vo_track.opus', '-filter_complex',
   '[0:a]aresample=48000,volume=0.95[bg];'
   '[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=1.15,asplit=2[v1][v2];'
   '[bg][v1]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[duck];'
   '[duck][v2]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]',
   '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart',
   'Spotify_Ad_MakingOf_9x16_VO.mp4')
print('done')
