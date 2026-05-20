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

These vulnerabilities are scoped to live demos. Do NOT fix them in this playground — they are the teaching target.

### Windows Note

`backup_database()` uses Unix `cp` command. On Windows workshop machines, run live demos from Git Bash or WSL.
