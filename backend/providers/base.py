"""Abstract base class for CLI providers."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class CLIProvider(ABC):
    """Abstract base class for CLI providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name (e.g., 'claude', 'gemini')."""
        pass

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Display name for UI (e.g., 'Claude Code', 'Gemini CLI')."""
        pass

    @abstractmethod
    async def execute(
        self,
        prompt: str,
        working_directory: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute CLI command with prompt.

        Returns:
            {
                "success": bool,
                "response": str,
                "error": Optional[str],
                "execution_time": float (seconds)
            }
        """
        pass

    @abstractmethod
    async def check_availability(self) -> Dict[str, Any]:
        """
        Check if CLI tool is installed and configured.

        Returns:
            {
                "available": bool,
                "version": Optional[str],
                "error": Optional[str]
            }
        """
        pass
