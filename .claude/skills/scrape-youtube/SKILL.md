---
name: scrape-youtube
description: Extract transcript from YouTube videos using yt-dlp. Prefers Korean subtitles, falls back to English. Use when user provides a YouTube URL and wants the transcript.
---

# Scrape YouTube Transcript

Extract transcripts from YouTube videos using yt-dlp. Saves to temp file for further processing.

## Workflow

### Step 1: Receive YouTube URL

Get the YouTube URL from the user. Accept various formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`

### Step 2: Get Video Title

Extract the video title for the filename:

```bash
yt-dlp --print "%(title)s" "<URL>"
```

### Step 3: Extract Subtitle

Run yt-dlp to download the subtitle file:

```bash
yt-dlp --write-sub --write-auto-sub --sub-lang "ko,en" --sub-format "vtt" --skip-download -o "/tmp/yt-transcript" "<URL>"
```

**Flags explained:**
- `--write-sub`: Download manual subtitles if available
- `--write-auto-sub`: Fall back to auto-generated subs
- `--sub-lang "ko,en"`: Prefer Korean, fallback to English
- `--sub-format vtt`: VTT format (easier to parse)
- `--skip-download`: Don't download the video itself

### Step 4: Clean VTT and Save

Use the cleaning script to convert VTT to plain text and save.

**Script location:** `.claude/skills/scrape-youtube/scripts/clean_vtt.py` (relative to project root)

```bash
python3 .claude/skills/scrape-youtube/scripts/clean_vtt.py /tmp/yt-transcript.ko.vtt --title "Video Title"
```

If Korean subtitle not found, use `.en.vtt` instead.

The script saves to `/tmp/{kebab-title}-{YYYYMMDD-HHMMSS}.txt` and prints the file path.

### Step 5: Notify User

Tell the user the file path where the transcript was saved.

### Step 6: Cleanup

Delete the temporary VTT file:

```bash
rm /tmp/yt-transcript*.vtt
```

## Tips

- If no subtitles are available, inform the user
- Auto-generated subtitles may have errors - note this to the user
- User can ask Claude to read and process the transcript file as needed
