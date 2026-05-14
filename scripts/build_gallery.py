import os, glob, json

models = []
for stl in glob.glob("exports/*.stl"):
    name = os.path.splitext(os.path.basename(stl))[0]
    imgs = glob.glob(f"gallery/img/{name}_*.png")
    models.append({"name": name, "stl": f"../exports/{name}.stl", "images": imgs})

html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>CAD Gallery</title>
  <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
  <style>
    body { font-family: sans-serif; max-width: 1200px; margin: 0 auto; padding: 2rem; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }
    .card { border: 1px solid #ddd; border-radius: 8px; padding: 1rem; }
    model-viewer { width: 100%; height: 240px; background: #f5f5f5; border-radius: 4px; }
    .thumbs { display: flex; gap: 6px; margin-top: 8px; }
    .thumbs img { width: 80px; height: 60px; object-fit: cover; border-radius: 4px; cursor: pointer; }
    h3 { margin: 8px 0 4px; font-size: 14px; }
  </style>
</head>
<body>
<h1>CAD Gallery</h1>
<div class="grid">
"""

for m in models:
    html += f"""
  <div class="card">
    <model-viewer src="{m['stl']}" auto-rotate camera-controls></model-viewer>
    <h3>{m['name']}</h3>
    <div class="thumbs">
"""
    for img in m["images"]:
        rel = os.path.relpath(img, "gallery")
        html += f'      <img src="{rel}" alt="{m["name"]}">\n'
    html += "    </div>\n  </div>\n"

html += "</div></body></html>"

with open("gallery/index.html", "w") as f:
    f.write(html)
print(f"Gallery built with {len(models)} models.")
