<!-- CANONICAL SOURCE OF TRUTH — do not teach anything that contradicts this file.
     Enforced by tools/lint_currency.py (fails on any forbidden legacy token in live content).
     Stand: 2026-07-04. -->

# Canonical Registry — Dynamic Workshop

## Current Claude models (as of 2026-07)

| Modell | Model-ID (kanonisch) | Kontext | In $/1M | Out $/1M | Rolle im Workshop |
|---|---|---|---|---|---|
| Claude Fable 5 | `claude-fable-5` | 1M | 10 | 50 | Premium/Mythos-Tier — härtestes, langlaufendes Reasoning |
| Claude Opus 4.8 | `claude-opus-4-8` | 1M | 5 | 25 | **Aktueller Default in Claude Code**; Architektur, tiefes Reasoning; Effort-Default `high` |
| Claude Sonnet 5 | `claude-sonnet-5` | 1M | 3 | 15 | Schnelles Standard-Coding, Alltag; erste Sonnet-Gen mit `xhigh`/`max` |
| Claude Haiku 4.5 | `claude-haiku-4-5` (voll: `claude-haiku-4-5-20251001`) | 200K | 1 | 5 | Bulk-Reads, einfache Suchen, Routine-Reviews |

- Tier-Aliase `opus` / `sonnet` / `haiku` / `fable` lösen automatisch auf die aktuelle Generation auf — bevorzugt in `model:`-Feldern verwenden, damit sie nicht driften.
- Effort-Tiers `low|medium|high|xhigh|max`. `xhigh`/`max` verfügbar auf **Opus 4.8, Sonnet 5, Fable 5** (nicht Haiku 4.5). Opus 4.8 defaultet auf `high`.
- Sonnet 5 Einführungspreis 2/10 bis 2026-08-31, danach 3/15 (Tabellen zeigen den Standardpreis).
- Immer `claude --version` / `/release-notes` / `/model` über jede hier gedruckte Zahl stellen.

## Struktur

- **4 Sessions / 65 Lerneinheiten (LE)** — Welle-F-Restrukturierung (`session-plan.md` ist die Ablauf-SSoT).
- Session 1 = Block 1 (Foundations, S1.1–S1.20). Session 2 = Block 2 (Ecosystem, S2.1–S2.20).
  Session 3 = Block 3 Advanced Kern (S3.1–S3.15). Session 4 = Block 3 Advanced Bonus (S4.1–S4.10).
- 17 Module (5+5+7) über 3 Blöcke bleiben die Volltext-Quelle; die 65-LE-Landkarte ist die Navigations-Schicht darüber.

## Forbidden legacy tokens (Lint blockt diese in Live-Content)

Diese bezeichnen Vorgänger-/retired Generationen und dürfen **nicht** als aktuelles Modell gelehrt werden
(Lint matcht case-insensitiv). Historische Referenzen ("früher X", Changelog) sind in `docs/` und
`resources/review-*/` erlaubt (Lint klammert sie aus).

```
claude-sonnet-4-6      (bzw. "Sonnet 4.6" / "sonnet-4.6")
claude-opus-4-7
claude-3-5-sonnet · claude-3-7-sonnet · claude-3-5-haiku   (retired)
```

<!-- LINT-FORBIDDEN: claude-sonnet-4-6 | sonnet 4.6 | claude-opus-4-7 | claude-3-5-sonnet | claude-3-7-sonnet | claude-3-5-haiku -->
