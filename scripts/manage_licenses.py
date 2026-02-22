#!/usr/bin/env python3
"""CLI tool to manage enterprise license keys.

Usage:
    python scripts/manage_licenses.py generate [--count N] [--label LABEL]
    python scripts/manage_licenses.py list
    python scripts/manage_licenses.py revoke KEY
    python scripts/manage_licenses.py grant-email EMAIL

Requires the app database to exist (run the server at least once first).
"""

import argparse
import secrets
import sqlite3
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "mycontext.db"


def get_conn():
    if not DB_PATH.exists():
        print(f"ERROR: Database not found at {DB_PATH}")
        print("Start the server at least once to create it.")
        sys.exit(1)
    return sqlite3.connect(str(DB_PATH))


def generate_key():
    """Generate a cryptographically random license key."""
    return f"MC-ENT-{secrets.token_hex(16).upper()}"


def cmd_generate(args):
    conn = get_conn()
    cur = conn.cursor()
    keys = []
    for _ in range(args.count):
        key_id = str(uuid.uuid4())
        key_val = generate_key()
        label = args.label or None
        cur.execute(
            "INSERT INTO license_keys (id, key, label, is_valid, created_at) "
            "VALUES (?, ?, ?, 1, ?)",
            (key_id, key_val, label, datetime.now(UTC).isoformat()),
        )
        keys.append(key_val)
    conn.commit()
    conn.close()

    print(f"Generated {args.count} license key(s):\n")
    for k in keys:
        print(f"  {k}")
    print("\nShare these with customers. Each key can be redeemed once.")


def cmd_list(args):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT key, label, is_valid, redeemed_by, created_at, redeemed_at "
        "FROM license_keys ORDER BY created_at DESC"
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No license keys found.")
        return

    fmt = "{:<45} {:<20} {:<15} {:<38} {:<22}"
    print(fmt.format("KEY", "LABEL", "STATUS", "REDEEMED BY", "CREATED"))
    print("-" * 140)
    for key, label, is_valid, redeemed_by, created_at, _redeemed_at in rows:
        status = "REVOKED" if not is_valid else ("REDEEMED" if redeemed_by else "AVAILABLE")
        label_str = (label or "")[:20]
        redeemed_str = (redeemed_by or "")[:38]
        created_str = (created_at or "")[:22]
        print(fmt.format(key, label_str, status, redeemed_str, created_str))


def cmd_revoke(args):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE license_keys SET is_valid = 0 WHERE key = ?", (args.key,))
    if cur.rowcount == 0:
        print(f"ERROR: Key not found: {args.key}")
        conn.close()
        sys.exit(1)
    conn.commit()
    conn.close()
    print(f"Key revoked: {args.key}")


def cmd_grant_email(args):
    """Directly grant enterprise license to a user by email (no key needed)."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE users SET enterprise_license = 1 WHERE email = ?", (args.email,))
    if cur.rowcount == 0:
        print(f"ERROR: User not found with email: {args.email}")
        conn.close()
        sys.exit(1)
    conn.commit()
    conn.close()
    print(f"Enterprise license granted to: {args.email}")


def main():
    parser = argparse.ArgumentParser(
        description="Manage mycontext enterprise license keys"
    )
    sub = parser.add_subparsers(dest="command")

    gen = sub.add_parser("generate", help="Generate new license keys")
    gen.add_argument("--count", type=int, default=1, help="Number of keys (default: 1)")
    gen.add_argument("--label", type=str, default=None, help="Optional label (e.g. customer name)")

    sub.add_parser("list", help="List all license keys and their status")

    rev = sub.add_parser("revoke", help="Revoke a license key")
    rev.add_argument("key", help="The license key to revoke")

    grant = sub.add_parser("grant-email", help="Grant enterprise directly by email")
    grant.add_argument("email", help="User email address")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    cmds = {
        "generate": cmd_generate,
        "list": cmd_list,
        "revoke": cmd_revoke,
        "grant-email": cmd_grant_email,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
