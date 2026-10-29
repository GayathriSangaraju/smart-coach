# Reusable development agents

This repository provides five manually invoked roles for Codex and Claude Code:

- `product-owner`
- `solution-architect`
- `developer`
- `code-reviewer`
- `tester`

Each role handles only the supplied GitHub issue or pull request and ends with a
handoff. Roles never invoke the next role or an agent team automatically.

## Keep generated definitions synchronized

Canonical instructions live in `agents/roles/`. Do not edit `.codex/agents/`
or `.claude/agents/` directly.

```text
uv run --no-project python scripts/sync_agents.py
uv run --no-project python scripts/sync_agents.py --check
```

## Codex

Run the command from the repository root. Replace the example number with the
real issue or pull request URL.

```text
codex "Run only the product-owner custom agent for https://github.com/dhaval-mistry/unshaken-smart-coach/issues/123. Do not invoke any other role."
codex "Run only the solution-architect custom agent for https://github.com/dhaval-mistry/unshaken-smart-coach/issues/123. Do not invoke any other role."
codex "Run only the developer custom agent for https://github.com/dhaval-mistry/unshaken-smart-coach/issues/123. Do not invoke any other role."
codex "Run only the code-reviewer custom agent for https://github.com/dhaval-mistry/unshaken-smart-coach/pull/123. Do not invoke any other role."
codex "Run only the tester custom agent for https://github.com/dhaval-mistry/unshaken-smart-coach/pull/123. Do not invoke any other role."
```

Codex has no project-agent CLI selector. Directly name the custom agent in the
prompt. In an interactive Codex session, use `/subagents` to inspect agent
threads after explicitly requesting a role.

The command form above was verified against the installed Codex CLI. Role
execution was intentionally not launched during configuration validation.

## Claude Code

Claude Code supports selecting a project agent for the whole session with
`--agent`:

```text
claude --agent product-owner "Work only on https://github.com/dhaval-mistry/unshaken-smart-coach/issues/123."
claude --agent solution-architect "Work only on https://github.com/dhaval-mistry/unshaken-smart-coach/issues/123."
claude --agent developer "Work only on https://github.com/dhaval-mistry/unshaken-smart-coach/issues/123."
claude --agent code-reviewer "Review only https://github.com/dhaval-mistry/unshaken-smart-coach/pull/123."
claude --agent tester "Test only https://github.com/dhaval-mistry/unshaken-smart-coach/pull/123."
```

Claude Code was not installed in the environment used to create these files,
so these commands and discovery could not be runtime-tested here. The file
layout and `--agent` syntax follow the official Claude Code subagent format.

## GitHub access

Before writing, each role checks available GitHub connectors, MCP tools, or an
authenticated `gh` CLI. Repository access and GitHub Project access are
separate. If a required write is unavailable, the role reports the missing
capability and returns ready-to-post content instead of claiming success.
