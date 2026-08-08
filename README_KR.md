<p align="center">
  <img src="assets/highfloor-codex-banner.png" alt="Highfloor for Codex — 바닥을 높이고, 천장은 열어 둡니다." width="100%">
</p>

<p align="center">
  <strong>OpenAI Codex를 위한 실용적인 스킬과 전문 에이전트 키트.</strong><br>
  하위 모델에는 분명한 길을, 상위 모델에는 더 넓은 사고의 여지를.
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README_KR.md"><strong>한국어</strong></a>
</p>

<p align="center">
  <a href="#설치">설치</a> ·
  <a href="#철학">철학</a> ·
  <a href="#skills">Skills</a> ·
  <a href="#custom-agents">Agents</a> ·
  <a href="#조합형-workflow">Workflows</a>
</p>

> [!NOTE]
> Highfloor for Codex는 독립적인 비공식 커뮤니티 프로젝트입니다.
> OpenAI와 제휴하거나 OpenAI의 보증·후원을 받는 프로젝트가 아닙니다.

> [!WARNING]
> 전체 묶음은 **여러 라이선스가 혼합된 source-available collection이며,
> 그 자체로 OSI open source가 아닙니다.** 수정·이식된 스킬 5개는
> Sustainable Use License 1.0을 유지합니다. 사용하거나 재배포하기 전에
> [라이선스와 원본 프로젝트 존중](#license와-upstream-respect)을
> 확인하십시오.

## 지금의 Highfloor

현재 Highfloor에는 제가 실제 Codex 환경에서 사용하는 구성요소가 들어
있습니다.

- 요구사항 정리, 진단, 조사, 범위 관리, 브라우저 작업, 디자인 방향,
  검증, 영상 분석과 낯선 코드베이스 구조화를 맡는 **15개의 집중된
  `cx-*` 스킬**
- 조사, 검토, 구현, 문서화를 각자의 전문 영역에서 수행하는
  **27개의 전문 에이전트**

Highfloor는 아직 독립형 에이전트 하네스나 자동 파이프라인이 아닙니다.
각 스킬과 에이전트는 분명한 역할을 가지며, 현재 작업에 필요한 것만
골라 조합하는 키트입니다.

장기적인 방향은 같은 철학을 실제 실행 환경에 담은 하네스입니다. 아래
철학은 지금의 키트와 앞으로 Highfloor라는 이름으로 만들 모든 것을
연결하는 설계 기준입니다.

## Highfloor를 만들게 된 계기

그동안 여러 에이전트 하네스와 플러그인, 키트, 라이브러리를 사용했습니다.
그 사이 모델은 빠르게 발전했고 새로운 도구와 작업 방식도 계속
등장했습니다. 모든 릴리스와 유행을 매번 따라가는 방식은 지속 가능하지
않았습니다. 지금 쓰는 도구보다 오래 유지될 판단 기준, 즉 제품보다 먼저
세울 원칙과 철학이 필요했습니다.

Highfloor는 그 원칙을 글로 정리하고, 이미 무겁게 커스터마이징해 사용하던
Codex 설정을 그 기준에 맞춰 전면 개편하면서 시작한 프로젝트입니다.

개인적인 작업 환경의 제약은 이 문제를 더 절실하게 만들었습니다. 개인
작업이 언제나 비싼 기업용 구독 플랜 위에서 돌아가는 것은 아닙니다. 구독
한도가 부족하면 더 저렴한 플랜과 중국계 모델 공급자를 포함한 여러
공급자를 오가야 합니다. 따라서 이 설정은 서로 다른 수준의 모델이
신뢰할 수 있는 결과를 내도록 도우면서도, 상위 모델이 가진 역량을
낭비하지 않아야 했습니다.

하위 모델에는 분명한 경로와 유용한 기본값, 언제 멈춰야 하는지 알려주는
조건이 필요합니다. 상위 모델에는 스스로 사고하고 상황에 적응하며 더
나은 방법을 찾을 여지가 필요합니다. 전자만 고려한 시스템은 상위 모델을
가두고, 후자만 고려한 시스템은 하위 모델을 불안정한 상태로 남겨 둡니다.
Highfloor는 두 문제를 함께 다루기 위한 시도입니다.

여기서 하위 모델과 상위 모델은 특정 회사나 모델 계보를 나누는 표현이
아닙니다. 현재 작업에서 사용할 수 있는 성능과 추론 역량의 상대적인
차이를 뜻합니다.

### Highfloor를 만들어 가는 방식

Highfloor는 제가 혼자 떠올린 생각만으로 설계하지도, 모델이 알아서
작성하게 두지도 않습니다. 저는 철학, 실제 사용 사례, 제약과 최종 결정을
제시합니다. 모델과 계속 대화하면서 가정을 반박하고, 여러 방향을
비교하고, 대안을 제안받습니다. 그 제안을 받아들이거나 수정하거나
기각하는 판단은 제가 내립니다. 결정된 내용은 문서나 코드로 옮기고
저장소의 기준에 맞는지 다시 검증합니다.

즉 인간이 이끌고 모델이 사고를 확장하는 설계 방식입니다. 대화는 선택지를
넓히지만, 프로젝트가 무엇을 말하고 어떻게 동작할지에 대한 책임은
maintainer에게 남습니다.

## 목표

> Highfloor의 목표는 모든 모델에 동일한 작업 절차를 강요하는 것이
> 아닙니다. 피할 수 있는 행동 편차를 줄이고, 최소 품질을 높이며,
> 상위 모델이 가진 판단력을 보존하는 것입니다.

## 철학

이 원칙은 현재의 스킬과 에이전트부터 미래의 하네스까지 Highfloor라는
이름으로 만드는 모든 것에 적용됩니다. 아직 모든 기능이 구현됐다는
주장이 아니라, Highfloor를 설계하고 평가하는 기준입니다.

이 원칙들은 고정된 교리가 아닙니다. 모델과 도구가 발전하고 경험이
쌓이면 표현과 세부 기준은 달라질 수 있습니다. 그러나 **Hard Floor →
Soft Scaffold → Open Ceiling**이라는 기본 구조와 **Raise the floor. Keep
the ceiling open.**이라는 방향은 Highfloor의 뼈대로 남습니다.
Highfloor의 변화는 새로운 유행이 등장할 때마다 뼈대를 교체하는 것이
아니라, 그 뼈대를 현실에 더 정확하게 적용하도록 다듬는 과정입니다.

### Hard Floor

모든 모델이 지켜야 할 공통의 최소 보장입니다.

- 사용자의 권한, 범위, 제약과 비목표를 존중합니다.
- 사실, 증거, 가정과 추론을 구분합니다.
- 충분한 증거 없이 완료를 선언하지 않습니다.
- 파괴적 작업, 외부 공개, 배포, 자격 증명과 비용의 경계를 분명히
  유지합니다.

### Soft Scaffold

정보나 확신이 부족할 때 스킬은 가장 작지만 유용한 절차를 제공합니다.

- 핵심을 좁히는 질문
- 명시적인 계약과 결정 기록
- 근거를 정리하는 방법과 판정 용어
- 분야에 맞는 가드레일
- 분명한 종료 조건과 대안

신뢰할 수 있는 증거로 판단이 끝났다면 이 보조 절차는 더 이상 필요하지
않습니다.

### Open Ceiling

상위 모델은 Hard Floor를 지키고 더 나은 증거를 제시하는 한, 주어진
절차를 압축하거나 대체하고 확장할 수 있습니다.

Highfloor는 모든 모델에 같은 사고 과정을 강요하지 않습니다. 결과와
경계를 안내합니다.

### 가드레일은 길을 보여줘야 합니다

좋은 하네스는 모델이 해서는 안 되는 모든 행동을 예상해 긴 금지 목록을
만드는 시스템이 아닙니다. 지금 무엇을 확인하고, 어떤 증거를 모으며,
어디에서 권한이 바뀌고, 언제 멈춰야 하는지를 보여주는 시스템이어야
합니다.

흡연자에게 백 곳의 금연구역만 알려주고 정작 흡연 가능한 장소를 알려주지
않는 상황을 생각해 봅시다. 그 사람은 여전히 가장 중요한 문제를 해결해야
합니다. “그래서 어디에서 피울 수 있는가?” 반대로 열 곳의 흡연구역을
알려주고 그 안에서만 흡연하면 된다고 설명하면 이해와 실행은 훨씬
빠릅니다.

모델을 위한 가드레일도 같은 형태를 가집니다. 하위 모델이 수많은 금지
사항 사이에서 허용된 행동을 추론하게 만들면 헤매거나 잘못된 답을 선택할
가능성이 커집니다. 해야 할 행동과 유효한 경로를 명확히 제시하면 더
안정적이고 일관되게 움직일 수 있습니다.

하지만 그 경로를 하나의 정답으로 지나치게 조여서도 안 됩니다. 상위
모델은 기본 경로에서 출발하되, 사고를 통해 가지를 뻗고 더 나은
해결책이나 창의적인 방법을 발견할 수 있어야 합니다.

이 철학이 모든 금지를 없애자는 뜻은 아닙니다. 파괴적 작업, 자격 증명,
개인정보, 외부 공개, 배포, 보안과 비용처럼 실제 위험이 바뀌는 지점에는
분명한 제한과 때로는 인간의 승인이 필요합니다. 그 경계 밖에서 Highfloor는
끝없는 금지 목록보다 해야 할 행동, 유용한 기본값, 증거와 종료 조건을
우선합니다.

### 바닥을 높이되 천장을 낮추지 않습니다

모델의 성능과 지식은 계속 발전합니다. **오늘의 하위 모델에 도움이 되는
세밀한 규칙이 내일의 상위 모델에는 불필요한 제한이 될 수 있습니다.**
모든 판단을 정책으로 고정하려는 하네스는 실수를 막는 동시에 판단력,
적응력과 창의성까지 억누를 수 있습니다.

Highfloor는 하위 모델의 피할 수 있는 실수를 줄이고 더 일관되게 작업하도록
도우면서도, 상위 모델을 체크리스트 실행기로 만들지 않으려 합니다. 이
균형에서 다음 슬로건이 나왔습니다.

> **Raise the floor. Keep the ceiling open.**

바닥은 모든 모델이 지켜야 할 최소 품질과 신뢰성을 뜻합니다. 열린 천장은
상위 모델이 그 기반 위에서 스스로 사고하고, 절차를 압축하거나
대체하며, 더 나은 해결책을 찾을 수 있는 여지를 뜻합니다.

### 인간의 판단은 중요한 경계에 둡니다

Human-in-the-loop는 프로덕션에서 필수적입니다. 동시에 인간은 자주 병목이
됩니다. 이 두 주장은 모순되지 않습니다.

사람이나 조직이 한 번도 반복해 수행하지 않았고 도메인 지식도 없는
분야에서는 퀄리티 높은 AI 자동화를 만들 수 없다고 생각합니다. 신뢰할 수
있는 자동화는 이미 지속적으로 수행하고, 수정하고, 검증해 온 도메인에서
출발합니다. 도메인 지식이 있어야 무엇이 좋은 결과인지, 어떤 예외가
있는지, 어느 정도의 증거를 믿을 수 있는지 정의할 수 있습니다.

인간은 목적, 범위, 위험 수용, 돌이킬 수 없는 행동과 최종 책임을 소유해야
합니다. 하지만 해가 없는 모든 중간 단계를 매번 승인할 필요는 없습니다.

인간의 불안과 조바심이 촘촘한 규칙과 승인 절차로 바뀌면, 하네스는 오히려
상위 모델의 능력을 제한할 수 있습니다. Highfloor는 결과와 권한이
실질적으로 바뀌는 지점에서 인간의 통제권을 분명히 하고, 승인된 경계
안에서는 모델이 충분히 사고하고 작업할 수 있게 합니다. 그래서
Human-in-the-loop는 단순한 안전장치가 아니라, 사람의 도메인 지식과 AI가
협업하는 좋은 방식의 일부입니다.

## 작업 원칙

- 자신감 있는 서술보다 증거
- 모델 이름보다 현재 상태에 따른 선택
- 하나의 스킬, 하나의 분명한 책임
- 의무적인 파이프라인보다 상황에 따라 조합하는 워크플로
- 위험에 비례하는 검증
- 중복 감사와 검증을 위한 검증 금지
- 런타임 실패는 수정 전에 원인부터 진단
- 일반론보다 현재 프로젝트의 규칙과 아키텍처
- 이식된 자료의 출처와 라이선스 경계 보존

## 설치

### 한 줄 설치

```sh
curl -fsSL https://raw.githubusercontent.com/BongSuCHOI/highfloor-codex/main/install.sh | sh
```

### 실행 전에 검토하기

공용 또는 프로덕션 컴퓨터에서는 설치 스크립트를 먼저 확인하십시오.

```sh
git clone https://github.com/BongSuCHOI/highfloor-codex.git
cd highfloor-codex
less install.sh
./install.sh
```

재현 가능한 설치에는 릴리스 버전을 고정합니다.

```sh
curl -fsSL https://raw.githubusercontent.com/BongSuCHOI/highfloor-codex/v0.1.0/install.sh \
  | HIGHFLOOR_REF=v0.1.0 sh
```

### 설치되는 위치

| 내용 | 기본 경로 |
|---|---|
| 스킬 | `${CODEX_HOME:-$HOME/.codex}/skills` |
| 전문 에이전트 | `${CODEX_HOME:-$HOME/.codex}/agents` |
| 설치 상태와 백업 | `${CODEX_HOME:-$HOME/.codex}/highfloor-codex` |

기본 `CODEX_HOME`을 사용하면 스킬은 `~/.codex/skills`, 에이전트는
`~/.codex/agents`에 설치됩니다. 상태 디렉터리는 Codex가 불러오는
스킬이나 에이전트가 아닙니다. 설치한 버전과 source ref, 두 설치 경로,
업데이트·`doctor`·제거에서 사용할 정확한 관리 목록을 기록합니다. 관리
항목을 교체하거나 은퇴시키거나 제거할 때만 이 안에 시간별 백업이
생깁니다.

설치와 업데이트는 같은 방식으로 동작합니다. 선택한 릴리스의 manifest에
있는 모든 이름을 설치된 사본과 비교합니다. 내용이 달라졌다면 먼저
백업하고 저장소 버전으로 교체하며, 같다면 그대로 둡니다. 이후 릴리스가
manifest에서 이름을 제거하면 업데이트는 그 항목을 은퇴한 것으로 보고
백업한 뒤 제거합니다. Manifest에서 항목을 빼도 설치된 사본이 관리되지
않는 상태로 보존되는 것은 아닙니다. 현재 installer에는 항목별 제외
기능이 없으므로, 로컬 변형은 fork에서 관리하거나 다른 namespace를
사용해야 합니다. Highfloor가 한 번도 관리하지 않은 다른 스킬과
에이전트는 건드리지 않습니다.

경로 지정, 오프라인 설치, 업데이트와 복구 방법은
[설치와 업데이트](docs/INSTALLATION.md)를 참고하십시오.

### 업데이트, 진단, 제거

```sh
./install.sh update
./install.sh doctor
./install.sh update --dry-run
./install.sh uninstall
```

설치·업데이트·제거 후에는 Codex를 재시작해 검색 상태를 갱신하십시오.

## Skills

각 스킬은 특정한 상황을 위한 집중된 작업 지침입니다. 사용자가 직접
지정할 수도 있고, 현재 작업이 `SKILL.md`에 적힌 사용 조건과 맞을 때
Codex가 불러올 수도 있습니다.

명시적으로 호출할 때는 `$cx-analyze-video` 또는 `$cx-understand-codebase`를
사용합니다. 후자는 뒤에 `analyze`, `dashboard`, `ask` 같은 action word를
붙여 routing합니다. Legacy `/watch`, `/understand` custom-prompt alias는
설치하지 않습니다.

| Skill | 하는 일 | 사용 시점 |
|---|---|---|
| [`cx-analyze-video`](skills/cx-analyze-video/SKILL.md) | Sampling frame과 caption 또는 명시적으로 승인된 transcription을 시간축으로 맞춥니다. | YouTube 등 공개 URL, 로컬 `.mp4`·`.mov`, screen recording에서 timestamp evidence가 필요할 때 사용합니다. |
| [`cx-interview`](skills/cx-interview/SKILL.md) | 모호한 요청을 사용자가 승인한 Task Contract로 정리합니다. | 구현 전에 중요한 경계나 성공 조건이 분명하지 않을 때 사용합니다. |
| [`cx-unstuck`](skills/cx-unstuck/SKILL.md) | 실패한 접근을 다시 검토하고 현실적인 대안을 몇 가지 제시합니다. | 같은 계획이나 구현 전략이 반복해서 실패하거나 실제 막다른 길에 도달했을 때 사용합니다. |
| [`cx-browser-automation`](skills/cx-browser-automation/SKILL.md) | 실제 브라우저를 조작하고 일어난 일을 증거로 남깁니다. | 페이지 이동, 폼 입력, 로그인 상태, 스크린샷, snapshot 또는 trace가 필요할 때 사용합니다. |
| [`cx-coding-agent-sessions`](skills/cx-coding-agent-sessions/SKILL.md) | 이전 코딩 에이전트 세션을 찾아 요약합니다. | 과거의 정확한 작업, prompt, session, child task 또는 transcript가 필요할 때 사용합니다. |
| [`cx-debugging`](skills/cx-debugging/SKILL.md) | 런타임 실패를 재현하고 확인된 원인과 추측을 구분합니다. | crash, hang, 잘못된 결과, 조용한 실패, flaky 동작 또는 binary 증상을 진단할 때 사용합니다. |
| [`cx-design-director`](skills/cx-design-director/SKILL.md) | 넓은 범위의 product UI 또는 UX 변경 방향을 정합니다. | 시각 언어, layout system, component pattern 또는 end-to-end flow가 바뀔 때 사용합니다. |
| [`cx-insane-search`](skills/cx-insane-search/SKILL.md) | 보호된 fetch 경로로 차단된 공개 콘텐츠를 읽고 retrieval evidence를 보존합니다. | 공개 페이지가 `402`, `403`, WAF, 빈 HTML, JavaScript-only rendering 또는 손상된 markup으로 막혔을 때 사용합니다. |
| [`cx-programming`](skills/cx-programming/SKILL.md) | Python, TypeScript, Go 또는 Rust의 까다로운 언어 동작을 다룹니다. | type, concurrency, resource, error, FFI 또는 toolchain 동작이 올바른 구현을 바꿀 수 있을 때 사용합니다. |
| [`cx-scope-check`](skills/cx-scope-check/SKILL.md) | 현재 작업을 승인된 Task Contract와 비교합니다. | 긴 작업, 재개, handoff 또는 커진 변경이 합의한 경계를 벗어났을 가능성이 있을 때 사용합니다. |
| [`cx-slopslap`](skills/cx-slopslap/SKILL.md) | 흔한 AI 생성형 UI 패턴을 찾아 제거합니다. | 사용자가 AI처럼 보이거나 통계적으로 반복되는 UI 스타일을 없애 달라고 명시했을 때 사용합니다. |
| [`cx-ultraresearch`](skills/cx-ultraresearch/SKILL.md) | claim-relative primary evidence, counterevidence와 명시적인 unresolved gap을 바탕으로 신중한 답을 만듭니다. | 사용자가 deep research, 엄밀한 비교 또는 많은 인용이 필요한 조사를 명시했을 때 사용합니다. |
| [`cx-acceptance-qa`](skills/cx-acceptance-qa/SKILL.md) | 완료했다고 주장한 작업을 명시적인 acceptance criteria와 비교합니다. | release, handoff 또는 formal QA에 `PASS`, `FAIL`, `NOT_PROVEN` 판정이 필요할 때 사용합니다. |
| [`cx-visual-qa`](skills/cx-visual-qa/SKILL.md) | 현재 렌더링된 결과를 시각 증거로 판정합니다. | 변경된 web, mobile, terminal 또는 TUI에 최종 시각 판정이 필요할 때 사용합니다. |
| [`cx-understand-codebase`](skills/cx-understand-codebase/SKILL.md) | Evidence-backed architecture graph와 선택적인 interactive local dashboard를 만듭니다. | 인수인계, onboarding 또는 낯선 codebase·agent harness의 logic과 architecture를 공부할 때 사용합니다. |

모든 설치 대상 skill의 canonical catalog와 governance 문서:

- [CX skill catalog](skills/CX_SKILL_CATALOG.md)
- [CX skill governance](skills/CX_SKILLS.md)
- [Migration and provenance manifest](skills/CX_MIGRATION_MANIFEST.md)

모든 adapted skill의 정확한 source pin, 유지한 material, license와 수정
기록은 각 `references/upstream.md`와
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)에도 남깁니다.

