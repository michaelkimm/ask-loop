#!/usr/bin/env python3
"""
Cycle 마크다운 파일을 생성합니다.
stdin에서 콘텐츠를 읽어 sessions/{session_id}/cycle_{n}.md에 저장합니다.

사용법:
    echo "콘텐츠" | python3 tools/create_cycle.py --session-id "20250116_143052" --cycle-number 1
"""
import argparse
import sys
import os
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(
        description='Cycle 마크다운 파일 생성',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
예시:
    cat << 'EOF' | python3 tools/create_cycle.py --session-id "20250116_143052" --cycle-number 1
    # 요구사항 구체화 - Cycle 1

    ## 이번 사이클 질문
    ...
    EOF
        '''
    )
    parser.add_argument(
        '--session-id',
        required=True,
        help='세션 식별자 (예: 20250116_143052)'
    )
    parser.add_argument(
        '--cycle-number',
        type=int,
        required=True,
        help='사이클 번호 (0부터 시작)'
    )
    args = parser.parse_args()

    # stdin 확인
    if sys.stdin.isatty():
        print("오류: 콘텐츠는 stdin으로 제공해야 합니다.", file=sys.stderr)
        print("예시: echo '콘텐츠' | python3 tools/create_cycle.py --session-id ID --cycle-number N", file=sys.stderr)
        sys.exit(1)

    content = sys.stdin.read()

    if not content.strip():
        print("오류: 빈 콘텐츠입니다.", file=sys.stderr)
        sys.exit(1)

    # 프로젝트 루트 기준으로 sessions 디렉토리 생성
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    session_dir = os.path.join(project_dir, 'sessions', args.session_id)

    os.makedirs(session_dir, exist_ok=True)

    # 파일 경로
    output_path = os.path.join(session_dir, f'cycle_{args.cycle_number}.md')

    # 파일 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"생성됨: {output_path}")
    print(f"크기: {len(content)} 바이트")


if __name__ == '__main__':
    main()
