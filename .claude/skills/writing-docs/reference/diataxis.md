# Diataxis Content Classification

## The Compass

Every documentation page is exactly ONE of these four types. If a page mixes types, split it.

| Type | Orientation | User asks | Voice | Success metric |
|------|------------|-----------|-------|----------------|
| **Tutorial** | Learning-oriented | "Teach me" | First-person plural ("we will..."), guided | Reader built something that works |
| **How-to** | Task-oriented | "Help me do X" | Imperative, concise | Reader accomplished their goal |
| **Explanation** | Understanding-oriented | "Help me think about this" | Discursive, contextual | Reader understands *why* |
| **Reference** | Information-oriented | "Give me the facts" | Neutral, exhaustive | Reader found the exact detail they needed |

## Classification Decision Tree

```
Is the reader trying to DO something specific right now?
├── YES: Do they already know what they're doing?
│   ├── YES → HOW-TO guide
│   └── NO → TUTORIAL
└── NO: Do they need a specific fact or signature?
    ├── YES → REFERENCE
    └── NO → EXPLANATION
```

## Anti-Patterns (Type Mixing)

- A tutorial that stops to explain architecture → split into tutorial + explanation
- A how-to that lists every parameter → split into how-to + reference
- A reference page that tries to teach concepts → split into reference + explanation
- An explanation that includes step-by-step instructions → split into explanation + how-to

---

## Section Templates

### Tutorial

Goal: the reader learns by doing. Every step produces a visible result.

```
## Introduction
What we'll build and why it matters. (2-3 sentences)

## Prerequisites
What the reader needs before starting. Be explicit.

## Step 1: [Action that produces a visible result]
Instructions → code → expected output.

## Step 2: [Next action]
Instructions → code → expected output.

## [... more steps]

## What We Built
Recap: what the reader achieved and what they learned.

## Next Steps
Links to how-to guides for real-world usage.
```

Rules:
- Every step MUST produce a visible, verifiable result
- Don't explain *why* — let the reader *do*. Link to explanations.
- Use first-person plural: "we will configure..." not "you should configure..."
- Keep it linear — no branching paths or "alternatively" blocks

### How-to Guide

Goal: the reader accomplishes a specific task. Assume competence.

```
## [Goal as title — e.g., "Deploy to Production"]

One sentence: what this guide helps you do and when you'd need it.

## Prerequisites
What you need before starting (tools, access, prior setup).

## Steps

<Steps>

### [Action verb + object]
Code example + minimal explanation.

### [Next action]
Code example + minimal explanation.

</Steps>

## Result
What you should see when done. How to verify it worked.

## Troubleshooting
Common errors and their fixes. (Optional, only if known pitfalls exist.)
```

Rules:
- Title names the GOAL, not the mechanism ("Deploy to production", not "Using the deploy script")
- Assume the reader is competent — don't over-explain
- Imperative voice: "Run this command", "Add this config"
- No background or theory — link to explanations if needed
- Keep it short. If > 10 steps, consider splitting.

### Explanation

Goal: the reader understands a concept, design decision, or system. This is where *why* lives.

```
## [Concept Name]

Introductory paragraph: what this is and why it matters. (3-5 sentences max)

## Key Concepts

| Term | Definition | Responsibility |
|------|-----------|----------------|
| **Name** | What it is (one sentence) | What it does (one sentence) |

## [How It Works / Architecture / Design]
Diagrams, data flow, component relationships.
At least one Mermaid diagram for system-level topics.

## [Why This Approach]
Trade-offs, alternatives considered, design drivers.
What becomes easier and what becomes harder.

## [Practical Implications]
How this affects day-to-day development.
What developers need to keep in mind.

## Related
Links to how-to guides, reference pages, and other explanations.
```

Rules:
- Terminology table required after intro (if introducing a system/subsystem)
- Mermaid diagram required for architecture topics
- Discuss trade-offs honestly — what we gave up and why
- Not tied to a specific task — this is conceptual
- Can be discursive — explore the topic from multiple angles
- Link to how-to guides for "how to actually do it"

### Reference

Goal: the reader finds a specific fact, signature, or parameter. Accuracy and completeness matter most.

```
## [API / Module / Entity Name]

One-line description of what this is.

## Key Concepts

| Term | Definition | Responsibility |
|------|-----------|----------------|
| **Name** | What it is (one sentence) | What it does (one sentence) |

## [Overview / Signature / Schema]
The primary interface: function signature, data schema, config shape.

## [Parameters / Fields / Options]
Table format. Every parameter documented. Types explicit.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `string` | required | ... |

## Examples
Minimal, focused code examples showing common usage patterns.

## Edge Cases & Gotchas
Known limitations, surprising behaviors, version-specific notes.
```

Rules:
- Mirror the code structure — if the code has 3 methods, the reference has 3 sections
- Completeness over narrative — every parameter, every option
- Neutral tone — just the facts
- Auto-generate where possible (from types, schemas, docstrings)
- Examples should be minimal — just enough to show usage, not teach concepts
- Terminology table if the reference introduces domain concepts