## Custom agents

### 조사와 결정

| Agent | Mode | 역할 |
|---|---|---|
| `explorer` | read-only | 변경 전에 어떤 파일과 코드 경로가 해당 동작을 담당하는지 찾습니다. |
| `docs-researcher` | read-only | 공식 문서에서 API, 기본값, 버전과 framework 동작을 확인합니다. |
| `research-analyst` | read-only | 신뢰할 수 있는 출처를 비교해 범위가 분명한 기술 질문에 답합니다. |
| `data-analyst` | read-only | 기존 dataset, metric, trend 또는 anomaly가 의사결정에 어떤 의미인지 설명합니다. |
| `architect` | read-only | 시스템 경계를 살펴보고 변경이나 migration의 유지보수 가능한 형태를 제시합니다. |
| `planner` | read-only | 승인된 결과를 실제로 실행할 수 있는 작업 순서와 검증으로 바꿉니다. |
| `critic` | read-only | 계획의 숨은 가정을 검토하고 중요한 추측 없이 실행할 수 있는지 판단합니다. |
| `risk-reviewer` | read-only | 중요한 제품, 기술, 운영, 법률 인접 영역과 delivery 위험을 찾습니다. |

### 진단과 review

| Agent | Mode | 역할 |
|---|---|---|
| `debugger` | evidence workspace | 런타임이나 binary 실패를 재현하고 증거가 입증하는 가장 작은 원인을 찾습니다. |
| `browser-debugger` | evidence workspace | 브라우저 실패를 재현하고 설명에 필요한 console, network, state, screenshot 또는 trace를 수집합니다. |
| `performance-investigator` | evidence workspace | 시간, 메모리, rendering 작업 또는 throughput이 어디에서 손실되는지 측정합니다. |
| `incident-responder` | read-only | incident의 영향, timeline, 안전한 containment, recovery 상태와 가능한 원인을 정리합니다. |
| `reviewer` | read-only | 변경 사항에서 defect, regression, 깨진 integration, security 영향과 빠진 test를 찾습니다. |
| `security-reviewer` | read-only | trust boundary, identity, permission, secret, input과 현실적인 attack path를 확인합니다. |
| `reliability-reviewer` | read-only | retry, timeout, recovery, observability와 degraded operation 처리 방식을 확인합니다. |
| `financial-systems-reviewer` | read-only | payment와 ledger 변경의 precision, idempotency, reconciliation, settlement와 audit safety를 확인합니다. |
| `accessibility-tester` | evidence workspace | 렌더링된 UI를 keyboard, semantics, interaction state와 assistive technology 관점에서 시험합니다. |

