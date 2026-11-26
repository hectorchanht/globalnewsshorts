#!/usr/bin/env python3
"""Make a narrated vertical video short for Global News Shorts.

Usage: python3 make_short.py <spec.json>

spec.json fields:
  slug        clip slug (may match the companion news.json slug)
  title       headline shown on the video and the clip page
  hook        one-line hook for the clip page / card
  description clip-page description (name the sources in it)
  script      narration text, ~120-150 words for a 45-60s short
  image_url   direct image URL (e.g. the source article's og:image)
  source      source line for the clip page, e.g.
              "Global News Shorts — based on Reuters and AP reporting"
  tags        list of tag strings
  upload_date "YYYY-MM-DD" (default: today, America/Edmonton)

Pipeline: MiniMax TTS (English narrator) -> ffmpeg 720x1280 vertical video
(source image with slow zoom, headline block, burned-in caption chunks,
brand kicker + domain mark) -> poster frame -> faster-whisper captions
appended to src/transcripts.json -> clip registered in src/clips.json.
Then run build.py + push as usual.

Exits non-zero on any failure so callers can fall back loudly, never silently.
"""
import json
import os
import subprocess
import sys
import textwrap
import urllib.request
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
WORK = os.path.join(ROOT, "work")
MMX = os.path.expanduser("~/workspace/custom-connectors/custom.minimax/bin/mmx-api")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
W, H = 720, 1280
FPS = 30


def run(cmd, **kw):
    print("+", " ".join(cmd)[:220], flush=True)
    subprocess.run(cmd, check=True, **kw)


def ffprobe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def tts(text, out_mp3):
    body = {
        "model": "speech-02-hd",
        "text": text,
        "stream": False,
        "voice_setting": {"voice_id": "English_expressive_narrator",
                          "speed": 1.0, "vol": 1.0, "pitch": 0},
        "audio_setting": {"sample_rate": 32000, "bitrate": 128000,
                          "format": "mp3", "channel": 1},
        "language_boost": "English",
    }
    body_path = out_mp3 + ".body.json"
    with open(body_path, "w") as f:
        json.dump(body, f)
    raw = subprocess.run([MMX, "POST", "/v1/t2a_v2", body_path],
                         capture_output=True, text=True, check=True).stdout
    resp = json.loads(raw)
    if (resp.get("base_resp") or {}).get("status_code") != 0:
        raise RuntimeError(f"TTS failed: {resp.get('base_resp')}")
    audio_hex = (resp.get("data") or {}).get("audio")
    if not audio_hex:
        raise RuntimeError("TTS returned no audio")
    with open(out_mp3, "wb") as f:
        f.write(bytes.fromhex(audio_hex))
    return resp.get("extra_info") or {}


def caption_chunks(script, duration):
    """Split the script into <=7-word chunks, timed proportionally by chars."""
    words = script.replace("\n", " ").split()
    chunks, cur = [], ""
    for w in words:
        if len((cur + " " + w).split()) <= 7:
            cur = (cur + " " + w).strip()
        else:
            chunks.append(cur)
            cur = w
    if cur:
        chunks.append(cur)
    total = sum(len(c) for c in chunks) or 1
    out, t = [], 0.0
    for c in chunks:
        d = duration * len(c) / total
        out.append((t, t + d, c))
        t += d
    return out


