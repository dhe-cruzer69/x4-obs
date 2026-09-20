from __future__ import annotations

import hashlib
import json
import time
import uuid
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from typing import Any, Iterator


def _sha256(data: bytes | str | None) -> str | None:
    if data is None:
        return None
    if isinstance(data, str):
        data = data.encode("utf-8")
    return "sha256:" + hashlib.sha256(data).hexdigest()


@dataclass
class Event:
    event: str
    agent: str | None = None
    tool: str | None = None
    timestamp: float = 0.0
    input_hash: str | None = None
    output_hash: str | None = None
    status: str = "success"
    parent: str | None = None
    receipt: str | None = None
    latency_ms: int = 0
    attributes: dict[str, Any] = field(default_factory=dict)
    trace_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class TraceAPI:
    def __init__(self) -> None:
        self.events: list[Event] = []
        self._tid = uuid.uuid4().hex
        self._stack: list[str] = []

    @contextmanager
    def agent(self, name: str, **attrs: Any) -> Iterator[Event]:
        t0 = time.perf_counter()
        parent = self._stack[-1] if self._stack else None
        ev = Event(
            event="agent",
            agent=name,
            timestamp=time.time(),
            parent=parent,
            trace_id=self._tid,
            attributes=dict(attrs),
        )
        token = f"agent:{name}:{uuid.uuid4().hex[:8]}"
        self._stack.append(token)
        try:
            yield ev
            ev.status = "success"
        except Exception:
            ev.status = "error"
            raise
        finally:
            ev.latency_ms = int((time.perf_counter() - t0) * 1000)
            self.events.append(ev)
            self._stack.pop()

    @contextmanager
    def tool(
        self,
        name: str,
        *,
        agent: str | None = None,
        input_data: bytes | str | None = None,
        **attrs: Any,
    ) -> Iterator[Event]:
        t0 = time.perf_counter()
        parent = self._stack[-1] if self._stack else None
        ev = Event(
            event="tool_call",
            agent=agent,
            tool=name,
            timestamp=time.time(),
            input_hash=_sha256(input_data),
            parent=parent,
            trace_id=self._tid,
            attributes=dict(attrs),
        )
        token = f"tool:{name}:{uuid.uuid4().hex[:8]}"
        self._stack.append(token)
        try:
            yield ev
            ev.status = "success"
        except Exception:
            ev.status = "error"
            raise
        finally:
            ev.latency_ms = int((time.perf_counter() - t0) * 1000)
            self.events.append(ev)
            self._stack.pop()

    def set_output(self, ev: Event, data: bytes | str | None) -> None:
        ev.output_hash = _sha256(data)

    def attach_receipt(self, ev: Event, receipt_id: str) -> None:
        ev.receipt = receipt_id

    def export_jsonl(self) -> str:
        lines = [json.dumps(e.to_dict(), sort_keys=True) for e in self.events]
        return "\n".join(lines) + ("\n" if lines else "")

    def reset(self) -> None:
        self.events.clear()
        self._tid = uuid.uuid4().hex
        self._stack.clear()


trace = TraceAPI()
