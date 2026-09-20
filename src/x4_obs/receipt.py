from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Receipt:
    receipt_id: str
    action: str
    target: str
    approved: bool
    actor: str
    sha256_before: str | None
    sha256_after: str | None
    timestamp: float
    attributes: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)


def make_receipt(
    action: str,
    target: str,
    *,
    approved: bool,
    actor: str = "system",
    before: bytes | None = None,
    after: bytes | None = None,
    **attrs: Any,
) -> Receipt:
    return Receipt(
        receipt_id=f"x4-{uuid.uuid4().hex[:12]}",
        action=action,
        target=target,
        approved=approved,
        actor=actor,
        sha256_before=hashlib.sha256(before).hexdigest() if before is not None else None,
        sha256_after=hashlib.sha256(after).hexdigest() if after is not None else None,
        timestamp=time.time(),
        attributes=dict(attrs),
    )
