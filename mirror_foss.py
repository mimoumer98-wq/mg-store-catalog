#!/usr/bin/env python3
# Mirror the open-source subset into apps/, recompute sha256+size, rewrite catalog.json.
import json, os, hashlib, urllib.request, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APPS = os.path.join(HERE, "apps")
os.makedirs(APPS, exist_ok=True)
BASE = "https://CHANGEME.github.io/mg-store-catalog"  # placeholder, replaced once GitHub user known

FOSS = {
    "org.videolan.vlc", "org.mozilla.firefox", "app.organicmaps", "freetube.com",
    "com.quran.labs.androidquran", "org.smarttube.stable",
    "app.revanced.android.gms", "net.mxbi.blackscreen",
}

cat = json.load(open(os.path.join(HERE, "catalog.json"), encoding="utf-8"))

def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "mg-store-mirror/1.0"})
    with urllib.request.urlopen(req, timeout=600) as r, open(dest, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)

results = []
for a in cat["apps"]:
    if a.get("packageName") not in FOSS:
        continue
    url = a["apkUrl"]
    fn = url.split("/")[-1]
    dest = os.path.join(APPS, fn)
    try:
        fetch(url, dest)
        with open(dest, "rb") as f:
            head = f.read(2)
        size = os.path.getsize(dest)
        if head != b"PK" or size < 10000:
            results.append((a["name"], "BAD(not apk)", size)); continue
        h = hashlib.sha256()
        with open(dest, "rb") as f:
            for b in iter(lambda: f.read(1 << 20), b""):
                h.update(b)
        a["apkUrl"] = f"{BASE}/apps/{fn}"
        a["sha256"] = h.hexdigest()
        a["sizeBytes"] = size
        results.append((a["name"], "OK", size))
    except Exception as e:
        results.append((a["name"], f"ERR {e}", 0))

json.dump(cat, open(os.path.join(HERE, "catalog.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

for name, st, sz in results:
    print(f"{st:14} {sz:>12} {name}")
print("DONE")
