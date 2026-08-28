import assert from 'node:assert/strict';
import { copyFileSync, mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import test from 'node:test';

const SCANNER = fileURLToPath(new URL('./scan-slop-signals.mjs', import.meta.url));

function withFixture(run) {
  const root = mkdtempSync(path.join(tmpdir(), 'cx-slopslap-scan-'));
  try {
    run(root);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
}

function scanWith(scanner, cwd, ...targets) {
  const result = spawnSync(process.execPath, [scanner, ...targets, '--json'], {
    cwd,
    encoding: 'utf8',
  });
  return {
    ...result,
    json: JSON.parse(result.stdout),
  };
}

function scan(cwd, ...targets) {
  return scanWith(SCANNER, cwd, ...targets);
}

test('prints help without scanning the current directory', () => {
  const result = spawnSync(process.execPath, [SCANNER, '--help'], {
    encoding: 'utf8',
  });

  assert.equal(result.status, 0);
  assert.match(result.stdout, /사용법:/u);
  assert.match(result.stdout, /종료 코드:/u);
  assert.doesNotMatch(result.stdout, /스캔: 파일/u);
});

test('reports complete coverage for a readable supported target', () => {
  withFixture((root) => {
    writeFileSync(path.join(root, 'clean.html'), '<main>Plain content</main>\n');

    const result = scan(root, 'clean.html');

    assert.equal(result.status, 0);
    assert.deepEqual(result.json.detectorErrors, []);
    assert.deepEqual(result.json.coverage, {
      complete: true,
      requestedTargets: ['clean.html'],
      scannedFiles: 1,
      limitations: [],
    });
  });
});

test('reports a missing target as incomplete instead of a clean scan', () => {
  withFixture((root) => {
    const result = scan(root, 'missing.html');

    assert.equal(result.status, 2);
    assert.equal(result.json.coverage.complete, false);
    assert.equal(result.json.coverage.scannedFiles, 0);
    assert.deepEqual(result.json.coverage.limitations, [
      {
        type: 'missing-target',
        target: 'missing.html',
        message: 'Target does not exist',
      },
    ]);
  });
});

test('sanitizes candidate excerpts into bounded single-line evidence', () => {
  withFixture((root) => {
    writeFileSync(path.join(root, 'flagged.html'), '<style>.cta{color:#6366f1}</style>\u0001\u2028hidden\n');

    const result = scan(root, 'flagged.html');
    const samples = result.json.report.flatMap((finding) => finding.samples);

    assert.equal(result.status, 0);
    assert.ok(samples.length > 0);
    for (const sample of samples) {
      assert.ok(sample.text.length <= 140);
      assert.doesNotMatch(sample.text, /[\u0000-\u001f\u007f\u2028\u2029]/u);
    }
  });
});

test('reports an invalid detector as incomplete instead of dropping it', () => {
  withFixture((root) => {
    const skillRoot = path.join(root, 'skill');
    const scanner = path.join(skillRoot, 'scripts', 'scan-slop-signals.mjs');
    mkdirSync(path.join(skillRoot, 'scripts'), { recursive: true });
    mkdirSync(path.join(skillRoot, 'assets', 'data'), { recursive: true });
    copyFileSync(SCANNER, scanner);
    writeFileSync(
      path.join(skillRoot, 'assets', 'data', 'aiSlopTaxonomyData.js'),
      "export const AI_SLOP_TAXONOMY=[{number:1,categories:[{groups:[{items:[{id:'broken',koName:'Broken',severity:'weak',detect:{kind:'code',signals:['[']}}]}]}]}];\n",
    );
    writeFileSync(path.join(root, 'clean.html'), '<main>Plain content</main>\n');

    const result = scanWith(scanner, root, 'clean.html');

    assert.equal(result.status, 2);
    assert.equal(result.json.coverage.complete, false);
    assert.equal(result.json.detectorErrors.length, 1);
    assert.equal(result.json.detectorErrors[0].id, 'broken');
    assert.equal(result.json.detectorErrors[0].signal, '[');
  });
});
