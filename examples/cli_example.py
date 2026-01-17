"""
Multi-Provider CLI API Wrapper - CLI Example

Usage:
    python cli_example.py "your question"
    python cli_example.py "your question" --provider claude
    python cli_example.py "your question" --provider gemini
    python cli_example.py --providers  # List available providers
    python cli_example.py -i  # Interactive mode
"""

import argparse
import requests
import sys
import json
import os

API_URL = os.getenv("API_URL", "http://localhost:5000")


def list_providers() -> bool:
    """List all available providers."""
    try:
        response = requests.get(f"{API_URL}/api/providers")

        if response.status_code != 200:
            print(f"Error: {response.text}", file=sys.stderr)
            return False

        data = response.json()
        print("\nAvailable Providers:")
        print("-" * 60)

        for provider in data["providers"]:
            status = "[OK] Available" if provider["available"] else "[NG] Not Available"
            version = f" (v{provider['version']})" if provider["version"] else ""
            print(f"  - {provider['display_name']:<20} [{provider['name']}] {status}{version}")

            if provider["error"] and not provider["available"]:
                print(f"    Error: {provider['error']}")

        print("-" * 60)
        return True

    except requests.exceptions.ConnectionError:
        print(f"Error: Cannot connect to API at {API_URL}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return False


def ask_provider(prompt: str, provider: str = None) -> str:
    """Ask a provider and return the response."""
    try:
        payload = {"prompt": prompt}
        if provider:
            payload["provider"] = provider

        response = requests.post(
            f"{API_URL}/api/ask",
            json=payload
        )

        if response.status_code != 200:
            return f"Error: {response.text}"

        data = response.json()

        if data["success"]:
            return data["response"]
        else:
            return f"Error: {data.get('error', 'Unknown error')}"

    except requests.exceptions.ConnectionError:
        return f"Error: Cannot connect to API at {API_URL}"
    except Exception as e:
        return f"Error: {str(e)}"


def interactive_mode(default_provider: str = None):
    """Run in interactive mode."""
    print("Multi-Provider CLI API Wrapper (quit: type 'quit' or 'exit')")
    print("-" * 50)

    if default_provider:
        print(f"Default provider: {default_provider}\n")

    while True:
        try:
            prompt = input("\nQuestion> ").strip()

            if prompt.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            if not prompt:
                continue

            print("\nResponse:")
            print(ask_provider(prompt, default_provider))

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Multi-Provider CLI API Wrapper"
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Question to ask"
    )
    parser.add_argument(
        "-p", "--provider",
        help="Which provider to use (claude, gemini, etc.)"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--providers",
        action="store_true",
        help="List available providers"
    )

    args = parser.parse_args()

    if args.providers:
        list_providers()
        return

    if args.interactive:
        interactive_mode(args.provider)
        return

    if args.prompt:
        print(ask_provider(args.prompt, args.provider))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
