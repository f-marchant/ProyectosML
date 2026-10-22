# long-horizon-prompting: secciones ampliadas

Secciones movidas desde SKILL.md para no superar los 20.000 caracteres.

## References

Internal references:
- [Annotated CDC prompt](./cdc-prompt-annotated.md) - The full published prompt with element-by-element annotation and provenance
- [Vendor guidance](./vendor-guidance.md) - Dated OpenAI and Anthropic long-horizon and multi-agent prompting doctrine with sources
- [Research evidence](./research-evidence.md) - Dated academic findings behind each brief element
- [Task brief template](./task-brief-template.md) - Reusable pseudo-formal brief template and pre-launch evaluation rubric

Related skills in this collection:
- multi-agent-patterns - Topology and coordination for the orchestrations these briefs steer
- harness-engineering - Runtime enforcement of what the brief can only request

External resources:
- OpenAI, published prompt for the GPT-5.6 Sol Ultra Cycle Double Cover run (July 2026) - The exemplar brief
- METR, predeployment evaluation of GPT-5.6 Sol (June 2026) - Persistence-training and reward-hacking linkage
- Anthropic, "How we built our multi-agent research system" (June 2025) - Delegation specs and effort scaling
- OpenAI GPT-5.x prompting guides and Anthropic Claude prompting docs - Vendor doctrine detailed in the vendor guidance reference

Numeric, benchmark, volatile, or vendor-performance claims in this skill carry inline `claim-*` IDs backed by `researcher/claims/index.jsonl`. Detailed numbers live in the dated reference files.

---

## Examples

**Example 1: Pseudo-formal brief skeleton**

```text
DEFINITIONS
  <every load-bearing term, including degenerate cases>

TASK
  <exact success predicate with quantifiers and scope>

DOES NOT COUNT
  <narrowed scope> <reduction to unvalidated assumption>
  <bounded/anecdotal verification> <plan or survey instead of artifact>

ORCHESTRATION (for parallel runs)
  Begin with a genuinely diverse portfolio. Keep early workers blind
  to the favored approach. Registry of approach families by idea, not
  wording. Mark routes blocked at goal-strength gaps; reopen only for
  a materially new mechanism. Cross-pollinate late.

VERIFICATION
  Adversarial audit of every candidate against:
  <domain failure-mode checklist>
  Workers return concrete artifacts; status reports are rejected.

RETURN CONDITION
  Return only when a candidate survives the audit. Do not return a
  reduction, partial result, or explanation of difficulty.

EFFORT
  Assume a solution exists. Spend at least <floor> before considering
  returning.

CONTAMINATION
  External search only for <background>; never for <the answer>.
```

**Example 2: Weak prompt to strong brief (root-cause analysis)**

```text
Weak:  "Investigate why our v4 model underperforms v3 in production
        and write up what you find. Be thorough."

Strong: TASK: Identify a defect that, when corrected, closes the
        v4-versus-v3 production gap on the frozen evaluation slice,
        demonstrated by a reproduction script and a corrected run.
        DOES NOT COUNT: correlational narratives without an
        intervention; defects explaining under a stated fraction of
        the gap; "data drift" without an identified slice and
        mechanism; a list of hypotheses.
        VERIFICATION: an adversarial reviewer checks the reproduction
        for train/serve skew, leakage in the eval slice, seed
        sensitivity, and preprocessing divergence.
        RETURN: only a candidate that survives that review.
```

The weak version invites a status report. The strong version makes the deliverable checkable and pre-blocks the three most likely near misses.

## Integration

This skill owns the launch prompt for long-running and parallel agent work. Adjacent skills own the machinery around it:

- multi-agent-patterns - Owns topology, handoffs, and coordination protocols; this skill writes the orchestration policy those structures execute
- harness-engineering - Owns runtime-enforced budgets, locked evaluators, and control surfaces; constraints that must survive optimization pressure move there
- evaluation - Owns deterministic evaluators and quality gates referenced by the brief's verification policy
- advanced-evaluation - Owns judge design, rubrics, and bias mitigation for the adversarial audit step
- self-improvement-loops - Owns loops that rewrite their own prompts and harnesses; briefs written here can become that loop's seed
- filesystem-context - Owns the durable progress ledgers and artifacts the reporting contract points at
- context-compression - Owns compaction and handoff mechanics when a run outlives its context window
- hosted-agents - Owns the sandboxed infrastructure long runs execute on

## Gotchas

1. **Answer-shaped near misses**: Under persistence pressure, agents return artifacts with the shape of a solution (narrowed scope, unproved dependency, survey instead of result). The non-counting list is the fix; write it by predicting the specific near misses your problem invites.
2. **Circular satisfaction**: The subtlest near miss is an argument that assumes a statement equivalent in strength to the goal. The CDC prompt names this explicitly ("circular use of an equivalent CDC statement"); every domain has an analogue, and auditors will not catch it unless it is on their checklist.
3. **Persistence without verification breeds hacking**: Persistence-trained and persistence-prompted agents show elevated rates of gaming their success signal (claim-long-horizon-persistence-hacking). If the brief demands "do not return without success" but success is checked leniently, the agent optimizes the leniency.
4. **Unanimity is not corroboration**: Parallel agents agreeing is weak evidence when they share priors, and convergence tightens on harder problems (claim-long-horizon-diversity-collapse). Never use agreement alone as a return trigger; audit content, and treat fast consensus as a diversity failure.
5. **Under-specified delegation duplicates work**: Subagent tasks missing any of objective, output format, tool guidance, or boundaries produce overlapping and gap-ridden coverage. The orchestrator prompt should require all four in every spawn.
6. **Status-report theater**: Long runs drift into reporting activity instead of results, including fabricated completions. Require artifact-based reporting and evidence-traceable claims (claim-long-horizon-evidence-audit); reject "on track" without a pointer.
7. **Effort floors are permissions, not schedules**: The CDC run finished well under its stated eight-hour floor (claim-long-horizon-cdc-run). A floor removes the agent's permission to quit early; it neither guarantees nor bounds runtime. Enforce actual time and cost budgets in the harness.
8. **Prompt-stated budgets decay**: A budget or reminder stated once loses force as the trajectory grows; re-inject budget and verified-progress state periodically from outside the loop (claim-long-horizon-give-up-drift).
9. **Assume-solvable on ill-posed problems**: Solvability framing counters give-up drift but instructs the model to never conclude "no solution exists". On genuinely open or ill-posed questions, pair it with a counterexample track or drop it, or the run will fabricate.
10. **Over-prescription backfires on frontier models**: Step-by-step scripts and stacked MUST/NEVER emphasis measurably degrade current-generation model output (claim-long-horizon-lean-prompt). Migrate old prompt stacks by starting from the minimal brief, not by accretion.

