#!/usr/bin/env python3
"""
check_context_budget.py — Validador de Presupuesto de Contexto (ICM Invariante 7).

Verifica que ningún archivo de contrato o especificación supere el límite
saludable de 8.000 tokens (estimación: ~4 caracteres por token).
"""

import sys
from pathlib import Path

MAX_TOKENS = 8000
CHARS_PER_TOKEN = 4  # Heurística estándar para texto y markdown


def estimate_tokens(text: str) -> int:
    return len(text) // CHARS_PER_TOKEN


def main():
    project_root = Path(__file__).resolve().parent.parent
    context_patterns = [
        "AGENTS.md",
        "CLAUDE.md",
        "CONTEXT.md",
        "_context/**/*.md",
        "research/**/*.md"
    ]

    files_checked = 0
    violations = []

    print(f"🔍 Evaluando presupuesto de contexto en: {project_root.name} (Límite: {MAX_TOKENS:,} tokens)")
    print("─" * 70)

    for pattern in context_patterns:
        for file_path in project_root.glob(pattern):
            if file_path.is_file():
                try:
                    content = file_path.read_text(encoding="utf-8")
                    tokens = estimate_tokens(content)
                    files_checked += 1
                    status = "✅ OK"
                    if tokens > MAX_TOKENS:
                        status = "❌ EXCEDIDO"
                        violations.append((file_path.relative_to(project_root), tokens))

                    rel_path = file_path.relative_to(project_root)
                    print(f" {status} | {tokens:5,d} tokens | {rel_path}")
                except Exception as e:
                    print(f" ⚠️ Error leyendo {file_path}: {e}")

    print("─" * 70)
    print(f"Total de archivos evaluados: {files_checked}")

    if violations:
        print(f"\n🚨 Se detectaron {len(violations)} violaciones del presupuesto de contexto (ICM Invariante 7):")
        for path, tokens in violations:
            print(f"   • {path}: {tokens:,} tokens (Máximo permitido: {MAX_TOKENS:,})")
        print("\nSugerencia: Divide el archivo en subetapas o mueve detalles a referencias secundarias.")
        sys.exit(1)
    else:
        print("\n🎉 Todos los archivos respetan la disciplina de contexto (< 8.000 tokens).")
        sys.exit(0)


if __name__ == "__main__":
    main()
