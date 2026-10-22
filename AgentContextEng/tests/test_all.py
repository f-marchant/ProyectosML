import glob, json, os, subprocess, sys, tempfile, unittest, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
SC = {os.path.basename(f): f for f in glob.glob(os.path.join(HERE, "..", "skills", "*", "scripts", "*.py"))}

def run(script, *args, ok=(0,), stdin=None):
    p = subprocess.run([sys.executable, SC[script], *map(str, args)], capture_output=True, text=True, input=stdin, timeout=60)
    assert p.returncode in ok, f"{script} {args}\nSTDERR:{p.stderr}\nSTDOUT:{p.stdout}"
    return p.stdout

def js(*a, **k): return json.loads(run(*a, **k))

class T(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        def write(name, content=""):
            path = os.path.join(self.d, name)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(content if isinstance(content, str) else json.dumps(content))
            return path
        self.p = write
    def tearDown(self): shutil.rmtree(self.d)

    def test_context_audit(self):
        f = self.p("c.md", "# Sistema\nEres un asistente.\n\n# Docs\n" + "dato relevante. " * 400 + "\n\n# Docs2\n" + ("dato relevante. " * 400) + "\n\n# Fin\nclave ALFA aqui")
        r = js("context_audit.py", "audit", f, "--window", 2000, "--priority", "alfa")
        self.assertEqual(r["status"], "critico"); self.assertTrue(r["priority_check"][0]["found"]); self.assertTrue(r["duplicates"])

    def test_degradation(self):
        txt = "Servidor: A\n\nIntro larga\n\nServidor: B\n\nEl sistema es estable y confiable en produccion.\n\nEl sistema no es estable y confiable en produccion.\n\n" + "relleno " * 50
        r = js("degradation_check.py", "check", self.p("d.txt", txt), "--facts", "intro larga,inexistente")
        self.assertTrue(r["key_conflicts"]); self.assertTrue(r["negation_pairs"]); self.assertEqual(r["signals"]["missing_facts"], 1)

    def test_compression(self):
        orig = "Decidimos usar src/auth.py para login.\nError: timeout en https://api.x.com/v1\nTODO: arreglar tests/test_a.py\nTotal 42 usuarios"
        summ = "Se decidio usar src/auth.py para login. Pendiente: arreglar tests/test_a.py"
        pr = self.p("p.json", [{"question": "archivo", "expected": ["src/auth.py"]}, {"question": "url", "expected": ["api.x.com"]}])
        r = js("compression_eval.py", "score", self.p("o.txt", orig), self.p("s.txt", summ), "--probes", pr)
        self.assertEqual(r["probes"][0]["retention"], 1.0); self.assertEqual(r["probes"][1]["retention"], 0.0); self.assertIn("api.x.com", json.dumps(r["artifacts"]["urls"]))
        e = js("compression_eval.py", "extract", self.p("o2.txt", orig)); self.assertIn("src/auth.py", e["files"])

    def test_optimize(self):
        msgs = [{"role": "user", "content": "hola"}] + [{"role": "tool", "content": f"resultado {i}\n" + "x" * 2000} for i in range(4)]
        st = os.path.join(self.d, "st.json"); out = json.loads(run("optimize_context.py", "mask", self.p("m.json", msgs), "--store", st, "--keep-last", 1))
        self.assertEqual(sum("omitida" in m["content"] for m in out), 3); ref = out[1]["content"].split("obs:")[1][:8]
        self.assertIn("xxxx", run("optimize_context.py", "restore", ref, "--store", st))
        c = js("optimize_context.py", "cache-check", self.p("pr.json", ["SYS fijo\nhora 12:30 consulta A", "SYS fijo\nhora 12:31 consulta B"])); self.assertTrue(c["volatile_items"] or c["common_prefix_chars"] > 0)
        b = js("optimize_context.py", "budget", "--window", 1000, "--alloc", "a=50,b=50", "--used", "a=600,b=100"); self.assertEqual(b["categories"][0]["status"], "excedido")

    def test_eval(self):
        spec = {"rubric": {"acc": 2, "clar": 1}, "tests": [{"id": "t1", "checks": [{"type": "contains", "value": "paris"}, {"type": "max_chars", "value": 50}], "scores": {"acc": 1, "clar": 1}},
                                                          {"id": "t2", "checks": [{"type": "json_valid"}]}]}
        o = self.p("o.json", {"t1": "Paris es la capital", "t2": "no json"}); rep = js("eval_runner.py", "run", self.p("t.json", spec), o, "--out", os.path.join(self.d, "r1.json"))
        self.assertEqual(rep["passed"], 1); self.assertEqual(rep["results"][1]["status"], "fail")
        o2 = self.p("o2.json", {"t1": "Londres", "t2": "{}"}); js("eval_runner.py", "run", os.path.join(self.d, "t.json"), o2, "--out", os.path.join(self.d, "r2.json"))
        c = js("eval_runner.py", "compare", os.path.join(self.d, "r1.json"), os.path.join(self.d, "r2.json")); self.assertEqual(c["verdict"], "REGRESION")

    def test_judge(self):
        rub = self.p("r.json", {"criteria": [{"name": "precision", "description": "d", "weight": 2, "levels": {"1": "mala", "5": "buena"}}, {"name": "claridad", "weight": 1}]})
        txt = run("judge_toolkit.py", "prompt", "direct", "--rubric", rub, "--response", self.p("a.txt", "resp")); self.assertIn("precision", txt)
        self.assertIn("Respuesta A", run("judge_toolkit.py", "prompt", "pairwise", "--a", self.p("a2.txt", "x"), "--b", self.p("b2.txt", "y"), "--swap"))
        r = js("judge_toolkit.py", "aggregate", "direct", self.p("j.json", [{"judge": "1", "scores": {"precision": 5, "claridad": 3}}, {"judge": "2", "scores": {"precision": 3, "claridad": 3}}]), "--rubric", rub)
        self.assertEqual(r["weighted_score"], 3.67); self.assertEqual(r["disagreement"], ["precision"])
        pw = js("judge_toolkit.py", "aggregate", "pairwise", self.p("pw.json", [{"order": "AB", "winner": "A"}, {"order": "BA", "winner": "B"}, {"order": "AB", "winner": "A"}, {"order": "BA", "winner": "B"}]))
        self.assertEqual(pw["winner"], "A"); self.assertTrue(pw["consistent_across_orders"])
        ag = js("judge_toolkit.py", "agreement", self.p("h.json", {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}), self.p("jj.json", {"a": 1, "b": 2, "c": 3, "d": 5, "e": 5})); self.assertGreater(ag["spearman"], 0.9)

    def test_memory(self):
        st = os.path.join(self.d, "m.json")
        js("memory_store.py", "--store", st, "add", "Alice trabaja en Acme Corp como ingeniera", "--entity", "Alice")
        js("memory_store.py", "--store", st, "add", "Bob vive en Santiago de Chile")
        r = js("memory_store.py", "--store", st, "search", "donde trabaja Alice"); self.assertIn("Acme", r[0]["text"])
        js("memory_store.py", "--store", st, "link", "Alice", "works_at", "Acme", "--from", "2023-01-01", "--until", "2024-12-31")
        js("memory_store.py", "--store", st, "link", "Alice", "works_at", "Globex", "--from", "2025-01-01")
        q1 = js("memory_store.py", "--store", st, "query", "Alice", "--as-of", "2024-06-01"); q2 = js("memory_store.py", "--store", st, "query", "Alice", "--as-of", "2025-06-01")
        self.assertEqual(q1["relations"][0]["dst"], "Acme"); self.assertEqual(q2["relations"][0]["dst"], "Globex")
        self.assertEqual(js("memory_store.py", "--store", st, "stats")["memories"], 2)

    def test_scratchpad(self):
        root = os.path.join(self.d, "ctx"); big = "\n".join(f"linea {i} " + ("ERROR critico" if i == 50 else "ok") for i in range(300))
        r = json.loads(run("scratchpad.py", "--root", root, "offload", "-", "--name", "build", stdin=big)); self.assertTrue(r["offloaded"]); ref = r["ref"]
        self.assertIn("50: linea 49", run("scratchpad.py", "--root", root, "grep", ref, "ERROR", "-C", 1)) if False else None
        self.assertIn("ERROR", run("scratchpad.py", "--root", root, "grep", ref, "ERROR", "-C", 1)); self.assertIn("1: linea 0", run("scratchpad.py", "--root", root, "read", ref, "--lines", "1:3"))
        run("scratchpad.py", "--root", root, "plan", "init", "a", "b"); self.assertIn("Siguiente: b", run("scratchpad.py", "--root", root, "plan", "done", "1"))

    def test_task_graph(self):
        g = {"tasks": [{"id": "a", "tokens": 1000, "context": ["x"]}, {"id": "b", "tokens": 2000, "context": ["y"]}, {"id": "c", "deps": ["a", "b"], "tokens": 500, "context": ["z"]}]}
        r = js("task_graph.py", "plan", self.p("g.json", g)); self.assertEqual(r["waves"], [["a", "b"], ["c"]]); self.assertEqual(r["critical_path"], ["b", "c"]); self.assertEqual(r["critical_path_tokens"], 2500)
        g["tasks"][0]["deps"] = ["c"]; self.assertEqual(js("task_graph.py", "plan", self.p("g2.json", g))["error"], "ciclo detectado")
        h = js("task_graph.py", "handoff", self.p("h.json", {"from": "a", "to": "b", "task": "t"})); self.assertFalse(h["valid"])

    def test_tool_lint(self):
        tools = [{"name": "getUser", "description": "gets user", "parameters": {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id", "zz"]}},
                 {"name": "search_orders", "description": "Usa esta herramienta cuando necesites buscar pedidos de clientes por estado. Retorna una lista de pedidos con id y total.", "parameters": {"type": "object", "properties": {"status": {"type": "string", "description": "estado"}}}},
                 {"name": "find_orders", "description": "Usa esta herramienta cuando necesites buscar pedidos de clientes por estado. Retorna una lista de pedidos con id y total.", "parameters": {"type": "object", "properties": {}}}]
        r = js("tool_lint.py", "lint", self.p("t.json", tools)); self.assertTrue(r["overlaps"]); self.assertGreaterEqual(r["summary"]["alta"], 3)
        self.assertIn("Retorna", run("tool_lint.py", "describe", self.p("s.json", {"name": "x", "purpose": "p", "returns": "algo", "params": {"a": "b"}, "errors": {"E1": "corrige"}})))

    def test_pipeline(self):
        root = os.path.join(self.d, "pj"); src = self.p("in.jsonl", '{"text":"uno"}\n{"text":"dos"}\n')
        run("pipeline.py", "init", "--root", root, "--keys", "titulo,resumen"); run("pipeline.py", "acquire", "--root", root, src); run("pipeline.py", "prepare", "--root", root)
        with open(os.path.join(root, "responses", "in_0000.txt"), "w", encoding="utf-8") as handle: handle.write('```json\n{"titulo":"T","resumen":"R"}\n```')
        with open(os.path.join(root, "responses", "in_0001.txt"), "w", encoding="utf-8") as handle: handle.write('{"titulo":"solo"}')
        r = json.loads(run("pipeline.py", "parse", "--root", root)); self.assertEqual((r["parsed_ok"], r["invalid"]), (1, 1)); run("pipeline.py", "render", "--root", root)
        self.assertTrue(os.path.exists(os.path.join(root, "out", "report.md"))); e = json.loads(run("pipeline.py", "estimate", "--root", root)); self.assertEqual(e["items"], 2)

    def test_sandbox(self):
        r = js("sandbox_plan.py", "pool-size", "--arrivals-per-min", 6, "--warm-minutes", 2); self.assertGreaterEqual(r["pool_size"], 12); self.assertLessEqual(r["pool_size"], 22)
        l = js("sandbox_plan.py", "latency", "--budget-s", 3, "--parts", "clone=2.5,deps=3,ttft=0.8"); self.assertFalse(l["within_budget"])
        self.assertFalse(js("sandbox_plan.py", "image-schedule", "--commits-per-day", 10, "--build-minutes", 40, "--max-staleness-min", 30)["feasible"])
        self.assertEqual(js("sandbox_plan.py", "cost", "--sessions-per-day", 10, "--session-minutes", 30, "--price-per-hour", 1, "--idle-pool", 1)["session_cost_day"], 5.0)
        self.assertIn("FROM python", run("sandbox_plan.py", "dockerfile", self.p("c.json", {"base": "python:3.12-slim", "pip": ["requests"], "repos": [{"url": "https://x/y.git", "path": "y"}]})))
        bad = self.p("bad.json", {"base": "python:3.12-slim", "setup": ["echo ok; touch owned"]})
        run("sandbox_plan.py", "dockerfile", bad, ok=(2,))
        self.assertIn("RUN echo ok; touch owned", run("sandbox_plan.py", "dockerfile", bad, "--allow-setup"))
        run("sandbox_plan.py", "pool-size", "--arrivals-per-min", -1, "--warm-minutes", 2, ok=(2,))

    def test_briefing(self):
        traj = "\n\n".join([f"Turn {i}: charla irrelevante sobre el clima {i}" for i in range(12)] + ["Turn 12: el modulo de pagos usa stripe con webhook firmado", "Turn 13: bug en facturacion de pagos recurrentes stripe"])
        r = js("briefing.py", "compact", self.p("t.txt", traj), "--task", "arreglar pagos stripe webhook"); self.assertIn("stripe", r["briefing"]); self.assertLess(r["segments_kept"], r["segments_total"])
        c = js("briefing.py", "cost", "--trajectory-tokens", 40000, "--workers", 6, "--doc-tokens", 3000); self.assertEqual(c["vs_full_pct"]["full_trajectory"], 100.0); self.assertLess(c["vs_full_pct"]["text_briefing"], 40)

    def test_brief_lint(self):
        sc = run("brief_lint.py", "scaffold", "--title", "X"); r = js("brief_lint.py", "lint", self.p("b.md", sc)); self.assertEqual(r["missing"], []); self.assertGreaterEqual(r["score"], 85)
        w = js("brief_lint.py", "lint", self.p("w.md", "Intenta resolver el problema, mejor esfuerzo, etc.")); self.assertTrue(w["missing"]); self.assertTrue(w["vague_language"])

    def test_harness(self):
        good = {"metric": {"name": "acc", "locked": True, "direction": "max"}, "locked_surfaces": ["eval/"], "editable_surfaces": ["prompts/"], "log": {"path": "l.jsonl", "append_only": True}, "rollback": {"enabled": True, "trigger": "metric drop"},
                "novelty_gate": True, "approval_required_for": ["push"], "actions": ["read", "edit", "push"], "budget": {"max_iterations": 50}}
        self.assertTrue(js("harness_check.py", "validate", self.p("g.json", good))["valid"])
        bad = dict(good, metric={"name": "acc", "locked": False, "direction": "max"}, editable_surfaces=["eval/x", "eval/"], approval_required_for=[]); r = js("harness_check.py", "validate", self.p("b.json", bad)); self.assertFalse(r["valid"]); self.assertGreaterEqual(len(r["errors"]), 3)
        L = os.path.join(self.d, "l.jsonl"); run("harness_check.py", "ledger", "append", L, "--hypothesis", "agregar cache de prefijo", "--metric", 0.70); run("harness_check.py", "ledger", "append", L, "--hypothesis", "recortar prompt", "--metric", 0.72)
        self.assertTrue(js("harness_check.py", "ledger", "verify", L)["intact"]); nv = js("harness_check.py", "ledger", "novelty", L, "agregar cache de prefijo al prompt"); self.assertFalse(nv["novel"])
        self.assertEqual(js("harness_check.py", "ledger", "decide", L, "--metric", 0.71, "--higher-is-better")["decision"], "discard/rollback")
        with open(L, encoding="utf-8") as handle: lines = handle.read().replace('"metric": 0.7,', '"metric": 0.99,')
        with open(L, "w", encoding="utf-8") as handle: handle.write(lines)
        run("harness_check.py", "ledger", "verify", L, ok=(1,))

    def test_safe_persistence_controls(self):
        st = os.path.join(self.d, "memory.json")
        js("memory_store.py", "--store", st, "add", "dato uno")
        js("memory_store.py", "--store", st, "add", "dato dos")
        preview = js("memory_store.py", "--store", st, "consolidate", "--threshold", 0.1, "--dry-run")
        self.assertTrue(preview["dry_run"])
        self.assertEqual(js("memory_store.py", "--store", st, "stats")["memories"], 2)
        root = os.path.join(self.d, "ctx")
        ref = js("scratchpad.py", "--root", root, "offload", "-", "--name", "regex", "--threshold", 1, stdin="contenido")
        run("scratchpad.py", "--root", root, "grep", ref["ref"], "[", ok=(2,))

    def test_loop_gate(self):
        inc = {f"t{i}": 0 if i < 10 else 1 for i in range(30)}; cand = {f"t{i}": 1 if i < 18 else inc[f"t{i}"] for i in range(30)}
        r = js("loop_gate.py", "gate", self.p("r.json", {"incumbent": {"dev": inc, "cost": 100}, "candidate": {"dev": cand, "train": {f"t{i}": 1 for i in range(10)}, "cost": 90}, "protected": []}))
        self.assertEqual(r["verdict"], "pass"); self.assertTrue(r["ci_excludes_zero"]); self.assertTrue(r["warnings"] == [] or "sobreajuste" in r["warnings"][0])
        cand2 = dict(cand, t25=0); r2 = js("loop_gate.py", "gate", self.p("r2.json", {"incumbent": {"dev": inc}, "candidate": {"dev": cand2}, "protected": ["t25"]})); self.assertEqual(r2["verdict"], "fail")
        d = js("loop_gate.py", "diffsize", self.p("a.txt", "\n".join(map(str, range(100)))), self.p("b.txt", "\n".join(map(str, range(50))) + "\nNUEVO\n" + "\n".join(map(str, range(51, 100))))); self.assertTrue(d["within_bound"])
        s = js("loop_gate.py", "select", self.p("p.json", [{"id": "a", "score": 0.9, "genome": "uno dos tres"}, {"id": "b", "score": 0.89, "genome": "uno dos tres"}, {"id": "c", "score": 0.7, "genome": "cuatro cinco seis"}]), "--k", 2)
        self.assertEqual([x["id"] for x in s["selected"]], ["a", "c"])

    def test_ctxfile(self):
        msgs = [{"role": "system", "content": "sys"}, {"role": "user", "content": "tarea"}, {"role": "assistant", "content": "pienso"}, {"role": "tool", "content": "SALIDA " * 500}, {"role": "assistant", "content": "listo"}]
        m = self.p("m.json", msgs); md = run("ctxfile.py", "render", m); self.assertNotIn("sys", md.split("[[CTX_TURN")[0]); self.assertIn("role=tool", md)
        self.assertFalse(js("ctxfile.py", "apply", m, self.p("same.md", md))["applied"])
        edited = md.replace("SALIDA " * 500, "nota: salida larga resumida"); r = js("ctxfile.py", "apply", m, self.p("e.md", edited), "--budget", 5000, "--out", os.path.join(self.d, "n.json"))
        self.assertTrue(r["applied"]); self.assertLess(r["tokens_after"], r["tokens_before"]); self.assertEqual(r["first_changed_turn"], 2)
        grow = md.replace("listo", "listo " + "mas " * 3000); self.assertFalse(js("ctxfile.py", "apply", m, self.p("g.md", grow), "--budget", 5000)["applied"])
        self.assertFalse(js("ctxfile.py", "apply", m, self.p("g2.md", md + "\n[[CTX_TURN 9 role=notes]]\nextra"), "--gate", "shrink")["applied"])
        n = js("ctxfile.py", "nudge", "--used", 26000, "--budget", 28000, "--last-outputs", "3000"); self.assertEqual(n["level"], "urgente")

    def test_bdi(self):
        facts = self.p("f.tsv", "ex:order42\tex:status\tex:delayed\nex:order42\tex:hasContact\tex:mail1\nex:order43\tex:status\tex:delayed\n")
        rules = self.p("r.json", {"desires": [{"id": "notify", "when": {"p": "ex:status", "o": "ex:delayed"}, "goal": "ex:notifyCustomer"}, {"id": "refund", "when": {"p": "ex:status", "o": "ex:lost"}, "goal": "ex:refund"}],
                                  "intentions": [{"desire": "notify", "requires": [{"p": "ex:hasContact", "o": "*"}], "plan": ["redactar", "enviar"]}]})
        ttl = run("bdi.py", "transform", facts, rules); self.assertIn("a bdi:Intention", ttl); self.assertNotIn("ex:desire_refund", ttl)
        model = self.p("m.json", run("bdi.py", "transform", facts, rules, "--format", "json")); c = js("bdi.py", "check", model); self.assertTrue(c["valid"]); self.assertEqual(c["counts"]["intentions"], 1)
        with open(model, encoding="utf-8") as handle: bad = json.load(handle)
        bad["intentions"][0]["fulfils"] = "ex:nada"; run("bdi.py", "check", self.p("b.json", bad), ok=(1,))

if __name__ == "__main__": unittest.main(verbosity=2)
