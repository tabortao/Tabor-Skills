#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Downloader
Downloads videos from YouTube, Bilibili and other platforms with customizable quality and format options.
Improved version with better error handling and debugging.
"""

import argparse
import sys
import subprocess
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    # Ensure stdout/stderr use UTF-8 where possible without detaching
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        # If reconfigure fails, try alternative approach
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def safe_print(text):
    """Print text safely, handling encoding errors."""
    try:
        print(text)
        sys.stdout.flush()  # Ensure immediate output
    except UnicodeEncodeError:
        try:
            print(text.encode('utf-8', errors='ignore').decode('utf-8'))
            sys.stdout.flush()
        except Exception:
            safe_text = text.encode('ascii', 'ignore').decode('ascii')
            print(safe_text)
            sys.stdout.flush()


def is_bilibili_url(url):
    """Check if the URL is from Bilibili."""
    if not url:
        return False
    try:
        parsed_url = urlparse(url)
        bilibili_pattern = r'(.*\.)?bilibili\.com$'
        return bool(re.search(bilibili_pattern, parsed_url.netloc))
    except Exception:
        return False


def format_bilibili_url(url):
    """
    Clean Bilibili URL by keeping only essential parameters.
    """
    if not is_bilibili_url(url):
        return url

    try:
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)

        # Construct base URL (without query params)
        base_path = parsed.path.rstrip('/')
        formatted_url = f"{parsed.scheme}://{parsed.netloc}{base_path}"

        # Keep 'p' parameter if present
        if 'p' in query_params:
            pid = query_params['p'][0]
            formatted_url += f"?p={pid}"

        return formatted_url
    except Exception:
        return url


def check_yt_dlp():
    """Check if yt-dlp is installed, install if not."""
    # Add user's local bin to PATH
    local_bin = str(Path.home() / ".local" / "bin")
    if local_bin not in os.environ.get("PATH", ""):
        os.environ["PATH"] = f"{local_bin}:{os.environ.get('PATH', '')}"

    try:
        result = subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True, text=True)
        safe_print(f"yt-dlp version: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    safe_print("yt-dlp not found. Installing...")
    try:
        # Try with --break-system-packages first (for newer pip versions)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--break-system-packages", "yt-dlp"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, result.args)
    except subprocess.CalledProcessError:
        try:
            # Fall back to regular install if --break-system-packages is not supported
            result = subprocess.run([sys.executable, "-m", "pip", "install", "--user", "yt-dlp"],
                                  capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            safe_print(f"Failed to install yt-dlp: {e}")
            if e.stderr:
                safe_print(f"Error details: {e.stderr}")
            return False

    safe_print("yt-dlp installed successfully!")
    return True


def get_video_info(url):
    """Get information about the video without downloading."""
    try:
        # Use a simpler call for info extraction
        result = subprocess.run(
            ["yt-dlp", "--dump-json", "--no-playlist", url],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=30  # Add timeout to prevent hanging
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            safe_print(f"Failed to get video info: {result.stderr}")
        return None
    except Exception as e:
        safe_print(f"Error getting video info: {e}")
        return None


def test_url_access(url):
    """Test if the URL is accessible."""
    try:
        import urllib.request
        import urllib.error

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.getcode() == 200
    except Exception as e:
        safe_print(f"URL access test failed: {e}")
        return False


def download_video_internal(url, output_path, quality, format_type, audio_only, is_retry=False):
    """
    Internal function to download video with specific URL.
    Returns (success, error_message)
    """
    # Check platform type
    is_bilibili = is_bilibili_url(url)

    # Build command
    cmd = ["yt-dlp"]

    # --- Bilibili-specific optimizations ---
    if is_bilibili:
        if not is_retry:
            safe_print("[Bilibili detected] Using optimized download strategy...")

        # Add required headers for Bilibili
        cmd.extend([
            "--add-header", "Referer:https://www.bilibili.com/",
            "--add-header", "User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ])

        # Try different extraction methods for Bilibili
        if not is_retry:
            cmd.extend(["--extractor-args", "bilibili:videomode=html5"])
        else:
            # On retry, try alternative approach
            cmd.extend(["--extractor-args", "bilibili:force_api=1"])

    # ----------------------------------------

    if audio_only:
        cmd.extend([
            "-x",  # Extract audio
            "--audio-format", "mp3",
            "--audio-quality", "0",  # Best quality
        ])
    else:
        # Video quality settings
        if quality == "best":
            format_string = "bestvideo+bestaudio/best"
        elif quality == "worst":
            format_string = "worstvideo+worstaudio/worst"
        else:
            # Specific resolution (e.g., 1080p, 720p)
            height = quality.replace("p", "")
            format_string = f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"

        cmd.extend([
            "-f", format_string,
            "--merge-output-format", format_type,
        ])

    # Output template - use Path for cross-platform compatibility
    output_template = str(Path(output_path) / "%(title)s.%(ext)s")
    cmd.extend([
        "-o", output_template,
        "--no-playlist",  # Don't download playlists by default
        "--verbose",  # Add verbose output for better debugging
    ])

    cmd.append(url)

    if not is_retry:
        safe_print(f"Downloading from: {url}")
        if is_bilibili:
            safe_print(f"Platform: Bilibili (with anti-412 protection)")
        safe_print(f"Quality: {quality}")
        safe_print(f"Format: {'mp3 (audio only)' if audio_only else format_type}")
        safe_print(f"Output: {output_path}\n")

        # Get video info first
        info = get_video_info(url)
        if info:
            safe_print(f"Title: {info.get('title', 'Unknown')}")
            duration = info.get('duration', 0)
            if duration:
                try:
                    duration_val = float(duration)
                    minutes = int(duration_val // 60)
                    seconds = int(duration_val % 60)
                    safe_print(f"Duration: {minutes}:{seconds:02d}")
                except (ValueError, TypeError):
                    safe_print(f"Duration: {duration}")
            safe_print(f"Uploader: {info.get('uploader', 'Unknown')}\n")
        else:
            safe_print("Warning: Could not fetch video info")
            safe_print("Attempting to download anyway...\n")

        safe_print("Starting download...")
        safe_print(f"Command: {' '.join(cmd)}")

    # Download the video - capture stderr for better error reporting
    safe_print("Running yt-dlp...")
    safe_print("Download progress will be shown below (this may take a while for large videos):")
    safe_print("-" * 60)

    # Use Popen for real-time output instead of capture_output
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Combine stderr with stdout
            text=True,
            encoding='utf-8',
            errors='replace',
            bufsize=1,  # Line buffered
            universal_newlines=True
        )

        # Read output line by line for real-time display
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                # Clean up the output for better display
                cleaned_output = output.strip()
                if cleaned_output:  # Only print non-empty lines
                    # Skip verbose debug lines that are too long
                    if len(cleaned_output) < 200:
                        safe_print(cleaned_output)
                    else:
                        # Show abbreviated version of long lines
                        safe_print(cleaned_output[:100] + "..." + cleaned_output[-50:])

        # Wait for process to complete and get return code
        return_code = process.wait(timeout=300)

        if return_code == 0:
            safe_print("-" * 60)
            safe_print("Download completed successfully!")
            return (True, None)
        else:
            error_msg = f"yt-dlp failed with exit code {return_code}"
            return (False, error_msg)

    except subprocess.TimeoutExpired:
        process.kill()
        return (False, "Download timed out after 5 minutes")
    except Exception as e:
        if 'process' in locals():
            process.kill()
        safe_print(f"[ERROR] Unexpected error during download: {str(e)}")
        return (False, f"Unexpected error during download: {str(e)}")



def download_video(url, output_path=None, quality="best", format_type="mp4", audio_only=False):
    """
    Download a video from YouTube, Bilibili or other platforms.

    Args:
        url: Video URL
        output_path: Directory to save the video (default: smart detection)
        quality: Quality setting (best, 1080p, 720p, 480p, 360p, worst)
        format_type: Output format (mp4, webm, mkv, etc.)
        audio_only: Download only audio (mp3)
    """
    safe_print("=== Video Downloader Started ===")

    # First check if yt-dlp is available
    if not check_yt_dlp():
        safe_print("[ERROR] Failed to install or find yt-dlp. Please install it manually:")
        safe_print("pip install yt-dlp")
        return False

    # Test URL accessibility
    safe_print(f"Testing URL accessibility: {url}")
    if not test_url_access(url):
        safe_print("[WARNING] URL might not be accessible. This could be due to:")
        safe_print("  - Network connectivity issues")
        safe_print("  - Video requires login/authentication")
        safe_print("  - Video is region-restricted")
        safe_print("  - Video has been removed or made private")
        safe_print("Continuing with download attempt anyway...")
        print()

    # Smart default output path detection
    if output_path is None:
        cwd = Path.cwd()

        # Try to detect if we are inside a .claude directory structure
        claude_base = None
        for parent in [cwd] + list(cwd.parents):
            if parent.name == ".claude":
                claude_base = parent.parent
                break

        if claude_base:
            # If we found a .claude directory, we use its parent as the base
            # Prefer 'Downloads' folder if it exists in the base directory
            downloads_dir = claude_base / "Downloads"
            if downloads_dir.exists() and downloads_dir.is_dir():
                output_path = str(downloads_dir)
            else:
                output_path = str(claude_base)
        else:
            # If no .claude found, use the current working directory
            output_path = str(cwd)

    # Ensure output directory exists and use absolute path
    try:
        output_path = os.path.abspath(output_path)
        os.makedirs(output_path, exist_ok=True)
        safe_print(f"Output directory: {output_path}")
    except Exception as e:
        safe_print(f"[ERROR] Failed to create output directory: {e}")
        return False

    is_bilibili = is_bilibili_url(url)

    if is_bilibili:
        original_url = url
        url = format_bilibili_url(url)
        if original_url != url:
            safe_print(f"Cleaned Bilibili URL: {url}")

    try:
        # Attempt download
        success, error_msg = download_video_internal(
            url, output_path, quality, format_type, audio_only, is_retry=False
        )

        if success:
            safe_print("\n[SUCCESS] Download complete!")
            safe_print(f"Saved to: {output_path}")

            # List files in output directory to show what was downloaded
            try:
                files = list(Path(output_path).glob("*"))
                video_files = [f for f in files if f.is_file() and f.suffix.lower() in ['.mp4', '.mp3', '.webm', '.mkv']]
                if video_files:
                    print()
                    safe_print("Downloaded files:")
                    safe_print("-" * 50)
                    for f in video_files:
                        size_bytes = f.stat().st_size
                        if size_bytes > 1024 * 1024:  # > 1MB
                            size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
                        elif size_bytes > 1024:  # > 1KB
                            size_str = f"{size_bytes / 1024:.1f} KB"
                        else:
                            size_str = f"{size_bytes} bytes"
                        safe_print(f"  ✓ {f.name}")
                        safe_print(f"    Size: {size_str}")
                        safe_print(f"    Location: {f.absolute()}")
                        print()
                else:
                    safe_print("No video files found in output directory.")
                    safe_print("Files in directory:")
                    for f in files:
                        if f.is_file():
                            safe_print(f"  - {f.name}")
            except Exception as e:
                safe_print(f"Could not list downloaded files: {e}")

            return True

        # If failed, try retry with different settings for Bilibili
        if not success and is_bilibili and not "412" in (error_msg or ""):
            safe_print("\n[RETRY] Attempting download with alternative settings...")
            time.sleep(2)  # Brief pause before retry

            success, retry_error_msg = download_video_internal(
                url, output_path, quality, format_type, audio_only, is_retry=True
            )

            if success:
                safe_print("\n[SUCCESS] Download complete on retry!")
                safe_print(f"Saved to: {output_path}")
                return True

        # If still failed, show error message
        print()
        safe_print("[ERROR] Error downloading video:")
        if error_msg:
            # Clean up error message for better readability
            clean_error = error_msg.replace('\n', '\n  ')
            safe_print(f"  {clean_error}")
        if 'retry_error_msg' in locals() and retry_error_msg:
            clean_retry_error = retry_error_msg.replace('\n', '\n  ')
            safe_print(f"  Retry error: {clean_retry_error}")

        # Provide helpful hints for common errors
        print()
        safe_print("[TROUBLESHOOTING TIPS]")
        if is_bilibili:
            safe_print("For Bilibili videos:")
            if error_msg and "412" in error_msg:
                safe_print("  • 412 error: Content not available in your region or requires login")
                safe_print("  • Try using cookies from your browser (use -c option)")
                safe_print("  • Wait a few minutes before retrying")
            elif error_msg and ("403" in error_msg or "forbidden" in error_msg.lower()):
                safe_print("  • 403 error: Access forbidden - Video might be restricted")
                safe_print("  • Try using cookies or a different quality setting")
            elif error_msg and ("404" in error_msg or "not found" in error_msg.lower()):
                safe_print("  • 404 error: Video not found - Check if the URL is correct")
            elif error_msg and "login" in error_msg.lower():
                safe_print("  • Login required - Use cookies from your browser (use -c option)")
            else:
                safe_print("  • Try using cookies from your browser (use -c option)")
                safe_print("  • Try a different quality setting (e.g., 720p instead of 1080p)")
                safe_print("  • Check your internet connection")
        else:
            safe_print("General troubleshooting:")
            safe_print("  • Check if the URL is correct and the video is still available")
            safe_print("  • Try a different quality setting")
            safe_print("  • Check your internet connection")
            safe_print("  • For private/restricted videos, try using cookies (use -c option)")

        print()
        safe_print("For more help, visit: https://github.com/yt-dlp/yt-dlp/wiki")

        return False

    except Exception as e:
        safe_print(f"\n[ERROR] Unexpected error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Download videos from YouTube, Bilibili and other platforms with customizable quality and format"
    )
    parser.add_argument("url", help="Video URL")
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output directory (default: current directory)"
    )
    parser.add_argument(
        "-q", "--quality",
        default="best",
        choices=["best", "1080p", "720p", "480p", "360p", "worst"],
        help="Video quality (default: best)"
    )
    parser.add_argument(
        "-f", "--format",
        default="mp4",
        choices=["mp4", "webm", "mkv"],
        help="Video format (default: mp4)"
    )
    parser.add_argument(
        "-a", "--audio-only",
        action="store_true",
        help="Download only audio as MP3"
    )

    args = parser.parse_args()

    success = download_video(
        url=args.url,
        output_path=args.output,
        quality=args.quality,
        format_type=args.format,
        audio_only=args.audio_only
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()