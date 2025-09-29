import json
from google_play_scraper import app

# Load game package IDs from games.json
with open("games.json", "r", encoding="utf-8") as f:
    package_ids = json.load(f)["games"]

html_output = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Privacy-Friendly Android Games</title>
  <style>
    body { font-family: Arial, sans-serif; background: #fafafa; max-width: 1100px; margin: auto; padding: 20px; }
    h1 { text-align: center; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
    .game { border: 1px solid #ddd; border-radius: 10px; background: white; padding: 15px; text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: transform 0.2s; }
    .game:hover { transform: translateY(-5px); }
    .game img.icon { width: 120px; border-radius: 20%; margin-bottom: 10px; }
    .status { font-weight: bold; color: green; margin: 8px 0; }
    a.badge img { width: 150px; }
  </style>
</head>
<body>
  <h1>🎮 Privacy-Friendly Android Games</h1>
  <div class="grid">
"""

for pkg in package_ids:
    try:
        result = app(pkg, lang="en", country="us")

        title = result.get("title", pkg)
        icon = result.get("icon", "")

        # Data safety status
        data_safety = result.get("dataSafety", {})
        collected = data_safety.get("dataCollected", [])
        shared = data_safety.get("dataShared", [])
        status = "✅ No data collected" if not collected and not shared else "⚠️ Some data collected"

        html_output += f"""
        <div class="game">
          <img src="{icon}" class="icon"/>
          <h2>{title}</h2>
          <p class="status">{status}</p>
          <a class="badge" href="https://play.google.com/store/apps/details?id={pkg}" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg"/>
          </a>
        </div>
        """
    except Exception as e:
        print(f"Error fetching {pkg}: {e}")

html_output += """
  </div>
</body>
</html>
"""

# Save output file
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("✅ index.html generated with clean grid view!")
