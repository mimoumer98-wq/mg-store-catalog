#!/usr/bin/env python3
# Ajoute en lot des APK (outils Coolray + open source) au catalogue MG Store.
import json, os, hashlib, subprocess, re, sys

APKDIR = "C:/Users/acer/Desktop/apk"
AAPT2 = "C:/Users/acer/AppData/Local/Android/Sdk/build-tools/35.0.0/aapt2.exe"
REPO = "mimoumer98-wq/mg-store-catalog"
TAG = "apps-v1"
BASE = f"https://github.com/{REPO}/releases/download/{TAG}"

# (fichier, nom affiché, catégorie, description)
ITEMS = [
    ("OrdinateurDeBord_FR_EN_AR_BoutonThemeWidget_v1.47.apk", "Coolray Dash", "Auto", "Ordinateur de bord FR/EN/AR avec widgets et thèmes."),
    ("DiPlay-v0.2.79-legacy-release.apk", "DiPlay", "Auto", "Affichage d'instrumentation / tête haute."),
    ("Bouton-Coolray-0.15-test.apk", "Bouton Coolray", "Auto", "Personnalisation des boutons du véhicule."),
    ("Coolray-Mini-Carte-v1.4R.apk", "Coolray Mini Carte", "Navigation", "Mini-carte en superposition."),
    ("Morphius-HU.apk", "Morphius", "Auto", "Outil tête d'unité pour Coolray."),
    ("SideEye.v1.1.apk", "SideEye", "Auto", "Caméra d'angle mort / assistance."),
    ("aures-eyes-1.1.apk", "Aures Eyes", "Auto", "Dashcam / caméra embarquée."),
    ("sunray-release-1.3.apk", "Sunray Toolkit", "Outils", "Boîte à outils pour l'autoradio."),
    ("stagelight-release-1.2.apk", "App Manager", "Outils", "Gestion des applications installées."),
    ("calendrier-fr.apk", "Calendrier", "Outils", "Calendrier des jours fériés."),
    ("headunit-revived-3.0.0.apk", "Headunit Revived", "Auto", "Projection smartphone (open source)."),
]

def badging(path):
    out = subprocess.run([AAPT2, "dump", "badging", path], capture_output=True, text=True, errors="ignore").stdout
    pkg = re.search(r"package: name='([^']+)' versionCode='([^']+)' versionName='([^']*)'", out)
    minsdk = re.search(r"sdkVersion:'([0-9]+)'", out)
    if not pkg: return None
    return pkg.group(1), int(pkg.group(2)), pkg.group(3) or "1.0", int(minsdk.group(1)) if minsdk else 21

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

cat = json.load(open("catalog.json", encoding="utf-8"))
added = []
for fn, name, category, desc in ITEMS:
    path = os.path.join(APKDIR, fn)
    if not os.path.exists(path):
        print("ABSENT:", fn); continue
    meta = badging(path)
    if not meta:
        print("ILLISIBLE:", fn); continue
    pkg, vc, vn, minsdk = meta
    size = os.path.getsize(path)
    sh = sha256(path)
    print(f"upload {fn} ({pkg} v{vn})…")
    subprocess.run(["gh", "release", "upload", TAG, path, "--clobber", "-R", REPO],
                   capture_output=True, text=True)
    cat["apps"] = [a for a in cat["apps"] if a.get("packageName") != pkg]
    cat["apps"].append({
        "id": pkg.replace(".", "-"), "name": name, "packageName": pkg,
        "versionName": vn, "versionCode": vc, "description": desc,
        "apkUrl": f"{BASE}/{fn}", "sha256": sh, "sizeBytes": size,
        "minAndroid": minsdk, "category": category, "featured": False,
    })
    added.append(f"{name} ({pkg}) v{vn}")

json.dump(cat, open("catalog.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("\nAJOUTÉES:", len(added)); [print(" +", a) for a in added]
print("TOTAL catalogue:", len(cat["apps"]), "apps")
