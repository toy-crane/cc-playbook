# CC Playbook

A collection of skills, custom commands, hooks, and resources for Claude Code.

## What's Inside

### Custom Commands

Custom slash commands to extend Claude Code functionality.

| Command | Description |
|---------|-------------|
| `/clarify` | Clarify vague ideas through Socratic questioning. Transforms abstract concepts into concrete understanding. |

### Skills

*Coming soon*

### Hooks

*Coming soon*

## Installation

Copy the desired files to your Claude Code configuration:

- **Project-level**: `.claude/` directory in your project
- **User-level**: `~/.claude/` directory for global access

### Example

```bash
# Clone the repo
git clone https://github.com/toy-crane/cc-playbook.git

# Copy a command to your project
cp cc-playbook/.claude/commands/clarify.md your-project/.claude/commands/
```

## Structure

```
.claude/
├── commands/       # Custom slash commands
├── skills/         # Skills for extended capabilities
└── hooks/          # Event-driven automation
```

## Contributing

Feel free to open issues or submit PRs with your own Claude Code configurations.

## License

MIT
