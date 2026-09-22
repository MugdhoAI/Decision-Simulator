from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class DebateReport:
    """Serializable record of one completed decision simulation."""

    decision: str
    options: list[str]
    user_context: str
    rounds: int
    transcript: list[str]
    created_at: str
    version: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n"


def build_report(
    decision: str,
    options: list[str],
    user_context: str,
    rounds: int,
    transcript: list[str],
    version: str,
) -> DebateReport:
    return DebateReport(
        decision=decision,
        options=list(options),
        user_context=user_context,
        rounds=rounds,
        transcript=list(transcript),
        created_at=datetime.now(timezone.utc).isoformat(),
        version=version,
    )


def write_report(report: DebateReport, path: str | Path) -> Path:
    """Atomically write a UTF-8 JSON report to a local path."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    fd, temp_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
        text=True,
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(report.to_json())
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, destination)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise
    return destination
