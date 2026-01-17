"""Claude Code CLI provider implementation."""

import asyncio
import os
import tempfile
import time
from typing import Dict, Any, Optional

from .base import CLIProvider


class ClaudeProvider(CLIProvider):
    """Provider for Claude Code CLI using temporary file approach."""

    @property
    def name(self) -> str:
        """Provider name."""
        return "claude"

    @property
    def display_name(self) -> str:
        """Display name for UI."""
        return "Claude Code"

    async def execute(
        self,
        prompt: str,
        working_directory: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute Claude CLI with prompt using temporary file approach.

        This method:
        1. Writes prompt to a temporary file
        2. Uses platform-specific command (type on Windows, cat on Unix)
        3. Pipes to claude --print
        4. Returns parsed response
        """
        temp_file = None
        start_time = time.time()

        try:
            # Write prompt to temporary file
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.txt',
                delete=False,
                encoding='utf-8'
            ) as f:
                f.write(prompt)
                temp_file = f.name

            # Build platform-specific command
            if os.name == 'nt':  # Windows
                cmd = f'type "{temp_file}" | claude --print'
            else:  # Linux/Mac
                cmd = f'cat "{temp_file}" | claude --print'

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
                    "error": error_msg or "Claude CLI returned an error",
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
                "error": "Claude CLI not found. Please ensure Claude Code is installed and in PATH.",
                "execution_time": execution_time
            }
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "success": False,
                "response": "",
                "error": f"Error executing Claude CLI: {str(e)}",
                "execution_time": execution_time
            }
        finally:
            # Clean up temporary file
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception:
                    pass  # Ignore cleanup errors

    async def check_availability(self) -> Dict[str, Any]:
        """
        Check if Claude CLI is installed and available.

        Tries to run 'claude --version' to verify installation.
        """
        try:
            process = await asyncio.create_subprocess_shell(
                'claude --version',
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
                    "error": error_msg or "Claude CLI check failed"
                }

        except FileNotFoundError:
            return {
                "available": False,
                "version": None,
                "error": "Claude CLI not found in PATH"
            }
        except Exception as e:
            return {
                "available": False,
                "version": None,
                "error": f"Error checking Claude CLI: {str(e)}"
            }
