# ask-loop

요구사항을 MCP 조사 기반 질문으로 구체화하는 Claude Code 커맨드.

## 사용법

```bash
claude
> /refine spec.md
```

더 구체화가 필요하면 다시 `/refine spec.md` 호출.

## 동작

1. **요구사항 분석** - 파일 읽고 기술/개념 식별
2. **MCP 조사** - 서브에이전트로 위임 (컨텍스트 절약)
   - Context7: 공식 문서
   - Grep.app: 구현 패턴
   - Exa: 최신 트렌드
3. **조사 기반 질문** - 트레이드오프 포함한 옵션 제시
4. **답변 반영** - 파일에 덮어쓰기

## 인용 규칙

MCP로 조사한 내용만 출처 표시. 추론은 표시 안 함.

```markdown
JWT는 stateless라서 확장이 용이하다[1].

## 참고 자료
[1] https://auth0.com/..., "JWTs are stateless..."
```

## 환경 설정

```bash
export EXA_API_KEY="..."  # Exa MCP용 (선택)
```
