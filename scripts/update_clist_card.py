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

text = str(data)[:1000].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="260">
  <rect width="100%" height="100%" rx="18" fill="#0d1117"/>
  <text x="30" y="50" font-size="30" fill="#ffffff" font-family="Arial">Joel Chavez (JhoZzel)</text>
  <text x="30" y="90" font-size="18" fill="#c9d1d9" font-family="Arial">CLIST dynamic card</text>
  <text x="30" y="130" font-size="14" fill="#7ee787" font-family="monospace">API response preview:</text>
  <foreignObject x="30" y="145" width="940" height="90">
    <div xmlns="http://www.w3.org/1999/xhtml" style="color:#c9d1d9;font-family:monospace;font-size:12px;white-space:pre-wrap;">
      {text}
    </div>
  </foreignObject>
  <text x="30" y="245" font-size="14" fill="#58a6ff" font-family="Arial">https://clist.by/coder/JhoZzel/</text>
</svg>"""

os.makedirs("assets", exist_ok=True)
with open("assets/clist-card.svg", "w", encoding="utf-8") as f:
    f.write(svg)