### 구현

| Agent | Mode | 역할 |
|---|---|---|
| `ai-engineer` | workspace-write | model call, prompt, tool, retrieval, evaluation과 production failure 처리를 구현합니다. |
| `data-engineer` | workspace-write | 복구 가능한 ingestion, transformation, data contract와 backfill workflow를 구현합니다. |
| `database-engineer` | workspace-write | compatibility와 운영 안전성을 지키며 schema, migration, query와 transaction을 변경합니다. |
| `infra-engineer` | workspace-write | 범위가 정해진 cloud, IaC, deployment, networking과 environment 변경을 구현합니다. |
| `mcp-developer` | workspace-write | schema, transport, authentication, capability와 host integration을 포함한 MCP server 또는 client를 만듭니다. |
| `mobile-engineer` | workspace-write | iOS 또는 Android의 screen, lifecycle, state, API와 platform별 동작을 구현합니다. |
| `systems-engineer` | workspace-write | ownership, concurrency, memory, process 또는 resource 제한이 핵심인 작업을 구현합니다. |
| `windows-engineer` | workspace-write | PowerShell, service, identity, policy, registry 또는 Windows administration 작업을 구현합니다. |
| `test-engineer` | workspace-write | 변경 위험에 맞는 집중된 regression test와 안정적인 fixture를 추가합니다. |
| `technical-writer` | workspace-write | 실제 구현과 일치하는 release, migration, onboarding과 operator 문서를 작성합니다. |

