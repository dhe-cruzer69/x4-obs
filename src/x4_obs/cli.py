from __future__ import annotations
import argparse
from .trace import trace

def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="x4-obs")
    p.add_argument("--demo", action="store_true")
    a = p.parse_args(argv)
    if a.demo:
        with trace.agent("demo"):
            with trace.tool("ping"): pass
        print(trace.export_jsonl())
    else:
        print("x4-obs — use --demo or import x4_obs.trace")
    return 0

if __name__ == "__main__": raise SystemExit(main())
