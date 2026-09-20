from __future__ import annotations
import json, time, uuid
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from typing import Any, Iterator

@dataclass
class Event:
    trace_id: str; event: str; name: str
    status: str = "success"; latency_ms: int = 0
    attributes: dict[str, Any] = field(default_factory=dict)

class TraceAPI:
    def __init__(self) -> None:
        self.events: list[Event] = []; self._tid = uuid.uuid4().hex
    @contextmanager
    def agent(self, name: str) -> Iterator[None]:
        t0 = time.perf_counter()
        try:
            yield; st = "success"
        except Exception:
            st = "error"; raise
        finally:
            self.events.append(Event(self._tid, "agent", name, st, int((time.perf_counter()-t0)*1000)))
    @contextmanager
    def tool(self, name: str) -> Iterator[None]:
        t0 = time.perf_counter()
        try:
            yield; st = "success"
        except Exception:
            st = "error"; raise
        finally:
            self.events.append(Event(self._tid, "tool.call", name, st, int((time.perf_counter()-t0)*1000)))
    def export_jsonl(self) -> str:
        return "\n".join(json.dumps(asdict(e)) for e in self.events) + ("\n" if self.events else "")

trace = TraceAPI()
