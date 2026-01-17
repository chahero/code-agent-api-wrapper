**한국어** | [English](README.en.md)

# Multi-Provider CLI API Wrapper

여러 LLM CLI 도구(Claude Code, Gemini CLI 등)를 하나의 API로 통합하여 사용할 수 있게 해주는 프로젝트입니다.

프로바이더 패턴을 사용하여 손쉽게 새로운 CLI 도구를 추가할 수 있으며, 모든 프로바이더에 일관된 REST API 인터페이스를 제공합니다.

## 사전 요구사항

- Python 3.10+
- 하나 이상의 CLI 도구 설치:
  - [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) (Claude Pro/Max 구독 필요)
  - [Gemini CLI](https://github.com/google/gemini-cli)

## 설치

```bash
# 저장소 클론
git clone https://github.com/your-username/claude-code-api-wrapper.git
cd claude-code-api-wrapper

# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 의존성 설치
pip install fastapi uvicorn python-dotenv requests
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

![Web UI Screenshot](docs/screenshot1.png)

### 주요 기능

- **여러 줄 입력**: Shift+Enter로 줄바꿈, Enter로 전송
- **API URL 관리**: 헤더의 드롭다운에서 여러 개의 API URL 저장 및 전환
- **채팅 이력**: 모든 대화가 자동으로 저장되며, 최대 20개까지 보관
  - 저장된 채팅 클릭하여 복원 가능
  - 개별 또는 전체 삭제 가능
- **채팅창 크기 조절**: 메시지 영역과 예시 사이의 바를 드래그하여 크기 조절
- **모바일 반응형**: 모바일/태블릿에서도 완벽히 작동
- **자동 저장**: 입력한 메시지들이 자동으로 브라우저 저장소에 저장됨

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
  "execution_time": 1.234,
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
      "version": "1.0.0",
      "error": null
    },
    {
      "name": "gemini",
      "display_name": "Gemini CLI",
      "available": false,
      "version": null,
      "error": "Gemini CLI not found in PATH"
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
  "execution_time": 1.234,
  "error": null
}
```

자동으로 `DEFAULT_PROVIDER` 설정값을 사용합니다.

### 프로바이더 지정

**Claude 프로바이더 사용:**
```bash
curl -X POST "http://localhost:8000/api/ask" \
  -H "Content-Type: application/json" \
  -d '{"provider": "claude", "prompt": "Hello, Claude!"}'
```

**Gemini 프로바이더 사용:**
```bash
curl -X POST "http://localhost:8000/api/ask" \
  -H "Content-Type: application/json" \
  -d '{"provider": "gemini", "prompt": "Hello, Gemini!"}'
```

**작업 디렉토리 지정:**
```bash
curl -X POST "http://localhost:8000/api/ask" \
  -H "Content-Type: application/json" \
  -d '{"provider": "claude", "prompt": "이 폴더의 파일들을 분석해줘", "working_directory": "F:\\my_project"}'
```

**사용 가능한 프로바이더 확인:**
```bash
curl "http://localhost:8000/api/providers"
```

## 클라이언트 예시

### Python CLI

```bash
cd examples

# 단일 질문 (기본 프로바이더 사용)
python cli_example.py "What is Python?"

# 특정 프로바이더 지정
python cli_example.py "What is Python?" --provider claude

# 사용 가능한 프로바이더 확인
python cli_example.py --providers

# 대화형 모드
python cli_example.py -i

# 특정 프로바이더로 대화형 모드
python cli_example.py -i --provider gemini
```

### 웹 UI

브라우저에서 http://localhost:8000 접속하여 프로바이더 선택 드롭다운을 통해 다양한 CLI 도구 사용

## 프로젝트 구조

```
code-agent-api-wrapper/
├── main.py                  # FastAPI 서버
├── backend/                 # 백엔드 모듈
│   ├── __init__.py
│   ├── config.py           # 설정 관리
│   ├── models.py           # Pydantic 모델
│   └── providers/          # 프로바이더 구현
│       ├── __init__.py     # 프로바이더 레지스트리
│       ├── base.py         # 추상 기반 클래스
│       ├── claude.py       # Claude Code 프로바이더
│       └── gemini.py       # Gemini CLI 프로바이더
├── examples/
│   ├── cli_example.py      # CLI 클라이언트 예시
│   └── index.html          # 웹 UI
├── .env.example            # 환경변수 예시
├── requirements.txt        # Python 의존성
└── README.md              # 이 파일
```

## 주의사항

- 사용하려는 CLI 도구가 설치되어 있고 인증이 완료되어 있어야 합니다.
- 각 CLI 도구의 사용량 제한을 준수하세요.
- 프로덕션 환경에서 사용 시 적절한 인증/인가를 추가하세요.

## 아키텍처

### 프로바이더 패턴

이 프로젝트는 플러그인 아키텍처를 사용하여 새로운 CLI 도구를 쉽게 추가할 수 있도록 설계되었습니다.

**새 프로바이더 추가:**

1. `backend/providers/` 디렉토리에 새 파일 생성 (예: `codex.py`)
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

그러면 자동으로 `/api/ask` 및 `/api/providers` 엔드포인트에서 사용 가능합니다.

## 라이선스

MIT License
