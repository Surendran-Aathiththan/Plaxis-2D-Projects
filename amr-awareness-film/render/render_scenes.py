#!/usr/bin/env python3
"""Render the seven scene clips (clips/sceneN.mp4) frame by frame with skia,
or stills for checking:  render_scenes.py --still 12.5 out.png"""
import subprocess, sys, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
import skia

sys.path.insert(0, str(Path(__file__).parent))
from gfx import W, H
from timing import SCENES, FPS, ROOT


def scene_fn(i):
    import importlib
    mod = importlib.import_module("scenes_a" if i <= 3 else "scenes_b" if i == 4 else "scenes_c")
    return getattr(mod, f"scene{i}")


def scene_of(t):
    for i, (a, b) in enumerate(SCENES, 1):
        if a <= t < b:
            return i
    return 7


def draw_frame(arr, t, i=None):
    i = i or scene_of(t)
    surf = skia.Surface(arr)
    cv = surf.getCanvas()
    cv.clear(skia.ColorBLACK)
    scene_fn(i)(cv, t)
    surf.flushAndSubmit()


def still(t, out):
    arr = np.zeros((H, W, 4), np.uint8)
    draw_frame(arr, t)
    skia.Image.fromarray(arr).save(out, skia.kPNG)


def render_scene(i, out_dir, start_frame=None, end_frame=None):
    a, b = SCENES[i - 1]
    n = int(round((b - a) * FPS))
    out = Path(out_dir) / f"scene{i}.mp4"
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                           "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    arr = np.zeros((H, W, 4), np.uint8)
    t0 = time.time()
    for f in range(n):
        draw_frame(arr, a + f / FPS, i)
        ff.stdin.write(arr.tobytes())
    ff.stdin.close()
    ff.wait()
    return i, n, time.time() - t0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--still":
        still(float(sys.argv[2]), sys.argv[3])
        sys.exit()
    which = [int(x) for x in sys.argv[1:]] or list(range(1, 8))
    out_dir = ROOT / "clips"
    out_dir.mkdir(exist_ok=True)
    # longest scenes first so the 4 workers finish together
    which.sort(key=lambda i: -(SCENES[i - 1][1] - SCENES[i - 1][0]))
    with ProcessPoolExecutor(max_workers=4) as ex:
        for i, n, dt in ex.map(render_scene, which, [out_dir] * len(which)):
            print(f"scene{i}: {n} frames in {dt:.0f}s ({n / dt:.1f} fps)", flush=True)
