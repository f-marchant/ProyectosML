# self-improvement-loops: secciones ampliadas

Secciones movidas desde SKILL.md para no superar los 20.000 caracteres.

## References

Internal reference:
- [Loop design evidence](./loop-design-evidence.md) - Dated per-system results, acceptance-rule details, ablation findings, and documented reward-hacking incidents backing this skill

Related skills in this collection:
- harness-engineering - Single-loop governance and control surfaces
- evaluation - Evaluator and quality-gate construction

External resources:
- Weng, "Harness Engineering for Self-Improvement" (Lil'Log, 2026) - Survey and framing of the optimization ladder and RSI challenges
- Zhang et al., "Self-Harness: Harnesses That Improve Themselves" (arXiv 2606.09498) - Failure-driven bounded self-edits with two-split acceptance
- Lee et al., "Meta-Harness: End-to-End Optimization of Model Harnesses" (arXiv 2603.28052) - Filesystem experience store and coding-agent proposer
- Ye et al., "Meta Context Engineering via Agentic Skill Evolution" (arXiv 2601.21557) - Mechanism-versus-artifact separation in context evolution
- Zhang et al., "Agentic Context Engineering" (arXiv 2510.04618) - Itemized deltas, deterministic merge, context collapse
- Zhang et al., "Darwin Godel Machine" (arXiv 2505.22954) - Archive-based harness evolution and documented objective hacking
- Zelikman et al., "Self-Taught Optimizer" (arXiv 2310.02304) - Recursive improver and the capability-threshold negative result
- Novikov et al., "AlphaEvolve" (arXiv 2506.13131) - Bounded mutation markers and evaluation cascades
- Lange et al., "ShinkaEvolve" (arXiv 2509.19349) - Novelty rejection and sample-efficient parent sampling
- METR, "Recent Frontier Models Are Reward Hacking" (2025) - Documented evaluator-gaming incidents in agentic tasks

Numeric, benchmark, volatile, or vendor-performance claims in this skill carry inline `claim-*` IDs backed by `researcher/claims/index.jsonl`. Detailed numbers live in the dated reference file.

---

## Examples

**Example 1: Two-split acceptance gate**

```python
def accept(candidate, baseline, held_in, held_out, repeats=3):
    d_in = mean_score(candidate, held_in, repeats) - mean_score(baseline, held_in, repeats)
    d_out = mean_score(candidate, held_out, repeats) - mean_score(baseline, held_out, repeats)
    if d_in < 0 or d_out < 0:
        return False              # no regression on either split
    return max(d_in, d_out) > 0  # strict improvement on at least one
```

The held-out split is invisible to the proposer. A candidate that gains on held-in by sacrificing held-out is rejected even if the sum is positive.

**Example 2: Experience archive layout**

```text
search-run/
  candidates/
    c0041/
      harness.py          # full candidate source
      scores.json          # per-split, per-repeat results
      traces/              # raw prompts, tool calls, outputs, state updates
      lineage.txt          # parent id, diff summary, decision, evidence
  frontier.json            # current Pareto set over (quality, cost)
  rejected.jsonl           # rejected candidates with reasons, append-only
```

The proposer greps this tree selectively. Nothing is summarized into its prompt by default.

**Example 3: Routing a failure to the right rung**

```text
Observed: agent repeatedly uses a deprecated API despite instructions.
Wrong fix: propose a harness-code edit adding retry logic.
Right fix: rung 2. Inject current API docs into task context at
execution time. Training-data defaults override prompt instructions,
so ground the context; do not add machinery.
```

## Integration

This skill connects to:

- harness-engineering - Owns the control surfaces (locked, editable, append-only, human) that this skill's loops operate within; every self-improvement loop presupposes that boundary design
- evaluation - Owns the deterministic evaluators, regression suites, and quality gates that serve as the locked fitness signal
- advanced-evaluation - Owns judge design and bias mitigation when candidate scoring requires model judgment
- filesystem-context - Owns the durable file layout patterns the experience archive builds on
- multi-agent-patterns - Parallel candidate evaluation and proposer-verifier separation are multi-agent topologies
- hosted-agents - Owns the sandboxed execution infrastructure that enforces the runtime boundary
- context-optimization - Owns one-shot context efficiency; this skill owns the loop that evolves context mechanisms over time
- self-managed-context - Owns the self-editing behavior and its cost signal when the evolved artifact is a model's context-management skill or policy

