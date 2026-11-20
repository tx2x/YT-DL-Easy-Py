# Changelog

All notable changes to YT-DL Easy Py are documented in this file.

## [1.1.0]

### Added
- Highlight audio formats that yt-dlp explicitly identifies as `original` or `default`, using a prominent `★ ORIGINAL / DEFAULT` label.
- Distinct visual labels for AV1 (`av01`), H.264 (`avc1`), and VP9 (`vp9`) video formats.
- A post-session prompt to start another download without restarting the application.

### Changed
- The repeat-session prompt defaults to **No**. Press Enter to exit.
- Updated the README with the new format-list cues and repeat-session behavior.

### Notes
- Original/default audio highlighting depends on yt-dlp including that designation in its format-list output. YT-DL Easy Py does not infer an original language from language codes.
- The original yt-dlp format rows and IDs are preserved; labels are added only for easier scanning.