Model configuration과 위임 기준은
[Complete agent catalog](docs/AGENT_CATALOG.md)를 참고하십시오.

> [!CAUTION]
> Agent TOML은 특정 Codex model 이름을 사용합니다. Account, product surface,
> future model catalog에 따라 일부 model을 사용할 수 없을 수 있습니다.
> 사용할 수 없는 경우 local agent configuration에서 가능한 model로 직접
> 바꾸십시오. Installer는 model을 임의로 치환하지 않습니다.

## 조합형 workflow

Highfloor workflow는 고정 pipeline이 아니라 상황에 맞춰 고르는
routing example입니다. 모든 작업을 같은 lifecycle에 강제로 통과시키는
도구를 여러 번 사용해 본 결과, 각 구성요소가 단독으로 실행되고 실제로
복잡해졌을 때만 조합할 수 있는 방식이 더 유용했습니다. 의무적인
pipeline은 작은 변경에도 가치가 없는 질문, 위임과 검증 비용을
발생시킵니다.

이 선택은 사용자에게 더 많은 판단을 요구합니다. Highfloor는 모든 경험
수준을 위한 one-command 만능 도구를 목표로 하지 않습니다. 대신 분명한
구성요소와 사례를 제공하고, 사람과 모델이 현재 상황에 필요한 가장 작은
workflow를 선택하게 합니다.

