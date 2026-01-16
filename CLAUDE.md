# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

사용자의 초기 요구사항을 최대 5회의 반복 사이클을 통해 점진적으로 구체화하는 단일 에이전트 시스템입니다.

## 핵심 명령어

```bash
# Cycle 파일 생성 (stdin으로 콘텐츠 전달)
cat << 'EOF' | python3 tools/create_cycle.py --session-id "YYYYMMDD_HHmmss" --cycle-number N
...콘텐츠...
EOF

# Result 파일 생성
cat << 'EOF' | python3 tools/create_result.py --session-id "ID" --cycles "cycle_0.md,cycle_1.md"
...콘텐츠...
EOF

# 구조적 검증 (의미적 검증은 Subagent로 별도 수행)
python3 tools/validate_spec.py --session-id "ID" --target-file "cycle_1.md" --spec-type cycle
```

## 아키텍처

```
Refinement Agent (단일 에이전트)
    │
    ├── 분석 → 충분성 판단 ─┬─ 충분 → result.md 생성
    │                      └─ 불충분 → AskUserQuestion → cycle 생성
    │
    ├── tools/
    │   ├── create_cycle.py    # stdin → sessions/{id}/cycle_{n}.md
    │   ├── create_result.py   # stdin → sessions/{id}/result.md
    │   └── validate_spec.py   # 구조적 검증 (의미적은 Subagent)
    │
    ├── specs/                 # 검증 기준 정의
    │   ├── cycle.spec.md      # 필수 섹션, 최소 200자
    │   └── result.spec.md     # 필수 섹션, 최소 500자
    │
    └── Hook: fast-fail-check.sh  # Write 후 자동 실행, 토큰 비용 0
```

## 핵심 규칙

1. **이전 cycle 파일 하나만 읽음** - 컨텍스트 최소화
2. **새로 언급된 기술만 MCP로 조사** - 중복 조사 방지
3. **충분성 판단을 질문 전에 수행** - 충분하면 STEP 4로 직행
4. **인용 시스템 필수** - 주장에 [1], [2] 표시 + `## 참고 자료`에 URL/원문 기록

## 워크플로우

상세 워크플로우와 출력물 예시는 `agents/refinement-agent.md` 참조.
도구 사용법 상세는 `skills/refinement/SKILL.md` 참조.

## 환경 설정

```bash
chmod +x scripts/*.sh tools/*.py
export EXA_API_KEY="..."            # Exa MCP용 (선택)
```
