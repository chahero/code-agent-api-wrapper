"""Provider registry and management."""

from typing import Dict, Optional

from .base import CLIProvider
from .claude import ClaudeProvider
from .gemini import GeminiProvider
from .codex import CodexProvider


class ProviderRegistry:
    """Manages available CLI providers."""

    def __init__(self):
        """Initialize the registry with default providers."""
        self._providers: Dict[str, CLIProvider] = {}
        self._register_default_providers()

    def _register_default_providers(self):
        """Register built-in providers."""
        self.register(ClaudeProvider())
        self.register(GeminiProvider())
        self.register(CodexProvider())

    def register(self, provider: CLIProvider):
        """
        Register a new provider.

        Args:
            provider: A CLIProvider instance to register
        """
        self._providers[provider.name] = provider

    def get(self, name: str) -> Optional[CLIProvider]:
        """
        Get provider by name.

        Args:
            name: Provider name

        Returns:
            The provider instance or None if not found
        """
        return self._providers.get(name)

    def list_all(self) -> Dict[str, CLIProvider]:
        """
        Get all registered providers.

        Returns:
            Dictionary of provider name to provider instance
        """
        return self._providers.copy()


# Global registry instance
registry = ProviderRegistry()
