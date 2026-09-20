from x4_obs.trace import TraceAPI
from x4_obs.receipt import make_receipt
from x4_obs.cli import main


def test_nested_events():
    t = TraceAPI()
    with t.agent("a"):
        with t.tool("t", input_data="in") as ev:
            t.set_output(ev, "out")
    assert len(t.events) == 2
    assert t.events[0].event == "agent"
    assert t.events[1].event == "tool_call"
    assert t.events[1].input_hash and t.events[1].output_hash
    assert t.events[1].parent is not None


def test_receipt():
    r = make_receipt("write", "f", approved=True, before=b"a", after=b"b")
    assert r.sha256_before != r.sha256_after
    assert r.receipt_id.startswith("x4-")


def test_cli_demo():
    assert main(["--demo"]) == 0
