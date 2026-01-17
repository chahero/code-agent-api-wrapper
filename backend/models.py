"""Pydantic models for request/response handling."""

from pydantic import BaseModel
from typing import Optional, List


class PromptRequest(BaseModel):
    """Request model for asking a provider."""

    provider: Optional[str] = None  # Provider name (defaults to configured default)
    prompt: str  # The prompt to send
    working_directory: Optional[str] = None  # Working directory for execution


class PromptResponse(BaseModel):
    """Response model from a provider."""

    success: bool
    provider: str  # Which provider was used
    response: str
    error: Optional[str] = None
    execution_time: Optional[float] = None  # Execution time in seconds


class ProviderInfo(BaseModel):
    """Information about a provider."""

    name: str
    display_name: str
    available: bool
    version: Optional[str] = None
    error: Optional[str] = None


class ProvidersListResponse(BaseModel):
    """Response listing available providers."""

    providers: List[ProviderInfo]