### 1. 모호한 feature에서 검증된 delivery까지

```text
구현에 영향을 주는 경계가 아직 모호함
  → cx-interview 실행
  → Task Contract 승인
      ├─ 지금 구현
      │    → 복잡할 때만 Plan 작성
      │    → 승인된 범위 구현
      │    → 변경된 동작 검증
      │    → 공식 판정이 필요할 때만 cx-acceptance-qa
      ├─ Contract를 나중을 위해 저장
      └─ 지속적인 작업이면 Codex Goal 시작
```

Plan은 승인된 작업을 어떻게 실행할지 설명합니다. Goal은 여러 차례 이어질
작업에서 objective를 계속 활성 상태로 유지합니다. 어느 것도 성공을
정의한 Task Contract를 대체하지 않으며, Goal은 사용자가 명시적으로
선택할 때만 만듭니다.

### 2. Runtime failure

```text
Runtime failure 발생
  → 진단 담당자를 하나만 선택
      ├─ 현재 task에서 진단하면 cx-debugging
      └─ 조사를 분리해야 하면 debugger
  → 실패를 재현하고 원인을 입증
  → 수정 요청이 있으면 원인을 해결하는 가장 작은 변경 적용
  → 가장 가까운 regression check 실행
  → Recovery 동작이 바뀌었을 때만 reliability-reviewer
```