def main():
    spec = json.load(open(sys.argv[1]))
    slug = spec["slug"]
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(os.path.join(SRC, "videos"), exist_ok=True)
    base = slug.replace("-", "_") + "_gns"
    src_file = base + ".mp4"

    # 1) narration
    mp3 = os.path.join(WORK, slug + ".mp3")
    info = tts(spec["script"], mp3)
    dur = ffprobe_duration(mp3)
    print(f"narration: {dur:.1f}s ({info.get('usage_characters')} chars)")

    # 2) image
    img = os.path.join(WORK, slug + ".jpg")
    req = urllib.request.Request(spec["image_url"],
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    if len(data) < 20000:
        raise RuntimeError(f"image suspiciously small: {len(data)} bytes")
    with open(img, "wb") as f:
        f.write(data)

    # 3) ffmpeg assembly
    frames = int(dur * FPS)
    filters = []
    # cover-crop to 2x canvas, slow zoom to 1.12, output 720x1280
    filters.append(
        f"[0:v]scale=1440:2560:force_original_aspect_ratio=increase,"
        f"crop=1440:2560,zoompan=z='min(1+0.12*on/{frames},1.12)':d={frames}:"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
        f"eq=brightness=-0.06[bg]")
    cur = "[bg]"
    # headline zone + caption zone shading
    filters.append(f"{cur}drawbox=x=0:y=0:w={W}:h=470:color=black@0.52:t=fill[b1]")
    cur = "[b1]"
    filters.append(f"{cur}drawbox=x=0:y=872:w={W}:h=360:color=black@0.55:t=fill[b2]")
    cur = "[b2]"

    def drawtext(textfile=None, text=None, size=40, color="white", x="36",
                 y="100", bold=True, extra=""):
        src = f"textfile='{textfile}'" if textfile else f"text='{text}'"
        font = FONT if bold else FONT_REG
        return (f"drawtext=fontfile={font}:{src}:fontsize={size}:"
                f"fontcolor={color}:x={x}:y={y}{extra}")

    # kicker
    filters.append(f"{cur}{drawtext(text='GLOBAL NEWS SHORTS', size=30, color='#e63946', y='46')}[k]")
    cur = "[k]"
    # headline (pre-wrapped)
    head_path = os.path.join(WORK, slug + "-headline.txt")
    with open(head_path, "w") as f:
        f.write("\n".join(textwrap.wrap(spec["title"], width=19)))
    filters.append(f"{cur}{drawtext(textfile=head_path, size=47, y='104', extra=':line_spacing=14')}[t]")
    cur = "[t]"
    # caption chunks (burned in)
    chunks = caption_chunks(spec["script"], dur)
    for i, (a, b, text) in enumerate(chunks):
        cf = os.path.join(WORK, f"{slug}-cap{i}.txt")
        with open(cf, "w") as f:
            f.write("\n".join(textwrap.wrap(text, width=24)))
        nxt = f"[c{i}]"
        filters.append(
            f"{cur}{drawtext(textfile=cf, size=39, x='(w-text_w)/2', y='946', extra=f':box=1:boxcolor=black@0.45:boxborderw=12:enable=between(t\\,{a:.2f}\\,{b:.2f})')}{nxt}")
        cur = nxt
    # domain mark
    filters.append(f"{cur}{drawtext(text='globalnewsshorts.com', size=23, color='white@0.9', x='w-text_w-24', y='h-38', bold=False)}[vout]")

    out_mp4 = os.path.join(SRC, "videos", src_file)
    run(["ffmpeg", "-y", "-loop", "1", "-i", img, "-i", mp3,
         "-filter_complex", ";".join(filters),
         "-map", "[vout]", "-map", "1:a",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-c:a", "aac", "-b:a", "128k", "-t", f"{dur:.2f}",
         "-movflags", "+faststart", out_mp4])
    total_dur = ffprobe_duration(out_mp4)

    # 4) poster from the assembled frame
    poster = os.path.join(SRC, f"poster-{base}.jpg")
    run(["ffmpeg", "-y", "-ss", "1.2", "-i", out_mp4, "-frames:v", "1",
         "-q:v", "3", poster])

    # 5) captions for the site player (faster-whisper, existing tool;
    #    faster_whisper lives in the fw venv on this machine)
    fw_python = os.path.expanduser("~/workspace/venvs/fw/bin/python3")
    py = fw_python if os.path.exists(fw_python) else sys.executable
    run([py, os.path.join(ROOT, "transcribe.py"), out_mp4, slug])

    # 6) register the clip
    dur_s = int(round(total_dur))
    if dur_s >= 60:
        iso = f"PT{dur_s // 60}M{dur_s % 60}S"
    else:
        iso = f"PT{dur_s}S"
    entry = {
        "slug": slug,
        "title": spec["title"],
        "hook": spec["hook"],
        "description": spec["description"],
        "src_file": src_file,
        "duration_s": dur_s,
        "duration_iso": iso,
        "aspect": "9:16",
        "upload_date": spec.get("upload_date") or date.today().isoformat(),
        "source": spec["source"],
        "tags": spec["tags"],
    }
    clips_path = os.path.join(SRC, "clips.json")
    clips = []
    if os.path.exists(clips_path):
        clips = json.load(open(clips_path))
    clips = [c for c in clips if c.get("slug") != slug] + [entry]
    with open(clips_path, "w") as f:
        json.dump(clips, f, indent=2, ensure_ascii=False)
    print(json.dumps({"ok": True, "slug": slug, "duration_s": dur_s,
                      "video": out_mp4, "poster": poster,
                      "clip_page": f"https://globalnewsshorts.com/clips/{slug}/"},
                     indent=2))


if __name__ == "__main__":
    main()
