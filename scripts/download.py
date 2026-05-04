"""Download the current-week TDCC shareholder dispersion snapshot.

Source:   https://opendata.tdcc.com.tw/getOD.ashx?id=1-5
Cadence:  TDCC publishes weekly on Fridays; the endpoint always serves the
          most recent week and overwrites older data without notice.
Storage:  snapshots/<YYYY>/<YYYY-MM-DD>.csv  (date = the snapshot's own
          "資料日期" field, not today's date)

Behavior:
  - If the snapshot's date is already archived locally, exit cleanly (skip).
  - Otherwise write the raw CSV to disk and print the new path.

This script is intentionally minimal — no SQLite, no normalization. The repo's
purpose is to mirror TDCC raw CSVs for long-term preservation and easy
downstream consumption.
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

import requests
import pandas as pd


TDCC_URL = "https://opendata.tdcc.com.tw/getOD.ashx?id=1-5"
USER_AGENT = "Mozilla/5.0 (tdcc-opendata-archive bot)"

REPO_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOTS_DIR = REPO_ROOT / "snapshots"


def download_bytes(timeout: int = 60) -> bytes:
    resp = requests.get(
        TDCC_URL,
        headers={"User-Agent": USER_AGENT},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.content


def extract_snapshot_date(csv_bytes: bytes) -> str:
    """Parse the first '資料日期' value. Format YYYYMMDD -> YYYY-MM-DD."""
    df = pd.read_csv(io.BytesIO(csv_bytes), encoding="utf-8-sig", dtype=str, nrows=1)
    raw = df.iloc[0]["資料日期"]
    return f"{raw[0:4]}-{raw[4:6]}-{raw[6:8]}"


def main() -> int:
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    raw = download_bytes()
    snapshot_date = extract_snapshot_date(raw)
    year = snapshot_date[:4]

    out_dir = SNAPSHOTS_DIR / year
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{snapshot_date}.csv"

    if out_path.exists():
        print(f"already archived: {out_path.relative_to(REPO_ROOT)} (skip)")
        return 0

    out_path.write_bytes(raw)
    print(f"new snapshot: {out_path.relative_to(REPO_ROOT)} "
          f"({len(raw) / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
