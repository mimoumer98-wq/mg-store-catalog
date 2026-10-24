#!/usr/bin/env python3
# Complete les icones manquantes en COMPOSANT l'icone adaptative (fond + logo)
# a partir des propres fichiers de chaque app. Ne touche pas aux iconUrl deja presentes.
import json, os, re, subprocess, zipfile, glob, io
from PIL import Image

AAPT2 = "C:/Users/acer/AppData/Local/Android/Sdk/build-tools/35.0.0/aapt2.exe"
APK_DIRS = ["C:/Users/acer/Desktop/apk", os.path.abspath("apps")]
PAGES = "https://mimoumer98-wq.github.io/mg-store-catalog/icons"
os.makedirs("icons", exist_ok=True)

apks = []
for d in APK_DIRS:
    apks += glob.glob(os.path.join(d, "*.apk"))

def pkg_of(apk):
    out = subprocess.run([AAPT2, "dump", "badging", apk], capture_output=True, text=True, errors="ignore").stdout
    m = re.search(r"package: name='([^']+)'", out)
    return m.group(1) if m else None

def load(z, name):
    return Image.open(io.BytesIO(z.read(name))).convert("RGBA")

def biggest(z, names):
    names = [n for n in names if n.lower().endswith((".png", ".webp"))]
    if not names: return None
    return max(names, key=lambda n: z.getinfo(n).file_size)

def compose_adaptive(apk):
    """Compose fond+logo de l'icone adaptative -> PIL.Image, ou None."""
    with zipfile.ZipFile(apk) as z:
        names = z.namelist()
        ic = [n for n in names if re.search(r"(mipmap|drawable)", n, re.I) and
              ("launcher" in n.lower() or "icon" in n.lower())]
        fg = biggest(z, [n for n in ic if "foreground" in n.lower()])
        bg = biggest(z, [n for n in ic if "background" in n.lower()])
        if not fg:
            return None
        fgi = load(z, fg)
        size = max(fgi.size)
        if bg:
            bgi = load(z, bg).resize((size, size))
        else:
            bgi = Image.new("RGBA", (size, size), (245, 246, 248, 255))
        fgi = fgi.resize((size, size))
        canvas = Image.alpha_composite(bgi, fgi)
        # recadre la zone de securite (centre 72/108) pour que le logo remplisse
        pad = int(size * (18/108))
        canvas = canvas.crop((pad, pad, size - pad, size - pad))
        return canvas

pkg_apk = {}
for apk in apks:
    p = pkg_of(apk)
    if p and p not in pkg_apk:
        pkg_apk[p] = apk

cat = json.load(open("catalog.json", encoding="utf-8"))
done, skip = [], []
for a in cat["apps"]:
    if a.get("iconUrl"):
        continue  # deja une icone -> on garde
    pkg = a.get("packageName")
    apk = pkg_apk.get(pkg)
    if not apk:
        skip.append(a["name"] + " (pas d'APK)"); continue
    try:
        img = compose_adaptive(apk)
        if img is None:
            skip.append(a["name"] + " (vectoriel pur)"); continue
        dest = os.path.join("icons", pkg + ".png")
        img.save(dest, "PNG")
        a["iconUrl"] = f"{PAGES}/{pkg}.png"
        done.append(f"{a['name']} -> {pkg}.png")
    except Exception as e:
        skip.append(f"{a['name']} (err {e})")

json.dump(cat, open("catalog.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"ICONES COMPOSEES: {len(done)}")
for x in done: print("  +", x)
print(f"\nRESTENT EN AVATAR: {len(skip)}")
for x in skip: print("  -", x)
