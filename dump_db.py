#!/usr/bin/env python3
"""Dump all tables from permesso.db."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "permesso.db"

if not DB_PATH.exists():
    print("Database not found:", DB_PATH)
    raise SystemExit(1)

db = sqlite3.connect(DB_PATH)
db.row_factory = sqlite3.Row

for (table,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    rows = db.execute(f"SELECT * FROM {table}").fetchall()
    cols = [desc[0] for desc in db.execute(f"SELECT * FROM {table}").description]

    print(f"\n{'=' * 60}")
    print(f" {table} ({len(rows)} rows)")
    print(f"{'=' * 60}")

    if not rows:
        print(" (empty)")
        continue

    # Calculate column widths
    widths = [max(len(str(col)), *(len(str(row[col])) for row in rows)) for col in cols]

    # Header
    header = " | ".join(str(col).ljust(w) for col, w in zip(cols, widths))
    print(header)
    print("-+-".join("-" * w for w in widths))

    # Rows
    for row in rows:
        print(" | ".join(str(row[col]).ljust(w) for col, w in zip(cols, widths)))

db.close()
