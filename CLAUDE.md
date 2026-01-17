# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

MCP 기반 기술 조사로 요구사항을 구체화하는 Claude Code 커맨드 (`/refine`).

## 사용법

```bash
claude
> /refine path/to/spec.md
```

## 아키텍처

```
.claude/commands/refine.md    # /refine 커맨드 정의
.mcp.json                     # MCP 서버 설정 (Context7, Grep.app, Exa)
```

## /refine 워크플로우

1. **요구사항 분석** - 파일에서 기술/개념 식별
2. **MCP 조사** - 서브에이전트(Task)로 위임하여 컨텍스트 절약
   - Context7: 공식 문서
   - Grep.app: 구현 패턴
   - Exa: 최신 트렌드 (EXA_API_KEY 필요)
3. **리서치 저장** - `{파일명}-research_summary.md`, `{파일명}-research_detail.md`
4. **질문** - AskUserQuestion으로 옵션 제시 (모든 질문에 "팀 내부 조사 후 결정" 옵션 포함)
5. **반영** - 답변을 원본 파일에 덮어쓰기

## 인용 규칙

MCP로 조사한 내용만 출처 표시. 추론은 표시 안 함.

```markdown
JWT는 stateless라서 확장이 용이하다[1].

## 참고 자료
[1] https://auth0.com/..., "JWTs are stateless..."
```

## 출력 형식

`/refine` 결과물에는 반드시 포함:
- `## 미결정 사항` > `### 사전 조사 필요` - "팀 내부 조사 후 결정" 답변 항목
- `## 미결정 사항` > `### 조사 후 결정 필요` - 위 조사에 의존하는 결정

## 환경 설정

```bash
export EXA_API_KEY="..."  # Exa MCP용 (선택)
```
