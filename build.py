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
.player video{width:100%;border-radius:14px;background:#000;aspect-ratio:9/16}
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
.src{max-width:700px;margin:22px auto 0;color:var(--muted);font-size:.85rem}
.src a{color:var(--muted)}
.share{max-width:700px;margin:26px auto 0;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.share .lbl{color:var(--muted);font-size:.85rem;font-weight:700}
.share a,.share button{display:inline-flex;align-items:center;gap:7px;background:#1a2242;border:1px solid #2a3568;color:var(--ink);border-radius:20px;padding:7px 14px;font-size:.83rem;text-decoration:none;cursor:pointer;font-family:inherit}
.share a:hover,.share button:hover{border-color:var(--accent)}
.share svg{width:15px;height:15px;fill:currentColor}
.more{padding:10px 0 70px}
.more h2{font-size:1.3rem;margin-bottom:16px}
.err{text-align:center;padding:90px 20px}
.err h1{font-size:3rem;margin-bottom:10px}
"""

PLAY_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true">'
            '<path d="M8 5v14l11-7z"/></svg>')


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
<nav class="links"><a href="/">Clips</a><a href="{IG}" rel="noopener">Instagram</a></nav>
</div></header>
"""

FOOTER = f"""
<footer class="site"><div class="wrap">
<span>© {date.today().year} {BRAND} — {TAGLINE}.</span>
<span><a href="/feed.xml">RSS</a> · Follow <a href="{IG}" rel="noopener">@globalnewsshorts</a> on Instagram</span>
</div></footer>
<script>
function copyLink(btn,url){{navigator.clipboard.writeText(url).then(()=>{{const t=btn.querySelector('.t');const o=t.textContent;t.textContent='Copied!';setTimeout(()=>t.textContent=o,1500);}});}}
</script>
</body>
</html>
"""


def fmt_dur(s):
    return f"{s // 60}:{s % 60:02d}"


def build():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    os.makedirs(os.path.join(DIST, "videos"))
    os.makedirs(os.path.join(DIST, "posters"))

    shutil.copy(os.path.join(SRC, "logo.png"), os.path.join(DIST, "logo.png"))
    shutil.copy(os.path.join(SRC, "favicon.svg"), os.path.join(DIST, "favicon.svg"))

    # full transcripts from faster-whisper base.en (src/transcripts.json)
    _tx_path = os.path.join(SRC, "transcripts.json")
    _tx = json.load(open(_tx_path)) if os.path.exists(_tx_path) else {}
    for c in CLIPS:
        cues = _tx.get(c["slug"])
        if cues:
            c["cues"] = [x["text"] for x in cues]
            c["transcript"] = " ".join(c["cues"])
            c["cue_count"] = len(cues)

    # ---- index ----
    cards = []
    for c in CLIPS:
        poster = f"/posters/{c['slug']}.jpg"
        cards.append(f"""
<a class="card" href="/clips/{c['slug']}/">
<div class="thumb"><img src="{poster}" alt="{esc(c['title'])}" loading="lazy">
<div class="play"><span>{PLAY_SVG}</span></div>
<span class="badge">{fmt_dur(c['duration_s'])}</span></div>
<div class="body"><h2>{esc(c['title'])}</h2>
<p class="hook">{esc(c['hook'])}</p>
<p class="meta">{c['upload_date']}</p></div></a>""")

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
</section>
<section class="grid">{''.join(cards)}</section>
</main>
""" + FOOTER)
    open(os.path.join(DIST, "index.html"), "w").write(index)

    # ---- clip pages ----
    for c in CLIPS:
        page_url = f"{SITE}/clips/{c['slug']}/"
        video_url = f"{SITE}/videos/{c['slug']}.mp4"
        poster_url = f"{SITE}/posters/{c['slug']}.jpg"
        qtitle = quote(c["title"])
        qurl = quote(page_url, safe="")
        tags = "".join(f"<span>{esc(t)}</span>" for t in c["tags"])
        paras = "".join(f"<p>{esc(x)}</p>" for x in c.get("cues", [c["transcript"]]))
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
        page = (head(f"{c['title']} | {BRAND}", c["description"], page_url,
                     f'<meta property="og:type" content="video.other">\n'
                     f'<meta property="og:image" content="{poster_url}">\n'
                     f'<meta property="og:video" content="{video_url}">\n'
                     f'<meta property="og:video:type" content="video/mp4">\n'
                     f'<meta property="og:video:width" content="720">\n'
                     f'<meta property="og:video:height" content="1280">\n'
                     f'<script type="application/ld+json">{json.dumps(ld)}</script>')
                + HEADER + f"""
<main class="wrap clip">
<div class="crumb"><a href="/">Clips</a> / {esc(c['title'])}</div>
<h1>{esc(c['title'])}</h1>
<p class="hook">{esc(c['hook'])}</p>
<div class="player">
<video controls playsinline preload="metadata" poster="/posters/{c['slug']}.jpg">
<source src="/videos/{c['slug']}.mp4" type="video/mp4">
</video>
</div>
<div class="desc"><p>{esc(c['description'])}</p>
<div class="tags">{tags}</div></div>
<details class="transcript"><summary>Full transcript ({c.get('cue_count', '?')} segments)</summary><div class="tbody">{paras}</div></details>
<p class="ai-note">✦ Transcript auto-generated by AI — may contain errors.</p>
<div class="share">
<span class="lbl">Share</span>
<button onclick="copyLink(this,'{page_url}')" aria-label="Copy link"><svg viewBox="0 0 24 24"><path d="M16 1H4a2 2 0 0 0-2 2v14h2V3h12V1zm3 4H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2zm0 16H8V7h11v14z"/></svg><span class="t">Copy link</span></button>
<a href="https://twitter.com/intent/tweet?text={qtitle}&url={qurl}" rel="noopener" aria-label="Share on X"><svg viewBox="0 0 24 24"><path d="M18.9 1.2h3.7l-8.1 9.2L24 22.8h-7.5l-5.9-7.6-6.7 7.6H.2l8.6-9.9L0 1.2h7.7l5.3 7 6-7zm-1.3 19.4h2L6.6 3.3H4.4l13.2 17.3z"/></svg>Post</a>
<a href="https://www.facebook.com/sharer/sharer.php?u={qurl}" rel="noopener" aria-label="Share on Facebook"><svg viewBox="0 0 24 24"><path d="M24 12a12 12 0 1 0-13.9 11.9v-8.4h-3v-3.5h3V9.4c0-3 1.8-4.7 4.5-4.7 1.3 0 2.7.2 2.7.2v3h-1.5c-1.5 0-2 1-2 1.9V12h3.3l-.5 3.5h-2.8v8.4A12 12 0 0 0 24 12z"/></svg>Share</a>
<a href="https://wa.me/?text={qtitle}%20{qurl}" rel="noopener" aria-label="Share on WhatsApp"><svg viewBox="0 0 24 24"><path d="M12 0a12 12 0 0 0-9.9 18.5L.5 24l5.7-1.5A12 12 0 1 0 12 0zm5.4 16.9c-.2.7-1.3 1.3-1.8 1.4-.5.1-1 .2-3.4-.7-2.9-1.2-4.7-4.1-4.9-4.3-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5s.8 1.9.8 2c.1.1.1.3 0 .5-.3.6-.6.8-.4 1.1.7 1.2 1.6 2 2.8 2.7.3.2.5.1.7-.1l.8-1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.6.4 0 .1 0 .6-.2 1.1z"/></svg>Send</a>
</div>
<div class="src">{esc(c['source'])} · <a href="{c['ig_url']}" rel="noopener">Watch on Instagram</a></div>
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

    # ---- 404 ----
    err = (head("Not found | " + BRAND, "Page not found.", SITE + "/404.html")
           + HEADER + """
<main class="wrap err"><h1>404</h1><p>That clip doesn't exist (yet). <a href="/">Back to clips</a>.</p></main>
""" + FOOTER)
    open(os.path.join(DIST, "404.html"), "w").write(err)

    # ---- sitemap (video extension) ----
    urls = [f"""<url><loc>{SITE}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>"""]
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

    open(os.path.join(DIST, "llms.txt"), "w").write(
        f"# {BRAND}\n\n> {DESC}\n\n## Clips\n\n" +
        "".join(f"- [{c['title']}]({SITE}/clips/{c['slug']}/): {c['description']}\n" for c in CLIPS) +
        f"\nInstagram: {IG}\n")

    print(f"built {len(CLIPS)} clips -> {DIST}")


if __name__ == "__main__":
    build()
