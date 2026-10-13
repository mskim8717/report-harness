# report-harness — 보고서 작성용 하네스 실습

감사연구원 AI 활용 교육 3일차 「보고서 작성용 하네스」 실습 폴더입니다. Claude Code가 이 폴더의 규칙(`CLAUDE.md`)과 절차(스킬)를 따라, 공식 원문에서 확인한 사실만 근거표에 적고, 위키로 정리한 뒤, 출처가 붙은 보고서 초안을 씁니다.

## 받기

터미널을 열고 아래 세 줄을 한 줄씩 넣고 Enter를 누릅니다.

```
git clone https://github.com/mskim8717/report-harness.git
cd report-harness
claude
```

- `git`이 없다는 메시지가 나오면: 이 페이지 위쪽 **Code → Download ZIP**으로 받아 압축을 풀고, 폴더 이름을 `report-harness`로 바꿔 홈 폴더에 둡니다.
- `claude`를 넣었을 때 아래쪽에 입력창이 뜨면 됩니다. 처음 열 때 이 폴더를 신뢰하는지 물으면 신뢰한다고 답합니다.

입력창이 뜨면 영국 NAO 원문을 받습니다. 이 PDF는 NAO 저작권 조건 때문에 저장소에 넣지 않았고, 공식 사이트에서 각자 받습니다. 아래 문장을 Claude 입력창에 붙여 넣고, 확인 창이 뜨면 허용을 고릅니다.

```
영국 NAO의 AI 전략 원문 PDF를 공식 주소 https://www.nao.org.uk/wp-content/uploads/2026/08/The-NAOs-AI-Strategy.pdf 에서 받아 sources/해외감사기구/The-NAOs-AI-Strategy.pdf로 저장해줘. 다른 파일은 고치지 마.
```

## 폴더

```
report-harness/
├── CLAUDE.md              규칙: 폴더·파일 이름·근거표와 위키 형식·보고서 형식
├── .claude/skills/
│   ├── collect-official-sources/   해외 감사기구 자료 수집 — 절차 1~4는 강의에서 채운다
│   ├── collect-nabo-budget/        국회예산정책처 예산 자료 수집 (완성본)
│   └── write-report-section/       보고서 초안 쓰기 (완성본)
├── .claude/agents/source-verifier.md   검토 담당자: 근거표 한 행을 원문과 대조
├── .claude/settings.json  sources/ 수정 금지 · 공식 사이트 읽기 허용
├── sources/               공식 원문 (읽기 전용, 폴더마다 _출처.md)
├── brief/                 의뢰서 — 템플릿과 예산 주제 의뢰서
├── evidence/  wiki/  report/   근거표 · 위키 · 보고서 초안 (스킬이 만든다). report/_보고서_템플릿.md는 초안의 머리·뼈대
├── tools/check_evidence.py     근거표 형식 검사
└── 교재/입력문카드.md      강의에서 복사해 붙여 넣는 카드
```

## 강의에서

`교재/입력문카드.md`의 카드를 순서대로 복사해 Claude 입력창에 붙여 넣습니다. 타이핑하지 않습니다.

- 직접 만드는 것: 수집 스킬의 절차 네 줄, 해외 감사기구 주제의 의뢰서 한 장
- 스킬이 만드는 것: 두 주제의 근거표·위키·보고서 초안
- 직접 확인하는 것: 보고서 문장 → 근거표 행 → 원문 쪽, 검토 담당자의 판정 표

## 원문 자료와 이용 조건

| 폴더 | 파일 | 이용 조건 |
| --- | --- | --- |
| `sources/해외감사기구/` | GAO AI Strategy (2026-08), Artificial Intelligence at GAO 웹 페이지 저장본, ECA Artificial Intelligence strategy 2026-2030 | GAO: 미국 GAO 저작물, 출처 표시 · ECA: CC BY 4.0(출처 표시·변경 표시) |
| `sources/국회예산정책처/` | 2026년도 예산안 총괄 분석 Ⅲ, NABO Focus 제132호 | 공공누리 제1유형(출처표시) |

- 영국 NAO의 「The NAO's AI Strategy」는 NAO 저작권 조건(연구·개인 학습용 복제만 허용) 때문에 이 저장소에 넣지 않았습니다. 위 「받기」의 문장으로 공식 사이트에서 각자 받습니다.
- PDF를 쪽 단위로 읽으려면 poppler(pdftoppm)가 필요합니다. GAO·ECA·국회예산정책처 PDF는 `_텍스트/` 추출본이 있어 없어도 읽지만, 수업 중 각자 받는 NAO PDF는 18쪽이라 쪽 지정 읽기가 필요하고 저작권 조건상 추출본을 둘 수 없습니다. **수업 전에 설치해 둡니다.** macOS `brew install poppler`, Windows `scoop install poppler` 또는 `choco install poppler`, Ubuntu `sudo apt install poppler-utils`. 터미널에서 `pdftoppm -v`가 버전을 보여주면 됩니다.
- 파일별 URL·발행일·출처 표시 문구는 각 폴더의 `_출처.md`에 있습니다. 이 저장소는 각 기관의 후원·보증을 받지 않았습니다.

## 근거표 형식 검사(선택)

Python이 있으면 근거표의 열·근거 번호·URL·위치·확인 상태 어휘를 검사할 수 있습니다. 사실이 원문과 맞는지는 검사하지 않습니다.

```
python3 tools/check_evidence.py
```
