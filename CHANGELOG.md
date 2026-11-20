# Changelog

All notable changes to YT-DL Easy Py are documented in this file.

## [1.2.0]

### Fixed
- Fixed format-table alignment by removing all injected prefixes and labels from yt-dlp's format rows.
- Kept codec and original/default audio highlighting using color only, preserving the original columns and format IDs.

### Added
- Added separate manual video and audio format selection. Users enter one video format ID and one audio format ID in separate prompts; YT-DL Easy Py constructs the yt-dlp selection expression.
- Added best-available defaults (`bestvideo*` and `bestaudio`) to the separate stream prompts.

### Changed
- Replaced the combined manual `VIDEO+AUDIO` format entry with a guided two-step selection.
- Updated README documentation and release notes for the revised format workflow.

### Notes
- Original/default audio highlighting is based only on labels present in yt-dlp's own format-list output.
- FFmpeg is still required to merge separate video and audio streams.

## [1.1.0]

### Added
- Highlight audio formats that yt-dlp explicitly identifies as `original` or `default`.
- Distinct visual colors/labels for AV1 (`av01`), H.264 (`avc1`), and VP9 (`vp9`) video formats.
- A post-session prompt to start another download without restarting the application.

### Changed
- The repeat-session prompt defaults to **No**. Press Enter to exit.

### Notes
- Original/default audio highlighting depends on yt-dlp including that designation in its format-list output.
