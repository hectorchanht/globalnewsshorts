#!/usr/bin/env python3
"""Build the Global News Shorts static site into dist/.

Add a new clip: drop the mp4 into src/videos-<slug>.mp4 (+ optional poster),
append an entry to CLIPS, run `python3 build.py`.
"""
import html
import json
import os
import shutil
from datetime import date, datetime, timezone
from email.utils import format_datetime
from urllib.parse import quote

SITE = "https://globalnewsshorts.com"
BRAND = "Global News Shorts"
TAGLINE = "USA & world, in shorts"
DESC = ("Global News Shorts — the important USA and world news, in short videos. "
        "Daily clips, straight to the point.")
IG = "https://www.instagram.com/globalnewsshorts/"

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
DIST = os.path.join(ROOT, "dist")

CLIPS = [
    {
        "slug": "fauci-pleads-the-fifth",
        "title": "Fauci Pleads the Fifth",
        "hook": "“Nothing says honesty like taking the Fifth, huh, Doc?”",
        "description": ("Sen. Josh Hawley grills Dr. Fauci in a Senate hearing — asking what day of the week "
                        "it is, what color tie he's wearing — and gets the Fifth Amendment every time. "
                        "111 invocations, zero answers."),
        "transcript": (
            "SEN. JOSH HAWLEY: “Nothing says honesty like taking the Fifth, huh, Doc? Let's try something: "
            "what day of the week is it today?”\n\n"
            "DR. FAUCI: “On the advice of counsel, I respectfully decline to answer based upon my rights "
            "under the Fifth Amendment to the Constitution.”\n\n"
            "SEN. JOSH HAWLEY: “What color tie are you wearing?”\n\n"
            "DR. FAUCI: “On the advice of counsel, I respectfully decline to answer based upon my rights "
            "under the Fifth Amendment to the Constitution.”\n\n"
            "SEN. JOSH HAWLEY: “What color is the carpet in front of you?”\n\n"
            "DR. FAUCI: “On the advice of counsel, I respectfully decline to answer based upon my rights "
            "under the Fifth Amendment to the Constitution.”"
        ),
        "src_file": "DbYXms1KByt_gns.mp4",
        "duration_s": 107,
        "duration_iso": "PT1M47S",
        "upload_date": "2026-10-06",
        "source": "via @senatorhawley on Instagram",
        "ig_url": "https://www.instagram.com/reel/DeJMuEavyCZ/",
        "tags": ["Josh Hawley", "Fauci", "Fifth Amendment", "Senate hearing", "US politics"],
    },
    {
        "slug": "hawley-grills-fauci",
        "title": "Hawley Grills Fauci on 111 Fifth Amendment Invocations",
        "hook": "“He looked very carefully at the carpet.”",
        "description": ("Sen. Hawley explains why he asked Dr. Fauci about his tie and the carpet: to test the "
                        "good faith of 111 Fifth Amendment invocations — including questions with no fear of "
                        "prosecution. “That is an abuse… there's no privilege for any of that.”"),
        "transcript": (
            "SEN. HAWLEY: “The reason that I asked Doctor Fauci what color his tie was and what day of the week "
            "it was and what color the carpet is... He looked, by the way. I thought he was going to answer "
            "that one. He looked very carefully at the carpet.”\n\n"
            "“The reason I asked those questions was precisely to test the good faith nature of his invocation "
            "of the Fifth Amendment.”\n\n"
            "“Given Doctor Fauci's 111 invocations of the Fifth Amendment, including the questions that he could "
            "have no fear of prosecution on. He's not going to get prosecuted for the color of his tie, shows "
            "that he had no interest and no intention of answering any of our questions, and that is an abuse... "
            "There's no privilege for any of that.”"
        ),
        "src_file": "DbtM6fvKmxe_gns.mp4",
        "duration_s": 43,
        "duration_iso": "PT43S",
        "upload_date": "2026-10-06",
        "source": "via @senatorhawley on Instagram",
        "ig_url": "https://www.instagram.com/reel/DbtM6fvKmxe/",
        "tags": ["Josh Hawley", "Fauci", "Fifth Amendment", "Senate hearing", "US politics"],
    },
    {
        "slug": "france-student-protests-tear-gas",
        "title": "France Student Protests: Tear Gas in Paris as Hundreds of Thousands March",
        "hook": "\u201cThey don't really care about us\u201d \u2014 students, teachers and parents flood the streets of Paris.",
        "description": ("France's student protest wave peaks on October 6 with a national day of demonstrations: "
                        "256,000 marchers counted by the Interior Ministry, 450,000 by organizers, up to 100,000 "
                        "in Paris marching from R\u00e9publique to Nation. What began September 21 at a Cr\u00e9teil high "
                        "school over teacher shortages, overcrowded classes and crumbling buildings has spread "
                        "nationwide \u2014 24 schools burned or ransacked, 78 staff injured, over 6,500 arrested, "
                        "mostly minors. Police fired tear gas as the Paris march ended; Prime Minister S\u00e9bastien "
                        "Lecornu suspended classes through the week."),
        "src_file": "france_student_protests_gns.mp4",
        "duration_s": 101,
        "duration_iso": "PT1M41S",
        "upload_date": "2026-10-06",
        "source": "News9 via YouTube",
        "ig_url": "https://www.youtube.com/watch?v=eyOeZz_e22Y",
        "tags": ["France", "student protests", "Paris", "tear gas", "education", "Macron"],
    },
    {
        "slug": "b1-bombers-fairford-iran-threat",
        "title": "US Pulls B-1 Bombers From UK Base Over Iran Threat",
        "hook": "\u201cThey didn't fly out by accident\u2026 there was a threat.\u201d",
        "description": ("Washington pulled about a dozen B-1 bombers from RAF Fairford in England over the "
                        "weekend after intelligence pointed to an Iran-linked threat against the base. The move "
                        "followed the September 27 arrest of five British men near the base over a suspected "
                        "terror plot \u2014 with a seventh arrest in London on Tuesday \u2014 and the UK prime "
                        "minister cited \u2018strong indications\u2019 of Iranian involvement, which Tehran denies. "
                        "President Trump confirmed the bombers \u2018didn't fly out by accident,\u2019 contradicting "
                        "Secretary of State Marco Rubio, who had called it a \u2018regular rotation.\u2019 Vice "
                        "President JD Vance said it was done \u2018out of an abundance of caution.\u2019 Fairford is "
                        "the only European airfield for US heavy bombers and was used in this year's strikes on Iran."),
        "src_file": "b1_bombers_fairford_gns.mp4",
        "duration_s": 56,
        "duration_iso": "PT56S",
        "aspect": "16:9",
        "upload_date": "2026-10-06",
        "source": "U.S. Air Force via DVIDS (public domain file footage)",
        "ig_url": "https://www.dvidshub.net/video/530964/b-1-take-off",
        "tags": ["B-1 bomber", "Iran", "Trump", "RAF Fairford", "US military", "UK"],
    },
    {
        "slug": "brazil-runoff-bolsonaro-lula",
        "title": "Fl\u00e1vio Bolsonaro Stuns Lula, Forces Brazil Runoff",
        "hook": "Polls said Lula would win the first round. They were wrong.",
        "description": ("Brazil is heading to a presidential runoff on October 25 after Fl\u00e1vio Bolsonaro \u2014 "
                        "the 45-year-old son of jailed former president Jair Bolsonaro \u2014 stunned the polls by "
                        "finishing first with 47.03% of the vote, ahead of incumbent President Luiz In\u00e1cio Lula "
                        "da Silva's 45.16%. Lula, 80, admitted he was \u2018convinced\u2019 he would win outright in "
                        "the first round. The 2.2-million-vote gap is one of the narrowest in recent Brazilian "
                        "history, and the two frontrunners took 92% of all votes \u2014 the most polarized first "
                        "round since democracy returned in 1985."),
        "src_file": "brazil_runoff_gns.mp4",
        "duration_s": 75,
        "duration_iso": "PT1M15S",
        "aspect": "16:9",
        "upload_date": "2026-10-06",
        "source": "DW News via YouTube",
        "ig_url": "https://www.youtube.com/watch?v=rFgpCoAV92c",
        "tags": ["Brazil", "Bolsonaro", "Lula", "election", "runoff", "Latin America"],
    },
]

