---
description: Package a skill folder into a distributable .skill file.
argument-hint: <path-to-skill-folder> [output-directory]
---

Package a Claude Code skill into a distributable .skill file.

## Usage

```
/package-skill <path-to-skill-folder> [output-directory]
```

## Arguments

- `$ARGUMENTS`: Skill folder path (required), optionally followed by output directory

## Task

1. Parse arguments from: $ARGUMENTS
   - First argument: skill folder path (required)
   - Second argument: output directory (optional)

2. Validate the skill folder exists and contains SKILL.md

3. Run the packaging script:
   ```bash
   python ~/.claude/skills/skill-creator/scripts/package_skill.py <skill-path> [output-dir]
   ```

4. Report the result:
   - On success: Show the path to the generated .skill file
   - On failure: Show validation errors and suggest fixes

## Example

```
/package-skill ./.claude/skills/my-skill
/package-skill ./.claude/skills/my-skill ./dist
```
