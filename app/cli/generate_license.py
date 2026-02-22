"""CLI tool to generate enterprise license keys.

Usage:
    python -m app.cli.generate_license                   # generate 1 key
    python -m app.cli.generate_license --count 5         # generate 5 keys
    python -m app.cli.generate_license --label "Acme Co" # label a key
    python -m app.cli.generate_license --list             # list all keys
"""

import argparse
import asyncio
import secrets
from datetime import datetime

from sqlalchemy import select

from app.db.database import AsyncSessionLocal, init_db
from app.db.models import LicenseKey


def generate_key() -> str:
    """Generate a URL-safe license key: ENT-XXXX-XXXX-XXXX-XXXX."""
    raw = secrets.token_hex(16)
    parts = [raw[i:i + 4].upper() for i in range(0, 16, 4)]
    return f"ENT-{'-'.join(parts)}"


async def create_keys(count: int, label: str | None) -> list[str]:
    await init_db()
    keys: list[str] = []
    async with AsyncSessionLocal() as session:
        for _ in range(count):
            key_str = generate_key()
            lk = LicenseKey(key=key_str, label=label)
            session.add(lk)
            keys.append(key_str)
        await session.commit()
    return keys


async def list_keys() -> None:
    await init_db()
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(LicenseKey).order_by(LicenseKey.created_at.desc())
        )
        rows = result.scalars().all()

    if not rows:
        print("No license keys found.")
        return

    header = f"{'Key':<30} {'Label':<20} {'Valid':<6} {'Redeemed By':<38} {'Created'}"
    print(header)
    print("-" * len(header))
    for r in rows:
        redeemed = r.redeemed_by or "-"
        label = r.label or "-"
        valid = "Yes" if r.is_valid else "No"
        created = r.created_at.strftime("%Y-%m-%d %H:%M") if isinstance(r.created_at, datetime) else str(r.created_at or "")
        print(f"{r.key:<30} {label:<20} {valid:<6} {redeemed:<38} {created}")


def main():
    parser = argparse.ArgumentParser(description="Generate or list enterprise license keys")
    parser.add_argument("--count", "-n", type=int, default=1, help="Number of keys to generate")
    parser.add_argument("--label", "-l", type=str, default=None, help="Optional label (e.g. company name)")
    parser.add_argument("--list", action="store_true", help="List all existing keys")
    args = parser.parse_args()

    if args.list:
        asyncio.run(list_keys())
    else:
        keys = asyncio.run(create_keys(args.count, args.label))
        print(f"Generated {len(keys)} license key(s):\n")
        for k in keys:
            print(f"  {k}")
        print("\nShare these with customers. Each key can be redeemed once.")


if __name__ == "__main__":
    main()
