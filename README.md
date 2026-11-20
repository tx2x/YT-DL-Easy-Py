# YT-DL Easy Py

**A simple, interactive, cross-platform command-line frontend for [yt-dlp](https://github.com/yt-dlp/yt-dlp).**

YT-DL Easy Py makes common video and playlist downloads easier to configure without having to remember yt-dlp's format-selection syntax. It is written in Python and uses yt-dlp as the download engine.

> **Important:** This project is an independent frontend, not a downloader engine. You must install [yt-dlp](https://github.com/yt-dlp/yt-dlp) separately. FFmpeg is strongly recommended for merging separate video/audio streams and converting audio.

## Features

- Download an individual video or an entire playlist from a URL.
- Detect YouTube links containing both a video ID and a playlist ID, then ask whether to download the video or playlist.
- Read multiple URLs from a UTF-8 text file (one URL per line; blank lines and lines beginning with `#` are ignored).
- Format-list highlighting to make codec and audio-language choices easier to scan:
  - Audio tracks explicitly marked `original` or `default` by yt-dlp are highlighted.
  - Video formats using AV1 (`av01`), H.264 (`avc1`), and VP9 (`vp9`) receive distinct labels.
  - The original yt-dlp format rows and format IDs remain visible and unchanged. The original/default marker is shown only when yt-dlp exposes that designation in its format-list output; the script does not guess which language is original.
- After each session, choose whether to start another download; the default is **No** (press Enter to exit).
- Interactive format choices:
  - Best available video and audio streams (automatic selection).
  - Choose video and audio format IDs separately, with best-available defaults.
  - Best single-file format without merging.
  - Best quality with MP4 as the preferred merge container.
  - Audio only, audio extracted to MP3, or video only.
- Confirmation prompts default to **Yes**; press Enter to accept.
- Configurable output directory, optional Desktop output folder, FFmpeg path, and extra yt-dlp arguments.
- Uses argument-safe process execution rather than shell command strings.
- Optional terminal colors with a plain-text fallback for older or limited terminals.
- English interface; downloaded titles and filenames retain their original Unicode characters.

## Requirements

- **Python 3.9 or newer**
- **yt-dlp** (required)
- **FFmpeg** (recommended; required for merging separate streams and audio conversion)

The script uses only the Python standard library. No third-party Python packages are required.

## Installation

### 1. Install Python

Install Python 3.9+ from [python.org](https://www.python.org/downloads/) or your Linux distribution's package manager. On Windows, enable the option to add Python to `PATH` during installation.

### 2. Install yt-dlp

The recommended Python installation method is:

```bash
python -m pip install -U yt-dlp
```

On systems where `python` refers to Python 2 or is not available, use `python3` instead. On Windows, `py -m pip install -U yt-dlp` is also common.

Alternatively, download the standalone `yt-dlp.exe` (Windows) or appropriate executable from the [yt-dlp releases page](https://github.com/yt-dlp/yt-dlp/releases) and place it in `PATH` or next to the script.

### 3. Install FFmpeg (recommended)

Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) or use your operating system's package manager. Ensure `ffmpeg` (and ideally `ffprobe`) is available in `PATH`, or provide its location using `--ffmpeg-location`.

### 4. Get YT-DL Easy Py

Download `yt_dl_easy.py` from this repository. No setup or package installation is needed for the script itself.

## Usage

Run the script from a terminal:

**Windows**

```powershell
py yt_dl_easy.py
```

**Linux**

```bash
python3 yt_dl_easy.py
```

Enter a video URL, playlist URL, or path to a text file containing URLs. Follow the interactive prompts to choose a format and confirm the download. The default output directory is `Outputs` in the current working directory.

### Example URL list

Create a UTF-8 text file, for example `urls.txt`:

```text
# Videos and playlists to download
https://www.youtube.com/watch?v=VIDEO_ID
https://www.youtube.com/playlist?list=PLAYLIST_ID
```

Then enter the path to `urls.txt` when prompted. Each non-empty, non-comment line is processed in order.

## Command-line options

| Option | Description | Default |
|---|---|---|
| `--exe PATH` | yt-dlp executable name or full path | `yt-dlp` |
| `--output DIR` | Output directory | `Outputs` |
| `--desktop` | Use `Desktop/Outputs` instead of `--output` | Off |
| `--ffmpeg-location PATH` | FFmpeg executable or directory | Auto-detect from `PATH` |
| `--options "ARGS"` | Additional arguments passed to yt-dlp | None |
| `--no-color` | Disable terminal colors | Off |
| `--debug` | Print environment and command-argument diagnostics | Off |
| `--version` | Print YT-DL Easy Py version | — |
| `-h`, `--help` | Show help | — |

Examples:

```bash
# Use a local downloader executable
python yt_dl_easy.py --exe ./yt-dlp

# Save downloads to a custom directory
python yt_dl_easy.py --output "/media/Video Archive"

# Use the Desktop/Outputs directory
python yt_dl_easy.py --desktop

# Specify FFmpeg explicitly
python yt_dl_easy.py --ffmpeg-location "/usr/local/bin"

# Add yt-dlp options to every download
python yt_dl_easy.py --options "--write-subs --sub-langs en"
```

`--options` is split into arguments without invoking a shell. Quote the complete option string so your terminal passes it as one argument. Do not include shell redirections or shell operators in it.

## Output layout

- Single videos are saved directly in the selected output directory.
- Playlist downloads are organized into a folder named after the playlist, with numbered entries where playlist metadata is available.
- The output directory is created automatically if it does not exist.

## Compatibility

The script is designed for Python 3.9+ on Windows and Linux. It avoids PowerShell-specific syntax and shell-dependent command construction. It uses standard Python subprocess argument lists, UTF-8 text handling, and gracefully disables ANSI colors when the terminal does not support them.

It is intended to work with Windows 11, Windows 10 consoles (including older console configurations), and common Linux terminals. Terminal font and code-page settings can still affect how a particular console displays Unicode characters; downloaded filenames are passed through Python/yt-dlp as Unicode.

macOS may also work, but is not a specifically tested target for this initial release.

## Updating yt-dlp

Update the downloader independently of this frontend:

```bash
python -m pip install -U yt-dlp
```

For a standalone executable, follow the update instructions for your installation method. YT-DL Easy Py does not attempt to update or replace yt-dlp automatically.

## Troubleshooting

**`yt-dlp not found`**  
Install yt-dlp, add it to `PATH`, place the executable beside the script, or pass its location with `--exe`.

**Separate video and audio streams are not merged**  
Install FFmpeg and make sure it is available in `PATH`, or specify it with `--ffmpeg-location`.

**A playlist link downloads only one video**  
When a YouTube URL contains both `v=` and `list=`, choose the playlist option at the prompt. For a video-only download, choose the video option.

**Text-file input reports an invalid URL**  
Use one complete `http://` or `https://` URL per line. Blank lines and comment lines beginning with `#` are ignored.

**Colors or special characters look incorrect**  
Try `--no-color`. On Windows, use a terminal with Unicode support and a font that contains the required characters. The script does not translate video titles or alter their Unicode characters.

## Privacy and responsible use

YT-DL Easy Py passes the URLs and options you provide to yt-dlp. It does not include analytics, telemetry, or an account system. You are responsible for complying with the terms of service of the websites you access and applicable copyright laws. Only download content you are authorized to download.

## License

This repository is distributed under the MIT License. See [LICENSE](LICENSE). The yt-dlp project is separate software and is distributed under its own license.

## Acknowledgements

- [ThioJoe / youtube-dl-easy](https://github.com/ThioJoe/youtube-dl-easy) — the original PowerShell project that inspired this utility.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — the download engine.
- [FFmpeg](https://ffmpeg.org/) — media processing and stream merging.

The code was written using web version of ChatGPT 😁.

---

**Project status:** Version `v1.2.0`. See [CHANGELOG.md](CHANGELOG.md) for release history. Bug reports and suggestions are welcome via GitHub Issues.
