#!/usr/bin/env python3
"""
Clean VTT subtitle file and save plain text transcript.
Usage:
  python clean_vtt.py <input.vtt> --title "Video Title"

Saves to: /tmp/{kebab-title}-{YYYYMMDD-HHMMSS}.txt
"""

import re
import sys
import argparse
from datetime import datetime


def clean_vtt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove WEBVTT header and metadata
    content = re.sub(r'^WEBVTT\n.*?\n\n', '', content, flags=re.DOTALL)

    # Remove timestamp lines (00:00:01.000 --> 00:00:04.000)
    content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}.*\n', '', content)

    # Remove cue identifiers (numeric lines)
    content = re.sub(r'^\d+\n', '', content, flags=re.MULTILINE)

    # Remove VTT tags like <c>, </c>, <00:00:01.000>, etc.
    content = re.sub(r'<[^>]+>', '', content)

    # Remove position/alignment metadata
    content = re.sub(r'align:start position:\d+%', '', content)

    # Split into lines and remove duplicates
    lines = content.strip().split('\n')
    cleaned_lines = []
    prev_line = ''

    for line in lines:
        line = line.strip()
        if line and line != prev_line:
            cleaned_lines.append(line)
            prev_line = line

    return '\n'.join(cleaned_lines)


def to_kebab_case(text: str) -> str:
    """Convert text to kebab-case for filename."""
    # Remove special characters, keep alphanumeric and spaces
    text = re.sub(r'[^\w\s-]', '', text)
    # Replace spaces with hyphens
    text = re.sub(r'\s+', '-', text.strip())
    # Lowercase
    return text.lower()[:50]  # Limit length


def save_transcript(transcript: str, title: str) -> str:
    """Save transcript to /tmp/ with title and datetime in filename."""
    kebab_title = to_kebab_case(title)
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = f"{kebab_title}-{timestamp}.txt"
    output_path = f"/tmp/{filename}"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(transcript)

    return output_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean VTT subtitle file')
    parser.add_argument('input', help='Input VTT file path')
    parser.add_argument('--title', default='youtube-transcript', help='Video title for filename')

    args = parser.parse_args()

    transcript = clean_vtt(args.input)
    output_path = save_transcript(transcript, args.title)
    print(f"Saved to: {output_path}")
