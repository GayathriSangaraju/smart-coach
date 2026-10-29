# Repository agent guidance

UNShaken Smart Coach is currently a planning and foundation project. Read the
root README, relevant setup documents, and any supplied GitHub issue or pull
request before acting. Planned features are not necessarily implemented.

## Reusable roles

Canonical role instructions live in `agents/roles/`. Files in `.codex/agents/`
and `.claude/agents/` are generated; do not edit them directly. Run
`uv run --no-project python scripts/sync_agents.py --check` to check drift.

Run only the role a participant explicitly requests. Do not automatically
invoke another role, an agent team, or a follow-on workflow. End with a manual
handoff. Humans approve requirements, architecture decisions, merges,
deployments, and changes to unresolved product rules.

## GitHub and safety

GitHub issues, pull requests, discussions, commits, and Project 5 are the work
record. Preserve human-authored content, check for duplicates before writing,
and distinguish approved decisions from proposals and open questions. Confirm
repository and Project authorization separately. If a write is unavailable,
provide ready-to-post content and report the missing capability.

Use existing permissions only. Never expose credentials or personal data,
merge, deploy, delete data, or migrate an existing/shared database without
separate human authorization. Respect unresolved decisions in
`docs/database/design.md` when that file is present.
