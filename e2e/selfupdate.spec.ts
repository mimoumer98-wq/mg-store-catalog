import { test, expect } from '@playwright/test';
import crypto from 'crypto';

// Teste l'auto-mise a jour de MG Store sur le VRAI catalogue en ligne.
const CATALOG = 'https://mimoumer98-wq.github.io/mg-store-catalog/catalog.json';
const PKG = 'com.mgstore.app';
const EXPECTED_VC = 102;

// Reproduit la logique de l'app (InstallManager/statusFor)
function decide(installed: number | null, catalogVc: number): string {
  if (installed === null) return 'Installer';
  if (installed < catalogVc) return 'Mettre à jour';
  return 'Ouvrir';
}

test('catalogue sert MG Store avec la nouvelle version (102)', async ({ request }) => {
  const cat = await (await request.get(CATALOG)).json();
  const mg = cat.apps.find((a: any) => a.packageName === PKG);
  expect(mg, 'MG Store present dans son propre catalogue').toBeTruthy();
  expect(mg.versionCode).toBe(EXPECTED_VC);
  console.log(`MG Store catalogue: v${mg.versionName} (vc=${mg.versionCode})`);
});

test('APK telechargeable + SHA-256 conforme au catalogue', async ({ request }) => {
  const cat = await (await request.get(CATALOG)).json();
  const mg = cat.apps.find((a: any) => a.packageName === PKG);
  const r = await request.get(mg.apkUrl);
  expect(r.status()).toBe(200);
  const buf = await r.body();
  expect(buf.length).toBe(mg.sizeBytes);
  const sha = crypto.createHash('sha256').update(buf).digest('hex');
  expect(sha).toBe(mg.sha256);
  console.log(`APK OK: ${buf.length} octets, sha256 verifie`);
});

test('decision MaJ : tablette en v100 -> "Mettre a jour"', async ({ request }) => {
  const cat = await (await request.get(CATALOG)).json();
  const vc = cat.apps.find((a: any) => a.packageName === PKG).versionCode;
  expect(decide(100, vc)).toBe('Mettre à jour');  // client deja equipe (v100)
  expect(decide(vc, vc)).toBe('Ouvrir');          // deja a jour
  expect(decide(null, vc)).toBe('Installer');     // pas installe
});
