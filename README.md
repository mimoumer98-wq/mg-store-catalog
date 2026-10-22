# MG Store — Catalogue

Catalogue (liste d'applications) servi à l'app **MG Store** (`com.mgstore.app`).
C'est **toi** qui le contrôles : tu ajoutes/retires des apps en éditant `catalog.json`.

## ✅ Déjà en ligne et fonctionnel

- **Catalogue live** : https://mimoumer98-wq.github.io/mg-store-catalog/catalog.json
- **APK hébergées** : dans la Release [`apps-v1`](https://github.com/mimoumer98-wq/mg-store-catalog/releases/tag/apps-v1)
- **L'app MG Store pointe déjà sur cette URL** (constante `CATALOG_URL`). Rien d'autre à configurer.
- Contenu actuel : **7 applications open source** (VLC, Organic Maps, FreeTube, Quran, SmartTube,
  microG, Black Screen) — auto-hébergées chez toi, 100 % en règle.

## Ajouter une application → en UNE commande

```bash
./add-app.sh /chemin/vers/mon-app.apk "Catégorie" "Description courte"
# ex : ./add-app.sh ~/Downloads/jeu.apk "Jeux" "Un jeu sympa"
```
Le script lit le package/version, calcule le **SHA-256** + la taille, **uploade l'APK** dans la
Release GitHub, **ajoute la ligne** dans `catalog.json` et **pousse**. 
→ La nouvelle app apparaît **automatiquement** dans MG Store sur **toutes les tablettes** à la
prochaine ouverture (l'app relit le catalogue en ligne ; aucune réinstallation nécessaire).

## Format d'une app dans `catalog.json`
```json
{
  "id": "mon-app",
  "name": "Mon Application",
  "packageName": "com.exemple.monapp",
  "versionName": "1.0",
  "versionCode": 1,
  "description": "Description courte.",
  "apkUrl": "https://github.com/mimoumer98-wq/mg-store-catalog/releases/download/apps-v1/mon-app.apk",
  "sha256": "<empreinte SHA-256 du .apk>",
  "sizeBytes": 123456,
  "minAndroid": 23,
  "category": "Outils",
  "featured": false
}
```
- `sha256` + `sizeBytes` : **obligatoires** (l'app vérifie l'intégrité avant d'installer).
- `category` : Auto, Navigation, Multimédia, Audio, Outils, Culture, Internet, Jeux…
- `apkUrl` : **HTTPS** obligatoire (Release GitHub conseillée — supporte les gros fichiers > 100 Mo).

## Fichiers du dépôt
- `catalog.json` — le catalogue public (7 apps). **C'est lui que l'app lit.**
- `catalog-full-reference.json` — référence des 43 apps du catalogue d'origine (non publiée telle quelle).
- `add-app.sh` — ajout d'une app en une commande.
- `apps/` — les APK en local (uploadées en Release, non versionnées).

## Important (droits)
Tu es responsable de n'y mettre que des apps que tu as le **droit** de distribuer (tes apps, ou des
apps libres/open-source). Les apps **propriétaires** (YouTube, Spotify, Chrome, Maps, TikTok…) et de
**streaming** relèvent de leurs licences respectives.
