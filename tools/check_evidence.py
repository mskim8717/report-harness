#!/usr/bin/env python3
"""근거표 형식 검사. 사실이 원문과 맞는지는 검사하지 않는다(그건 source-verifier와 사람이 한다).

사용: python3 tools/check_evidence.py                 # evidence/*.md 전부
      python3 tools/check_evidence.py evidence/<주제>.md
검사: 표 머리 6열 · 행마다 6칸 · 첫 칸의 근거 번호(E-1 같은 형식, 1부터 차례대로) ·
      원문 칸의 URL · 정확한 위치 칸 · 확인 상태 어휘(CLAUDE.md 사실 기록 원칙).
문제가 있으면 파일 줄 번호와 함께 FAIL을 출력하고 종료 코드 1을 돌려준다.
"""
import glob
import os
import re
import sys

HEADER = ["기관", "사실", "상태·기준일·단위", "원문 제목·URL", "정확한 위치", "확인 상태"]
STATUS = ("확인(sources/ 저장본)", "확인(원문 추출", "확인(WebFetch 추출본)", "재확인 필요(미열람)", "재확인 필요(원문 열지 못함)")
ROW_ID = re.compile(r"^([A-Z])-(\d+)\s+\S")
URL = re.compile(r"https?://\S+")


def cells(line):
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return None
    return [c.strip() for c in re.split(r"(?<!\\)\|", s[1:-1])]


def check(path):
    fails, rows, in_table, seen = [], 0, False, {}
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    for no, line in enumerate(lines, 1):
        c = cells(line)
        if c is None:
            if in_table:
                break  # 표 하나만 본다
            continue
        if not in_table:
            if c == HEADER:
                in_table = True
            continue
        if all(set(x) <= set("-: ") for x in c):
            continue  # 구분 줄
        rows += 1
        if len(c) != 6:
            fails.append((no, "?", f"칸 수 {len(c)}개(6개여야 함)"))
            continue
        m = ROW_ID.match(c[0])
        rid = f"{m.group(1)}-{m.group(2)}" if m else c[0][:12] or "?"
        if not m:
            fails.append((no, rid, "첫 칸이 'E-1 GAO'처럼 근거 번호와 기관이 아님"))
        else:
            prev = seen.get(m.group(1), 0)
            if int(m.group(2)) != prev + 1:
                fails.append((no, rid, f"근거 번호 순서가 어긋남(앞 번호 {m.group(1)}-{prev})"))
            seen[m.group(1)] = int(m.group(2))
        if not c[1]:
            fails.append((no, rid, "사실 칸이 비어 있음"))
        if not c[2]:
            fails.append((no, rid, "상태·기준일·단위 칸이 비어 있음"))
        if not URL.search(c[3]):
            fails.append((no, rid, "원문 칸에 URL이 없음"))
        if not c[4]:
            fails.append((no, rid, "정확한 위치 칸이 비어 있음"))
        if not c[5].startswith(STATUS):
            fails.append((no, rid, f"확인 상태 어휘가 아님: '{c[5][:30]}'"))
    if not in_table:
        fails.append((0, "-", "근거표 머리(6열)를 찾지 못함: | " + " | ".join(HEADER) + " |"))
    return rows, fails


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = argv or sorted(glob.glob(os.path.join(root, "evidence", "*.md")))
    if not paths:
        print("evidence/에 근거표가 없습니다.")
        return 0
    bad = 0
    for p in paths:
        rows, fails = check(p)
        name = os.path.relpath(p, root)
        if fails:
            bad += 1
            for no, rid, msg in fails:
                print(f"FAIL {name}:{no} {rid} {msg}")
        else:
            print(f"OK   {name} ({rows}행)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
