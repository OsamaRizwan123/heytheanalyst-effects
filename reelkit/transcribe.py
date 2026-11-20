"""Transcribe a video into timed speech segments (offline, Whisper + Silero VAD via sherpa-onnx).

Usage:
  python -m reelkit.transcribe raw.mov -o segs.json [--models models/]

Models (download once into models/):
  sherpa-onnx-whisper-base.en  https://github.com/k2-fsa/sherpa-onnx/releases (asr-models)
  silero_vad.onnx              https://github.com/k2-fsa/sherpa-onnx/releases (asr-models)
"""
import argparse, json, subprocess, tempfile, wave, os
import numpy as np

def speech_bursts(wav_path, win=0.05, factor=3.5):
    """Fallback word finder: returns (start, end) of loud bursts. Good for 'not this / but this' timing."""
    w = wave.open(wav_path); sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
    n = int(sr * win); e = np.array([np.sqrt((a[i:i + n] ** 2).mean()) for i in range(0, len(a) - n, n)])
    thr = np.percentile(e, 40) * factor; on = e > thr; out = []; i = 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and on[j:j + 3].any(): j += 1
            if j - i >= 2: out.append((round(i * win, 2), round(j * win, 2)))
            i = j
        else: i += 1
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("-o", default="segs.json")
    ap.add_argument("--models", default="models"); a = ap.parse_args()
    tmp = tempfile.mktemp(suffix=".wav")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", a.video, "-ac", "1", "-ar", "16000", tmp], check=True)
    try:
        import sherpa_onnx
    except ImportError:
        print("sherpa-onnx not installed; writing loud-burst timings only"); json.dump(speech_bursts(tmp), open(a.o, "w")); return
    d = os.path.join(a.models, "sherpa-onnx-whisper-base.en") + "/"
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d + "base.en-encoder.int8.onnx",
        decoder=d + "base.en-decoder.int8.onnx", tokens=d + "base.en-tokens.txt", num_threads=2)
    cfg = sherpa_onnx.VadModelConfig(); cfg.silero_vad.model = os.path.join(a.models, "silero_vad.onnx")
    cfg.silero_vad.min_silence_duration = 0.08; cfg.silero_vad.min_speech_duration = 0.2; cfg.sample_rate = 16000
    vad = sherpa_onnx.VoiceActivityDetector(cfg, buffer_size_in_seconds=120)
    wf = wave.open(tmp); sr = wf.getframerate()
    audio = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
    out = []
    def drain():
        while not vad.empty():
            seg = vad.front; st = seg.start / sr; s = rec.create_stream(); s.accept_waveform(sr, seg.samples)
            rec.decode_stream(s); out.append([round(st, 2), round(st + len(seg.samples) / sr, 2), s.result.text.strip()]); vad.pop()
    w = cfg.silero_vad.window_size
    for i in range(0, len(audio), w): vad.accept_waveform(audio[i:i + w]); drain()
    vad.flush(); drain()
    for s in out: print(f"{s[0]:6.2f}-{s[1]:6.2f} {s[2]}")
    json.dump(out, open(a.o, "w"), indent=1)

if __name__ == "__main__": main()
