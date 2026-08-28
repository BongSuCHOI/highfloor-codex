/**
 * AI-slop 기계 스캐너
 *
 * aiSlopTaxonomyData.js(v0.4+)의 detect.signals 를 대상 코드에 돌려
 * 클리셰 후보 히트를 항목별로 집계한다. 신호는 가중 플래그이지 판결이 아니다:
 * 이 스크립트의 출력은 slopslap 점검의 후보 목록이고, 최종 판정은 각 항목의
 * detect.note 오탐 경고와 프로젝트 의도를 반영한 판단 단계가 한다.
 *
 * 사용법:
 *   node scripts/scan-slop-signals.mjs                 # 기본 대상 전체
 *   node scripts/scan-slop-signals.mjs app/page.jsx src/components/landing
 *   node scripts/scan-slop-signals.mjs --json          # 에이전트 소비용 JSON
 *   node scripts/scan-slop-signals.mjs --max 5         # 항목당 샘플 라인 수 (기본 3)
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const TARGET_ROOT = process.cwd();
const args = process.argv.slice(2);
if (args.includes('--help') || args.includes('-h')) {
  console.log(`사용법:
  node scripts/scan-slop-signals.mjs [target ...] [--json] [--max N]

옵션:
  --json    구조화된 JSON 출력
  --max N   검출 항목별 최대 sample 수 (기본 3)
  -h, --help
            도움말 출력

종료 코드:
  0  요청한 지원 파일을 완전하게 스캔함
  2  target, read, 또는 detector 오류로 coverage가 불완전함`);
  process.exit(0);
}

const { AI_SLOP_TAXONOMY } = await import(path.join(ROOT, 'assets/data/aiSlopTaxonomyData.js'));
const asJson = args.includes('--json');
const maxIdx = args.indexOf('--max');
const MAX_SAMPLES = maxIdx !== -1 ? Number(args[maxIdx + 1]) : 3;
const targets = args.filter((a, i) => !a.startsWith('--') && (maxIdx === -1 || i !== maxIdx + 1));

// 기본 대상: 라우트 + 컴포넌트 + 카피 상수 (사전·택소노미 데이터 자체는 자기참조라 제외)
const DEFAULT_TARGETS = ['.'];
const EXCLUDE = /TaxonomyData\.js$|node_modules|\.next|\.git|\.codex[/\\]slopslap|\.stories\.jsx$|slideTitleMap\.json$/;
const EXTS = new Set(['.js', '.jsx', '.ts', '.tsx', '.css', '.html', '.vue', '.svelte', '.astro']);
const limitations = [];

function sanitizeExcerpt(value, maxLength = 140) {
  return String(value)
    .replace(/[\u0000-\u001f\u007f\u2028\u2029]+/gu, ' ')
    .replace(/\s{2,}/gu, ' ')
    .trim()
    .slice(0, maxLength);
}

function addLimitation(type, target, message) {
  limitations.push({ type, target, message: sanitizeExcerpt(message, 240) });
}

function collectFiles(target) {
  const abs = path.isAbsolute(target) ? target : path.resolve(TARGET_ROOT, target);
  let stat;
  try {
    stat = fs.statSync(abs);
  } catch (error) {
    if (error.code === 'ENOENT')
      addLimitation('missing-target', target, 'Target does not exist');
    else
      addLimitation('stat-error', target, error.message);
    return [];
  }
  if (stat.isFile()) return EXCLUDE.test(abs) ? [] : [abs];
  const out = [];
  let entries;
  try {
    entries = fs.readdirSync(abs);
  } catch (error) {
    addLimitation('read-directory-error', target, error.message);
    return out;
  }
  for (const entry of entries) {
    const p = path.join(abs, entry);
    if (EXCLUDE.test(p)) continue;
    let s;
    try {
      s = fs.statSync(p);
    } catch (error) {
      addLimitation('stat-error', path.relative(TARGET_ROOT, p), error.message);
      continue;
    }
    if (s.isDirectory()) out.push(...collectFiles(p));
    else if (EXTS.has(path.extname(p))) out.push(p);
  }
  return out;
}

// detect 신호 수집 (code·hybrid 만. judgment 는 스캔 대상 아님)
const detectors = [];
const detectorErrors = [];
for (const part of AI_SLOP_TAXONOMY)
  for (const cat of part.categories)
    for (const g of cat.groups)
      for (const it of g.items) {
        if (!it.detect || it.detect.kind === 'judgment' || !it.detect.signals) continue;
        const regexes = it.detect.signals.map((s) => {
          try {
            return new RegExp(s, 'u');
          } catch {
            try {
              return new RegExp(s);
            } catch (error) {
              detectorErrors.push({ id: it.id, signal: sanitizeExcerpt(s), message: sanitizeExcerpt(error.message, 240) });
              return null;
            }
          }
        }).filter(Boolean);
        detectors.push({ id: it.id, koName: it.koName, part: part.number, kind: it.detect.kind, severity: it.severity, note: it.detect.note || '', regexes });
      }

const requestedTargets = targets.length ? targets : DEFAULT_TARGETS;
const files = [...new Set(requestedTargets.flatMap(collectFiles))];
const hits = new Map(); // id → [{file, line, text}]
let scannedFiles = 0;

for (const file of files) {
  const rel = path.relative(TARGET_ROOT, file);
  let lines;
  try {
    lines = fs.readFileSync(file, 'utf8').split('\n');
  } catch (error) {
    addLimitation('read-file-error', rel, error.message);
    continue;
  }
  scannedFiles += 1;
  lines.forEach((text, i) => {
    for (const d of detectors) {
      if (d.regexes.some((r) => r.test(text))) {
        if (!hits.has(d.id)) hits.set(d.id, []);
        hits.get(d.id).push({ file: rel, line: i + 1, text: sanitizeExcerpt(text) });
      }
    }
  });
}

if (files.length === 0 && limitations.length === 0)
  addLimitation('no-supported-files', requestedTargets.join(', '), 'No supported files found');

const coverage = {
  complete: detectorErrors.length === 0 && limitations.length === 0,
  requestedTargets,
  scannedFiles,
  limitations,
};

const report = detectors
  .filter((d) => hits.has(d.id))
  .map((d) => ({ id: d.id, koName: d.koName, part: d.part, kind: d.kind, severity: d.severity, count: hits.get(d.id).length, note: d.note, samples: hits.get(d.id).slice(0, MAX_SAMPLES) }))
  .sort((a, b) => b.count - a.count);

if (asJson) {
  console.log(JSON.stringify({ scannedFiles, detectors: detectors.length, detectorErrors, coverage, flagged: report.length, report }, null, 2));
} else {
  console.log(`스캔: 파일 ${scannedFiles}개 · 검출기 ${detectors.length}개(code/hybrid) · 플래그 ${report.length}항목`);
  console.log('주의: 히트는 후보 플래그다. 각 항목의 note(오탐 조건)를 반영해 판정할 것.\n');
  for (const error of detectorErrors)
    console.log(`검출기 오류: ${error.id} · ${error.signal} · ${error.message}`);
  for (const limitation of limitations)
    console.log(`커버리지 제한: ${limitation.type} · ${limitation.target} · ${limitation.message}`);
  if (!coverage.complete) console.log('');
  for (const r of report) {
    console.log(`■ ${r.id} (${r.koName}) · P${r.part} · ${r.severity} · ${r.kind} · ${r.count}건`);
    if (r.note) console.log(`  note: ${r.note}`);
    for (const s of r.samples) console.log(`  - ${s.file}:${s.line}  ${s.text}`);
    console.log('');
  }
  const clean = detectors.length - report.length;
  console.log(`무히트 검출기 ${clean}개: 지원 파일과 활성 검출기 범위에서만 관찰 없음`);
}

if (!coverage.complete) process.exitCode = 2;
