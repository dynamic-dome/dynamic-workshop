# Security Analogies — Workshop Reference

> Zentrale Sammlung aller Physical-Security-Analogien, die im Workshop verwendet werden.
> Diese Datei ist die Source-of-Truth. Andere Workshop-Dokumente referenzieren sie.

## Mapping Tabelle

| Claude Code Concept | Physical Security Analogy | Why |
|---|---|---|
| **claude.ai (Web Chat)** | Security consultant on the phone | Advice without physical access |
| **Claude Code CLI** | Consultant with badge access | Operates in environment, real effects |
| **CLAUDE.md** | Site access policy / standing orders | Read at every shift start |
| **Auto-Memory** | Patrol log auto-recording | Captures observations without explicit ask |
| **.claude/rules/** | Zone-specific security policies | Different rules per area |
| **Context Window** | Control room with limited monitors | Active info on screens, old archives |
| **Skill** | Standard Operating Procedure (SOP) | Reusable instructions |
| **Command** | Alarm button | Trigger that fires the SOP |
| **Hook** | Access control sensor / alarm sensor | Fires automatically on event |
| **PreToolUse hook** | Card reader check | Can block before action |
| **PostToolUse hook** | Door-open log | Reacts after the fact |
| **Plugin** | Security module | Self-contained bundle (sensors + logic + procedures) |
| **MCP** | Integrated building management | Many systems wired into one console |
| **RAG (NotebookLM)** | Building blueprints | Project-specific knowledge, not generic |
| **Subagent** | Patrol team member | Specialist with their own context |
| **Agent Teams** | Patrol roster | Multiple coordinated agents |
| **Permission Modes** | Card-access clearance levels | Visitor vs maintenance vs master |
| **Protected Paths** | Vault rooms (uncrackable) | Hardcoded even with master key |
| **Worktree** | Test bench / replica setup | Isolated from production system |
| **Sandboxing** | Air-gapped test environment | Limited blast radius |
| **Codex Swarm** | External contractor team | Different vendor, different visibility |
| **Devil's Advocate Swarm** | Adversarial pentest team | Argues against your implementation |
| **/security-review** | Routine security audit | Built-in scheduled check |
| **/ultrareview** | Independent third-party audit | Cloud-based, broader scope |
| **Circuit Breaker (hook pattern)** | Deadman switch in alarm system | Stops runaway processes |
| **Background Agent** | Patrol shift schedule | See/attach/stop active patrols |
| **Effort Level** | Specialist skill level | Junior/Senior/Expert hour rates |
| **Channels (MCP push)** | Radio dispatch to patrols | External events into live session |
| **Telegram Bridge (custom)** | Group chat for ops center | Multi-operator coordination |
| **Remote Control / Teleport** | Phone-based remote ops control | Solo operator, mobile |

---

## Wie nutzen?

Dieses File ist **Single Source of Truth**. Wenn du im Workshop eine neue Analogie ergänzen willst:

1. Hier eintragen
2. In den Modulen/Demos NICHT eine eigene Version anlegen — stattdessen verlinken (`siehe security-analogies.md`)

In den Workshop-Files verlinken statt duplizieren:
- `resources/cheatsheet.md`
- `agents/workshop-mentor.md`
- `skills/workshop/SKILL.md`

---

*Stand: 2026-05-20*
