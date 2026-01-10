#!/usr/bin/env python3
"""Clean VTT subtitle files and convert to plain text."""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


def clean_vtt(vtt_content: str) -> str:
    """Remove VTT formatting and extract plain text."""
    lines = vtt_content.split('\n')
    text_lines = []
    seen_lines = set()

    for line in lines:
        # Skip VTT header
        if line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue
        # Skip timestamp lines
        if re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3}\s*-->', line):
            continue
        # Skip sequence numbers
        if re.match(r'^\d+$', line.strip()):
            continue
        # Skip empty lines
        if not line.strip():
            continue
        # Skip position/alignment tags
        if re.match(r'^align:', line) or re.match(r'^position:', line):
            continue

        # Remove inline VTT tags like <c>, </c>, <00:00:00.000>
        cleaned = re.sub(r'<[^>]+>', '', line)
        cleaned = cleaned.strip()

        # Skip duplicates (common in auto-generated subs)
        if cleaned and cleaned not in seen_lines:
            seen_lines.add(cleaned)
            text_lines.append(cleaned)

    return '\n'.join(text_lines)


def to_kebab_case(title: str) -> str:
    """Convert title to kebab-case filename."""
    # Remove special characters except spaces and Korean
    cleaned = re.sub(r'[^\w\s가-힣-]', '', title)
    # Replace spaces with hyphens
    kebab = re.sub(r'\s+', '-', cleaned.strip())
    # Convert to lowercase and limit length
    return kebab.lower()[:50]


def main():
    parser = argparse.ArgumentParser(description='Clean VTT subtitle files')
    parser.add_argument('vtt_file', help='Path to VTT file')
    parser.add_argument('--title', '-t', help='Video title for output filename', default='transcript')
    args = parser.parse_args()

    vtt_path = Path(args.vtt_file)
    if not vtt_path.exists():
        print(f"Error: File not found: {vtt_path}", file=sys.stderr)
        sys.exit(1)

    # Read and clean
    vtt_content = vtt_path.read_text(encoding='utf-8')
    cleaned_text = clean_vtt(vtt_content)

    # Generate output filename
    kebab_title = to_kebab_case(args.title)
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    output_filename = f"{kebab_title}-{timestamp}.txt"
    output_path = Path('/tmp') / output_filename

    # Save
    output_path.write_text(cleaned_text, encoding='utf-8')
    print(output_path)


if __name__ == '__main__':
    main()
