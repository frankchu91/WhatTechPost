#!/usr/bin/env python3
"""Render a grouped horizontal bar chart to PNG (HTML+CSS via headless Chrome).

Spec is JSON on stdin or --spec file:
{
  "title": "Kitesurf vs Chromium (lower is better)",
  "series": [{"name":"Kitesurf","color":"#f6821f"},{"name":"Chromium","color":"#64748b"}],
  "groups": [
    {"label":"Screenshot CPU (ms)", "values":[380,1173]},
    {"label":"HTML extract CPU (ms)", "values":[229,877]},
    {"label":"Memory (MiB)", "values":[40,270]}
  ]
}
Usage: python3 scripts/make_barchart.py --spec chart.json --out assets/foo.png
"""
import argparse, html, json, os, subprocess, sys, tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build_html(spec):
    series = spec["series"]
    gmax = max(v for g in spec["groups"] for v in g["values"]) or 1
    legend = "".join(
        f'<span class="lg"><i style="background:{s["color"]}"></i>{html.escape(s["name"])}</span>'
        for s in series)
    rows = []
    for g in spec["groups"]:
        bars = ""
        for i, v in enumerate(g["values"]):
            pct = 100 * v / gmax
            bars += (f'<div class="barrow"><div class="bar" style="width:{pct:.1f}%;'
                     f'background:{series[i]["color"]}"></div><div class="val">{v:,}</div></div>')
        rows.append(f'<div class="group"><div class="glabel">{html.escape(g["label"])}</div>'
                    f'<div class="bars">{bars}</div></div>')
    body = "".join(rows)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
* {{ margin:0; box-sizing:border-box; }}
body {{ width:1000px; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  background:#0a0f1c; color:#e7edf7; padding:40px 48px; }}
.title {{ font-size:26px; font-weight:800; letter-spacing:-.5px; }}
.legend {{ margin:10px 0 26px; color:#93a4c0; font-size:15px; display:flex; gap:22px; }}
.lg {{ display:flex; align-items:center; gap:8px; }}
.lg i {{ width:14px; height:14px; border-radius:3px; display:inline-block; }}
.group {{ margin-bottom:22px; }}
.glabel {{ font-size:15px; color:#b8c4d8; margin-bottom:8px; font-weight:600; }}
.barrow {{ display:flex; align-items:center; gap:12px; margin:6px 0; }}
.bar {{ height:26px; border-radius:6px; min-width:2px; }}
.val {{ font-family:"SF Mono",ui-monospace,Menlo,monospace; font-size:15px; color:#cdd8ea; }}
.brand {{ margin-top:16px; text-align:right; font-size:13px; font-weight:700; letter-spacing:2px; color:#41506a; }}
</style></head><body>
<div class="title">{html.escape(spec["title"])}</div>
<div class="legend">{legend}</div>
{body}
<div class="brand">WHATTECHPOST</div>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    spec = json.load(open(a.spec)) if a.spec else json.load(sys.stdin)
    out = a.out if os.path.isabs(a.out) else os.path.join(ROOT, a.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(build_html(spec)); tmp = f.name
    # fit window height to content: header ~170 + ~76 per group + brand/pad ~50
    hgt = 150 + 76 * len(spec["groups"]) + 60
    subprocess.run([CHROME, "--headless", "--disable-gpu", f"--screenshot={out}",
                    f"--window-size=1000,{hgt}", "--hide-scrollbars", tmp],
                   check=True, capture_output=True)
    os.unlink(tmp)
    print("wrote", out)


if __name__ == "__main__":
    main()
