# ask-loop

사용자의 초기 요구사항을 최대 5회의 반복 사이클을 통해 점진적으로 구체화하는 Claude Code 에이전트 시스템.

## 사전 준비

```bash
# 스크립트 실행 권한 부여
chmod +x scripts/*.sh tools/*.py

# (선택) Exa MCP 사용 시
export EXA_API_KEY="your-api-key"
```

## 실행 방법

1. 이 디렉토리에서 Claude Code 실행:
   ```bash
   claude
   ```

2. 요구사항 구체화 요청:
   ```
   요구사항을 구체화해줘
   ```

3. 에이전트가 `agents/refinement-agent.md` 워크플로우에 따라:
   - 초기 요구사항 질문
   - 반복적 구체화 (최대 5회)
   - `sessions/{YYYYMMDD_HHmmss}/` 에 결과 저장

## 출력물

```
sessions/{session_id}/
├── cycle_0.md    # 초기 요구사항
├── cycle_1.md    # 1차 구체화
├── ...
└── result.md     # 최종 요구사항 문서
```

## 구조

- `agents/` - 에이전트 워크플로우 정의
- `tools/` - Python 도구 (cycle/result 생성, 검증)
- `specs/` - 출력물 명세 (검증 기준)
- `skills/` - 도구 사용법 문서
