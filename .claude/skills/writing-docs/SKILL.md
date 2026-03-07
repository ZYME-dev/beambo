---
name: writing-docs
description: Use when creating, editing, restructuring, or reviewing technical documentation in apps/docs/. Classifies content by Diataxis type, proposes structure and navigation placement for user approval, then drafts following Fumadocs conventions and project writing principles. Triggers on "write docs", "add a doc page", "document this", "update docs", "improve docs".
---

# Writing Technical Documentation

Create and maintain documentation in `apps/docs/content/docs/` following Diataxis content classification, Fumadocs MDX conventions, and project writing principles.

## When to Use

- Creating a new documentation page
- Restructuring or splitting existing content
- Editing or improving an existing page
- Reviewing documentation quality

## When NOT to Use

- Writing Architecture Decision Records (ADRs) — separate skill
- Auto-generating API reference from code
- Editing non-docs markdown (READMEs, specs, plans in `llm/`)
- Writing inline code comments or docstrings

## Workflow

### Phase 1: Explore & Scope — REQUIRES USER APPROVAL

Before writing any content, you MUST gather context and present a structure for approval.

#### Step 1: Dispatch parallel exploration agents

Launch TWO subagents in parallel using the Agent tool:

**Code explorer** — understands the feature/system being documented:
- Read the relevant source code (modules, types, tests)
- Identify key abstractions, public APIs, data flow
- Note naming conventions and domain terms used in code
- Summarize: what it does, how it works, key concepts

**Docs explorer** — maps the current state of documentation:
- Run `tree apps/docs/content/docs/ -I node_modules` to capture the full content tree
- Search for existing pages related to the topic
- Check if the topic is already partially documented, outdated, or missing
- Review neighboring pages for context, terminology, and cross-links
- Summarize: current tree, what exists, what's missing, what needs updating

Wait for both agents to complete before proceeding.

#### Step 2: Classify & outline

Using the exploration results:

1. **Classify the Diataxis type.** Read `reference/diataxis.md` for the compass. Every page is exactly ONE type: tutorial, how-to, explanation, or reference. If it straddles two types, plan to split it.

2. **Determine navigation placement.** Where does this page live in `content/docs/`? Which section? Does it need a new subsection? What `meta.json` entries need updating?

3. **Draft the outline.** List each H2 section with a 1-line description of what it covers. Follow the section template for the classified type (see `reference/diataxis.md`).

#### Step 3: STOP — present for user approval

Present to the user:
- Key findings from both explorers (brief)
- Diataxis type and rationale
- File path and navigation placement
- Section outline with 1-line descriptions
- Any `meta.json` changes needed
- Existing pages that need cross-linking or updating

Do NOT proceed to Phase 2 until the user approves the structure.

### Phase 2: Draft

Write section-by-section, applying ALL of these principles:

**Content principles:**
- **Code-first.** Lead with a complete, runnable example. Prose annotates the code, not the other way around.
- **Progressive disclosure.** Simplest correct path first. Details, edge cases, and advanced config go in later sections, expandable blocks, or linked pages.
- **One concept per page.** If you find yourself writing about two distinct things, split the page.
- **Don't bury the lede.** Action first, motivation after. Put the `pnpm install` before the three paragraphs of context.
- **Audience-aware.** State prerequisites upfront. Don't assume the reader has context from other pages without linking.

**Terminology table.** For explanation and reference pages that introduce a system or subsystem, include a terminology table immediately after the introductory paragraph:

```markdown
## Key Concepts

| Term     | Definition                | Responsibility              |
| -------- | ------------------------- | --------------------------- |
| **Name** | What it is (one sentence) | What it does (one sentence) |
```

Rules for the terminology table:
- **Term**: the exact name used in code and conversation — no synonyms
- **Definition**: one sentence, what it *is*
- **Responsibility**: one sentence, what it *does* (Single Responsibility framing)
- Placed after intro paragraph, before detailed sections
- Only on pages introducing a system, subsystem, or bounded context — not every page

**Diagrams.** Architecture and system-level explanation pages USUALLY include at least one Mermaid diagram. Use diagrams for: system overviews, data flow, state machines, component relationships. Don't diagram trivial things.

**Consistency.** Use the project's established terminology. If a concept has a name in the codebase, use that name. Don't invent synonyms.

Follow Fumadocs conventions from `reference/fumadocs.md` for frontmatter, components, and file structure.

### Phase 3: Verify

After drafting, review the page against this checklist:

- [ ] Single Diataxis type — no type mixing
- [ ] Terminology table present (if introducing a system/subsystem)
- [ ] Code examples are complete and specify language tags
- [ ] Mermaid diagram included (if architecture/system-level)
- [ ] Frontmatter has `title` and `description` (< 160 chars)
- [ ] `meta.json` updated with new page entry
- [ ] H2 as top-level headings (H1 auto-generated from title)
- [ ] Prerequisites stated or linked
- [ ] Page makes sense without reading other pages first
- [ ] No walls of text — visual hierarchy with headings, lists, callouts, code

Flag any sections that reference specific versions, configs, or outputs as at risk of staleness.

## Writing Style (compact rules)

- Active voice, second person ("you configure", not "the configuration is done by")
- Present tense ("this module handles", not "this module will handle")
- Sentence-case headings
- Short paragraphs (3-5 sentences max)
- Bold for key terms on first use
- Use `<Callout type="info">` for key takeaways, `<Callout type="warn">` for gotchas
- Use `<Tabs>` for Python/TypeScript polyglot examples
- Use `<Steps>` for sequential instructions
- Use `<Cards>` for navigation hub pages

## Reference Files

- `reference/diataxis.md` — content type compass, section templates per type
- `reference/fumadocs.md` — MDX conventions, components, frontmatter, meta.json format
