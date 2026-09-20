from x4_obs.trace import TraceAPI
from x4_obs.receipt import make_receipt

def test_events():
    t = TraceAPI()
    with t.agent("a"):
        with t.tool("t"): pass
    assert len(t.events) == 2

def test_receipt():
    r = make_receipt("write", "f", approved=True, before=b"a", after=b"b")
    assert r.sha256_before != r.sha256_after
