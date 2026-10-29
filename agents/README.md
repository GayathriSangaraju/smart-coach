# Reusable development agents

The five canonical role definitions live in [`roles/`](roles/). Generated
tool-specific definitions live in `.codex/agents/` and `.claude/agents/`.

Edit only the canonical files, then regenerate both tool formats:

```text
uv run --no-project python scripts/sync_agents.py
uv run --no-project python scripts/sync_agents.py --check
```

The check command validates role names, generated TOML, Claude YAML
frontmatter, instruction parity, explicit-only invocation rules, and drift.