같은 증거에서 의견을 두 개 얻기 위해 skill과 agent를 함께 실행하지
않습니다.

### 3. UI redesign

```text
넓은 범위의 UI 또는 UX 변경 요청
  → cx-design-director로 방향 설정
  → 필요할 때만 현재 browser 상태 확인
  → 승인된 방향 구현
  → Interaction 또는 semantics가 바뀌면 accessibility-tester
  → cx-visual-qa로 현재 렌더링 결과 판정
```

`cx-slopslap`은 사용자가 AI-slop 제거를 명시했을 때만 사용합니다.

### 4. 차단된 source가 포함된 deep comparison

```text
사용자가 deep research를 명시적으로 요청
  → cx-ultraresearch 사용
  → 차단된 공개 페이지에만 cx-insane-search 사용
  → 한 번의 fetch에서 받은 content + retrieval-evidence handoff 재사용
  → 증거가 실제로 좋아질 때만 별도 질문 위임
  → 출처와 함께 결론 설명
  → supported, unresolved, refuted, 관찰과 추론 구분
```

### 5. Resume과 scope recovery

```text
이전 context가 사라짐
  → cx-coding-agent-sessions로 정확한 task 복구
  → 승인된 Task Contract와 결정 확인
  → 현재 작업이 벗어났을 수 있으면 cx-scope-check
      ├─ Contract가 여전히 맞음 → 계속 진행
      └─ 중요한 변경이 필요함 → cx-interview로 돌아감
```

추가 사례는 [Workflow recipes](docs/WORKFLOWS.md)에 있습니다.

## 키트에서 하네스로

Highfloor는 지금 바로 쓸 수 있는 구성요소, 즉 이 저장소의 Codex 스킬과
전문 에이전트에서 시작합니다.

