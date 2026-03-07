---
name: writing-adrs
description: Create Architecture Decision Records in llm/adrs/. Three modes —
  extract decisions from a spec, extract from the current session, or write a
  standalone ADR. Triggers on "extract ADRs", "create an ADR", "record this
  decision", "writing ADRs", "what did we decide".
metadata:
  argument-hint: "[spec path or 'session']"
---

# Writing ADRs

Create Architecture Decision Records — atomic, immutable records answering "why did we choose X over Y?"

## What an ADR Is

An **ADR** (Architecture Decision Record) is a **single decision, frozen in time**.

- One decision per file — atomic, not narrative
- Immutable — never edited once accepted. Supersede instead.
- Rationale-focused — the "why" matters more than the "what"
- Not a spec (specs are narrative design docs), not a plan (plans are execution steps)

### What deserves an ADR?

**Yes:** architectural choices, technology selections, pattern decisions, rejected alternatives worth remembering.

**No:** implementation details ("we used a for-loop"), trivial choices nobody would question, temporary workarounds.

**Threshold:** would a new agent (or future-you) reasonably question this choice? If yes, record it.

## The Form

**Location:** `llm/adrs/YYYY-MM-DD-kebab-title.md`

Date-prefixed, consistent with specs and plans. Natural `ls` sorting is chronological. If multiple ADRs share a date, the kebab suffix disambiguates.

### Template

```markdown
---
title: Use UUID v7 for all entity identifiers
date: 2026-03-02
description: Time-ordered UUIDs for natural sort order and better index locality
---

# Use UUID v7 for all entity identifiers

## Context

[1-3 paragraphs. Forces at play. Why this decision was needed. Value-neutral.]

## Decision

We will [active voice, one clear statement].

## Alternatives Considered

- **[Alternative A]** — rejected because [reason]
- **[Alternative B]** — rejected because [reason]

## Consequences

- [+] [positive outcome]
- [-] [negative outcome or accepted trade-off]
- [!] [risk to monitor]
```

### Frontmatter

Every ADR starts with YAML frontmatter — three fields, no more:

- **title** (required) — the decision stated concisely
- **date** (required) — creation date, YYYY-MM-DD
- **description** (required) — one line answering "why should I open this file?"

All ADRs are implicitly **accepted** — no status field. If a decision is superseded, create a new ADR and note "Supersedes [title](link)" in its Context section.

### What's NOT in the template

- No status field — all ADRs are accepted by definition
- No "AI Guidance" section — the Decision + Consequences IS the guidance
- No "Confirmation" section — linters and CI handle enforcement

### The Index (`llm/adrs/README.md`)

```markdown
# Architecture Decision Records

| Date | Decision |
|------|----------|
| 2026-03-02 | [Use decision records](2026-03-02-use-decision-records.md) |
| 2026-03-02 | [Use UUID v7 everywhere](2026-03-02-use-uuid-v7-everywhere.md) |
```

Maintained by this skill — updated every time an ADR is created.

## Three Modes

### Mode 1: Extract from a spec

**Input:** path to a spec file (e.g., `llm/specs/2026-02-17-mutation-session-architecture.md`)

1. Read the spec
2. Read existing ADRs in `llm/adrs/` (avoid duplicates)
3. Identify decisions — look for: "we will", "we chose X over Y", trade-off discussions, technology selections, pattern choices, rejected alternatives
4. Present candidate decisions as a numbered list with one-line summaries
5. **User selects** which to extract — not everything is ADR-worthy
6. Draft one ADR file per selected decision
7. Add a `## Decisions` section to the spec linking to the extracted ADRs
8. Update `llm/adrs/README.md` index

### Mode 2: Extract from session

**Input:** "session" or "this conversation"

1. Review the conversation for decisions made during the session
2. Read existing ADRs (avoid duplicates)
3. Present candidate decisions for selection
4. Draft ADR files for selected decisions
5. Update index

### Mode 3: Write standalone

**Input:** a specific decision stated inline (e.g., "record that we chose Temporal over Date")

1. Read existing ADRs (check for duplicates or related decisions)
2. Draft a single ADR through brief dialogue — clarify context and alternatives if not obvious
3. Update index

## Process

Regardless of mode:

1. **Determine filename** — use today's date + kebab title, check `llm/adrs/` for duplicates
2. **Create `llm/adrs/` directory** if it doesn't exist, along with `README.md`
3. **Draft ADRs** — use the template, keep them short (20-40 lines)
4. **Present for review** — show each draft, let the user adjust before writing
5. **Write files** — one file per decision
6. **Update index** — append to `README.md` table
7. **Cross-link** — if extracted from a spec, update the spec with a Decisions section

## Rules

- **Never edit an ADR.** To change a decision, create a new ADR that supersedes it.
- **Don't over-extract.** 3-5 decisions from a typical spec is normal. 15 means you're recording implementation details, not decisions.
- **Keep them short.** If an ADR exceeds 50 lines, it's probably two decisions or drifting into spec territory.
- **Active voice in the Decision section.** "We will use X" not "X was chosen" — ownership matters.

## Complementary Skills

| Skill | Relationship |
|-------|-------------|
| `writing-specs` | Upstream — specs produce decisions, this skill harvests them |
| `writing-docs` | Parallel — ADRs can inform documentation but aren't docs themselves |
| `/implement` | Downstream — plans should respect existing ADRs |
