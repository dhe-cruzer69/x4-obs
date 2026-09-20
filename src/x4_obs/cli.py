from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .receipt import make_receipt
from .trace import trace


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="x4-obs", description="Agent telemetry + evidence receipts")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    p.add_argument("--demo", action="store_true", help="Emit sample JSONL events")

    sub = p.add_subparsers(dest="cmd")

    rec = sub.add_parser("receipt", help="Create a receipt")
    rec.add_argument("--action", required=True)
    rec.add_argument("--target", required=True)
    rec.add_argument("--approved", action="store_true")
    rec.add_argument("--actor", default="cli")

    args = p.parse_args(argv)

    if args.demo:
        with trace.agent("demo-agent"):
            with trace.tool("ping", input_data=b"ping") as ev:
                trace.set_output(ev, b"pong")
            r = make_receipt("demo", "/tmp/x", approved=True, before=b"a", after=b"b")
            with trace.tool("write", agent="demo-agent") as ev2:
                trace.attach_receipt(ev2, r.receipt_id)
        sys.stdout.write(trace.export_jsonl())
        return 0

    if args.cmd == "receipt":
        r = make_receipt(
            args.action,
            args.target,
            approved=bool(args.approved),
            actor=args.actor,
        )
        print(r.to_json())
        return 0

    print("x4-obs — use --demo or: x4-obs receipt --action … --target …")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
