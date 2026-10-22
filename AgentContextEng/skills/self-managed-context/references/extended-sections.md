# self-managed-context: secciones ampliadas

Secciones movidas desde SKILL.md para no superar los 20.000 caracteres.

## References

Internal references:
- [Harness protocol](./harness-protocol.md) - Read when: implementing the mirror file, parse-back, edit gate, budget controller, rollback, ICL gate, RL advantage, or SCR configuration
- [Evidence](./evidence.md) - Read when: citing benchmark numbers, comparing baselines, or checking limitations and release scope

Related skills in this collection:
- context-compression - Read when: designing the content of replacement notes
- context-optimization - Read when: the harness, not the model, controls the context
- self-improvement-loops - Read when: wrapping strategy evolution or RL in acceptance gates and archives

External resources:
- Paper: [Context Language Models](https://arxiv.org/abs/2609.37725)
- Code: [facebookresearch/context-language-models](https://github.com/facebookresearch/context-language-models)
- Safety report: [Self-generated prompt injections in compaction summaries](https://alignment.openai.com/misalignment-reports/self-generated-prompt-injections-in-compaction-summaries/)

---

## Examples

**Example 1: Harness step with invariants outside the editable region**

```python
def step(messages, command, budget, gate="fit", protect=2):
    prefix = messages[:protect]                        # system + task, never rendered
    rendered = render_editable(messages, protect)      # [[CTX_TURN n role=...]] blocks
    write_file(MIRROR, rendered)
    result = run_shell(command)                        # model edits MIRROR with code tools
    edited = read_file(MIRROR)

    applied = False
    receipt = ""
    if edited.strip() != rendered.strip():
        candidate = parse_back(edited, prefix)         # non-assistant roles fold to user
        baseline = count(parse_back(rendered, prefix)) # same ruler: round-tripped original
        grew = count(candidate) > baseline
        if grew and not (gate == "fit" and count(candidate) <= budget):
            receipt = f"context: edit REJECTED ({gate} rule)"
        else:
            messages, applied = candidate, True
            receipt = ("context: edit applied but GREW; replace, do not duplicate"
                       if grew else "context: edit applied")
    elif MIRROR in command:                            # targeted the file, changed nothing
        receipt = (f"context: NO change (exit {result.code})" if result.code
                   else "context: NO change; edit matched nothing, target [[CTX_TURN n role=...]]")

    free_turn = applied and result.output == "" and result.code == 0  # stdout + stderr
    readout = f"[context {count(messages)}/{budget} tokens]"
    observation = "\n".join(part for part in (result.output, receipt, readout) if part)
    return messages + [tool_message(observation)], free_turn
```

**Example 2: A cheap, model-issued edit**

The agent collapses three settled search turns in one batch, replaces them with a generous note that copies forward ruled-out candidates and exact values, and prints nothing so the turn is free.

```bash
python3 - <<'PY'
import re
p = "/tmp/.live_ctx/LIVE_CTX_MAIN.txt"
s = open(p).read()
note = ("[notes] RULED OUT: v2.1 tag (no changelog entry), do not retry. "
        "TRIED: grep -rn 'retry_policy' src/ ; git log -S backoff. "
        "VERIFIED: backoff cap set in src/net/client.py:88. NEXT: read client tests.")
s = re.sub(r"\[\[CTX_TURN 4 [^\]]*\]\].*?(?=\n\[\[CTX_TURN 7 )",
           "[[CTX_TURN 4 role=assistant]]\n" + note + "\n", s, flags=re.S)
open(p, "w").write(s)
PY
```

**Example 3: Success-gated efficiency advantage**

```python
def efficiency_advantage(group):
    winners = [t for t in group if t.success]
    if len(winners) < 2:
        return {t.id: 0.0 for t in group}
    mean_cost = sum(t.prefix_reuse_flops for t in winners) / len(winners)
    return {
        t.id: clip((mean_cost - t.prefix_reuse_flops) / mean_cost, -1, 1) if t.success else 0.0
        for t in group
    }

# per-token advantage: outcome everywhere, efficiency only on context-edit tokens
# A[i, t] = outcome_advantage[i] + w_eff * efficiency_advantage[i] * edit_mask[i][t]
```

## Integration

This skill connects to:

- context-compression - Supplies what a good replacement note preserves; this skill decides who triggers it and where it lands in the context
- context-optimization - Owns cache-stable layout and masking under harness control; this skill adds the cost of model-initiated mid-context edits
- filesystem-context - Offloading to files is half of eviction; this skill covers removing the original from the live window
- context-degradation - Explains why bloated or stale context hurts; self-management is one response the model controls
- harness-engineering - The pinned prefix, edit gate, and rollback are locked harness surfaces under this design
- self-improvement-loops - Governs the evolution loop and acceptance gates when the context-editing skill is optimized
- multi-agent-patterns - Subagent and swarm designs where each agent manages its own context file
- latent-briefing - The latent alternative: compacting KV state passed between agents instead of editing text

## Guidelines

1. Keep the system prompt and task pinned outside the editable region and re-pin them from originals on every parse.
2. Fold every model-written role except `assistant` to `user`; never parse a `system` header into system authority.
3. Return a receipt whenever a command changes or targets the context file, including no-match, failed, and rejected edits.
4. Do not charge task steps for pure edit turns.
5. Supply a deterministic token readout on every result; never rely on the model's own estimate.
6. Keep low-fill nudges informational; reserve how-to instructions for mid and high fill.
7. Size the urgent warning band from recent tool output sizes.
8. Price edits by the text that follows them; batch edits and avoid compacting a small head under a large useful tail.
9. Measure prefix-reuse compute, not context length, and report it beside accuracy.
10. In any optimization of strategy, let cost re-rank only successful attempts and restrict efficiency credit to edit tokens.

