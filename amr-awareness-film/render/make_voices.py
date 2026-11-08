#!/usr/bin/env python3
"""Synthesise every Tamil line, fit them into the scene timings, and write:

  build/voices/<id>.wav      processed per-segment audio (48 kHz mono)
  audio/dialogue.wav         full 180 s dialogue stem, lines at their times
  build/timeline.json        segment times + lip-sync envelopes for the renderer
  subtitles/amr_film_en.srt  English subtitles timed to the real audio

Needs network access to speech.platform.bing.com (edge-tts).
"""
import asyncio, json, os, subprocess, sys, wave
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from script_data import SCENES, VOICES, SEGMENTS, SCENE_DIALOGUE_LIMIT, TARGET_SCENES, PREPAUSE

ROOT = Path(__file__).resolve().parent.parent
BUILD, VOX = ROOT / "build", ROOT / "build" / "voices"
SR, FPS, TOTAL = 48000, 25, 180
VOX.mkdir(parents=True, exist_ok=True)
(ROOT / "audio").mkdir(exist_ok=True)


async def tts(text, spk, out):
    import edge_tts
    v = VOICES[spk]
    if out.exists() and out.stat().st_size > 1000:
        return
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    for attempt in range(4):
        try:
            c = edge_tts.Communicate(text, v["voice"], rate=v["rate"], pitch=v["pitch"], proxy=proxy)
            await c.save(str(out))
            if out.stat().st_size > 1000:
                return
        except Exception as e:  # network hiccup: back off and retry
            print(f"  retry {out.name}: {e}", file=sys.stderr)
        await asyncio.sleep(2 ** attempt)
    raise RuntimeError(f"TTS failed for {out.name}")


def to_wav(src, dst, fx=None, tempo=1.0):
    chain = ["silenceremove=start_periods=1:start_threshold=-45dB",
             "areverse", "silenceremove=start_periods=1:start_threshold=-45dB", "areverse"]
    if tempo > 1.001:
        chain.append(f"atempo={tempo:.4f}")
    if fx:
        chain.append(fx)
    subprocess.run(["ffmpeg", "-v", "error", "-y", *sum([["-i", str(s)] for s in src], []),
                    "-filter_complex",
                    (f"{''.join(f'[{i}:a]' for i in range(len(src)))}amix=inputs={len(src)}:normalize=0," if len(src) > 1 else "[0:a]")
                    + ",".join(chain) + ",aresample=48000[a]",
                    "-map", "[a]", "-ac", "1", "-ar", str(SR), str(dst)], check=True)


