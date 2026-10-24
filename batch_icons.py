#!/usr/bin/env python3
# Extrait l'icone REELLE de chaque app (depuis son APK) et la branche dans catalog.json.
import json, os, re, subprocess, zipfile, glob

AAPT2 = "C:/Users/acer/AppData/Local/Android/Sdk/build-tools/35.0.0/aapt2.exe"
APK_DIRS = ["C:/Users/acer/Desktop/apk", os.path.abspath("apps")]
PAGES = "https://mimoumer98-wq.github.io/mg-store-catalog/icons"
os.makedirs("icons", exist_ok=True)

# index tous les APK dispo localement
apks = []
for d in APK_DIRS:
    apks += glob.glob(os.path.join(d, "*.apk"))

def info(apk):
    out = subprocess.run([AAPT2, "dump", "badging", apk], capture_output=True, text=True, errors="ignore").stdout
    pkg = re.search(r"package: name='([^']+)'", out)
    if not pkg: return None, None
    # icones par densite -> on prend la plus haute densite en PNG/WEBP (raster)
    icons = re.findall(r"application-icon-(\d+):'([^']+)'", out)
    best = None
    for dpi, path in sorted(icons, key=lambda x: int(x[0])):
        if path.lower().endswith((".png", ".webp")):
            best = path
    if not best:
        m = re.search(r"application:.*icon='([^']+)'", out)
        if m and m.group(1).lower().endswith((".png", ".webp")): best = m.group(1)
    return pkg.group(1), best

# package -> (apk, icon_res_path)
pkg_map = {}
for apk in apks:
    pkg, icon = info(apk)
    if pkg and icon and pkg not in pkg_map:
        pkg_map[pkg] = (apk, icon)

cat = json.load(open("catalog.json", encoding="utf-8"))
done, skip = [], []
for a in cat["apps"]:
    pkg = a.get("packageName")
    if pkg not in pkg_map:
        skip.append(a["name"]); continue
    apk, iconpath = pkg_map[pkg]
    ext = ".webp" if iconpath.lower().endswith(".webp") else ".png"
    dest = os.path.join("icons", pkg + ext)
    try:
        with zipfile.ZipFile(apk) as z, open(dest, "wb") as f:
            f.write(z.read(iconpath))
        a["iconUrl"] = f"{PAGES}/{pkg}{ext}"
        done.append(f"{a['name']} -> {pkg}{ext}")
    except Exception as e:
        skip.append(f"{a['name']} (err {e})")

json.dump(cat, open("catalog.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"ICONES AJOUTEES: {len(done)}")
for x in done: print("  +", x)
print(f"\nSANS APK LOCAL (avatar conserve): {len(skip)}")
for x in skip: print("  -", x)
