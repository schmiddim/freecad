import os, glob, json, shutil

# Kopiere exports in gallery für GitHub Pages
os.makedirs("gallery/models", exist_ok=True)
for stl in glob.glob("exports/*.stl"):
    shutil.copy(stl, "gallery/models/")

models = []
for stl in glob.glob("exports/*.stl"):
    name = os.path.splitext(os.path.basename(stl))[0]
    imgs = sorted(glob.glob(f"gallery/img/{name}_*.png"))
    models.append({"name": name, "stl": f"models/{name}.stl", "images": imgs})

html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>CAD Gallery</title>
  <script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/loaders/STLLoader.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/controls/OrbitControls.js"></script>
  <style>
    body { font-family: sans-serif; max-width: 1200px; margin: 0 auto; padding: 2rem; background: #fafafa; }
    h1 { color: #333; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1.5rem; }
    .card { border: 1px solid #ddd; border-radius: 8px; padding: 1rem; background: white; }
    .stl-viewer { width: 100%; height: 240px; background: #f0f0f0; border-radius: 4px; }
    .thumbs { display: flex; gap: 6px; margin-top: 8px; flex-wrap: wrap; }
    .thumbs img { width: 80px; height: 60px; object-fit: cover; border-radius: 4px; cursor: pointer; border: 1px solid #ddd; }
    .thumbs img:hover { border-color: #007bff; }
    h3 { margin: 8px 0 4px; font-size: 14px; color: #333; }
    .download { font-size: 12px; color: #007bff; text-decoration: none; }
    .download:hover { text-decoration: underline; }
  </style>
</head>
<body>
<h1>CAD Gallery</h1>
<div class="grid">
"""

for i, m in enumerate(models):
    html += f"""
  <div class="card">
    <div class="stl-viewer" id="viewer-{i}" data-stl="{m['stl']}"></div>
    <h3>{m['name']}</h3>
    <a class="download" href="{m['stl']}" download>Download STL</a>
    <div class="thumbs">
"""
    for img in m["images"]:
        rel = os.path.relpath(img, "gallery")
        html += f'      <img src="{rel}" alt="{m["name"]}">\n'
    html += "    </div>\n  </div>\n"

html += """</div>
<script>
document.querySelectorAll('.stl-viewer').forEach(container => {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xf0f0f0);
  
  const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  container.appendChild(renderer.domElement);
  
  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  
  scene.add(new THREE.AmbientLight(0x404040, 2));
  const dirLight = new THREE.DirectionalLight(0xffffff, 1);
  dirLight.position.set(1, 1, 1);
  scene.add(dirLight);
  
  const loader = new THREE.STLLoader();
  loader.load(container.dataset.stl, geometry => {
    const material = new THREE.MeshStandardMaterial({ color: 0x0077be, metalness: 0.3, roughness: 0.6 });
    const mesh = new THREE.Mesh(geometry, material);
    
    geometry.computeBoundingBox();
    const center = geometry.boundingBox.getCenter(new THREE.Vector3());
    const size = geometry.boundingBox.getSize(new THREE.Vector3());
    mesh.position.sub(center);
    
    scene.add(mesh);
    camera.position.z = Math.max(size.x, size.y, size.z) * 2;
    controls.update();
  });
  
  function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
  }
  animate();
});
</script>
</body></html>"""

with open("gallery/index.html", "w") as f:
    f.write(html)
print(f"Gallery built with {len(models)} models.")
