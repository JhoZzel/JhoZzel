import os
import requests

username = os.environ["CLIST_USERNAME"]
api_key = os.environ["CLIST_API_KEY"]

url = "https://clist.by/api/v2/account/"
params = {
    "username": username,
    "api_key": api_key,
    "format": "json",
}

r = requests.get(url, params=params)
r.raise_for_status()
data = r.json()

objects = data.get("objects", [])

targets = {
    "codeforces.com": "Codeforces",
    "atcoder.jp": "AtCoder",
    "leetcode.com": "LeetCode",
    "codechef.com": "CodeChef",
    "hackerrank.com": "HackerRank",
}

best = {}

for obj in objects:
    resource = obj.get("resource")
    if resource not in targets:
        continue

    rating = obj.get("rating")
    contests = obj.get("n_contests")
    handle = obj.get("handle", "-")

    if resource not in best:
        best[resource] = {
            "label": targets[resource],
            "handle": handle,
            "rating": rating,
            "contests": contests,
        }
        continue

    old_rating = best[resource]["rating"]
    if rating is not None and (old_rating is None or rating > old_rating):
        best[resource] = {
            "label": targets[resource],
            "handle": handle,
            "rating": rating,
            "contests": contests,
        }

rows = []
for resource in ["codeforces.com", "atcoder.jp", "leetcode.com", "codechef.com", "hackerrank.com"]:
    if resource not in best:
        continue

    item = best[resource]
    rating = item["rating"] if item["rating"] is not None else "-"
    contests = item["contests"] if item["contests"] is not None else "-"
    rows.append((item["label"], item["handle"], rating, contests))

height = 170 + 34 * len(rows)

lines_svg = []
y = 95
for label, handle, rating, contests in rows:
    lines_svg.append(
        f'<text x="40" y="{y}" font-size="18" fill="#c9d1d9" font-family="Arial">'
        f'{label}: {handle} | rating: {rating} | contests: {contests}'
        f'</text>'
    )
    y += 34

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="950" height="{height}" viewBox="0 0 950 {height}">
  <rect x="0" y="0" width="950" height="{height}" rx="22" fill="#0d1117"/>
  <rect x="20" y="20" width="910" height="{height - 40}" rx="18" fill="#161b22" stroke="#30363d"/>

  <text x="40" y="58" font-size="34" fill="#ffffff" font-family="Arial" font-weight="bold">
    Joel Chavez (JhoZzel)
  </text>

  <text x="40" y="88" font-size="18" fill="#8b949e" font-family="Arial">
    Competitive Programming Profiles
  </text>

  {''.join(lines_svg)}

  <line x1="40" y1="{height - 52}" x2="910" y2="{height - 52}" stroke="#30363d"/>

  <text x="40" y="{height - 24}" font-size="16" fill="#58a6ff" font-family="Arial">
    clist.by/coder/JhoZzel/
  </text>
</svg>'''

os.makedirs("assets", exist_ok=True)
with open("assets/clist-card.svg", "w", encoding="utf-8") as f:
    f.write(svg)
