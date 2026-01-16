# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

사용자의 초기 요구사항을 최대 5회의 반복 사이클을 통해 점진적으로 구체화하는 단일 에이전트 시스템입니다. 각 사이클마다 MCP를 통해 기술 조사를 수행하고, 구조적/의미적 검증을 거쳐 품질을 보장합니다.

## 핵심 명령어

```bash
# 세션 ID 생성
SESSION_ID=$(date +"%Y%m%d_%H%M%S")

# Cycle 파일 생성 (stdin으로 콘텐츠 전달)
cat << 'EOF' | python3 tools/create_cycle.py --session-id "$SESSION_ID" --cycle-number N
...콘텐츠...
EOF

# Result 파일 생성
cat << 'EOF' | python3 tools/create_result.py --session-id "$SESSION_ID" --cycles "cycle_0.md,cycle_1.md"
...콘텐츠...
EOF

# 구조적 검증
python3 tools/validate_spec.py --session-id "$SESSION_ID" --target-file "cycle_1.md" --spec-type cycle
```

## 검증 체계

### 구조적 검증 (validate_spec.py)

- Exit 0: 통과 / Exit 2: 차단 오류 (재시도 필요)
- cycle: 필수 섹션 6개 + 최소 200자
- result: 필수 섹션 5개 + 최소 500자

### 의미적 검증 (Subagent)

구조적 검증 후 Task(subagent_type="general-purpose")로 수행:
1. `specs/{type}.spec.md`의 "의미적 명세" 섹션 읽기
2. 대상 파일 검증
3. JSON 결과 반환: `{"valid": bool, "issues": [...], "suggestions": [...]}`

상세는 `skills/refinement/SKILL.md`의 "의미적 검증" 섹션 참조.

## 아키텍처

```
Refinement Agent (단일 에이전트)
    │
    ├── 분석 → 충분성 판단 ─┬─ 충분 → result.md 생성
    │                      └─ 불충분 → AskUserQuestion → cycle 생성
    │
    ├── tools/                 # Python 유틸리티
    │   ├── create_cycle.py    # stdin → sessions/{id}/cycle_{n}.md
    │   ├── create_result.py   # stdin → sessions/{id}/result.md
    │   └── validate_spec.py   # 구조적 검증 (Exit 0/2)
    │
    ├── specs/                 # 검증 기준 정의
    │   ├── cycle.spec.md      # 구조적 + 의미적 명세
    │   └── result.spec.md     # 구조적 + 의미적 명세
    │
    ├── MCP 서버               # 기술 조사용
    │   ├── Context7           # 공식 문서 조회
    │   ├── Grep.app           # 코드 패턴 검색
    │   └── Exa                # 웹 검색 (EXA_API_KEY 필요)
    │
    └── Hook: fast-fail-check.sh  # Write 후 자동 실행, 토큰 비용 0
```

## 핵심 규칙

1. **이전 cycle 파일 하나만 읽음** - 컨텍스트 최소화, 히스토리 전체 읽지 않음
2. **미조사 기술만 MCP로 조사** - `investigated_techs` 집합으로 중복 방지
3. **충분성 판단을 질문 전에 수행** - 모든 요건 충족 시 STEP 4로 직행
4. **인용 시스템 필수** - 주장에 [1], [2] 표시 + `## 참고 자료`에 URL/원문 기록

## 워크플로우

1. **STEP 1**: 초기 요구사항 확보 → cycle_0.md
2. **STEP 2**: 분석 → 충분성 판단 → (불충분 시) 질문 → cycle_n.md → 검증
3. **STEP 3**: max_iterations 도달 시 추가 반복 확인
4. **STEP 4**: result.md 생성 → 검증 → 완료

상세 워크플로우와 출력물 예시는 `agents/refinement-agent.md` 참조.

## 출력물 구조

```
sessions/{YYYYMMDD_HHMMSS}/
├── cycle_0.md    # 초기 요구사항
├── cycle_1.md    # 1차 구체화
├── ...
└── result.md     # 최종 요구사항 문서
```

## 환경 설정

```bash
chmod +x scripts/*.sh tools/*.py
export EXA_API_KEY="..."            # Exa MCP용 (선택)
```