CSS = """*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0b1020;--card:#141b33;--ink:#eef1f8;--muted:#9aa3bd;--accent:#e63946;--navy:#1d2a5c}
body{background:var(--bg);color:var(--ink);font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.6}
a{color:inherit}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
header.top{border-bottom:1px solid #1f2745;padding:14px 0;position:sticky;top:0;background:rgba(11,16,32,.92);backdrop-filter:blur(8px);z-index:10}
.top .wrap{display:flex;align-items:center;gap:12px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;font-weight:800;font-size:1.05rem;letter-spacing:.2px}
.brand img{width:34px;height:34px;border-radius:50%}
nav.links{margin-left:auto;display:flex;gap:18px;font-size:.92rem}
nav.links a{text-decoration:none;color:var(--muted)}
nav.links a:hover{color:var(--ink)}
.hero{padding:56px 0 36px;text-align:center}
.hero .kicker{color:var(--accent);font-weight:700;letter-spacing:2.5px;text-transform:uppercase;font-size:.78rem}
.hero h1{font-size:clamp(2rem,5vw,3.2rem);line-height:1.15;margin:12px 0 10px}
.hero p{color:var(--muted);max-width:620px;margin:0 auto}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:22px;padding:28px 0 60px}
.card{background:var(--card);border:1px solid #232c52;border-radius:14px;overflow:hidden;text-decoration:none;transition:transform .15s,border-color .15s}
.card:hover{transform:translateY(-3px);border-color:var(--accent)}
.thumb{position:relative;aspect-ratio:9/16;overflow:hidden;background:#000}
.thumb img{width:100%;height:100%;object-fit:cover;display:block}
.play{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.play span{width:64px;height:64px;border-radius:50%;background:rgba(230,57,70,.92);display:flex;align-items:center;justify-content:center}
.play svg{width:26px;height:26px;fill:#fff;margin-left:3px}
.badge{position:absolute;bottom:10px;right:10px;background:rgba(0,0,0,.75);font-size:.75rem;padding:3px 9px;border-radius:20px}
.card .body{padding:16px 18px 18px}
.card h2{font-size:1.08rem;line-height:1.35;margin-bottom:6px}
.card .hook{color:var(--muted);font-size:.9rem}
.card .meta{color:var(--muted);font-size:.78rem;margin-top:10px}
footer.site{border-top:1px solid #1f2745;padding:34px 0 46px;color:var(--muted);font-size:.88rem}
footer.site .wrap{display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between}
footer.site a{text-decoration:none}
footer.site a:hover{color:var(--ink)}
.clip{padding:34px 0 60px}
.crumb{color:var(--muted);font-size:.85rem;margin-bottom:14px}
.crumb a{color:var(--muted);text-decoration:none}
.crumb a:hover{color:var(--ink)}
.clip h1{font-size:clamp(1.6rem,4vw,2.4rem);line-height:1.2;margin:8px 0 6px}
.clip .hook{color:var(--muted);font-size:1.05rem;margin-bottom:20px}
.player{max-width:430px;margin:0 auto}
.player .plyr{width:100%}
.clip .desc{max-width:700px;margin:26px auto 0}
.clip .desc p{color:#cfd6ea;margin-bottom:14px}
.tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.tags span{background:#1a2242;border:1px solid #2a3568;border-radius:20px;padding:4px 12px;font-size:.78rem;color:var(--muted)}
details.transcript{max-width:700px;margin:22px auto 0;background:var(--card);border:1px solid #232c52;border-radius:12px;padding:16px 18px}
details.transcript summary{cursor:pointer;font-weight:700}
details.transcript .tbody{margin-top:12px}
details.transcript .tbody p{color:#cfd6ea;font-size:.93rem;margin:0 0 12px}
details.transcript .tbody p:last-child{margin-bottom:0}
.ai-note{max-width:700px;margin:10px auto 0;color:var(--muted);font-size:.78rem;display:flex;align-items:center;gap:6px}
.ts{background:#1a2242;border:1px solid #2a3568;color:#8fb4ff;border-radius:12px;padding:1px 8px;font-size:.72rem;font-family:monospace;cursor:pointer;margin-right:8px;white-space:nowrap}
.ts:hover{border-color:var(--accent);color:#fff}
.prevnext{max-width:700px;margin:30px auto 0;display:flex;justify-content:space-between;gap:12px}
.prevnext a{background:var(--card);border:1px solid #232c52;border-radius:12px;padding:12px 16px;text-decoration:none;flex:1;max-width:48%}
.prevnext a:hover{border-color:var(--accent)}
.prevnext .k{color:var(--muted);font-size:.72rem;text-transform:uppercase;letter-spacing:1px}
.prevnext .t{font-weight:700;font-size:.92rem;margin-top:4px;line-height:1.35}
.prevnext .next{text-align:right}
.taglist{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 60px}
.taglist a{background:var(--card);border:1px solid #232c52;border-radius:20px;padding:8px 18px;text-decoration:none;font-size:.9rem}
.taglist a:hover{border-color:var(--accent)}
.taglist .n{color:var(--muted);font-size:.78rem;margin-left:6px}
.src{max-width:700px;margin:22px auto 0;color:var(--muted);font-size:.85rem}
.src a{color:var(--muted)}
.share{max-width:700px;margin:26px auto 0;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.share .lbl{color:var(--muted);font-size:.85rem;font-weight:700}
.share a,.share button{display:inline-flex;align-items:center;gap:7px;background:#1a2242;border:1px solid #2a3568;color:var(--ink);border-radius:20px;padding:7px 14px;font-size:.83rem;text-decoration:none;cursor:pointer;font-family:inherit}
.share a:hover,.share button:hover{border-color:var(--accent)}
.share svg{width:15px;height:15px;fill:currentColor}
.embed-box{max-width:700px;margin:14px auto 0;background:#10162e;border:1px solid #232c52;border-radius:12px;padding:14px 16px;display:none}
.embed-box.open{display:block}
.embed-box textarea{width:100%;background:#0b1020;color:#cfd6ea;border:1px solid #2a3568;border-radius:8px;padding:10px;font-family:monospace;font-size:.78rem;resize:vertical;min-height:64px}
.embed-box .row{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.embed-box .row strong{font-size:.9rem}
.embed-box .row button{background:#1a2242;border:1px solid #2a3568;color:var(--ink);border-radius:16px;padding:5px 12px;font-size:.78rem;cursor:pointer;font-family:inherit}
.searchbar{max-width:520px;margin:26px auto 0;display:flex;gap:10px}
.searchbar input{flex:1;background:#10162e;border:1px solid #2a3568;border-radius:24px;padding:12px 20px;color:var(--ink);font-size:.95rem;font-family:inherit;outline:none}
.searchbar input:focus{border-color:var(--accent)}
.searchbar input::placeholder{color:var(--muted)}
#search-meta{color:var(--muted);font-size:.85rem;margin:14px 0 0;min-height:1.4em}
.embedpage{margin:0;background:#000;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;padding:12px}
.embedpage .plyr{width:100%;max-width:400px}
.embedpage .t{color:#9aa3bd;font-size:.8rem;margin-top:10px;text-align:center}
.embedpage .t a{color:#cfd6ea}
.more{padding:10px 0 70px}
.more h2{font-size:1.3rem;margin-bottom:16px}
.about{padding:40px 0 70px;max-width:700px}
.about h1{font-size:clamp(1.8rem,4vw,2.6rem);margin:10px 0 18px}
.about p{color:#cfd6ea;margin-bottom:16px}
.about h2{font-size:1.25rem;margin:28px 0 12px}
.about ul{color:#cfd6ea;margin:0 0 16px 20px}
.about li{margin-bottom:8px}
.about .contact{background:var(--card);border:1px solid #232c52;border-radius:12px;padding:18px 20px;margin-top:24px}
.about .contact a{color:#fff;font-weight:700}
.related{padding:8px 0 70px}
.related h2{font-size:1.3rem;margin-bottom:16px}
.tags a{background:#1a2242;border:1px solid #2a3568;border-radius:20px;padding:4px 12px;font-size:.78rem;color:var(--muted);text-decoration:none}
.tags a:hover{border-color:var(--accent);color:var(--ink)}
.err{text-align:center;padding:90px 20px}
.err h1{font-size:3rem;margin-bottom:10px}
/* ---- Plyr video player theme ---- */
.player .plyr{border-radius:14px;overflow:hidden;--plyr-color-main:#e63946}
.embedpage .plyr{border-radius:8px;overflow:hidden;--plyr-color-main:#e63946}
"""

