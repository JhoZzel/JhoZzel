import os
import requests

username = os.environ["CLIST_USERNAME"]
api_key = os.environ["CLIST_API_KEY"]

# DEBUG: buscar todos los handles de leetcode asociados a tu cuenta
debug_url = "https://clist.by/api/v2/account/"
debug_params = {
    "username": username,
    "api_key": api_key,
    "format": "json",
    "resource": "leetcode.com",
    "limit": 50,
}
r2 = requests.get(debug_url, params=debug_params)
data2 = r2.json()
print("=== ALL LEETCODE ACCOUNTS ===")
for obj in data2.get("objects", []):
    print(f"  handle={obj.get('handle')} rating={obj.get('rating')} contests={obj.get('n_contests')}")
print("=== END ===")

MY_ACCOUNTS = [
    ("codeforces.com",    "Joel_Uwu",  "Codeforces",    "#f78166"),
    ("atcoder.jp",        "JhoZzel",   "AtCoder",        "#f0883e"),
    ("leetcode.com",      "JhoZzel",   "LeetCode",       "#58a6ff"),
    ("dmoj.ca",           "JoelCH04",  "DMOJ",           "#a371f7"),
    ("codechef.com",      "jhozzel",   "CodeChef",       "#3fb950"),
    ("geeksforgeeks.org", "jhozzel",   "GeeksForGeeks",  "#39d353"),
]

rows = []
for resource, handle, label, color in MY_ACCOUNTS:
    url = "https://clist.by/api/v2/account/"
    params = {
        "username": username,
        "api_key": api_key,
        "format": "json",
        "resource": resource,
        "handle": handle,
        "limit": 10,
    }
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        objects = data.get("objects", [])
        print(f"{label}: found {len(objects)} results")
        for obj in objects:
            print(f"  handle={obj.get('handle')} rating={obj.get('rating')} contests={obj.get('n_contests')}")

        match = next((o for o in objects if o.get("handle", "").lower() == handle.lower()), None)
        if match:
            rows.append({
                "label": label,
                "handle": match.get("handle", handle),
                "rating": match.get("rating"),
                "contests": match.get("n_contests") or 0,
                "color": color,
            })
        else:
            rows.append({"label": label, "handle": handle, "rating": None, "contests": 0, "color": color})
    except Exception as e:
        print(f"{label}: error — {e}")
        rows.append({"label": label, "handle": handle, "rating": None, "contests": 0, "color": color})

def make_row_svg(x, y, label, handle, rating, contests, accent):
    rating_str = str(rating) if rating is not None else "—"
    rating_color = accent if rating is not None else "#7d8590"
    return (
        f'<rect x="{x}" y="{y+8}" width="4" height="26" rx="2" fill="{accent}"/>'
        f'<text x="{x+14}" y="{y+22}" font-family="Arial,sans-serif" font-size="14" font-weight="700" fill="#e6edf3">{label}</text>'
        f'<text x="{x+14}" y="{y+38}" font-family="Arial,sans-serif" font-size="12" fill="#7d8590">'
        f'{handle}  ·  <tspan fill="{rating_color}">{rating_str}</tspan>  ·  {contests} contests'
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
