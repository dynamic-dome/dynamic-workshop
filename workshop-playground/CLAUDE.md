# CLAUDE.md — Workshop Playground

## Project

Practice repository of the Claude Code Praxisbibliothek: a small access-control CLI in Python and a simplified OSDP
frame decoder in C. It exists to be read, reviewed and changed in exercises. It is not production code.

## Conventions

- **Language**: English for code, variable names and comments.
- **Python version**: 3.10+
- **Test framework**: pytest
- **Error handling**: Prefer explicit error handling — no bare `except:` clauses. Always catch specific exceptions and provide meaningful error messages.
- **Logging**: Use the built-in `logging` module; do not use `print()` for operational output.
- **Changes**: Work on a branch of your own or in a worktree. Do not commit to `main`: other exercises start from the
  state that is there.

## Structure

```
workshop-playground/
├── access_control.py       # Main CLI application
├── test_access_control.py  # pytest test suite
├── osdp_frame_decoder.c    # Simplified OSDP frame decoder (C)
├── Makefile                # Optional build and static analysis for the C file
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

The `backup` subcommand needs a POSIX shell. On Windows, run it from Git Bash or WSL.

## Running Tests

```bash
pip install -r requirements.txt
pytest -v
```

## OSDP Frame Decoder (C)

`osdp_frame_decoder.c` simulates an OSDP (Open Supervised Device Protocol) frame decoder, the kind of code found on
an access-control panel. The struct uses a simplified single-byte layout; real OSDP (SIA OSDP v2.2 /
IEC 60839-11-5) puts ADDR before a 16-bit little-endian LEN and uses a CRC-16/CCITT trailer. The header comment of
the source says so too.

Reading and reviewing the source needs no compiler. The build targets are optional and assume a POSIX toolchain
(macOS/Linux, or Windows via WSL / MSYS2-mingw + `clang-tools-extra`):

```bash
make                  # Build (needs gcc)
make static-check     # Static analysis (needs clang)
make scan-build       # Deeper static analysis (needs scan-build, if installed)
```

On Windows without WSL/MSYS2, skip `make`; `make static-check` then fails with "command not found", which is expected.
