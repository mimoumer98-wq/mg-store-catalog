#!/usr/bin/env bash
# Ajoute une application au catalogue MG Store en UNE commande.
#
#   ./add-app.sh <chemin/vers/app.apk> "<Catégorie>" "<Description>" [featured]
#
# Exemple :
#   ./add-app.sh ~/Downloads/monapp.apk "Outils" "Mon super outil"
#   ./add-app.sh ~/Downloads/jeu.apk "Jeux" "Un jeu sympa" featured
#
# Le script : lit package/version/nom via aapt2, calcule sha256 + taille,
# uploade l'APK dans la Release GitHub, ajoute l'entrée dans catalog.json, pousse.
set -euo pipefail

APK="${1:?Donne le chemin de l'APK}"
CAT="${2:-Outils}"
DESC="${3:-}"
FEAT="false"; [ "${4:-}" = "featured" ] && FEAT="true"

REPO="mimoumer98-wq/mg-store-catalog"
TAG="apps-v1"
PAGES_BASE="https://github.com/${REPO}/releases/download/${TAG}"
HERE="$(cd "$(dirname "$0")" && pwd)"
BT="${BUILD_TOOLS:-$HOME/AppData/Local/Android/Sdk/build-tools/35.0.0}"
AAPT2="$BT/aapt2.exe"; [ -x "$AAPT2" ] || AAPT2="$BT/aapt2"

[ -f "$APK" ] || { echo "APK introuvable: $APK"; exit 1; }
[ "$(head -c2 "$APK")" = "PK" ] || { echo "Ce n'est pas un APK valide"; exit 1; }

echo ">> Lecture des métadonnées…"
B="$("$AAPT2" dump badging "$APK")"
PKG=$(printf '%s' "$B"  | sed -n "s/.*package: name='\([^']*\)'.*/\1/p" | head -1)
VNAME=$(printf '%s' "$B"| sed -n "s/.*versionName='\([^']*\)'.*/\1/p" | head -1)
VCODE=$(printf '%s' "$B"| sed -n "s/.*versionCode='\([^']*\)'.*/\1/p" | head -1)
LABEL=$(printf '%s' "$B"| sed -n "s/^application-label:'\([^']*\)'.*/\1/p" | head -1)
MINSDK=$(printf '%s' "$B"|sed -n "s/^minSdkVersion:'\([^']*\)'.*/\1/p" | head -1)
FN="$(basename "$APK")"
SIZE=$(stat -c %s "$APK")
SHA=$(sha256sum "$APK" | cut -d' ' -f1)
[ -n "$DESC" ] || DESC="$LABEL"
[ -n "$MINSDK" ] || MINSDK=23
echo "   $LABEL ($PKG) v$VNAME  ${SIZE} o"

echo ">> Upload de l'APK dans la Release $TAG…"
gh release upload "$TAG" "$APK" -R "$REPO" --clobber

echo ">> Mise à jour de catalog.json…"
python - "$HERE/catalog.json" "$FN" "$PKG" "$VNAME" "$VCODE" "$LABEL" "$CAT" "$DESC" "$SHA" "$SIZE" "$MINSDK" "$FEAT" "$PAGES_BASE" <<'PY'
import json,sys
(path,fn,pkg,vname,vcode,label,cat,desc,sha,size,minsdk,feat,base)=sys.argv[1:14]
c=json.load(open(path,encoding='utf-8'))
entry={"id":pkg.replace('.','-'),"name":label,"packageName":pkg,"versionName":vname,
 "versionCode":int(vcode),"description":desc,"apkUrl":f"{base}/{fn}","sha256":sha,
 "sizeBytes":int(size),"minAndroid":int(minsdk),"category":cat,"featured":feat=="true"}
apps=[a for a in c["apps"] if a.get("packageName")!=pkg]  # remplace si déjà présent
apps.append(entry)
c["apps"]=apps
json.dump(c,open(path,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print(f"   -> {label} ajouté ({len(apps)} apps au total)")
PY

echo ">> Publication (git push)…"
cd "$HERE"
git add catalog.json
git commit -q -m "Ajout app: $LABEL ($PKG)"
git push -q
echo ">> OK. L'app apparaîtra dans MG Store après la synchro (≈1 min pour GitHub Pages)."
