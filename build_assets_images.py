import base64
from pathlib import Path

IMG_DIR = Path("img")
OUT_FILE = Path("assets-images.js")

# Extensiones que vamos a empaquetar
EXTS = {".webp", ".png", ".jpg", ".jpeg", ".gif"}

def mime_for(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".webp": return "image/webp"
    if ext == ".png":  return "image/png"
    if ext in (".jpg", ".jpeg"): return "image/jpeg"
    if ext == ".gif":  return "image/gif"
    return "application/octet-stream"

pairs = []

for f in IMG_DIR.rglob("*"):
    if f.is_file() and f.suffix.lower() in EXTS:
        rel = f.as_posix()                 # "img/items/xxx.webp"
        b64 = base64.b64encode(f.read_bytes()).decode("ascii")
        mime = mime_for(f)
        data_uri = f"data:{mime};base64,{b64}"
        pairs.append((rel, data_uri))

pairs.sort(key=lambda x: x[0])

with OUT_FILE.open("w", encoding="utf-8") as w:
    w.write("// Auto-generado. NO editar a mano.\n")
    w.write("window.ASSET_IMAGES = window.ASSET_IMAGES || {};\n")
    for k, v in pairs:
        # Ojo: claves EXACTAS, respetando mayúsculas/minúsculas
        w.write(f'window.ASSET_IMAGES[{k!r}] = {v!r};\n')

print(f"OK -> {OUT_FILE} con {len(pairs)} imágenes")
