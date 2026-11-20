#!/usr/bin/env python3
"""Collect a World Bank macro series and publish run-level evidence."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
now = datetime.now(timezone.utc)
source_url = "https://api.worldbank.org/v2/country/KR/indicator/NY.GDP.MKTP.CD?format=json&per_page=100"
request = Request(source_url, headers={"Accept": "application/json", "User-Agent": "LetsAsset observability"})
with urlopen(request, timeout=30) as response:
    source = json.loads(response.read().decode("utf-8"))
rows = source[1] if isinstance(source, list) and len(source) > 1 and isinstance(source[1], list) else []
records = [{"date": row.get("date"), "value": row.get("value"), "country": (row.get("country") or {}).get("value")} for row in rows if row.get("date")]
if not records:
    raise RuntimeError("World Bank response has no dated observations")
raw = {"source": "World Bank Open Data", "source_url": source_url, "observed_at": now.isoformat(), "indicator": "NY.GDP.MKTP.CD", "records": records}
raw_bytes = json.dumps(raw, ensure_ascii=False, sort_keys=True).encode("utf-8")
raw_path = ROOT / "data" / "raw" / "world_bank_kr_gdp.json"
raw_path.parent.mkdir(parents=True, exist_ok=True)
raw_path.write_bytes(raw_bytes + b"\n")
payload = {
    "schema": "lets_observability_v1",
    "run_id": f"asset-unimplemented-{now.strftime('%Y%m%dT%H%M%SZ')}",
    "observed_at": now.isoformat(),
    "service_id": "asset",
    "source": "world_bank_open_data",
    "stages": {
        "collect": {"status": "success", "ok": len(records), "artifact": True},
        "analyze": {"status": "not_started", "ok": None},
        "quality": {"status": "success", "quality_issue_count": 0, "detail": "dated indicator rows"},
        "publish": {"status": "success", "artifact": True},
    },
    "counts": {"records": len(records)},
    "artifacts": {"raw": hashlib.sha256(raw_bytes).hexdigest()},
    "note": "World Bank Korea GDP series snapshot.",
}
out = ROOT / "data" / "observability" / "latest.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"World Bank rows observed: {len(records)}")
