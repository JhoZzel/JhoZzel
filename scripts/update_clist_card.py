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

print("All accounts found:")
for obj in objects:
    print(f"  resource={obj.get('resource')} handle={obj.get('handle')} rating={obj.get('rating')} contests={obj.get('n_contests')}")

MY_ACCOUNTS = {
    "codeforces.com":    ("Codeforces",    "Joel_Uwu",  "#f78166"),
    "atcoder.jp":        ("AtCoder",       "JhoZzel",   "#f0883e"),
    "leetcode.com":      ("LeetCode",      "jhozzel",   "#58a6ff"),
    "dmoj.ca":           ("DMOJ",          "JoelCH04",  "#a371f7"),
    "codechef.com":      ("CodeChef",      "jhozzel",   "#3fb950"),
    "geeksforgeeks.org": ("GeeksForGeeks", "jhozzel",   "#39d353"),
}

rows = []
for resource, (label, my_handle, color) in MY_ACCOUNTS.items():
    best = None
    for obj in objects:
        obj_resource = obj.get("resource", "")
        obj_handle = obj.get("handle", "")
        if obj_resource != resource:
            continue
        if obj_handle.lower() != my_handle.lower():
            continue
        rating = obj.get("rating")
        contests = obj.get("n_contests") or 0
        best = {"label": label, "handle": obj_handle, "rating": rating, "contests": contests, "color": color}
        break
    if best:
        rows.append(best)
    else:
        rows.append({"label": label, "handle": my_handle, "rating": None, "contests": 0, "color": color})

def make_row_svg(x, y, label, handle, rating, contests, accent):
    rating_str = str(rating) if rating is not None else "—"
    rating_color = accent if rating is not None else "#7d8590"
    contests_str = str(contests)
    return (
        f'<rect x="{x}" y="{y+8}" width="4" height="26" rx="2" fill="{accent}"/>'
        f'<text x="{x+14}" y="{y+22}" font-family="Arial,sans-serif" font-size="14" font-weight="700" fill="#e6edf3">{label}</text>'
        f'<text x="{x+14}" y="{y+38}" font-family="Arial,sans-serif" font-size="12" fill="#7d8590">'
        f'{handle}  ·  <tspan fill="{rating_color}">{rating_str}</tspan>  ·  {contests_str} contests'
        f'</text>'
    )

W = 900
PAD = 32
COL_W = (W - PAD * 2 - 20) // 2
ROW_H = 56
HEADER_H = 90
FOOTER_H = 50

n_rows_grid = (len(rows) + 1) // 2
height = HEADER_H + ROW_H * n_rows_grid + FOOTER_H

svg_rows = []
for i, row in enumerate(rows):
    col = i % 2
    row_i = i // 2
    x = PAD + col * (COL_W + 20)
    y = HEADER_H + row_i * ROW_H
    svg_rows.append(make_row_svg(x, y, row["label"], row["handle"], row["rating"], row["contests"], row["color"]))

sep_y = HEADER_H + n_rows_grid * ROW_H + 10

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}">
  <rect width="{W}" height="{height}" rx="16" fill="#0d1117"/>
  <rect width="{W}" height="{height}" rx="16" fill="none" stroke="#30363d" stroke-width="1"/>

  <text x="{PAD}" y="46" font-family="Arial,sans-serif" font-size="24" font-weight="700" fill="#e6edf3">Joel Chavez</text>
  <text x="{PAD + 185}" y="46" font-family="Arial,sans-serif" font-size="24" font-weight="400" fill="#388bfd">/ JhoZzel</text>
  <text x="{PAD}" y="68" font-family="Arial,sans-serif" font-size="13" fill="#7d8590">Competitive Programming Profiles</text>
  <line x1="{PAD}" y1="80" x2="{W - PAD}" y2="80" stroke="#21262d" stroke-width="1"/>

  {"".join(svg_rows)}

  <line x1="{PAD}" y1="{sep_y}" x2="{W - PAD}" y2="{sep_y}" stroke="#21262d" stroke-width="1"/>
  <text x="{PAD}" y="{sep_y + 26}" font-family="Arial,sans-serif" font-size="12" fill="#388bfd">clist.by/coder/JhoZzel</text>
  <text x="{W - PAD}" y="{sep_y + 26}" font-family="Arial,sans-serif" font-size="11" fill="#7d8590" text-anchor="end">updated automatically · github-actions</text>
</svg>'''

os.makedirs("assets", exist_ok=True)
with open("assets/clist-card.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("Card generated successfully")