PLAY_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true">'
            '<path d="M8 5v14l11-7z"/></svg>')


# ---- Plyr video player (CDN) ----
PLYR_VER = "3.7.8"
PLYR_CSS_URL = f"https://cdn.jsdelivr.net/npm/plyr@{PLYR_VER}/dist/plyr.css"
PLYR_JS_URL = f"https://cdn.jsdelivr.net/npm/plyr@{PLYR_VER}/dist/plyr.min.js"
PLYR_CSS_TAG = f'<link rel="stylesheet" href="{PLYR_CSS_URL}">'

# Slugs that get a <track> captions element (populated in build() from transcripts.json).
_CAPTION_SLUGS = set()

# Plain (non-f) string: embedded verbatim into every clip + embed page.
PLAYER_JS = """(function(){
var vid='__VID__',ratio='__RATIO__';
var v=document.getElementById(vid);
if(!v)return;
if(!window.Plyr){v.setAttribute('controls','');return;}
var p=new Plyr(v,{
ratio:ratio,
controls:['play-large','play','progress','current-time','duration','mute','volume','captions','settings','fullscreen'],
settings:['captions','speed'],
seekTime:10,
tooltips:{controls:true,seek:true},
captions:{active:true,language:'en',update:true},
speed:{selected:1,options:[0.5,0.75,1,1.25,1.5,2]},
fullscreen:{enabled:true,fallback:true,iosNative:true}
});
window.__plyrPlayers=window.__plyrPlayers||{};
window.__plyrPlayers[vid]=p;
var t0=location.search.match(/[?&]t=(\\d+(?:\\.\\d+)?)/);
if(t0){var t=parseFloat(t0[1]);p.on('loadedmetadata',function(){p.currentTime=t;});}
})();"""


