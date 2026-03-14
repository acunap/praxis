---
name: complexity-review
description: Reviews technical proposals against 30 complexity dimensions. Questions necessity of scale, consistency, and resilience. Use when proposing technologies (Kafka, microservices, event sourcing) or designing systems. Pushes for simplest viable approach.
---
icon: 🔍

# Complexity Review

Review technical proposals by:
1. Systematically reviewing against the 30 Complexity Dimensions (see REFERENCE.md)
2. Questioning every complexity driver
3. Proposing simpler alternatives
4. Identifying what can be postponed

## The 6 Complexity Categories

Use these categories to systematically challenge technical proposals. For the complete 30 dimensions checklist, see [REFERENCE.md](REFERENCE.md).

### 1. Data Volume and Nature (5 dimensions)
- Data size, number of elements, growth rate, processing weight, lifespan
- **Key questions**: "How much data really?", "Do we need to handle this scale now?"

### 2. Interaction and Frequency (4 dimensions)
- Interaction frequency, latency, concurrency, elasticity
- **Key questions**: "How often does this happen?", "Can we use batch instead of real-time?"

### 3. Consistency, Order, Dependencies (5 dimensions)
- Processing order, scope of order, consistency guarantees, distributed transactions, state
- **Key questions**: "Does order matter?", "Can we use eventual consistency?"

### 4. Resilience, Security, Fault Tolerance (8 dimensions)
- Error criticality, idempotence, side effects, uniqueness, reversibility, inconsistency tolerance, exactly-once, auditability
- **Key questions**: "What happens if this fails?", "Can we accept graceful degradation?"

### 5. Integration, External Dependencies, Versions (4 dimensions)
- External dependencies, security/privacy, versioning, interoperability
- **Key questions**: "Can we mock external services initially?", "Do we need versioning now?"

### 6. Efficiency, Maintainability, Evolution (4 dimensions)
- Refactoring flexibility, cost sensitivity, availability requirements, scaling time
- **Key questions**: "Can we change this later?", "Do we need 99.99% uptime or is 99% OK?"

## Quick Reference: Proposal → Dimensions to Challenge

| Proposal Contains | Challenge These Dimensions | Alternative to Consider |
|-------------------|---------------------------|-------------------------|
| Kafka, event streaming, message queues | #6 (frequency), #10 (order), #12 (consistency), #13 (transactions) | PostgreSQL + cron job, simple polling |
| Microservices | #8 (concurrency), #13 (distributed transactions), #14 (state), #23 (dependencies) | Modular monolith, well-structured modules |
| Event sourcing, CQRS | #10 (order), #12 (consistency), #22 (auditability), #27 (refactoring) | Append-only table, structured logging |
| Caching layer (Redis, Memcached) | #5 (lifespan), #7 (latency), #12 (consistency), #20 (inconsistency tolerance) | In-memory cache, query optimization first |
| Auto-scaling, serverless | #8 (concurrency), #9 (elasticity), #28 (cost), #30 (scaling time) | Fixed capacity, manual scaling initially |
| NoSQL database | #2 (elements), #12 (consistency), #13 (transactions), #27 (refactoring) | PostgreSQL with JSONB, evaluate need first |
| Multiple databases | #23 (dependencies), #27 (refactoring), #28 (cost) | Single database with clear schema |
| Real-time features, WebSockets | #6 (frequency), #7 (latency), #8 (concurrency), #14 (state) | Polling, periodic refresh (5-30 sec) |

## Review Process

### Step 1: Identify Complexity Drivers
List all the complexity dimensions the proposal addresses (scale, consistency, resilience, etc.)

### Step 2: Challenge Each One
Review all 30 dimensions against the proposal. Most will pass without issue — only document the ones that **raise a real concern or challenge** the proposal.

For each dimension that raises a concern, document a **Complexity Challenge (CD)** in the plan document:

```
### CD-{N}: {Dimension name} — {one-line challenge}
- **Status**: Open / Resolved
- **Dimension**: #{number} — {dimension name}
- **Challenge**: {What assumption is being questioned? What seems over-engineered?}
- **Context**: {Why this matters for this specific proposal}
- **Options** (if applicable):
  - A) {simpler alternative}
  - B) {proposed approach}
- **Resolution**: {How it was resolved — which option was chosen and why}
```

For each challenge, ask:
- **Is this assumption based on actual requirements or speculation?**
- **What's the simplest alternative that could work today?**
- **Can we postpone this until we have data?**

**Important:**
- Do NOT document dimensions that pass without concern — only those that genuinely challenge the proposal.
- If a challenge needs user input to resolve, mark it as **Open** and present it to the user before continuing to the next challenge. Resolve challenges **one at a time**, like Open Questions.

### Step 3: Propose Simpler Alternatives
Generate 2-3 progressively simpler versions of the proposal:
- **Version 1 (Simplest):** Absolute minimum, possibly manual. Must be deployable in 1-3 days.
- **Version 2 (Moderate):** Some automation, limited scale
- **Version 3 (Proposed):** Original proposal (only if justified)

Explain WHY the simpler version is better — not just "it's simpler". Include concrete criteria for when to add complexity later (e.g., "only if load > 10K/sec").

Document the versions in the plan as part of the complexity review output.

### Step 4: Highlight What Can Be Postponed
List features/complexity that can be added later:
- "We can add retries later if we see failures"
- "We can scale horizontally later if load increases"
- "We can add monitoring later if this becomes critical"

### Step 5: Analyze Basal Cost
For each component/feature in the proposal, estimate the **ongoing cost** it imposes on the team.

### Step 6: Write to Plan
The complexity review output MUST be written to the plan document — not just presented verbally. This includes:
- Only the CDs (Complexity Challenges) that raised real concerns, with their resolutions
- The progressive versions (simplest → proposed)
- The postponement list
- The final recommendation

This ensures reviewers can see the reasoning and the review is not lost after the conversation ends.

## Basal Cost of Software

Every dimension of complexity has an ongoing cost simply by existing — not the initial build cost, but the tax you pay forever after. It accumulates, grows non-linearly with coupling, and can exhaust a team.

Components: cognitive load, testing burden, maintenance (dependencies, docs), operational overhead (monitoring, debugging), future change cost (each new feature must account for existing complexity).

If basal cost consumes 70-80% of team capacity, only 20-30% remains for new features — the team is in a capacity trap.

When reviewing any proposal, ask:
- "What's the ongoing cost of this?"
- "How much team capacity will this consume in 6 months?"
- "What's the simplest version with 10x lower basal cost?"
- "Can we remove something else to make room for this?"

## When reviewing proposals

- Question every complexity driver — do not accept assumptions about scale, performance, or reliability without data
- Always ask: "Do we have data showing we need this?"
- Default to postponement: "Can we add this later when we know we need it?"
- Consider impact: "What's the worst that could happen if we don't build this?"
- Seek efficiency: "Can we achieve the same impact with fewer resources?"
- Apply time pressure: "What if we only had half the time?"

## Reference

For the complete list of 30 Complexity Dimensions with detailed questions, specialized checklists, and more examples, see [REFERENCE.md](REFERENCE.md) in this skill directory.
