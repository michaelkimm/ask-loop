#!/bin/bash
set -euo pipefail

# Fast-fail 검증 스크립트
# Hook에서 호출되어 기본적인 파일 유효성을 검증합니다.
# 토큰 비용 0으로 즉시 실행됩니다.

# 스크립트 위치 기준으로 프로젝트 루트 찾기
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# 최신 세션 디렉토리 찾기
LATEST_SESSION=$(ls -td "${PROJECT_DIR}/sessions"/*/ 2>/dev/null | head -1 || echo "")

# 세션 디렉토리가 없으면 통과 (아직 세션 시작 전)
if [ -z "$LATEST_SESSION" ]; then
    exit 0
fi

# 최신 .md 파일 찾기
TARGET_FILE=$(ls -t "${LATEST_SESSION}"*.md 2>/dev/null | head -1 || echo "")

# 파일이 없으면 통과
if [ -z "$TARGET_FILE" ]; then
    exit 0
fi

# 파일 존재 확인
if [ ! -f "$TARGET_FILE" ]; then
    echo "오류: 파일이 존재하지 않습니다: $TARGET_FILE" >&2
    exit 2
fi

# 빈 파일 확인
if [ ! -s "$TARGET_FILE" ]; then
    echo "오류: 파일이 비어있습니다: $TARGET_FILE" >&2
    exit 2
fi

# 최소 크기 확인 (50 바이트)
FILE_SIZE=$(wc -c < "$TARGET_FILE")
if [ "$FILE_SIZE" -lt 50 ]; then
    echo "오류: 파일이 너무 작습니다: ${FILE_SIZE}B (최소 50B 필요)" >&2
    exit 2
fi

# UTF-8 인코딩 확인
if ! file "$TARGET_FILE" | grep -qE "UTF-8|ASCII|text"; then
    echo "오류: UTF-8 또는 ASCII 인코딩이 아닙니다" >&2
    exit 2
fi

# 모든 검증 통과
exit 0