def player_markup(vid, poster, aspect, slug, extra_attrs="", inner=""):
    """Plyr player markup: video + captions track + CDN script + init script."""
    ratio = aspect.replace("/", ":")
    track = (f'<track kind="captions" label="English" srclang="en" '
             f'src="/captions/{slug}.vtt" default>' if slug in _CAPTION_SLUGS else "")
    js = PLAYER_JS.replace("__VID__", vid).replace("__RATIO__", ratio)
    return (
        f'<video id="{vid}" class="plyr" playsinline preload="metadata" '
        f'poster="{poster}" style="aspect-ratio:{aspect}"{extra_attrs}>{inner}{track}</video>'
        f'<script src="{PLYR_JS_URL}"></script>'
        '<script>' + js + '</script>'
    )

def esc(s):
    return html.escape(s, quote=True)


BEACON = ("<!-- Cloudflare Web Analytics -->"
          "<script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' "
          'data-cf-beacon=\'{"token": "859afe99778f4d5b9554a9b5c7c84bb8"}\'></script>'
          "<!-- End Cloudflare Web Analytics -->")


def head(title, desc, canonical, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<meta name="theme-color" content="#0b1020">
{BEACON}
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="{BRAND} clips" href="/feed.xml">
{extra}
<style>{CSS}</style>
</head>
<body>
"""


HEADER = f"""
<header class="top"><div class="wrap">
<a class="brand" href="/"><img src="/logo.png" alt="Global News Shorts logo"><span>Global News Shorts</span></a>
<nav class="links"><a href="/">Clips</a><a href="/about/">About</a><a href="{IG}" rel="noopener">Instagram</a></nav>
</div></header>
"""

FOOTER = f"""
<footer class="site"><div class="wrap">
<span>© {date.today().year} {BRAND} — {TAGLINE}.</span>
<span><a href="/feed.xml">RSS</a> · <a href="/tags/">Tags</a> · <a href="/about/">About</a> · Follow <a href="{IG}" rel="noopener">@globalnewsshorts</a> on Instagram</span>
</div></footer>
<script>
function copyLink(btn,url){{navigator.clipboard.writeText(url).then(()=>{{const t=btn.querySelector('.t');const o=t.textContent;t.textContent='Copied!';setTimeout(()=>t.textContent=o,1500);}});}}
function copyEmbed(btn){{const ta=document.getElementById('embedcode');ta.select();navigator.clipboard.writeText(ta.value).then(()=>{{const o=btn.textContent;btn.textContent='Copied!';setTimeout(()=>btn.textContent=o,1500);}});}}
function seekTo(btn){{const v=document.getElementById('clipvideo');if(!v)return;const t=parseFloat(btn.dataset.t);const ps=window.__plyrPlayers||{{}};const p=ps['clipvideo'];if(p){{p.currentTime=t;p.play();}}else{{v.currentTime=t;v.play();}}v.scrollIntoView({{behavior:'smooth',block:'center'}});}}
</script>
</body>
</html>
"""


def fmt_dur(s):
    return f"{s // 60}:{s % 60:02d}"


def _vtt_time(s):
    s = max(0.0, float(s))
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:06.3f}"


def cues_to_vtt(cues):
    """Convert faster-whisper cues ([{start, end, text}]) to WebVTT."""
    out = ["WEBVTT", ""]
    for x in cues:
        text = x["text"].replace("-->", "->").replace("&", "&amp;").replace("<", "&lt;").strip()
        if not text:
            continue
        out += [_vtt_time(x["start"]) + " --> " + _vtt_time(x["end"]), text, ""]
    return "\n".join(out) + "\n"


def clip_card(c):
    poster = f"/posters/{c['slug']}.jpg"
    ar = c.get("aspect", "9:16").replace(":", "/")
    return f"""
<a class="card" href="/clips/{c['slug']}/">
<div class="thumb" style="aspect-ratio:{ar}"><img src="{poster}" alt="{esc(c['title'])}" loading="lazy">
<div class="play"><span>{PLAY_SVG}</span></div>
<span class="badge">{fmt_dur(c['duration_s'])}</span></div>
<div class="body"><h2>{esc(c['title'])}</h2>
<p class="hook">{esc(c['hook'])}</p>
<p class="meta">{c['upload_date']}</p></div></a>"""


def tag_slug(t):
    return t.lower().replace(" ", "-")


def all_tags():
    seen = {}
    for c in CLIPS:
        for t in c["tags"]:
            seen.setdefault(tag_slug(t), t)
    return seen


def build():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    os.makedirs(os.path.join(DIST, "videos"))
    os.makedirs(os.path.join(DIST, "posters"))
    os.makedirs(os.path.join(DIST, "captions"))

    shutil.copy(os.path.join(SRC, "logo.png"), os.path.join(DIST, "logo.png"))
    shutil.copy(os.path.join(SRC, "favicon.svg"), os.path.join(DIST, "favicon.svg"))

    # IndexNow key file (https://www.indexnow.org/) — optional
    _key = None
    _key_path = os.path.join(SRC, "indexnow.key")
    if os.path.exists(_key_path):
        _key = open(_key_path).read().strip()
        open(os.path.join(DIST, _key + ".txt"), "w").write(_key)

    # full transcripts from faster-whisper base.en (src/transcripts.json)
    _tx_path = os.path.join(SRC, "transcripts.json")
    _tx = json.load(open(_tx_path)) if os.path.exists(_tx_path) else {}
    for c in CLIPS:
        cues = _tx.get(c["slug"])
        if cues:
            c["cues"] = [{"t": x["start"], "text": x["text"]} for x in cues]
            c["transcript"] = " ".join(x["text"] for x in c["cues"])
            c["cue_count"] = len(cues)
            # WebVTT captions for the Plyr <track> element
            vtt = cues_to_vtt(cues)
            open(os.path.join(DIST, "captions", c["slug"] + ".vtt"), "w").write(vtt)
            _CAPTION_SLUGS.add(c["slug"])

    # ---- index ----
    cards = "".join(clip_card(c) for c in CLIPS)

    site_ld = json.dumps({
        "@context": "https://schema.org", "@type": "WebSite",
        "name": BRAND, "url": SITE + "/",
        "description": DESC,
    })
    index = (head(f"{BRAND} — {TAGLINE}", DESC, SITE + "/",
                  '<meta property="og:type" content="website">\n'
                  f'<meta property="og:image" content="{SITE}/logo.png">\n'
                  f'<script type="application/ld+json">{site_ld}</script>')
             + HEADER + f"""
<main class="wrap">
<section class="hero">
<div class="kicker">Global News Shorts</div>
<h1>USA &amp; world, in shorts.</h1>
<p>The important stuff, daily — short clips from the hearings, speeches and moments that matter.</p>
<div class="searchbar"><input id="q" type="search" placeholder="Search clips, topics, transcripts…" aria-label="Search clips" autocomplete="off"></div>
<p id="search-meta"></p>
</section>
<section class="grid" id="clipgrid">{cards}</section>
</main>
<script>
let IDX=null;
async function ensureIdx(){{if(!IDX){{IDX=await (await fetch('/search-index.json')).json();}}return IDX;}}
document.getElementById('q').addEventListener('input',async e=>{{
const q=e.target.value.trim().toLowerCase();
const grid=document.getElementById('clipgrid');const meta=document.getElementById('search-meta');
if(q.length<2){{grid.innerHTML=window._allCards;meta.textContent='';return;}}
const idx=await ensureIdx();
const hits=idx.filter(c=>(c.title+' '+c.hook+' '+c.desc+' '+c.tags+' '+c.text).toLowerCase().includes(q));
meta.textContent=hits.length?hits.length+' result'+(hits.length>1?'s':'')+' for “'+e.target.value.trim()+'”':'No clips match “'+e.target.value.trim()+'”.';
grid.innerHTML=hits.map(window._card).join('');
}});
window._allCards=document.getElementById('clipgrid').innerHTML;
window._card=c=>`<a class="card" href="$${{c.url}}"><div class="thumb"><img src="$${{c.poster}}" alt="$${{c.title}}" loading="lazy"><div class="play"><span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span></div><span class="badge">$${{c.dur}}</span></div><div class="body"><h2>$${{c.title}}</h2><p class="hook">$${{c.hook}}</p><p class="meta">$${{c.date}}</p></div></a>`;
</script>
""" + FOOTER)
    open(os.path.join(DIST, "index.html"), "w").write(index)

    # ---- clip pages ----
    for c in CLIPS:
        page_url = f"{SITE}/clips/{c['slug']}/"
        video_url = f"{SITE}/videos/{c['slug']}.mp4"
        poster_url = f"{SITE}/posters/{c['slug']}.jpg"
        qtitle = quote(c["title"])
        qurl = quote(page_url, safe="")
        ar = c.get("aspect", "9:16")
        ar_css = ar.replace(":", "/")
        vw, vh = (1280, 720) if ar == "16:9" else (720, 1280)
        pmax = "720px" if ar == "16:9" else "430px"
        tags = "".join(
            f'<a href="/tags/{tag_slug(t)}/">{esc(t)}</a>' for t in c["tags"])
        _u = c["ig_url"]
        watch_label = ("Watch on YouTube" if ("youtube.com" in _u or "youtu.be" in _u)
                       else "Watch on DVIDS" if "dvidshub.net" in _u
                       else "Watch on Instagram")
        related = [o for o in CLIPS if o["slug"] != c["slug"]]
        related.sort(key=lambda o: (-len(set(o["tags"]) & set(c["tags"])), o["slug"]))
        rel_html = "".join(clip_card(o) for o in related[:4])
        rel_section = (f"""
<section class="related"><h2>Related clips</h2><div class="grid">{rel_html}</div></section>"""
                       if rel_html else "")
        idx = CLIPS.index(c)
        prev_c = CLIPS[idx - 1] if idx > 0 else None
        next_c = CLIPS[idx + 1] if idx < len(CLIPS) - 1 else None
        pn = ""
        if prev_c or next_c:
            pn = '<nav class="prevnext">'
            pn += (f'<a href="/clips/{prev_c["slug"]}/"><div class="k">← Previous</div>'
                   f'<div class="t">{esc(prev_c["title"])}</div></a>'
                   if prev_c else '<span></span>')
            pn += (f'<a class="next" href="/clips/{next_c["slug"]}/"><div class="k">Next →</div>'
                   f'<div class="t">{esc(next_c["title"])}</div></a>'
                   if next_c else '')
            pn += '</nav>'
        paras = ""
        tx_block = ""
        if c.get("cues"):
            paras = "".join(
                f'<p><button class="ts" data-t="{x["t"]}" '
                f'onclick="seekTo(this)" aria-label="Jump to {fmt_dur(int(x["t"]))}">'
                f'{fmt_dur(int(x["t"]))}</button> {esc(x["text"])}</p>'
                for x in c["cues"])
            nseg = c.get("cue_count", len(c["cues"]))
            tx_block = (f'<details class="transcript"><summary>Full transcript '
                        f'({nseg} segments)</summary><div class="tbody">{paras}</div></details>\n'
                        '<p class="ai-note">\u2726 Transcript auto-generated by AI \u2014 may contain errors.</p>')
        ld = {
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": c["title"],
            "description": c["description"],
            "thumbnailUrl": poster_url,
            "uploadDate": c["upload_date"],
            "duration": c["duration_iso"],
            "contentUrl": video_url,
            "embedUrl": page_url,
            "publisher": {
                "@type": "Organization",
                "name": BRAND,
                "logo": {"@type": "ImageObject", "url": f"{SITE}/logo.png"},
            },
        }
        pmark = player_markup(
            "clipvideo",
            f"/posters/{c['slug']}.jpg",
            ar_css,
            c["slug"],
            "",
            f'<source src="/videos/{c["slug"]}.mp4" type="video/mp4">')
        page = (head(f"{c['title']} | {BRAND}", c["description"], page_url,
                     f'<meta property="og:type" content="video.other">\n'
                     f'<meta property="og:image" content="{poster_url}">\n'
                     f'<meta property="og:video" content="{video_url}">\n'
                     f'<meta property="og:video:type" content="video/mp4">\n'
                     f'<meta property="og:video:width" content="{vw}">\n'
                     f'<meta property="og:video:height" content="{vh}">\n'
                     f'<script type="application/ld+json">{json.dumps(ld)}</script>\n'
                     f'{PLYR_CSS_TAG}')
                + HEADER + f"""
<main class="wrap clip">
<div class="crumb"><a href="/">Clips</a> / {esc(c['title'])}</div>
<h1>{esc(c['title'])}</h1>
<p class="hook">{esc(c['hook'])}</p>
<div class="player" style="max-width:{pmax}">
{pmark}
</div>
<div class="desc"><p>{esc(c['description'])}</p>
<div class="tags">{tags}</div></div>
{tx_block}
<div class="share">
<span class="lbl">Share</span>
<button onclick="copyLink(this,'{page_url}')" aria-label="Copy link"><svg viewBox="0 0 24 24"><path d="M16 1H4a2 2 0 0 0-2 2v14h2V3h12V1zm3 4H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2zm0 16H8V7h11v14z"/></svg><span class="t">Copy link</span></button>
<a href="https://twitter.com/intent/tweet?text={qtitle}&url={qurl}" rel="noopener" aria-label="Share on X"><svg viewBox="0 0 24 24"><path d="M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2.33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8.532.929 1.329 7.754 11.09h-3.182z"/></svg>Post</a>
<a href="https://www.facebook.com/sharer/sharer.php?u={qurl}" rel="noopener" aria-label="Share on Facebook"><svg viewBox="0 0 24 24"><path d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"/></svg>Share</a>
<a href="https://wa.me/?text={qtitle}%20{qurl}" rel="noopener" aria-label="Share on WhatsApp"><svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>Send</a>
<button onclick="document.getElementById('embedbox').classList.toggle('open')" aria-label="Embed this clip"><svg viewBox="0 0 24 24"><path d="M9.4 16.6 4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0 4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg><span class="t">Embed</span></button>
</div>
<div class="embed-box" id="embedbox">
<div class="row"><strong>Embed this clip</strong><button onclick="copyEmbed(this)">Copy code</button></div>
<textarea id="embedcode" readonly>&lt;iframe width="360" height="640" src="{SITE}/embed/{c['slug']}/" frameborder="0" allowfullscreen&gt;&lt;/iframe&gt;</textarea>
</div>
<div class="src">{esc(c['source'])} · <a href="{c['ig_url']}" rel="noopener">{watch_label}</a></div>
{rel_section}
{pn}
</main>
""" + FOOTER)
        d = os.path.join(DIST, "clips", c["slug"])
        os.makedirs(d)
        open(os.path.join(d, "index.html"), "w").write(page)

        # copy media
        shutil.copy(os.path.join("/home/hatch/workspace/goals/hawley-ig-auto-translate-bot/hidden_files/clips",
                                 c["src_file"]),
                    os.path.join(DIST, "videos", c["slug"] + ".mp4"))
        src_poster = os.path.join(SRC, f"poster-{c['src_file'].replace('.mp4', '')}.jpg")
        shutil.copy(src_poster, os.path.join(DIST, "posters", c["slug"] + ".jpg"))

    # ---- more clips section is on index already ----

    # ---- embed pages (noindex) ----
    for c in CLIPS:
        ar = c.get("aspect", "9:16").replace(":", "/")
        emax = "720px" if ar == "16/9" else "400px"
        emark = player_markup(
            "embedvideo",
            f"/posters/{c['slug']}.jpg",
            ar,
            c["slug"],
            f' src="/videos/{c["slug"]}.mp4"')
        epage = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{esc(c['title'])} | {BRAND}</title>
<style>{CSS}</style>
{PLYR_CSS_TAG}
</head>
<body>
<div class="embedpage">
<div style="width:100%;max-width:{emax}">
{emark}
</div>
<div class="t">{esc(c['title'])} — <a href="/clips/{c['slug']}/" target="_blank" rel="noopener">{BRAND}</a></div>
</div>
</body>
</html>
"""
        d = os.path.join(DIST, "embed", c["slug"])
        os.makedirs(d)
        open(os.path.join(d, "index.html"), "w").write(epage)

    # ---- 404 ----
    err = (head("Not found | " + BRAND, "Page not found.", SITE + "/404.html")
           + HEADER + """
<main class="wrap err"><h1>404</h1><p>That clip doesn't exist (yet). <a href="/">Back to clips</a>.</p></main>
""" + FOOTER)
    open(os.path.join(DIST, "404.html"), "w").write(err)

    # ---- about ----
    about = (head(f"About | {BRAND}",
                  "What Global News Shorts is: the important USA and world news, in short videos — plus how to get in touch.",
                  SITE + "/about/",
                  '<meta property="og:type" content="website">\n'
                  f'<meta property="og:image" content="{SITE}/logo.png">')
               + HEADER + """
<main class="wrap about">
<div class="crumb"><a href="/">Home</a> / About</div>
<h1>About Global News Shorts</h1>
<p><strong>Global News Shorts</strong> is USA &amp; world news, in shorts. The important stuff, daily —
short clips from the hearings, speeches and moments that matter, cut straight to the point.</p>
<h2>What you'll find here</h2>
<ul>
<li>Short vertical video clips, most with a full transcript you can read or search.</li>
<li>Clips are chosen for substance — what was actually said, not the spin around it.</li>
<li>New clips are added as they're published on our Instagram.</li>
</ul>
<h2>Transcripts</h2>
<p>Most clip pages carry a full transcript auto-generated by AI. It's there so you can
search the words and skim the substance — but AI can mishear, so treat the video itself
as the source of truth. A few clips (heavy crowd noise, music or chanting) ship without one.</p>
<div class="contact">
<strong>Tips &amp; corrections:</strong>
<a href="mailto:hello@globalnewsshorts.com">hello@globalnewsshorts.com</a><br>
<span style="color:var(--muted);font-size:.85rem">Follow <a href="https://www.instagram.com/globalnewsshorts/" rel="noopener">@globalnewsshorts</a> on Instagram for the daily clips.</span>
</div>
</main>
""" + FOOTER)
    d = os.path.join(DIST, "about")
    os.makedirs(d)
    open(os.path.join(d, "index.html"), "w").write(about)

    # ---- tag pages ----
    tag_map = all_tags()
    for slug, name in tag_map.items():
        tagged = [c for c in CLIPS if tag_slug(name) == slug]
        cards = "".join(clip_card(c) for c in tagged)
        tpage = (head(f"{name} clips | {BRAND}",
                      f"Global News Shorts clips tagged {name}.",
                      f"{SITE}/tags/{slug}/",
                      '<meta property="og:type" content="website">\n'
                      f'<meta property="og:image" content="{SITE}/logo.png">')
                 + HEADER + f"""
<main class="wrap">
<div class="crumb" style="margin-top:24px"><a href="/">Clips</a> / {esc(name)}</div>
<h1 style="margin:8px 0 4px">#{esc(name)}</h1>
<p style="color:var(--muted);margin-bottom:8px">{len(tagged)} clip{'s' if len(tagged)!=1 else ''}</p>
<section class="grid">{cards}</section>
</main>
""" + FOOTER)
        d = os.path.join(DIST, "tags", slug)
        os.makedirs(d)
        open(os.path.join(d, "index.html"), "w").write(tpage)

    # ---- tags index ----
    def _tag_count(slug):
        return sum(1 for c in CLIPS if slug in [tag_slug(t) for t in c["tags"]])
    taglinks = "".join(
        f'<a href="/tags/{slug}/">#{esc(name)}<span class="n">{_tag_count(slug)}</span></a>'
        for slug, name in sorted(tag_map.items(), key=lambda kv: kv[1].lower()))
    tidx = (head(f"All tags | {BRAND}",
                  "Browse Global News Shorts clips by topic tag.",
                  f"{SITE}/tags/",
                  '<meta property="og:type" content="website">\n'
                  f'<meta property="og:image" content="{SITE}/logo.png">')
            + HEADER + f"""
<main class="wrap">
<div class="crumb" style="margin-top:24px"><a href="/">Clips</a> / Tags</div>
<h1 style="margin:8px 0 4px">Browse by tag</h1>
<p style="color:var(--muted)">Every topic we clip, A–Z.</p>
<div class="taglist">{taglinks}</div>
</main>
""" + FOOTER)
    d = os.path.join(DIST, "tags")
    open(os.path.join(d, "index.html"), "w").write(tidx)

    # ---- sitemap (video extension) ----
    urls = [f"""<url><loc>{SITE}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>""",
            f"""<url><loc>{SITE}/about/</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>""",
            f"""<url><loc>{SITE}/tags/</loc><changefreq>weekly</changefreq><priority>0.4</priority></url>"""]
    for slug in tag_map:
        urls.append(f"""<url><loc>{SITE}/tags/{slug}/</loc><changefreq>weekly</changefreq><priority>0.4</priority></url>""")
    for c in CLIPS:
        urls.append(f"""<url><loc>{SITE}/clips/{c['slug']}/</loc><changefreq>monthly</changefreq><priority>0.8</priority>
<video:video>
<video:thumbnail_loc>{SITE}/posters/{c['slug']}.jpg</video:thumbnail_loc>
<video:title>{esc(c['title'])}</video:title>
<video:description>{esc(c['description'])}</video:description>
<video:content_loc>{SITE}/videos/{c['slug']}.mp4</video:content_loc>
<video:duration>{c['duration_s']}</video:duration>
<video:publication_date>{c['upload_date']}</video:publication_date>
<video:family_friendly>yes</video:family_friendly>
<video:live>no</video:live>
</video:video></url>""")
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
          ' xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">\n'
          + "\n".join(urls) + "\n</urlset>\n")
    open(os.path.join(DIST, "sitemap.xml"), "w").write(sm)

    open(os.path.join(DIST, "robots.txt"), "w").write(
        "User-agent: *\nAllow: /\n\nSitemap: https://globalnewsshorts.com/sitemap.xml\n")

    # ---- RSS feed ----
    items = []
    for c in CLIPS:
        vpath = os.path.join(DIST, "videos", c["slug"] + ".mp4")
        vsize = os.path.getsize(vpath)
        pub = format_datetime(datetime.fromisoformat(c["upload_date"]).replace(
            hour=12, tzinfo=timezone.utc))
        items.append(f"""<item>
<title>{esc(c['title'])}</title>
<link>{SITE}/clips/{c['slug']}/</link>
<guid isPermaLink="true">{SITE}/clips/{c['slug']}/</guid>
<description>{esc(c['description'])}</description>
<pubDate>{pub}</pubDate>
<enclosure url="{SITE}/videos/{c['slug']}.mp4" length="{vsize}" type="video/mp4"/>
</item>""")
    rss = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n<channel>\n'
           f"<title>{BRAND} — clips</title>\n"
           f"<link>{SITE}/</link>\n"
           f"<description>{esc(DESC)}</description>\n"
           "<language>en-us</language>\n"
           + "\n".join(items) + "\n</channel>\n</rss>\n")
    open(os.path.join(DIST, "feed.xml"), "w").write(rss)

    # ---- search index ----
    sidx = [{
        "title": c["title"],
        "hook": c["hook"],
        "desc": c["description"],
        "tags": " ".join(c["tags"]),
        "text": c.get("transcript", ""),
        "url": f"/clips/{c['slug']}/",
        "poster": f"/posters/{c['slug']}.jpg",
        "dur": fmt_dur(c["duration_s"]),
        "date": c["upload_date"],
    } for c in CLIPS]
    open(os.path.join(DIST, "search-index.json"), "w").write(json.dumps(sidx))

    open(os.path.join(DIST, "llms.txt"), "w").write(
        f"# {BRAND}\n\n> {DESC}\n\n## Clips\n\n" +
        "".join(f"- [{c['title']}]({SITE}/clips/{c['slug']}/): {c['description']}\n" for c in CLIPS) +
        f"\nInstagram: {IG}\n")

    print(f"built {len(CLIPS)} clips -> {DIST}")


if __name__ == "__main__":
    build()
