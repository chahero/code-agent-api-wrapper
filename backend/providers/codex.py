"""Codex CLI provider implementation."""

import asyncio
import os
import tempfile
import time
from typing import Dict, Any, Optional

from .base import CLIProvider


class CodexProvider(CLIProvider):
    """Provider for Codex CLI using temporary file approach."""

    @property
    def name(self) -> str:
        """Provider name."""
        return "codex"

    @property
    def display_name(self) -> str:
        """Display name for UI."""
        return "Codex"

    async def execute(
        self,
        prompt: str,
        working_directory: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute Codex CLI with prompt using direct string approach.

        This method:
        1. Escapes the prompt string properly
        2. Passes prompt directly to codex command
        3. Returns parsed response
        """
        start_time = time.time()

        try:
            # Escape the prompt for shell (proper escaping for direct string approach)
            escaped_prompt = prompt.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')

            # Build command with escaped prompt
            cmd = f'codex "{escaped_prompt}"'

            # Execute command
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_directory
            )

            stdout, stderr = await process.communicate()
            execution_time = time.time() - start_time

            if process.returncode != 0:
                error_msg = stderr.decode("utf-8", errors="replace").strip()
                return {
                    "success": False,
                    "response": "",
                    "error": error_msg or "Codex CLI returned an error",
                    "execution_time": execution_time
                }

            return {
                "success": True,
                "response": stdout.decode("utf-8", errors="replace"),
                "error": None,
                "execution_time": execution_time
            }

        except FileNotFoundError:
            execution_time = time.time() - start_time
            return {
                "success": False,
                "response": "",
                "error": "Codex CLI not found. Please ensure Codex is installed and in PATH.",
                "execution_time": execution_time
            }
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "success": False,
                "response": "",
                "error": f"Error executing Codex CLI: {str(e)}",
                "execution_time": execution_time
            }

    async def check_availability(self) -> Dict[str, Any]:
        """
        Check if Codex CLI is installed and available.

        Tries to run 'codex --version' to verify installation.
        """
        try:
            process = await asyncio.create_subprocess_shell(
                'codex --version',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                version = stdout.decode("utf-8", errors="replace").strip()
                return {
                    "available": True,
                    "version": version if version else "installed",
                    "error": None
                }
            else:
                error_msg = stderr.decode("utf-8", errors="replace").strip()
                return {
                    "available": False,
                    "version": None,
                    "error": error_msg or "Codex CLI check failed"
                }

        except FileNotFoundError:
            return {
                "available": False,
                "version": None,
                "error": "Codex CLI not found in PATH"
            }
        except Exception as e:
            return {
                "available": False,
                "version": None,
                "error": f"Error checking Codex CLI: {str(e)}"
            }
