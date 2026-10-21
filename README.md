# MG Store — Catalogue

Catalogue (liste d'applications) servi à l'app **MG Store** (`com.mgstore.app`).
C'est **toi** qui le contrôles : tu ajoutes/retires des apps en éditant `catalog.json`.

## Hébergement (HTTPS obligatoire — l'app refuse le HTTP en clair)

Le plus simple : **GitHub Pages** (gratuit, HTTPS).

1. Crée un dépôt GitHub, ex. `mg-store-catalog`.
2. Mets-y `catalog.json` (et tes fichiers `.apk` si tu veux les héberger toi-même).
3. Active **Settings → Pages → Deploy from branch → main / root**.
4. Ton URL devient : `https://<TON-USER>.github.io/mg-store-catalog/catalog.json`
5. Cette URL doit être celle configurée dans l'app MG Store (constante `DEFAULT_CATALOG`).
   Actuellement l'app pointe sur un **placeholder** `https://CHANGEME.github.io/...` → à remplacer
   par ton URL (je le fais dès que tu me donnes ton user GitHub + nom du dépôt).

## Format d'une app dans `catalog.json`

```json
{
  "id": "mon-app",
  "name": "Mon Application",
  "packageName": "com.exemple.monapp",
  "versionName": "1.0",
  "versionCode": 1,
  "description": "Description courte.",
  "apkUrl": "https://<TON-USER>.github.io/mg-store-catalog/mon-app.apk",
  "sha256": "<empreinte SHA-256 du fichier .apk>",
  "sizeBytes": 123456,
  "minAndroid": 23,
  "category": "Outils",
  "featured": false
}
```

- `sha256` + `sizeBytes` : **obligatoires** (l'app vérifie l'intégrité avant d'installer).
  Calcul : `sha256sum mon-app.apk` et taille = octets du fichier.
- `category` : Auto, Navigation, Multimédia, Audio, Outils, Culture, Internet, Jeux…
- `apkUrl` : doit être en **HTTPS**.

## Héberger tes propres APK
Dépose le `.apk` dans le dépôt (ou une Release GitHub), mets son URL HTTPS dans `apkUrl`,
puis renseigne `sha256` et `sizeBytes`. C'est tout.

## Important (droits)
Ce catalogue liste des apps. Tu es responsable de n'y mettre que des apps que tu as le **droit**
de distribuer (tes apps, ou des apps libres/open-source). Les apps **propriétaires**
(YouTube, Spotify, Chrome, Maps, TikTok…) et de **streaming** relèvent de leurs licences respectives.

## État du `catalog.json` fourni
Généré à partir du catalogue public existant, **sans** l'entrée « CoolStore » et **sans** mécanisme
de mise à jour forcée. Les `apkUrl` pointent pour l'instant vers l'hébergement d'origine : remplace-les
progressivement par tes propres liens pour être totalement indépendant.