장기적인 방향은 같은 철학을 실행 환경에 적용하는 하네스입니다. 작업을
안내하고, 필요한 도움을 선택하며, 권한의 경계를 지키고, 실패에서
복구하며, 인간의 판단이 실질적으로 필요한 순간에 질문하는 시스템을
지향합니다.

## 저장소 구조

```text
highfloor-codex/
├── .github/              issue form, PR template, CI
├── agents/               설치 가능한 custom-agent TOML 27개
├── assets/               repository artwork
├── docs/                 설치, catalog, workflow, architecture
├── LICENSES/             upstream license text
├── manifest/             installer가 소유하는 정확한 목록
├── scripts/              repository·installer validation
├── skills/               CX governance와 설치 가능한 skill 15개
├── AGENTS.md             contributor용 Codex instruction
├── install.sh            install, update, doctor, uninstall
├── LICENSE               original-content license와 범위
├── README.md             canonical English overview
├── README_KR.md          한국어 overview
└── THIRD_PARTY_NOTICES.md
```

## 호환성

- POSIX `sh`가 있는 macOS 또는 Linux
- `curl`, `tar`, `find`, `sed`, `grep`, `diff`, `cmp`와 표준 file tool
- skill과 custom agent를 지원하는 Codex release
- repository validation과 `cx-analyze-video`용 Python 3.11+

선택적인 skill별 runtime:

- `cx-analyze-video`: `ffmpeg`, `ffprobe`; 공개 URL에만 `yt-dlp` 필요
- `cx-understand-codebase`: Node.js 22+, `npx`; 고정된 workspace package는
  첫 실행 때 분석 대상 repository나 installer-managed skill source가 아닌
  source-versioned user cache에 설치

Installer 자체는 dependency-free입니다. `config.toml`이나 system package를
수정하지 않으며 remote source archive가 필요할 때만 GitHub에 접속합니다.

## 보안

- 원격 스크립트는 `sh`에 전달하기 전에 검토하십시오.
- 재현 가능한 설치는 release tag를 고정하십시오.
- 설치 프로그램이 관리하는 대상은 두 개의 일반 텍스트 manifest로
  제한됩니다.
- 충돌 항목은 교체 전에 백업합니다.
- 업데이트는 관련 없는 스킬과 에이전트를 삭제하지 않습니다.
- 외부 video transcription은 사용자가 해당 영상의 audio upload와 cost
  boundary를 승인하기 전까지 비활성화됩니다.
- Codebase dashboard는 `127.0.0.1`에만 bind하고 random token을 요구하며
  자동으로 열리지 않습니다.
- 취약점은 public issue가 아니라 [SECURITY.md](SECURITY.md)의 절차로
  보고하십시오.

## 프로젝트 자료

- [기여 안내](CONTRIBUTING.md)
- [보안 정책](SECURITY.md)
- [지원 범위](SUPPORT.md)
- [행동 강령](CODE_OF_CONDUCT.md)
- [변경 기록](CHANGELOG.md)
- [릴리스 안내](docs/RELEASING.md)
- [저장소 아키텍처](docs/ARCHITECTURE.md)

기여는 분명한 책임, 사용자 권한, 증거와 원본 프로젝트에 대한 존중을
지킬 때 환영합니다. 커밋, pull request, merge, 검증, 버전과 릴리스
규칙은 기여 안내에 정리되어 있습니다.

## License와 upstream respect

이 collection은 mixed-license입니다.

### Upstream 프로젝트와 적용 방식

Highfloor는 실질적으로 가져오거나 수정한 모든 component의 출처를
보존합니다. 아래 표는 각 upstream이 제공한 기반과 Highfloor에서 다르게
구성한 이유를 요약합니다. 정확한 source pin, 유지한 파일, license와
수정 기록은 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), 각 adapted
skill의 `references/upstream*.md`, 그리고 `cx-*` 계열의
[migration manifest](skills/CX_MIGRATION_MANIFEST.md)에 기록되어 있습니다.

