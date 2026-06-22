"""
Access Control Management Tool
Workshop demo application — contains intentional vulnerabilities for security audit exercise.
DO NOT use in production.
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ------------------------------------------------------------------ #
# VULNERABILITY 1: Hardcoded credential                              #
# ------------------------------------------------------------------ #
ADMIN_PASSWORD = "admin123"  # hardcoded secret — should use env var or secrets manager

DB_FILE = "users.json"
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "access.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def load_db() -> dict:
    """Load the user database from disk. Returns empty structure if missing."""
    if not os.path.exists(DB_FILE):
        return {"users": []}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        logger.error("Failed to load database: %s", exc)
        return {"users": []}


def save_db(data: dict) -> None:
    """Persist the user database to disk."""
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except OSError as exc:
        logger.error("Failed to save database: %s", exc)
        raise


# ---------------------------------------------------------------------------
# Core access-control logic
# ---------------------------------------------------------------------------

def add_user(username: str) -> bool:
    """Add a user to the access list. Returns True if added, False if already exists."""
    db = load_db()
    if username in db["users"]:
        logger.info("User '%s' already exists.", username)
        return False
    db["users"].append(username)
    save_db(db)
    log_event("ADD", username, success=True)
    logger.info("User '%s' added.", username)
    return True


def remove_user(username: str) -> bool:
    """Remove a user from the access list. Returns True if removed, False if not found."""
    db = load_db()
    if username not in db["users"]:
        logger.info("User '%s' not found.", username)
        return False
    db["users"].remove(username)
    save_db(db)
    log_event("REMOVE", username, success=True)
    logger.info("User '%s' removed.", username)
    return True


def check_access(username: str) -> bool:
    """Return True if the user is on the access list."""
    db = load_db()
    result = username in db["users"]
    log_event("CHECK", username, success=result)
    return result


# ------------------------------------------------------------------ #
# VULNERABILITY 5 (domain logic): Fail-OPEN access check             #
# A pattern scanner won't flag this — there's no injection, no        #
# hardcoded secret, no path traversal. It is a LOGIC flaw only a      #
# physical-security reviewer catches: when the user database is       #
# missing or corrupt, this "resilient" check GRANTS access            #
# (fail-OPEN) so the door "keeps working" during an outage. The       #
# correct behavior for access control is fail-SECURE — DENY on any    #
# error. On a real panel, a corrupted users.json would unlock every   #
# door. Contrast with check_access()/load_db(), which fail secure.    #
# ------------------------------------------------------------------ #
def check_access_resilient(username: str) -> bool:
    """
    'Resilient' door check used by the panel's online path.
    VULNERABILITY (fail-open): returns True (ACCESS GRANTED) when the database
    is missing or unreadable, instead of failing secure (ACCESS DENIED).
    """
    if not os.path.exists(DB_FILE):
        return True  # fail-open: "don't lock people out if the DB is gone" (WRONG)
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
    except (json.JSONDecodeError, OSError):
        return True  # fail-open: grant on a corrupt DB (WRONG — should DENY)
    return username in db.get("users", [])


def list_users() -> list:
    """Return the current list of users."""
    return load_db().get("users", [])


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log_event(action: str, username: str, success: bool) -> None:
    """Append an access event to the log file."""
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.now().isoformat()
    status = "GRANTED" if success else "DENIED"
    entry = f"{timestamp} | {action} | {username} | {status}\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry)
    except OSError as exc:
        logger.warning("Could not write to log: %s", exc)


# ------------------------------------------------------------------ #
# VULNERABILITY 2: Path traversal in log reading                     #
# ------------------------------------------------------------------ #
def read_log(log_name: str) -> str:
    """
    Read a log file by name.
    VULNERABILITY: no path sanitization — path traversal is possible.
    e.g. log_name = '../../etc/passwd' would leak system files.
    """
    with open(f"logs/{log_name}") as f:  # no sanitization!
        return f.read()


# ------------------------------------------------------------------ #
# VULNERABILITY 3: Command injection in backup function              #
# ------------------------------------------------------------------ #
def backup_database(filename: str) -> None:
    """
    Create a backup copy of the database.
    VULNERABILITY: shell=True with unsanitized user input allows command injection.
    e.g. filename = 'backup.json; rm -rf /' would execute the second command.
    """
    subprocess.run(f"cp {DB_FILE} {filename}", shell=True)  # shell=True with user input!
    logger.info("Database backed up to '%s'.", filename)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Access Control Management Tool (Workshop Demo)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List all users with access")

    add_p = sub.add_parser("add", help="Grant access to a user")
    add_p.add_argument("username", help="Username to add")

    rem_p = sub.add_parser("remove", help="Revoke access from a user")
    rem_p.add_argument("username", help="Username to remove")

    chk_p = sub.add_parser("check", help="Check if a user has access")
    chk_p.add_argument("username", help="Username to check")

    bkp_p = sub.add_parser("backup", help="Backup the database")
    bkp_p.add_argument("filename", help="Destination filename")

    log_p = sub.add_parser("read-log", help="Read a log file")
    log_p.add_argument("log_name", help="Log filename (within logs/ directory)")

    door_p = sub.add_parser("door-check", help="Resilient door check (panel online path)")
    door_p.add_argument("username", help="Username to check at the door")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list":
        users = list_users()
        if users:
            print("Users with access:")
            for u in users:
                print(f"  - {u}")
        else:
            print("No users in access list.")

    elif args.command == "add":
        added = add_user(args.username)
        return 0 if added else 1

    elif args.command == "remove":
        removed = remove_user(args.username)
        return 0 if removed else 1

    elif args.command == "check":
        has_access = check_access(args.username)
        status = "ACCESS GRANTED" if has_access else "ACCESS DENIED"
        print(f"{args.username}: {status}")
        return 0 if has_access else 1

    elif args.command == "door-check":
        granted = check_access_resilient(args.username)
        status = "ACCESS GRANTED" if granted else "ACCESS DENIED"
        print(f"{args.username}: {status}")
        return 0 if granted else 1

    elif args.command == "backup":
        backup_database(args.filename)

    elif args.command == "read-log":
        try:
            content = read_log(args.log_name)
            print(content)
        except OSError as exc:
            logger.error("Cannot read log: %s", exc)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
