#!/usr/bin/env python3
"""Generate a branded dev.to cover image (1000x420 PNG) from HTML+CSS via headless Chrome.

Usage:
  python3 scripts/make_cover.py --kicker "HANDS-ON" --title "..." \
      --meta "github.com/NVIDIA-NeMo/Switchyard" --accent "#38bdf8" --out assets/foo.png

Covers are committed to the repo; reference them in a post's front matter as
  cover_image: https://raw.githubusercontent.com/<user>/<repo>/main/assets/foo.png
"""
import argparse, html, os, subprocess, sys, tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8"><style>
* {{ margin:0; box-sizing:border-box; }}
body {{ width:1000px; height:420px; overflow:hidden;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
.card {{ width:1000px; height:420px; position:relative;
  background:radial-gradient(1200px 500px at 80% -10%, {accent}22, transparent 60%), linear-gradient(135deg,#0a0f1c 0%,#111a2e 100%);
  color:#fff; padding:56px 64px; display:flex; flex-direction:column; justify-content:space-between; }}
.grid {{ position:absolute; inset:0; background-image:linear-gradient(#ffffff08 1px,transparent 1px),linear-gradient(90deg,#ffffff08 1px,transparent 1px); background-size:40px 40px; }}
.kicker {{ font-size:15px; letter-spacing:4px; font-weight:800; color:{accent}; position:relative; }}
.title {{ font-size:{tsize}px; line-height:1.08; font-weight:800; letter-spacing:-1px; position:relative; max-width:850px; }}
.foot {{ display:flex; align-items:center; gap:14px; position:relative; }}
.dot {{ width:10px; height:10px; border-radius:50%; background:{accent}; box-shadow:0 0 16px {accent}; }}
.meta {{ font-family:"SF Mono",ui-monospace,Menlo,monospace; font-size:16px; color:#93a4c0; }}
.brand {{ margin-left:auto; font-size:14px; font-weight:700; letter-spacing:2px; color:#5b6b86; }}
</style></head><body><div class="card"><div class="grid"></div>
<div class="kicker">{kicker}</div>
<div class="title">{title}</div>
<div class="foot"><div class="dot"></div><div class="meta">{meta}</div><div class="brand">WHATTECHPOST</div></div>
</div></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kicker", default="TECH ANALYSIS")
    ap.add_argument("--title", required=True)
    ap.add_argument("--meta", default="")
    ap.add_argument("--accent", default="#38bdf8")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    tsize = 52 if len(a.title) < 46 else (44 if len(a.title) < 64 else 38)
    doc = TEMPLATE.format(kicker=html.escape(a.kicker), title=html.escape(a.title),
                          meta=html.escape(a.meta), accent=a.accent, tsize=tsize)
    out = a.out if os.path.isabs(a.out) else os.path.join(ROOT, a.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(doc); tmp = f.name
    subprocess.run([CHROME, "--headless", "--disable-gpu", f"--screenshot={out}",
                    "--window-size=1000,420", "--hide-scrollbars", tmp],
                   check=True, capture_output=True)
    os.unlink(tmp)
    print("wrote", out)


if __name__ == "__main__":
    main()
