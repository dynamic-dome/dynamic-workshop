# CLAUDE.md — Workshop Playground

## Project

Demo repository for Claude Code workshop hands-on exercises and security audit demos.

## Conventions

- **Language**: English for code, variable names, comments. German for communication with participants.
- **Python version**: 3.10+
- **Test framework**: pytest
- **Error handling**: Prefer explicit error handling — no bare `except:` clauses. Always catch specific exceptions and provide meaningful error messages.
- **Logging**: Use the built-in `logging` module; do not use `print()` for operational output.

## Structure

```
workshop-playground/
├── access_control.py       # Main CLI application
├── test_access_control.py  # pytest test suite
├── requirements.txt        # Dependencies
├── users.json              # User database (auto-created)
└── logs/                   # Access log directory (auto-created)
```

## Running the App

```bash
python access_control.py --help
python access_control.py add alice
python access_control.py check alice
python access_control.py remove alice
python access_control.py backup users_backup.json
```

## Running Tests

```bash
pip install -r requirements.txt
pytest -v
```

## Workshop Notes

This repo contains **intentional vulnerabilities** for Block 3.3 Security Demo.
Do NOT use this code in production.

## Intentional Vulnerabilities (for Block 3.3 Demos)

This playground contains three deliberately planted vulnerabilities used in workshop demos and exercises:

1. **Command Injection** — `backup_database()` in `access_control.py:~140`
   - `subprocess.run(f"cp {DB_FILE} {filename}", shell=True)` with unvalidated CLI input
   - Demo: Adversarial swarm should find this

2. **Hardcoded Credentials** — `ADMIN_PASSWORD = "admin123"` on `access_control.py:19`
   - Used at module scope, easy to grep but unused in flow (intentional for demo discoverability)

3. **Path Traversal** — `read_log()` in `access_control.py:~127`
   - `open(f"logs/{log_name}")` with unvalidated CLI input from `read-log` command

Plus a bonus ungeplante issue:

4. **Log-Injection / Log-Forging** — `log_event()` in `access_control.py:105-113`
   - Writes `username` and `action` unfiltered into log file
   - Newline-injection can create forged log lines

And one **domain-logic** vulnerability that a pattern scanner will *not* trivially find:

5. **Fail-OPEN access check** — `check_access_resilient()` in `access_control.py`
   - When `users.json` is missing or corrupt, it returns `True` (ACCESS GRANTED) instead of failing secure
   - No injection / no secret / no traversal — only a physical-security reviewer spots it. Reachable via the `door-check` subcommand: `python access_control.py door-check eve` grants access with no database present.
   - Teaching point: **fail-secure vs. fail-open** — contrast it with `check_access()` / `load_db()`, which deny on error. This is the *scanner vs. domain expertise* lesson of Exercise 3.3.

These vulnerabilities are scoped to live demos. Do NOT fix them in this playground — they are the teaching target.

### Windows Note

`backup_database()` uses Unix `cp` command. On Windows workshop machines, run live demos from Git Bash or WSL.

## OSDP Frame Decoder (C) — Embedded Domain Playground

`osdp_frame_decoder.c` is a second playground specifically for Embedded / Physical Security
contexts. It simulates an OSDP (Open Supervised Device Protocol) frame decoder — the kind
of code you'd find on a real access-control panel.

### Intentional Vulnerabilities (do NOT fix)

| # | Vulnerability | Location | Why it matters |
|---:|---|---|---|
| 1 | Buffer Overflow | `decode_data_payload()` | Classic embedded vuln — unvalidated `length` field from wire data |
| 2 | Integer Overflow | `compute_crc()` | `byte_count` computed in `uint8_t` wraps for large `length` → CRC over the wrong bounds |
| 3 | Format String | `log_frame()` | Attacker-controlled `cmd_name` as format string |
| 4 | Off-by-one (bonus) | `read_frame_crc()` | Reads the CRC one byte past the frame end |

> **Frame-format note:** the struct uses a simplified single-byte teaching layout. Real OSDP
> (SIA OSDP v2.2 / IEC 60839-11-5) puts ADDR before a **16-bit little-endian** LEN and uses a
> **CRC-16/CCITT** trailer — see the header comment in the source. Locations are referenced by
> **function name** (not line number) so the targets survive future edits.
>
> **Note (not a vuln):** `main()`'s hex parser was hardened against an unplanned `size_t`
> underflow on empty/odd-length input. The four teaching vulns above are unchanged.

### Build & Test

**The Block 3.3 demo does not need a compiler.** The Devil's-Advocate swarm reviews the
C **source** (`osdp_frame_decoder.c`) directly — no build or static-analysis run is
required to demonstrate the vulnerability patterns. This is the recommended path on a
typical **Windows** workshop machine, where `gcc`/`clang`/`scan-build` are usually absent.

The build targets below are **optional** and assume a POSIX toolchain (macOS/Linux, or
Windows via WSL / MSYS2-mingw + `clang-tools-extra`):

```bash
cd workshop-playground/
make                  # Build (needs gcc)
make static-check     # Static analysis (needs clang)
make scan-build       # Deeper static analysis (needs scan-build, if installed)
```

> On Windows without WSL/MSYS2: skip `make` entirely and run the swarm against the source
> file — `make static-check` will fail with "command not found" and that is expected.

### Use in Demos

- **Block 3.3 Demo (Devil's Advocate Swarm):** Run swarm against `osdp_frame_decoder.c`
  alongside `access_control.py`. Compare findings on C-code vs Python-code patterns.
- **Block 3.7 Demo (Troubleshooting):** Use static-analysis output as input for /debug
  conversations.

### Cross-Compile Note

For real Embedded targets, add `make cortex-m` (requires `arm-none-eabi-gcc` toolchain).
The workshop-playground does not require cross-compilation to demonstrate the patterns.
