# Reusable development agents

This repository provides five manually invoked roles for Codex and Claude Code:

- `product-owner`
- `solution-architect`
- `developer`
- `code-reviewer`
- `tester`

Product Owner accepts requirements for an initial backlog or an existing issue
for refinement; an issue URL and assignee are not required for initial backlog
creation. Other roles work from a supplied GitHub issue or pull request. Roles
end with a manual handoff and never invoke the next role or an agent team
automatically.

## Keep generated definitions synchronized

Canonical instructions live in `agents/roles/`. Do not edit `.codex/agents/`
or `.claude/agents/` directly.

```text
uv run --no-project python scripts/sync_agents.py
uv run --no-project python scripts/sync_agents.py --check
```

## Codex

### Product Owner: initial backlog

Start from requirements, ideas, screenshots, or repository documents. Replace
the example requirements with your own; include screenshot/document references
available to your session when relevant.

```text
codex "Run only the product-owner custom agent. Requirements: users can browse exercises and save personal workout templates. Read relevant repository documents, check existing issues for duplicates, and ask about missing decisions. Draft stories with scope, exclusions, dependencies, suggested priorities, and testable acceptance criteria. Present the proposed backlog for approval before creating or updating issues. Leave issues unassigned. Do not invoke another role."
```

### Product Owner: create approved issues

Use this in the same session after reviewing the proposed backlog. If starting
a new session, supply the exact approved stories and approval context.

```text
Create or update only the backlog stories I just approved in dhaval-mistry/unshaken-smart-coach. Continue only as product-owner. Check for duplicates again immediately before creating issues. Leave issues unassigned. Add them to Project 5 only if authenticated Project write access exists. Report issue URLs and any updates you could not make. Do not invoke another role.
```

### Product Owner: refine an existing story

```text
codex "Run only the product-owner custom agent to refine https://github.com/dhaval-mistry/unshaken-smart-coach/issues/123. Read the issue and relevant discussions, identify gaps and dependencies, and propose acceptance criteria and changes for approval before updating GitHub. Preserve human-authored content and recorded decisions. Do not require an assignee or invoke another role."
```

### Other roles

Run the command from the repository root. Replace the example number with the
real issue or pull request URL.

```text
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
claude --agent product-owner "Requirements: users can browse exercises and save personal workout templates. Read relevant repository documents, check for duplicate issues, and ask about missing decisions. Propose a backlog with scope, exclusions, dependencies, suggested priorities, and testable acceptance criteria for approval before writing to GitHub. Leave issues unassigned. Do not invoke another role."
claude --agent product-owner "Refine https://github.com/dhaval-mistry/unshaken-smart-coach/issues/123. Read discussions and propose changes for approval before updating GitHub. Preserve human-authored content and recorded decisions. Do not require an assignee or invoke another role."
claude --agent solution-architect "Work only on https://github.com/dhaval-mistry/unshaken-smart-coach/issues/123."
claude --agent developer "Work only on https://github.com/dhaval-mistry/unshaken-smart-coach/issues/123."
claude --agent code-reviewer "Review only https://github.com/dhaval-mistry/unshaken-smart-coach/pull/123."
claude --agent tester "Test only https://github.com/dhaval-mistry/unshaken-smart-coach/pull/123."
```

For approved issue creation, send the same continuation prompt shown above in
the active Product Owner session. Starting a new session requires supplying the
exact approved stories and approval context again.

Claude Code was not installed in the environment used to create these files,
so these commands and discovery could not be runtime-tested here. The file
layout and `--agent` syntax follow the official Claude Code subagent format.

## GitHub access

Before writing, each role checks available GitHub connectors, MCP tools, or an
authenticated `gh` CLI. Repository access and GitHub Project access are
separate. If a required write is unavailable, the role reports the missing
capability and returns ready-to-post content instead of claiming success.
