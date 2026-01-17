[English](README.md) | [한국어](README.kr.md)

# Code Agent API Wrapper

A unified REST API wrapper that integrates multiple LLM CLI tools (Claude Code, Gemini CLI, Codex) into a single interface.

This project uses a plugin-based provider pattern, making it easy to add new CLI tools, and provides a consistent REST API interface across all providers.

## Prerequisites

- Python 3.10+
- One or more CLI tools installed:
  - [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) (Requires Claude Pro/Max subscription)
  - [Gemini CLI](https://github.com/google/gemini-cli)
  - [Codex CLI](https://github.com/openai/codex)

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/code-agent-api-wrapper.git
cd code-agent-api-wrapper

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

```bash
# Create environment configuration
cp .env.example .env
```

Edit `.env`:
```
PORT=8000
HOST=0.0.0.0
DEFAULT_PROVIDER=claude
```

**Configuration Options:**
- `PORT`: API server port (default: 8000)
- `HOST`: API server host (default: 0.0.0.0)
- `DEFAULT_PROVIDER`: Default provider when not specified (default: claude)

## Running the Server

```bash
python main.py
```

Once the server starts:
- API Documentation: http://localhost:8000/docs
- Web UI: http://localhost:8000
- Provider Status: http://localhost:8000/api/providers

## Web UI Features

- **Multi-line Input**: Shift+Enter for new line, Enter to send
- **API URL Management**: Switch between multiple API URLs via dropdown
- **Chat History**: Auto-save chats (max 20), load, or delete individual chats
- **Resizable Chat Window**: Drag the handle between message area and examples
- **Responsive Design**: Works perfectly on mobile and tablets
- **Auto-save**: Messages automatically saved to browser storage
- **Provider Selection**: Dropdown to choose between available providers

## API Usage

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/ask` | Send prompt to provider (recommended) |
| POST | `/ask` | Send to default provider (backwards compatible) |
| GET | `/api/providers` | List available providers with status |
| GET | `/health` | Health check |
| GET | `/` | Web UI |

### POST /api/ask (Recommended)

**Request:**
```json
{
  "provider": "claude",
  "prompt": "Hello, Claude!",
  "working_directory": null
}
```

**Response:**
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

**Response:**
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

### POST /ask (Backwards Compatibility)

**Request:**
```json
{
  "prompt": "Hello!",
  "working_directory": null
}
```

**Response:**
```json
{
  "success": true,
  "provider": "claude",
  "response": "Hello!",
  "execution_time": 6.2,
  "error": null
}
```

Automatically uses `DEFAULT_PROVIDER` configuration.

### Example Requests

**Using Claude provider:**
```bash
curl -X POST "http://localhost:8000/api/ask" \
  -H "Content-Type: application/json" \
  -d '{"provider": "claude", "prompt": "What is Python?"}'
```

**Using Gemini provider:**
```bash
curl -X POST "http://localhost:8000/api/ask" \
  -H "Content-Type: application/json" \
  -d '{"provider": "gemini", "prompt": "What is JavaScript?"}'
```

**Using Codex provider:**
```bash
curl -X POST "http://localhost:8000/api/ask" \
  -H "Content-Type: application/json" \
  -d '{"provider": "codex", "prompt": "Explain REST API"}'
```

**List available providers:**
```bash
curl "http://localhost:8000/api/providers"
```

## CLI Client

### Usage Examples

```bash
# Single question with default provider
python examples/cli_example.py "What is Python?"

# Specify provider
python examples/cli_example.py "What is Python?" --provider claude
python examples/cli_example.py "What is JavaScript?" --provider gemini
python examples/cli_example.py "Explain REST API" --provider codex

# List available providers
python examples/cli_example.py --providers

# Interactive mode
python examples/cli_example.py -i

# Interactive mode with specific provider
python examples/cli_example.py -i --provider gemini
```

### Custom API URL

```bash
# Windows CMD
set API_URL=http://localhost:8000
python examples/cli_example.py "Question"

# Windows PowerShell
$env:API_URL="http://localhost:8000"
python examples/cli_example.py "Question"

# Linux/Mac
export API_URL=http://localhost:8000
python examples/cli_example.py "Question"
```

## Project Structure

```
code-agent-api-wrapper/
├── main.py                      # FastAPI server
├── backend/                     # Backend module
│   ├── __init__.py
│   ├── config.py               # Configuration management
│   ├── models.py               # Pydantic models
│   └── providers/              # Provider implementations
│       ├── __init__.py         # Provider registry
│       ├── base.py             # Abstract base class
│       ├── claude.py           # Claude Code provider
│       ├── gemini.py           # Gemini CLI provider
│       └── codex.py            # Codex provider
├── examples/
│   ├── cli_example.py          # CLI client
│   └── index.html              # Web UI
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
├── README.md                   # English documentation
└── README.kr.md               # Korean documentation
```

## Architecture

### Provider Pattern

This project uses a plugin-based architecture for easy extensibility.

**Adding a New Provider:**

1. Create new file in `backend/providers/` (e.g., `myprovider.py`)
2. Extend `CLIProvider` abstract class
3. Implement `execute()` and `check_availability()` methods
4. Register in `backend/providers/__init__.py`

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
        # Implementation...
        pass

    async def check_availability(self):
        # Implementation...
        pass
```

After registration, it's automatically available via `/api/ask` and `/api/providers`.

## Providers

### Claude Code
- **Execution Method**: Temporary file approach (more robust for complex prompts)
- **Performance**: ~6 seconds per request
- **Availability Check**: `claude --version`

### Gemini CLI
- **Execution Method**: Direct string passing
- **Performance**: ~20 seconds per request (slower but reliable)
- **Availability Check**: `gemini --version`

### Codex
- **Execution Method**: Non-interactive exec subcommand
- **Performance**: ~4-5 seconds per request
- **Availability Check**: `codex --version`

## Important Notes

- Ensure all CLI tools are installed and authenticated before use
- Respect rate limits and usage policies of each CLI tool
- In production environments, add appropriate authentication/authorization
- Each provider has different response times; plan accordingly

## License

MIT License

## Contributing

Contributions are welcome! To add a new provider:

1. Create provider class extending `CLIProvider`
2. Implement `execute()` and `check_availability()`
3. Register in provider registry
4. Test thoroughly
5. Submit pull request

## Future Providers

- [ ] OpenAI ChatGPT CLI
- [ ] LLaMA CLI
- [ ] Local model runners
- [ ] Custom providers
