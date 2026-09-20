# x4-obs

[![CI](https://github.com/dhe-cruzer69/x4-obs/actions/workflows/ci.yml/badge.svg)](https://github.com/dhe-cruzer69/x4-obs/actions)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

**Local-first agent telemetry with SHA-256 evidence receipts.**

```text
x4-skills → x4-mcpgen → x4-sec → x4-runtime → x4-obs
```

## 30-second demo

```bash
pip install -e ".[dev]"
x4-obs --demo
x4-obs receipt --action write --target ./file --approved
```

## Event shape

```json
{
  "event": "tool_call",
  "agent": "researcher",
  "tool": "github.search",
  "timestamp": 1726820000.1,
  "input_hash": "sha256:…",
  "output_hash": "sha256:…",
  "status": "success",
  "parent": null,
  "receipt": "x4-a1b2c3d4e5f6"
}
```

## Features (v0.1)

- JSONL event stream
- SHA-256 input/output hashes
- Execution lineage (`parent`)
- Receipts for approved actions
- Local-only (no network)
- OpenTelemetry-compatible field names (export later)

## License

Apache-2.0
