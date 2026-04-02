#!/usr/bin/env python3
"""
Save to Dinox - Save Markdown content to Dinox note-taking app

Usage:
    python save_to_dinox.py "path/to/file.md" [--title "Title"] [--tags "tag1,tag2"]
    python save_to_dinox.py --content "markdown content" [--title "Title"] [--tags "tag1,tag2"]
"""

import argparse
import os
import sys
from pathlib import Path

# Add UTF-8 encoding for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

try:
    import requests
except ImportError:
    print("Error: requests module not installed. Run: pip install requests")
    sys.exit(1)


def load_env_file():
    """Load environment variables from .env file"""
    script_dir = Path(__file__).parent.parent.parent.parent
    env_file = script_dir / ".env"

    if env_file.exists():
        with open(env_file, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())


load_env_file()


class DinoxClient:
    """Dinox API client for saving notes"""

    def __init__(self, token=None):
        self.token = token or os.environ.get("DINOX_TOKEN")
        if not self.token:
            raise ValueError("DINOX_TOKEN not found. Set it in .env or pass --token")

        self.base_url = "https://aisdk.chatgo.pro/api/openapi"
        self.headers = {
            "Content-Type": "application/json"
        }

    def save_markdown(self, content, title=None, tags=None):
        """
        Save markdown content to Dinox

        Args:
            content: Markdown content
            title: Optional title
            tags: Optional list of tags

        Returns:
            dict: API response
        """
        # Prepare content with title if provided
        if title:
            # Add title as H1 at the beginning
            full_content = f"# {title}\n\n{content}"
        else:
            full_content = content

        # Add tags at the end if provided
        if tags:
            tag_line = " ".join([f"#{tag}" for tag in tags])
            full_content = f"{full_content}\n\n{tag_line}"

        # First try: Use markdown import endpoint
        markdown_import_url = f"{self.base_url}/markdown/import/{self.token}"

        response = requests.post(
            markdown_import_url,
            headers=self.headers,
            json={"content": full_content},
            timeout=30
        )

        if response.ok:
            result = response.json()
            if result.get("code") == "000000":
                return {
                    "success": True,
                    "noteId": result.get("data", {}).get("noteId"),
                    "method": "markdown_import",
                    "response": result
                }

        # Fallback: Try createNote endpoint with title and tags
        create_note_url = f"{self.base_url}/createNote"
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.token
        }

        payload = {
            "title": title or "Untitled",
            "content": content,
            "tags": tags or []
        }

        response = requests.post(
            create_note_url,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        return {
            "success": True,
            "method": "create_note",
            "response": response.json()
        }

    def save_file(self, file_path, title=None, tags=None):
        """Read a markdown file and save to Dinox"""
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Use title from file if not provided
        if not title:
            # Try to get first heading
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('#'):
                    title = line.lstrip('#').strip()
                    break

        return self.save_markdown(content, title=title, tags=tags)


def main():
    parser = argparse.ArgumentParser(
        description="Save Markdown content to Dinox note-taking app",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Save a markdown file
  %(prog)s "my_notes.md"

  # Save with custom title
  %(prog)s "my_notes.md" --title "今日笔记"

  # Save with tags
  %(prog)s "my_notes.md" --tags "AI,技术,笔记"

  # Save raw content
  %(prog)s --content "# Hello\\n\\nWorld"

Environment Variables:
  DINOX_TOKEN    Your Dinox API token
        """
    )

    parser.add_argument(
        "file",
        nargs="?",
        help="Path to markdown file"
    )

    parser.add_argument(
        "--content",
        help="Markdown content directly (instead of file)"
    )

    parser.add_argument(
        "--title",
        help="Title for the note"
    )

    parser.add_argument(
        "--tags",
        help="Comma-separated tags (e.g., 'AI,技术,笔记')"
    )

    parser.add_argument(
        "--token",
        help="Dinox API token (or set DINOX_TOKEN env var)"
    )

    args = parser.parse_args()

    # Validate input
    if not args.file and not args.content:
        parser.error("Either FILE or --content must be provided")

    if args.file and args.content:
        parser.error("Cannot use both FILE and --content")

    # Parse tags
    tags = None
    if args.tags:
        tags = [tag.strip() for tag in args.tags.split(',')]

    try:
        client = DinoxClient(token=args.token)

        if args.content:
            result = client.save_markdown(args.content, title=args.title, tags=tags)
        else:
            result = client.save_file(args.file, title=args.title, tags=tags)

        print("\n" + "="*50)
        print("✅ Saved to Dinox!")
        print("="*50)

        if result.get("noteId"):
            print(f"Note ID: {result['noteId']}")
        print(f"Method: {result.get('method', 'unknown')}")
        print("="*50)

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