def read_wav(p):
    with wave.open(str(p)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768


def raw_paths(seg_id, spk):
    if spk == "both":
        return [VOX / f"{seg_id}_phys.mp3", VOX / f"{seg_id}_micro.mp3"]
    return [VOX / f"{seg_id}.mp3"]


async def synth_all():
    sem = asyncio.Semaphore(4)
    async def one(text, spk, out):
        async with sem:
            await tts(text, spk, out)
    jobs = []
    for sid, sc, spk, t, ta, en in SEGMENTS:
        if spk == "both":
            jobs += [one(ta, "phys_en", VOX / f"{sid}_phys.mp3"), one(ta, "micro_en", VOX / f"{sid}_micro.mp3")]
        else:
            jobs.append(one(ta, spk, VOX / f"{sid}.mp3"))
    await asyncio.gather(*jobs)


def layout_scene(segs, durs, limit, tempo, extra=0.0):
    """Place a scene's lines. Target scenes keep their beat times; the others
    start at the first target and pack lines with gaps (+PREPAUSE holds)."""
    out, prev_end, prev_spk = [], -1e9, None
    for k, ((sid, sc, spk, t, ta, en), d) in enumerate(zip(segs, durs)):
        d = d / tempo
        if en is None:              # laughs etc. may overlap
            s = max(t, prev_end - 0.4)
        elif sc in TARGET_SCENES or k == 0:
            s = max(t, prev_end + 0.12)
        else:
            gap = (0.15 if spk == prev_spk else 0.35) + extra + PREPAUSE.get(sid, 0.0)
            s = prev_end + gap
        out.append((s, s + d))
        prev_end, prev_spk = max(prev_end, s + d), spk
    return out, prev_end <= limit


def main():
    print("Synthesising voices…")
    asyncio.run(synth_all())
    # measure natural durations
    durs = {}
    for sid, sc, spk, t, ta, en in SEGMENTS:
        tmp = VOX / f"{sid}_probe.wav"
        to_wav(raw_paths(sid, spk), tmp)
        durs[sid] = len(read_wav(tmp)) / SR
        tmp.unlink()

    timeline, track = [], np.zeros(SR * TOTAL, np.float32)
    for sc in range(1, 8):
        segs = [s for s in SEGMENTS if s[1] == sc]
        d = [durs[s[0]] for s in segs]
        limit = SCENE_DIALOGUE_LIMIT[sc]
        tempo = 1.0
        placed, ok = layout_scene(segs, d, limit, tempo)
        while not ok and tempo < 1.45:
            tempo += 0.01
            placed, ok = layout_scene(segs, d, limit, tempo)
        if ok and tempo == 1.0 and sc not in TARGET_SCENES:
            # spread spare time over the gaps (max +0.4 s each) for natural pacing
            extra = 0.0
            while extra < 0.4:
                trial, fits = layout_scene(segs, d, limit, tempo, extra + 0.02)
                if not fits:
                    break
                extra += 0.02
                placed = trial
        if not ok:
            print(f"WARNING scene {sc}: dialogue overruns by {placed[-1][1]-limit:.2f}s", file=sys.stderr)
        print(f"scene {sc}: {sum(d):5.1f}s of speech, tempo x{tempo:.2f}, ends {max(e for _, e in placed):6.2f}/{limit}")
        for (sid, _, spk, t, ta, en), (s, e) in zip(segs, placed):
            fx = VOICES.get(spk, {}).get("fx")
            wav = VOX / f"{sid}.wav"
            to_wav(raw_paths(sid, spk), wav, fx=fx, tempo=tempo)
            a = read_wav(wav)
            i = int(s * SR)
            seg = a[: max(0, min(len(a), len(track) - i))]
            track[i:i + len(seg)] += seg
            # lip-sync envelope: RMS per video frame, normalised 0..1
            hop = SR // FPS
            n = len(a) // hop + 1
            rms = np.array([np.sqrt(np.mean(a[k*hop:(k+1)*hop] ** 2) + 1e-9) for k in range(n)])
            env = np.clip(rms / (np.percentile(rms, 90) + 1e-6), 0, 1)
            timeline.append(dict(id=sid, scene=sc, speaker=spk, start=round(s, 3),
                                 end=round(s + len(a) / SR, 3), en=en,
                                 env=[round(float(x), 2) for x in env]))

    # dialogue stem
    peak = np.max(np.abs(track))
    if peak > 0.98:
        track *= 0.98 / peak
    with wave.open(str(ROOT / "audio" / "dialogue.wav"), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((track * 32767).astype(np.int16).tobytes())

    # subtitles from real timings
    subs = [x for x in timeline if x["en"]]
    def ts(x):
        h, r = divmod(x, 3600); m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
    lines = []
    for k, x in enumerate(subs):
        scene_end = SCENES[x["scene"] - 1][1]
        nxt = subs[k + 1]["start"] - 0.08 if k + 1 < len(subs) else 1e9
        end = min(max(x["end"] + 0.9, x["start"] + 1.8), nxt, scene_end - 0.05)
        end = max(end, x["end"]) if x["end"] < nxt else nxt
        lines += [str(k + 1), f"{ts(x['start'])} --> {ts(end)}", x["en"], ""]
    (ROOT / "subtitles" / "amr_film_en.srt").write_text("\n".join(lines), encoding="utf-8")
    (BUILD / "timeline.json").write_text(json.dumps(timeline))
    print(f"Wrote {len(timeline)} segments, {len(subs)} subtitle cues")


if __name__ == "__main__":
    main()
