---
name: video-downloader-skill
description: "Downloads videos and audio from YouTube, Bilibili, Twitter, and other platforms using yt-dlp. Features real-time progress display, Windows optimization, enhanced Bilibili support, and improved error handling."
---

# Video Downloader Skill

This skill downloads content from major video platforms by invoking the `scripts/video_download.py` script with enhanced Windows support and real-time progress display.

## When to Use

Use this skill when the user's intent is to **download**, **save**, or **grab** online video or audio. Common trigger commands include:

- "Download this Bilibili video..."
- "Extract audio from this YouTube video and convert it to MP3."
- "Save this Twitter video in 1080p."
- "Can I download the video from this link?"
- "Download this video with real-time progress"

## Command Structure

**Cross-Platform Commands:**
```bash
# Windows
python scripts/video_download.py "<URL>" [OPTIONS]

# macOS/Linux
python3 scripts/video_download.py "<URL>" [OPTIONS]
```

## Core Parameters

| Parameter | Short | Description | Default |
|---|---|---|---|
| `--output` | `-o` | Specify output directory | Current directory |
| `--quality` | `-q` | Set video quality (`best`, `1080p`, `720p`...) | `best` |
| `--format` | `-f` | Set video format (`mp4`, `webm`, `mkv`) | `mp4` |
| `--audio-only` | `-a` | Download audio only and convert to MP3 | Off |

**Note**: The `--cookies` parameter is supported by the underlying yt-dlp but not directly exposed in this interface.

## Usage Examples

1.  **Basic Download (Best Quality, MP4)**

    ```bash
    # Windows
    python scripts/video_download.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    # macOS/Linux
    python3 scripts/video_download.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    ```

2.  **Download Bilibili Video with Specific Quality**

    ```bash
    # Windows
    python scripts/video_download.py "https://www.bilibili.com/video/BV1xx411c7mD" -q 1080p

    # macOS/Linux
    python3 scripts/video_download.py "https://www.bilibili.com/video/BV1xx411c7mD" -q 1080p
    ```

3.  **Extract Audio Only**

    ```bash
    # Windows
    python scripts/video_download.py "https://www.youtube.com/watch?v=..." -a

    # macOS/Linux
    python3 scripts/video_download.py "https://www.youtube.com/watch?v=..." -a
    ```

4.  **Download to Platform-Specific Directory**

    ```bash
    # Windows (with Chinese path support)
    python scripts/video_download.py "<URL>" -o "C:\Users\用户名\Downloads"

    # macOS/Linux
    python3 scripts/video_download.py "<URL>" -o /path/to/downloads
    ```

## Supported Platforms

This skill uses `yt-dlp` under the hood and theoretically supports [numerous sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) supported by it, including but not limited to:

- YouTube
- Bilibili (with enhanced anti-blocking protection)
- Twitter / X
- Vimeo
- Facebook
- TikTok

## Key Features & Improvements

### 🚀 Real-time Progress Display
- **Live Output**: Real-time download progress with clean, informative display
- **Progress Tracking**: Shows download progress bars and detailed status
- **Smart Filtering**: Removes verbose debug output, displays only essential information

### 🪟 Windows Platform Optimization
- **UTF-8 Support**: Full support for Chinese paths and filenames
- **Console Compatibility**: Optimized for Windows console output
- **Encoding Robustness**: Enhanced error handling for encoding issues

### 🎯 Enhanced Bilibili Support
- **Anti-412 Protection**: Built-in protection against Bilibili's anti-scraping measures
- **Auto-Retry**: Automatic retry with alternative settings on failure
- **Error-Specific Handling**: Dedicated solutions for 412, 403, 404 errors

### 🛠️ Improved User Experience
- **File Information**: Detailed display of filename, size, and complete path
- **Smart Error Messages**: User-friendly prompts with specific troubleshooting guides
- **Network Detection**: Automatic detection and reporting of connectivity issues
- **URL Testing**: Pre-download URL accessibility verification

### ⚡ Performance & Reliability
- **Timeout Protection**: 5-minute timeout to prevent hanging processes
- **File Verification**: Automatic listing of downloaded files with sizes
- **Smart Path Detection**: Automatic detection of optimal download directories
- **Cross-platform**: Seamless operation across Windows, macOS, and Linux with platform-specific optimizations

## Notes

- **Dependencies**: The script automatically handles the installation of `yt-dlp`, no manual intervention required.
- **Filenames**: Downloaded filenames are automatically generated based on the video title.
- **Playlists**: By default, only single videos are downloaded; playlists are not processed.
- **Windows Users**: Full support for Chinese characters in paths and filenames.
- **Bilibili Users**: Enhanced support with automatic error recovery and retry mechanisms.
