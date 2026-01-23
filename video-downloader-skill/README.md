# Video Downloader Skill

`video-downloader-skill` is a powerful command-line tool for downloading videos and audio from numerous websites, including YouTube, Bilibili, and Twitter. It is built on top of the popular `yt-dlp` library and provides a streamlined interface for common downloading tasks with **enhanced Windows support and real-time progress display**.

This skill is designed to be used as a Claude Code Skill, allowing for easy integration into automated workflows.

## Features

- **Wide Platform Support**: Download from YouTube, Bilibili, Twitter, and any other site supported by `yt-dlp`.
- **Real-time Progress Display**: Live download progress with clean, informative output and progress bars.
- **Windows Platform Optimized**: Enhanced UTF-8 encoding support for Chinese paths and filenames, robust error handling for Windows console.
- **Quality Selection**: Choose your desired video quality, from `worst` to `best`, including specific resolutions like `1080p` or `720p`.
- **Format Conversion**: Save videos in your preferred format, such as `mp4`, `webm`, or `mkv`.
- **Audio Extraction**: Easily extract audio from a video and save it as an `mp3` file.
- **Enhanced Bilibili Support**: Optimized for Bilibili with anti-412 protection, automatic retry mechanisms, and specialized error handling.
- **Cookie Support**: Use your browser's cookies to download videos that require a login.
- **Improved User Experience**: Detailed file information display (filename, size, path), clear error messages with troubleshooting guides.
- **Automatic Dependency Management**: The script automatically checks for and installs `yt-dlp` if it's not found.

## Installation

No manual installation is required. The script handles its own dependencies. Simply clone this repository and run the script.

```bash
git clone https://github.com/viva-org/video-downloader-skill.git
cd video-downloader-skill
```

## Cross-Platform Usage

The skill automatically detects your operating system and uses the appropriate Python command:

- **Windows**: `python scripts/video_download.py`
- **macOS/Linux**: `python3 scripts/video_download.py`

## Usage

The skill is executed via the `video_download.py` script located in the `scripts/` directory.

**Command Structure:**
```bash
# Windows
python scripts/video_download.py "<URL>" [OPTIONS]

# macOS/Linux
python3 scripts/video_download.py "<URL>" [OPTIONS]
```

### Parameters

| Parameter      | Short | Description                                       | Default      |
|----------------|-------|---------------------------------------------------|--------------|
| `--output`     | `-o`  | Specifies the output directory.                   | Current Dir. |
| `--quality`    | `-q`  | Sets the video quality (`best`, `1080p`, etc.).   | `best`       |
| `--format`     | `-f`  | Sets the video container format (`mp4`, `webm`).  | `mp4`        |
| `--audio-only` | `-a`  | Downloads only the audio as an MP3 file.          | `False`      |

**Note**: The `--cookies` parameter is supported by the underlying yt-dlp but not directly exposed in this interface. For advanced authentication needs, please use yt-dlp directly.

### Examples

1.  **Basic Download (Best Quality, MP4)**

    ```bash
    # Windows
    python scripts/video_download.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    # macOS/Linux
    python3 scripts/video_download.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    ```

2.  **Download a Bilibili Video in 1080p**

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

4.  **Download to a Specific Directory**

    ```bash
    # Windows
    python scripts/video_download.py "<URL>" -o "C:\Users\用户名\Downloads"

    # macOS/Linux
    python3 scripts/video_download.py "<URL>" -o /path/to/downloads
    ```

## Supported Platforms

This skill uses `yt-dlp` as its backend, which supports a vast number of websites. For a complete list, please refer to the [official list of supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

Commonly used platforms include:

- YouTube
- Bilibili (with enhanced anti-blocking protection)
- Twitter / X
- Vimeo
- Facebook
- TikTok

## 🔧 Optimization Highlights

### Real-time Progress Display ✅
- **Live Output**: Changed from `subprocess.run` to `subprocess.Popen` for real-time progress display
- **Clean Progress Bars**: Shows download progress with detailed information
- **Smart Output Filtering**: Removes verbose debug output, displays only essential information

### Windows Platform Optimization ✅
- **UTF-8 Encoding**: Enhanced support for Chinese paths and filenames
- **Robust Error Handling**: Improved encoding error handling for Windows console
- **Cross-platform Compatibility**: Ensures smooth operation on Windows systems

### User Experience Improvements ✅
- **Detailed File Information**: Shows filename, size, and complete path after download
- **Clear Error Messages**: User-friendly error prompts with troubleshooting guides
- **Enhanced Bilibili Support**: Specialized error handling for Bilibili-specific issues

### Error Handling Enhancement ✅
- **Detailed Error Classification**: Specific solutions for different error types
- **Bilibili-specific Errors**: Dedicated handling for 412, 403, 404 errors
- **Network Issue Detection**: Friendly prompts for connectivity problems

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
