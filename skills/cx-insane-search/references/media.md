# Public Media Metadata and Subtitles

For a public YouTube or supported media URL, the engine may invoke pinned `yt-dlp` through `uvx` to read metadata or available subtitles without downloading the media.

Use it for title, uploader, duration, public metadata and creator-provided or publicly available subtitle tracks. Respect geo, age, login and rights restrictions. Do not pass browser cookies, credentials or private playlist state.

Prefer a transcript supplied by the platform or creator. Report when only auto-generated subtitles are available.
