# Reusable development agents

The five canonical role definitions live in [`roles/`](roles/). Generated
tool-specific definitions live in `.codex/agents/` and `.claude/agents/`.

Edit only the canonical files, then regenerate/check both tools:

```text
uv run --no-project python scripts/sync_agents.py --tool all
uv run --no-project python scripts/sync_agents.py --tool all --check
```

The check validates role names, generated TOML and Claude frontmatter,
instruction parity, explicit-only invocation rules, role boundaries, and drift.
For changes limited to one tool, use `--tool codex` or `--tool claude` instead.
The canonical role files remain the only instruction source. Both tool formats
now include the reviewed role requirements; no model is pinned.
