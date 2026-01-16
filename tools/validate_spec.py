#!/usr/bin/env python3
"""
출력물이 명세를 준수하는지 검증합니다.
구조적 검증은 결정론적으로 수행하고, 의미적 검증은 Refinement Agent가 직접 수행합니다.

사용법:
    python3 tools/validate_spec.py --session-id "20250116_143052" --target-file "cycle_1.md" --spec-type "cycle"

Exit 코드:
    0: 검증 통과
    2: 차단 오류 (명세 위반)
"""
import argparse
import sys
import os
import re
import json


def validate_cycle_structural(content: str) -> list[str]:
    """Cycle 파일의 구조적 검증 (결정론적)"""
    errors = []

    # 제목 검증
    if not re.search(r'^# 요구사항 구체화 - Cycle \d+', content, re.MULTILINE):
        errors.append("제목 형식 오류: '# 요구사항 구체화 - Cycle {n}' 필요")

    # 필수 섹션 검증
    required_sections = [
        '## 이번 사이클 질문',
        '## 사용자 응답',
        '## 현재까지 구체화된 요구사항',
        '## 고려했지만 미반영된 사항',
        '## 다음 사이클 검토 필요 사항',
        '## 참고 자료'
    ]
    for section in required_sections:
        if section not in content:
            errors.append(f"필수 섹션 누락: {section}")

    # 정량적 검증
    if len(content) < 200:
        errors.append(f"최소 길이 미달: {len(content)}자 (200자 이상 필요)")

    return errors


def validate_result_structural(content: str) -> list[str]:
    """Result 파일의 구조적 검증 (결정론적)"""
    errors = []

    # 제목 검증
    if '# 최종 요구사항' not in content:
        errors.append("제목 누락: '# 최종 요구사항' 필요")

    # 필수 섹션 검증
    required_sections = [
        '## 개요',
        '## 상세 요구사항',
        '## 고려했지만 미반영된 사항',
        '## 구체화 히스토리',
        '## 참고 자료'
    ]
    for section in required_sections:
        if section not in content:
            errors.append(f"필수 섹션 누락: {section}")

    # 정량적 검증
    if len(content) < 500:
        errors.append(f"최소 길이 미달: {len(content)}자 (500자 이상 필요)")

    return errors


def validate_semantic(content: str, spec_type: str, spec_content: str) -> dict:
    """의미적 검증 - Refinement Agent(Claude Code)가 직접 수행"""
    return {
        'valid': True,
        'skipped': True,
        'message': '의미적 검증은 Refinement Agent가 직접 수행합니다. specs/*.spec.md 참조.'
    }


def main():
    parser = argparse.ArgumentParser(
        description='출력물 명세 검증',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--session-id',
        required=True,
        help='세션 식별자'
    )
    parser.add_argument(
        '--target-file',
        required=True,
        help='검증할 파일명 (예: cycle_1.md, result.md)'
    )
    parser.add_argument(
        '--spec-type',
        required=True,
        choices=['cycle', 'result'],
        help='명세 유형'
    )
    parser.add_argument(
        '--structural-only',
        action='store_true',
        help='구조적 검증만 수행 (API 호출 없음)'
    )
    args = parser.parse_args()

    # 경로 설정
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    target_path = os.path.join(project_dir, 'sessions', args.session_id, args.target_file)
    spec_path = os.path.join(project_dir, 'specs', f'{args.spec_type}.spec.md')

    # 파일 존재 확인
    if not os.path.exists(target_path):
        print(f"오류: 대상 파일이 존재하지 않습니다: {target_path}", file=sys.stderr)
        sys.exit(2)

    if not os.path.exists(spec_path):
        print(f"오류: 명세 파일이 존재하지 않습니다: {spec_path}", file=sys.stderr)
        sys.exit(2)

    # 파일 읽기
    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()

    with open(spec_path, 'r', encoding='utf-8') as f:
        spec_content = f.read()

    # 구조적 검증
    if args.spec_type == 'cycle':
        structural_errors = validate_cycle_structural(content)
    else:
        structural_errors = validate_result_structural(content)

    if structural_errors:
        print("구조적 검증 실패:", file=sys.stderr)
        for err in structural_errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(2)

    print("구조적 검증 통과")

    if args.structural_only:
        print("의미적 검증 스킵 (--structural-only)")
        sys.exit(0)

    # 의미적 검증
    result = validate_semantic(content, args.spec_type, spec_content)

    if result.get('skipped'):
        print(f"의미적 검증: {result.get('message')}")
        sys.exit(0)

    if result.get('error'):
        print(f"의미적 검증 오류: {result['error']}", file=sys.stderr)
        sys.exit(1)  # 비차단 오류

    if not result.get('valid'):
        print("의미적 검증 실패:", file=sys.stderr)
        for issue in result.get('issues', []):
            print(f"  - {issue}", file=sys.stderr)
        sys.exit(2)

    print(f"의미적 검증 통과 (품질 점수: {result.get('quality_score', 'N/A')}/10)")


if __name__ == '__main__':
    main()
