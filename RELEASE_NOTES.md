# YT-DL Easy Py v1.0.0

**First public release**

YT-DL Easy Py is a Python-based, cross-platform interactive frontend for yt-dlp, inspired by ThioJoe's original `youtube-dl-easy` PowerShell script.

## Highlights

- Python 3 implementation designed for Windows and Linux.
- Single-video, playlist, and text-file URL input workflows.
- Explicit choice when a YouTube URL contains both a video and playlist identifier.
- Interactive format presets for best quality, single-file formats, MP4-preferred merging, custom format codes, audio-only, MP3 extraction, and video-only downloads.
- Yes/No confirmation prompts accept the default **Yes** when Enter is pressed.
- Configurable output directory, Desktop output shortcut, FFmpeg location, and extra yt-dlp arguments.
- Optional ANSI styling with a no-color fallback.
- Unicode-aware input and output handling.
- No third-party Python dependencies.

## Requirements

- Python 3.9+
- yt-dlp
- FFmpeg recommended (needed for stream merging and audio conversion)

## Installation

```bash
python -m pip install -U yt-dlp
```

Download `yt_dl_easy.py` from the release assets or repository and run:

```bash
python yt_dl_easy.py
```

On Windows, `py yt_dl_easy.py` may be used instead. See `README.md` for full installation, configuration, examples, and troubleshooting.

## Known limitations

- This is an interactive frontend, not a replacement for yt-dlp. Website support and extraction behavior depend on the installed yt-dlp version.
- FFmpeg is an external dependency for merging separate streams and converting audio.
- The initial release has been designed for Windows 10/11 and Linux, but has not been exhaustively tested across every terminal emulator, distribution, or console configuration.
- Updating yt-dlp is performed separately using the installation method originally chosen.

## Checksums

No checksum is published in this source release. Generate SHA-256 checksums for the exact release assets uploaded to GitHub and add them to the GitHub Release description if you want to provide verified downloads.
