[English](README.md) | [한국어](README.kr.md)

# Code Agent API Wrapper

여러 LLM CLI 도구(Claude Code, Gemini CLI, Codex)를 하나의 REST API로 통합하여 사용할 수 있게 해주는 프로젝트입니다.

프로바이더 패턴을 사용하여 손쉽게 새로운 CLI 도구를 추가할 수 있으며, 모든 프로바이더에 일관된 REST API 인터페이스를 제공합니다.

## 사전 요구사항

- Python 3.10+
- 하나 이상의 CLI 도구 설치:
  - [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) (Claude Pro/Max 구독 필요)
  - [Gemini CLI](https://github.com/google/gemini-cli)
  - [Codex CLI](https://github.com/openai/codex)

## 설치

```bash
# 저장소 클론
git clone https://github.com/your-username/code-agent-api-wrapper.git
cd code-agent-api-wrapper

# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

## 설정

```bash
# 환경변수 파일 생성
cp .env.example .env
```

`.env` 파일 편집:
```
PORT=8000
HOST=0.0.0.0
DEFAULT_PROVIDER=claude
```

**설정 옵션:**
- `PORT`: API 서버 포트 (기본값: 8000)
- `HOST`: API 서버 호스트 (기본값: 0.0.0.0)
- `DEFAULT_PROVIDER`: 기본 프로바이더 (기본값: claude)

## 실행

```bash
python main.py
```

서버가 시작되면:
- API 문서: http://localhost:8000/docs
- 웹 UI: http://localhost:8000
- 프로바이더 상태: http://localhost:8000/api/providers

## 웹 UI 기능

- **여러 줄 입력**: Shift+Enter로 줄바꿈, Enter로 전송
- **API URL 관리**: 드롭다운에서 여러 개의 API URL 저장 및 전환
- **채팅 이력**: 모든 대화가 자동으로 저장되며, 최대 20개까지 보관
  - 저장된 채팅 클릭하여 복원 가능
  - 개별 또는 전체 삭제 가능
- **채팅창 크기 조절**: 메시지 영역과 예시 사이의 바를 드래그하여 조절
- **모바일 반응형**: 모바일/태블릿에서도 완벽히 작동
- **자동 저장**: 입력한 메시지들이 자동으로 브라우저 저장소에 저장됨
- **프로바이더 선택**: 드롭다운을 통해 사용 가능한 프로바이더 선택

## API 사용법

### 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/ask` | 프로바이더에 질문 (권장) |
| POST | `/ask` | 기본 프로바이더에 질문 (하위호환성) |
| GET | `/api/providers` | 사용 가능한 프로바이더 목록 |
| GET | `/health` | 서버 상태 확인 |
| GET | `/` | 웹 UI |

### POST /api/ask (권장)

**요청:**
```json
{
  "provider": "claude",
  "prompt": "Hello, Claude!",
  "working_directory": null
}
```

**응답:**
```json
{
  "success": true,
  "provider": "claude",
  "response": "Hello! How can I help you today?",
  "execution_time": 6.2,
  "error": null
}
```

### GET /api/providers

**응답:**
```json
{
  "providers": [
    {
      "name": "claude",
      "display_name": "Claude Code",
      "available": true,
      "version": "2.1.9 (Claude Code)",
      "error": null
    },
    {
      "name": "gemini",
      "display_name": "Gemini CLI",
      "available": true,
      "version": "0.24.0",
      "error": null
    },
    {
      "name": "codex",
      "display_name": "Codex",
      "available": true,
      "version": "codex-cli 0.41.0",
      "error": null
    }
  ]
}
```

### POST /ask (하위호환성)

**요청:**
```json
{
  "prompt": "Hello!",
  "working_directory": null
}
```

**응답:**
```json
{
  "success": true,
  "provider": "claude",
  "response": "Hello!",
  "execution_time": 6.2,
  "error": null
}
```

자동으로 `DEFAULT_PROVIDER` 설정값을 사용합니다.

### 요청 예시

**Claude 프로바이더 사용:**
```bash
curl -X POST "http://localhost:8000/api/ask" \
  -H "Content-Type: application/json" \
  -d '{"provider": "claude", "prompt": "Python이 뭐야?"}'
```

**Gemini 프로바이더 사용:**
```bash
curl -X POST "http://localhost:8000/api/ask" \
  -H "Content-Type: application/json" \
  -d '{"provider": "gemini", "prompt": "JavaScript가 뭐야?"}'
```

**Codex 프로바이더 사용:**
```bash
curl -X POST "http://localhost:8000/api/ask" \
  -H "Content-Type: application/json" \
  -d '{"provider": "codex", "prompt": "REST API 설명"}'
```

**사용 가능한 프로바이더 확인:**
```bash
curl "http://localhost:8000/api/providers"
```

## CLI 클라이언트

### 사용 예시

```bash
# 기본 프로바이더로 단일 질문
python examples/cli_example.py "Python이 뭐야?"

# 특정 프로바이더 지정
python examples/cli_example.py "Python이 뭐야?" --provider claude
python examples/cli_example.py "JavaScript가 뭐야?" --provider gemini
python examples/cli_example.py "REST API 설명" --provider codex

# 사용 가능한 프로바이더 확인
python examples/cli_example.py --providers

# 대화형 모드
python examples/cli_example.py -i

# 특정 프로바이더로 대화형 모드
python examples/cli_example.py -i --provider gemini
```

### 커스텀 API URL

```bash
# Windows CMD
set API_URL=http://localhost:8000
python examples/cli_example.py "질문"

# Windows PowerShell
$env:API_URL="http://localhost:8000"
python examples/cli_example.py "질문"

# Linux/Mac
export API_URL=http://localhost:8000
python examples/cli_example.py "질문"
```

## 프로젝트 구조

```
code-agent-api-wrapper/
├── main.py                      # FastAPI 서버
├── backend/                     # 백엔드 모듈
│   ├── __init__.py
│   ├── config.py               # 설정 관리
│   ├── models.py               # Pydantic 모델
│   └── providers/              # 프로바이더 구현
│       ├── __init__.py         # 프로바이더 레지스트리
│       ├── base.py             # 추상 기반 클래스
│       ├── claude.py           # Claude Code 프로바이더
│       ├── gemini.py           # Gemini CLI 프로바이더
│       └── codex.py            # Codex 프로바이더
├── examples/
│   ├── cli_example.py          # CLI 클라이언트
│   └── index.html              # 웹 UI
├── .env.example                # 환경변수 템플릿
├── requirements.txt            # Python 의존성
├── README.md                   # 영어 문서
└── README.kr.md               # 한국어 문서
```

## 아키텍처

### 프로바이더 패턴

이 프로젝트는 플러그인 아키텍처를 사용하여 새로운 CLI 도구를 쉽게 추가할 수 있도록 설계되었습니다.

**새 프로바이더 추가:**

1. `backend/providers/` 디렉토리에 새 파일 생성 (예: `myprovider.py`)
2. `CLIProvider` 추상 클래스 상속
3. `execute()`와 `check_availability()` 메서드 구현
4. `backend/providers/__init__.py`에 등록

```python
from .base import CLIProvider

class MyProvider(CLIProvider):
    @property
    def name(self) -> str:
        return "myprovider"

    @property
    def display_name(self) -> str:
        return "My CLI Tool"

    async def execute(self, prompt: str, working_directory=None):
        # 구현...
        pass

    async def check_availability(self):
        # 구현...
        pass
```

등록 후 자동으로 `/api/ask` 및 `/api/providers` 엔드포인트에서 사용 가능합니다.

## 프로바이더 설명

### Claude Code
- **실행 방식**: 임시 파일 방식 (복잡한 프롬프트에 더 안정적)
- **성능**: 요청당 약 6초
- **가용성 확인**: `claude --version`

### Gemini CLI
- **실행 방식**: 직접 문자열 전달
- **성능**: 요청당 약 20초 (느리지만 안정적)
- **가용성 확인**: `gemini --version`

### Codex
- **실행 방식**: Non-interactive exec 서브커맨드
- **성능**: 요청당 약 4-5초
- **가용성 확인**: `codex --version`

## 주의사항

- 사용하려는 CLI 도구가 설치되어 있고 인증이 완료되어 있어야 합니다
- 각 CLI 도구의 사용량 제한을 준수하세요
- 프로덕션 환경에서 사용 시 적절한 인증/인가를 추가하세요
- 각 프로바이더마다 응답 시간이 다르므로 이를 고려하여 사용하세요

## 라이선스

MIT License

## 기여하기

기여는 언제나 환영합니다! 새로운 프로바이더를 추가하려면:

1. `CLIProvider`를 상속하는 프로바이더 클래스 생성
2. `execute()`와 `check_availability()` 구현
3. 프로바이더 레지스트리에 등록
4. 철저히 테스트
5. Pull Request 제출

## 향후 지원 예정 프로바이더

- [ ] OpenAI ChatGPT CLI
- [ ] LLaMA CLI
- [ ] 로컬 모델 러너
- [ ] 커스텀 프로바이더