| Highfloor component | Upstream | Highfloor에서 적용한 방식 |
|---|---|---|
| `CODEX_AGENTS.md`와 동기화된 maintainer global instruction | [`multica-ai/andrej-karpathy-skills`](https://github.com/multica-ai/andrej-karpathy-skills) — upstream metadata의 MIT 표시 | 구현 전 사고, 단순성, 수술적 범위, 목표 중심 실행이라는 네 개념을 기존 Highfloor 구현 원칙 안에 독립적인 문장으로 녹였습니다. 중복 runtime skill이나 별도 checklist는 만들지 않았습니다. |
| `cx-analyze-video` | [`bradautomates/claude-video`](https://github.com/bradautomates/claude-video) — MIT | Frame, caption, focus range, deduplication, transcription engine은 유지합니다. Claude slash command와 hook은 Codex skill routing으로 바꾸고, preflight-only setup, 명시적 upload 승인, guarded cleanup과 evidence lane을 추가했습니다. |
| `cx-understand-codebase` | [`Egonex-AI/Understand-Anything`](https://github.com/Egonex-AI/Understand-Anything) — MIT | Scanner, semantic batching, graph schema, specialist prompt, incremental model과 interactive viewer를 보존합니다. 하나의 Codex skill과 action word, 정확한 worktree 분석, source-versioned runtime cache, partial-result boundary와 local token-gated serving을 적용했습니다. |
| `cx-interview`, `cx-acceptance-qa`, `cx-scope-check`, `cx-unstuck` | [`Q00/ouroboros`](https://github.com/Q00/ouroboros) — MIT | 요구사항 명료화, acceptance, drift 확인과 reframing 방법을 보존합니다. 단순 리네임이나 복사본이 아니라, Ouroboros 전용 MCP, session, scoring, orchestration과 persona runtime을 제외하고 독립 실행 가능한 Codex skill로 재작성했습니다. |
| `cx-coding-agent-sessions`, `cx-debugging`, `cx-programming`, `cx-ultraresearch`, `cx-visual-qa` | [`code-yeongyu/oh-my-openagent`](https://github.com/code-yeongyu/oh-my-openagent) — Sustainable Use License 1.0 | 원장의 skill을 Codex routing, permission boundary, 집중된 evidence와 Highfloor의 event-driven workflow에 맞게 압축·재구성하거나 수정했습니다. 문서에 표시된 일부 upstream 파일은 그대로 유지하거나 byte-identical 상태로 보존합니다. |
| `cx-browser-automation` | [`microsoft/playwright-cli`](https://github.com/microsoft/playwright-cli) — Apache-2.0 | Browser interaction을 Codex에 맞게 수정하고 local wrapper와 evidence 지침을 추가했으며, browser 조작과 최종 visual 판정을 분리했습니다. `vercel-labs/agent-browser`는 번들하지 않고 runtime dependency로 호출합니다. |
| `cx-insane-search` | [`fivetaku/insane-search`](https://github.com/fivetaku/insane-search) — MIT | 수정한 engine과 test material을 유지하면서 공개 콘텐츠 접근, permission, fallback과 failure boundary를 Codex에 맞게 다시 작성했습니다. |
| `cx-insane-search`, `cx-ultraresearch` | [`fivetaku/insane-research`](https://github.com/fivetaku/insane-research) — MIT | Retrieval metadata, source map, claim map, countersearch, contradiction, temporal evidence 개념 중 선택한 부분을 독립적인 문장으로 반영했습니다. 고정 7단계 orchestration, automatic agent fan-out, permission bypass, mandatory artifact, claim validator와 report evaluator는 포함하지 않습니다. |
| `cx-slopslap` | [`vibedesignlab/slopslap`](https://github.com/vibedesignlab/slopslap) — MIT | Upstream taxonomy, data, reference와 script를 보존하면서 host discovery, concurrency, Git behavior, report serving과 browser resolution을 수정했습니다. |
| `cx-design-director` | Original Highfloor content; optional [`ibelick/ui-skills`](https://github.com/ibelick/ui-skills) runtime lookup — MIT | Skill 자체는 Highfloor original material입니다. UI Skills는 외부 reference source로 호출할 수 있지만 그 내용을 번들하거나 Highfloor 소유로 표시하지 않습니다. |

### License 경계

- Original Highfloor content는 root [MIT License](LICENSE)를 따릅니다.
- Third-party와 derivative content는 각각의 upstream license를 유지합니다.
- Root MIT license는 derivative material을 재라이선스하지 않습니다.
- 개별 component를 추출하거나 재배포하기 전에 상세 provenance 기록을
  확인하십시오.

Sustainable Use License 1.0은 OSI-approved open-source license가 아니므로,
전체 repository를 MIT 또는 완전한 open-source bundle이라고 표현하지
마십시오. 완전한 OSI-compatible distribution이 필요하다면
`cx-coding-agent-sessions`, `cx-debugging`, `cx-programming`,
`cx-ultraresearch`, `cx-visual-qa`를 분리하거나 대체하고, 해당 material을
제외한 별도 versioned manifest를 공개해야 합니다.

## 경계

- Codex의 기본 정책과 사용자의 권한이 항상 우선합니다.
- 워크플로는 유용할 때 조합하는 예시이며, 모든 작업이 거쳐야 하는
  단계가 아닙니다.
- 설치 프로그램은 이 저장소의 manifest에 적힌 스킬과 에이전트만
  관리합니다. 선택 기능에 필요한 별도 실행 환경은 자동 설치하지
  않습니다.
- 사용할 수 있는 모델은 Codex 계정과 제품 환경에 따라 달라집니다.
- 공개 콘텐츠 도구는 로그인, paywall, CAPTCHA, 사설 네트워크와 권한
  경계에서 멈춥니다.
- Highfloor는 명확성, 안전성 또는 증거를 실질적으로 개선할 때만 절차를
  추가합니다.

## 상태

`0.1.0`은 첫 public release입니다. `1.0.0` 이전에는 interface가 발전할
수 있지만, name과 migration behavior는 이 첫 tag부터 semantic
versioning을 따릅니다.
