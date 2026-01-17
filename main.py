"""Multi-provider CLI API wrapper using FastAPI."""

import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.config import config
from backend.models import PromptRequest, PromptResponse, ProviderInfo, ProvidersListResponse
from backend.providers import registry

load_dotenv()

app = FastAPI(
    title="Multi-Provider CLI API Wrapper",
    description="Universal CLI API wrapper supporting multiple LLM providers",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/ask", response_model=PromptResponse)
async def ask_llm(request: PromptRequest):
    """
    Send prompt to specified provider.

    Args:
        request: PromptRequest with provider, prompt, and optional working_directory

    Returns:
        PromptResponse with success status and response/error
    """
    # Determine which provider to use
    provider_name = request.provider or config.DEFAULT_PROVIDER

    # Get the provider
    provider = registry.get(provider_name)
    if not provider:
        available = ", ".join(registry.list_all().keys())
        raise HTTPException(
            status_code=404,
            detail=f"Provider '{provider_name}' not found. Available: {available}"
        )

    # Execute the prompt
    result = await provider.execute(request.prompt, request.working_directory)

    return PromptResponse(
        provider=provider_name,
        **result
    )


@app.post("/ask", response_model=PromptResponse)
async def ask_legacy(request: PromptRequest):
    """
    Legacy endpoint for backwards compatibility.

    Defaults to configured default provider if none specified.
    """
    if not request.provider:
        request.provider = config.DEFAULT_PROVIDER
    return await ask_llm(request)


@app.get("/api/providers", response_model=ProvidersListResponse)
async def list_providers():
    """
    List all available providers with their status.

    Returns:
        ProvidersListResponse with list of provider info
    """
    # Check all providers in parallel for faster response
    tasks = [
        provider.check_availability()
        for name, provider in registry.list_all().items()
    ]
    statuses = await asyncio.gather(*tasks)

    providers_info = [
        ProviderInfo(
            name=provider.name,
            display_name=provider.display_name,
            **status
        )
        for (name, provider), status in zip(registry.list_all().items(), statuses)
    ]

    return ProvidersListResponse(providers=providers_info)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/")
async def root():
    """Serve web UI."""
    html_path = Path(__file__).parent / "examples" / "index.html"
    return FileResponse(html_path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config.HOST, port=config.PORT)
