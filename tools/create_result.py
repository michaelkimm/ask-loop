#!/usr/bin/env python3
"""
최종 결과 마크다운 파일을 생성합니다.
stdin에서 콘텐츠를 읽어 sessions/{session_id}/result.md에 저장합니다.

사용법:
    echo "콘텐츠" | python3 tools/create_result.py --session-id "20250116_143052" --cycles "cycle_0.md,cycle_1.md,cycle_2.md"
"""
import argparse
import sys
import os


def main():
    parser = argparse.ArgumentParser(
        description='최종 결과 마크다운 파일 생성',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
예시:
    cat << 'EOF' | python3 tools/create_result.py --session-id "20250116_143052" --cycles "cycle_0.md,cycle_1.md"
    # 최종 요구사항

    ## 개요
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
        '--cycles',
        required=True,
        help='포함된 cycle 파일명들 (쉼표로 구분, 예: cycle_0.md,cycle_1.md)'
    )
    args = parser.parse_args()

    # stdin 확인
    if sys.stdin.isatty():
        print("오류: 콘텐츠는 stdin으로 제공해야 합니다.", file=sys.stderr)
        print("예시: echo '콘텐츠' | python3 tools/create_result.py --session-id ID --cycles FILES", file=sys.stderr)
        sys.exit(1)

    content = sys.stdin.read()

    if not content.strip():
        print("오류: 빈 콘텐츠입니다.", file=sys.stderr)
        sys.exit(1)

    # 프로젝트 루트 기준으로 sessions 디렉토리
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    session_dir = os.path.join(project_dir, 'sessions', args.session_id)

    if not os.path.exists(session_dir):
        print(f"오류: 세션 디렉토리가 존재하지 않습니다: {session_dir}", file=sys.stderr)
        sys.exit(1)

    # cycle 파일 존재 확인
    cycle_files = [f.strip() for f in args.cycles.split(',')]
    for cycle_file in cycle_files:
        cycle_path = os.path.join(session_dir, cycle_file)
        if not os.path.exists(cycle_path):
            print(f"경고: cycle 파일이 존재하지 않습니다: {cycle_path}", file=sys.stderr)

    # 파일 경로
    output_path = os.path.join(session_dir, 'result.md')

    # 파일 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"생성됨: {output_path}")
    print(f"크기: {len(content)} 바이트")
    print(f"기반 cycles: {', '.join(cycle_files)}")


if __name__ == '__main__':
    main()
