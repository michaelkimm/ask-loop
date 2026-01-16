# Refinement Tools

요구사항 구체화 작업을 위한 도구 사용법입니다.

## validate_spec

출력물이 명세를 준수하는지 검증합니다.

```bash
# 구조적 검증만 (빠름, API 호출 없음)
python3 tools/validate_spec.py \
  --session-id "<session_id>" \
  --target-file "<file_name>" \
  --spec-type "<cycle|result>" \
  --structural-only

# 전체 검증 (구조적 + 의미적, API 호출 포함)
python3 tools/validate_spec.py \
  --session-id "<session_id>" \
  --target-file "<file_name>" \
  --spec-type "<cycle|result>"
```

**Exit 코드:**
- `0`: 검증 통과
- `1`: 비차단 오류 (API 미사용 가능 등)
- `2`: 차단 오류 (명세 위반, 재시도 필요)

## create_cycle

Cycle 마크다운 파일을 생성합니다.

```bash
cat << 'EOF' | python3 tools/create_cycle.py \
  --session-id "<session_id>" \
  --cycle-number <n>
# 요구사항 구체화 - Cycle {n}

## 이번 사이클 질문
...

## 사용자 응답
...

## 현재까지 구체화된 요구사항
...

## 고려했지만 미반영된 사항
...

## 다음 사이클 검토 필요 사항
...
EOF
```

## create_result

최종 결과 파일을 생성합니다.

```bash
cat << 'EOF' | python3 tools/create_result.py \
  --session-id "<session_id>" \
  --cycles "<comma_separated_files>"
# 최종 요구사항

## 개요
...

## 상세 요구사항
...

## 고려했지만 미반영된 사항
...

## 구체화 히스토리
...
EOF
```

## 세션 ID 생성

세션 ID는 `{YYYYMMDD}_{HHmmss}` 형식을 사용합니다.

```bash
# 예시
SESSION_ID=$(date +"%Y%m%d_%H%M%S")
echo $SESSION_ID  # 20250116_143052
```

## MCP 활용

새로 언급된 기술 스택에 대해서만 MCP를 호출합니다:

| MCP | 용도 | 호출 시점 |
|-----|------|----------|
| Context7 | 공식 문서 조회 | 설정값, API 스펙 확인 필요 시 |
| Grep.app | 코드 패턴 검색 | 실제 구현 예시 필요 시 |
| Exa | 웹 검색 | 최신 트렌드, 비교 자료 필요 시 |

**주의:** 이미 조사한 기술은 재조사하지 않습니다.
