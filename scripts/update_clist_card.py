import os
import requests

username = os.environ["CLIST_USERNAME"]
api_key = os.environ["CLIST_API_KEY"]

url = "https://clist.by/api/v2/account/"
params = {
    "username": username,
    "api_key": api_key,
    "format": "json",
    "limit": 200,
}

r = requests.get(url, params=params)
r.raise_for_status()
data = r.json()
objects = data.get("objects", [])

MY_ACCOUNTS = {
    "codeforces.com":    ("Codeforces", "Joel_Uwu",  "#f78166"),
    "atcoder.jp":        ("AtCoder",    "JhoZzel",    "#f0883e"),
    "leetcode.com":      ("LeetCode",   "jhozzel",    "#58a6ff"),
    "dmoj.ca":           ("DMOJ",       "JoelCH04",   "#a371f7"),
    "codechef.com":      ("CodeChef",   "jhozzel",    "#3fb950"),
    "geeksforgeeks.org": ("GeeksForGeeks", "jhozzel", "#39d353"),
}

rows = []
for resource, (label, my_handle, color) in MY_ACCOUNTS.items():
    best = None
    for obj in objects:
        if obj.get("resource") != resource:
            continue
        handle = obj.get("handle", "")
        if handle.lower() != my_handle.lower():
            continue
        rating = obj.get("rating")
        contests = obj.get("n_contests") or 0
        if best is None or (rating is not None and (best["rating"] is None or rating > best["rating"])):
            best = {"label": label, "handle": handle, "rating": rating, "contests": contests, "color": color}
    if best:
        rows.append(best)
    else:
        rows.append({"label": label, "handle": my_handle, "rating": None, "contests": 0, "color": color})

def rating_color(rating, base_color):
    if rating is None:
        return "#7d8590"
    return base_color

ROW_H = 48
HEADER_H = 88
FOOTER_H = 52
height = HEADER_H + ROW_H * len(rows) + FOOTER_H

left_rows = []
right_rows = []
for i, row in enumerate(rows):
    rating_str = str(row["rating"]) if row["rating"] is not None else "—"
    contests_str = str(row["contests"])
    rc = rating_color(row["rating"], row["color"])
    entry = (row["label"], row["handle"], rating_str, contests_str, row["color"], rc)
    if i % 2 == 0:
        left_rows.append(entry)
    else:
        right_rows.append(entry)

lines = []

def make_row(x, y, label, handle, rating, contests, accent, rating_color):
    bar_x = x
    text_x = x + 16
    lines.append(f'<rect x="{bar_x}" y="{y+6}" width="4" height="28" rx="2" fill="{accent}"/>')
    lines.append(f'<text x="{text_x}" y="{y+20}" font-family="Arial,sans-serif" font-size="13" font-weight="700" fill="#e6edf3">{label}</text>')
    lines.append(f'<text x="{text_x}" y="{y+36}" font-family="Arial,sans-serif" font-size="11" fill="#7d8590">{handle}  ·  <tspan fill="{rating_color}">{rating}</tspan>  ·  {contests} contests</text>')

y = HEADER_H
for i, (left, right) in enumerate(zip(left_rows, right_rows if right_rows else [None]*len(left_rows))):
    make_row(32, y, *left)
    if right:
        make_row(352, y, *right)
    y += ROW_H

if len(left_rows) > len(right_rows):
    make_row(32, y - ROW_H if len(right_rows) > 0 else y, *left_rows[-1])

rows_svg = "\n".join(lines)

sep_y = HEADER_H + ROW_H * ((len(rows) + 1) // 2) + (ROW_H if len(rows) % 2 == 0 else 0)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" viewBox="0 0 900 {height}">
  <rect width="900" height="{height}" rx="16" fill="#0d1117"/>
  <rect width="900" height="{height}" rx="16" fill="none" stroke="#30363d" stroke-width="1"/>

  <text x="32" y="44" font-family="Arial,sans-serif" font-size="22" font-weight="700" fill="#e6edf3">Joel Chavez</text>
  <text x="210" y="44" font-family="Arial,sans-serif" font-size="22" font-weight="400" fill="#388bfd">/ JhoZzel</text>
  <text x="32" y="66" font-family="Arial,sans-serif" font-size="13" fill="#7d8590">Competitive Programming Profiles</text>
  <line x1="32" y1="78" x2="868" y2="78" stroke="#21262d" stroke-width="1"/>

  {rows_svg}

  <line x1="32" y1="{height - FOOTER_H + 8}" x2="868" y2="{height - FOOTER_H + 8}" stroke="#21262d" stroke-width="1"/>
  <text x="32" y="{height - 18}" font-family="Arial,sans-serif" font-size="12" fill="#388bfd">clist.by/coder/JhoZzel</text>
  <text x="868" y="{height - 18}" font-family="Arial,sans-serif" font-size="11" fill="#7d8590" text-anchor="end">updated automatically · github-actions</text>
</svg>'''

os.makedirs("assets", exist_ok=True)
with open("assets/clist-card.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("Card generated successfully")
